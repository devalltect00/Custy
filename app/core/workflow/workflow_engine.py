# app/core/workflow/workflow_engine.py

import logging
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from colorama import Fore, Style

from app.cli.constants.enums import BumpChoices, StageModeChoices, StrategyChoices
from app.constants.git_workflow_rules import (
    ALLOWED_COMMIT_TYPES,
    NON_CRITICAL_BRANCHES,
)
from app.constants.path import (
    CHANGELOG_PATH,
    CUSTY_BACKUP_COMMIT_DIR,
    CUSTY_BACKUP_TAG_DIR,
    CUSTY_TAG_MESSAGE_TEMPLATE,
)
from app.core.backup import BackupManager
from app.core.branch_workflow import BranchWorkflowManager
from app.core.changelog.generator import ChangelogGenerator
from app.core.cleanup.backups.handle_cleanup_backups import HandleCleanupBackups
from app.core.editor import EditorService
from app.core.exceptions.validation_error import ValidationError  # adjust if needed
from app.core.files.update_files import (
    update_version_target,
    update_version_universal,
)
from app.core.git_ops.commit.settings import (
    CommitValidationProvider,
    CommitValidationSettings,
)
from app.core.git_ops.commit.validator import (
    validate_commit_message_file,
    validate_commit_message_format,
)
from app.core.git_ops.git.factory import create_git_service
from app.core.git_ops.git.service import GitService
from app.core.git_ops.helper import (
    CommitizenHelper,
    get_sorted_tags,
    maybe_assert_is_final,
)
from app.core.git_ops.hooks import (
    GitHookPlan,
    GitHookPolicyError,
    GitHookService,
    HookExecution,
)
from app.core.git_ops.tag_strategy import (
    CommitizenStrategy,
    DateStrategy,
    GitCountStrategy,
    PEP440Strategy,
    SemverStrategy,
)
from app.core.git_ops.versioning import (
    ReleaseInfo,
    ReleaseNoteBuilder,
    VersionBridge,
    VersionType,
)
from app.core.project import detect_project_layout, detect_project_name
from app.core.shared import GitOperationError
from app.core.workflow.workflow_config import WorkflowConfig

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    High-level workflow orchestrator.

    Responsibilities:
    - validate inputs & environment
    - orchestrate services (git, commitizen, etc.)
    - NO low-level command execution
    - Execute business logic (commit, tag, version, etc.)
    - Hold runtime state
    - Provide services to pipeline steps

    Notes:
    - Receives all input via WorkflowConfig
    - Does NOT know about CLI or Pipeline
    """

    def __init__(self, config: WorkflowConfig) -> None:
        # =========================================================
        # 📦 Configuration (immutable input)
        # =========================================================
        self.config = config

        # ===== Inputs =====
        self.commit_message_input = config.commit_message_input
        self.commit_message_file = config.commit_message_file
        self.check_cz = config.check_cz
        self.commit_validation_settings = config.commit_validation_settings
        if self.check_cz:
            self.commit_validation_settings = CommitValidationSettings(
                provider=CommitValidationProvider.COMMITIZEN,
                require_tool=True,
            )
        self.commit_validation_provider: CommitValidationProvider | None = None
        self.git_hook_settings = config.git_hook_settings
        self.commit_hook_plan: GitHookPlan | None = None
        self.tag_input = config.tag_input
        self.tag_message_input = config.tag_message_input
        self.tag_message_file = config.tag_message_file
        self.strategy_input = config.strategy
        self.bump_level = config.bump_level
        self.pre_release = config.pre_release
        self.post_release = config.post_release
        self.dev_release = config.dev_release
        self.meta = config.meta
        self.epoch = config.epoch
        self.force_tag = config.force_tag
        self.version_file = config.version_file
        self.auto_stage = config.auto_stage
        self.stage_mode = config.stage_mode
        self.force_changelog = config.force_changelog
        self.force_commit = config.force_commit
        self.sync_backup = config.sync_backup
        self.skip_tag = config.skip_tag
        self.skip_checks = config.skip_checks

        self.remote = config.remote
        self.default_remote = config.default_remote
        self.all_remote = config.all_remote
        self.push_to = config.push_to
        self.main_remotes = config.main_remotes
        self.backup_remotes = config.backup_remotes

        self.commit_message_backup_dir = config.commit_message_backup_dir
        self.tag_message_backup_dir = config.tag_message_backup_dir
        self.cleanup_backup_type = config.cleanup_backup_type
        self.backup_retention_count = config.backup_retention_count

        self.dry_run = config.dry_run
        self.no_debug = config.no_debug
        self.log_level = config.log_level

        # ===== Runtime =====
        self.tag: str = self.tag_input or ""
        self.tag_message: str = ""
        self.changes_to_staged: list[str] = []

        # =========================================================
        # 🔧 Core Services
        # =========================================================
        self.gitService: GitService = create_git_service(dry_run=self.dry_run)
        self.commitizenHelper = CommitizenHelper(dry_run=self.dry_run)
        self.changelogGenerator = ChangelogGenerator(
            dry_run=self.dry_run,
            pending_commit_path=self.commit_message_file,
        )
        self.backupManager = BackupManager(
            keep=self.backup_retention_count,
            dry_run=self.dry_run,
        )
        self.branchWorkflowManager = BranchWorkflowManager(
            no_debug=self.no_debug,
            sync_backup=self.sync_backup,
            dry_run=self.dry_run,
        )
        self.editorService = EditorService(settings=config.editor_settings)
        self.gitHookService = GitHookService(settings=self.git_hook_settings)

        # Silent mode
        if self.no_debug:
            self._set_silent_mode()
            logger.debug("🐞 No Debug")

    # =========================================================
    # Silent Mode
    # =========================================================
    def _set_silent_mode(self):
        """
        Enable silent mode for runner-based components.
        """
        # GitService → executor → runner
        if hasattr(self.gitService, "executor"):
            self.gitService.executor.runner.set_silent(True)

        # Commitizen helper
        # # if hasattr(self, "cz"):
        # #    self.commitizenHelper.runner.set_silent(True)
        self.commitizenHelper.runner.set_silent(True)

        # Changelog generator
        # # if hasattr(self, "changelog_generator"):
        # #     self.changelogGenerator.runner.set_silent(True)
        self.changelogGenerator.runner.set_silent(True)

    # =========================================================
    # Public Validation Entry
    # =========================================================
    def validate(self) -> None:
        """
        Run all validation steps required before executing workflow.

        Order matters:
        1. Environment checks
        2. File checks
        3. Git state checks
        """

        self.ensure_git_repo()
        self.ensure_remote_exists()
        self.ensure_version_file()
        self.ensure_commit_message_file()
        self.ensure_tag_message_file()
        self.ensure_staged_changes()
        self.ensure_commit_validation_provider()
        self.ensure_commit_hook_policy()
        self.ensure_commit_message_file_exists()
        self.ensure_tag_message_file_exists()

    # =========================================================
    # Validation Steps
    # =========================================================

    def ensure_git_repo(self):
        """
        Ensure current directory is a Git repository.
        """
        if not self.gitService.is_git_repo():
            raise ValidationError(
                message="Git repository not found.",
                hint="Run `git init`",
                code="NOT_GIT_REPO",
            )

    def ensure_remote_exists(self, remote: str | None = None) -> None:
        """
        Ensure a required Git remote exists.

        Args:
            remote: Optional explicit remote name. When omitted, validate every
                remote selected by the current push configuration.

        Behavior:
            - Uses GitService abstraction
            - Can be skipped via --skip-checks
        """

        if self.skip_checks:
            return

        if remote:
            remotes = [remote]
        else:
            current_branch = self.gitService.get_current_branch()
            main_remotes, backup_remotes = self._resolve_push_remote_groups(
                current_branch=current_branch
            )
            remotes = [*main_remotes, *backup_remotes]

        for resolved_remote in remotes:
            if not self.gitService.check_remote(resolved_remote):
                raise ValidationError(
                    message=(
                        f"Git remote '{resolved_remote}' not found or unreachable."
                    ),
                    hint=(
                        "Add the remote with git remote add "
                        f"{resolved_remote} <url> or update Custy's Git configuration."
                    ),
                    code="REMOTE_NOT_FOUND",
                    context={"remote": resolved_remote},
                )

    def ensure_version_file(self):
        """
        Validate an explicit or automatically detected version target.

        Repositories without supported version metadata are valid. They use
        Git tags as the version source and skip project-file synchronization.
        """

        if self.version_file and not self.version_file.exists():
            raise ValidationError(
                message=f"Version file '{self.version_file}' not found.",
                hint=(
                    "Set tool.custy.cli.paths.version_file to 'auto' or "
                    "configure an existing version target."
                ),
                code="VERSION_FILE_NOT_FOUND",
            )

        if not self.version_file:
            logger.info(
                "No supported project version file detected; "
                "using Git-tag-only versioning."
            )

    def ensure_commit_message_file(self):
        """
        Ensure commit message file exists.
        """
        if not self.commit_message_file or not self.commit_message_file.exists():
            raise ValidationError(
                message=f"Commit message file '{self.commit_message_file}' not found.",
                hint="Run `custy init config`",
                code="COMMIT_MSG_FILE_NOT_FOUND",
            )

    def ensure_tag_message_file(self):
        """
        Ensure tag message file exists.
        """
        if not self.tag_message_file or not self.tag_message_file.exists():
            raise ValidationError(
                message=f"Tag message file '{self.tag_message_file}' not found.",
                hint="Run `custy init config`",
                code="TAG_MSG_FILE_NOT_FOUND",
            )

    def ensure_staged_changes(self):
        """
        Ensure there are staged changes before committing.

        Behavior:
        - Checks via GitService
        - Supports auto-stage
        - Supports force commit
        """

        if self.gitService.has_staged_files():
            return

        print("self.auto_stage===========", self.auto_stage)

        # ===== Auto-stage =====
        if self.auto_stage:
            logger.warning("⚠️ No staged changes detected. Auto staging...")
            logger.debug("📦 Auto-running: git add .")

            if self.stage_mode == StageModeChoices.UPDATE:
                self.gitService.auto_stage_update()
            else:
                self.gitService.auto_stage_all()

            if self.dry_run:
                logger.info(
                    "[dry_run](dry-run)[/dry_run] Auto-stage was simulated; "
                    "the real Git index remains unchanged."
                )
                return

            if not self.dry_run:
                if not self.gitService.has_staged_files():
                    logger.debug(
                        "⚠️ Still no staged files after auto-staging. but proceeding due to --force-commit."
                    )
                    if self.force_commit:
                        logger.warning("⚠️ Proceeding due to --force-commit")
                        return

                    logger.debug(
                        "⚠️ [yellow]Warning[/yellow]: Still no staged changes after `git add .`"
                    )
                    confirm = (
                        input("No staged files. Continue? (y/n): ").strip().lower()
                    )
                    if confirm not in ["y", "yes"]:
                        raise ValidationError(
                            message="Aborted due to empty staging.",
                            hint="Stage files using `git add`",
                            code="EMPTY_STAGING_ABORTED",
                        )
                    logger.debug("⚠️ Continuing despite no staged. files.")

            staged_files = self.gitService.list_staged_files()

            if staged_files:
                logger.info("[cyan]📝 Files staged:[/cyan]")
                for f in staged_files:
                    logger.info(f"[green]  - {f}[/green]")
            else:
                logger.debug("⚠️ No files were staged.")
                if self.force_commit:
                    logger.warning("⚠️ Proceeding with empty commit (--force-commit)")
                    return

                raise ValidationError(
                    message="No files staged after auto-stage.",
                    hint="Check your working directory",
                    code="AUTO_STAGE_FAILED",
                )

        elif self.force_commit:
            logger.warning("⚠️ No staged files but continuing (--force-commit)")
            return

        else:
            if self.dry_run:
                logger.warning(
                    "[yellow](dry-run)[/yellow] No staged changes detected. "
                    "Would normally fail with NO_STAGED_CHANGES.\n"
                    "Hint: Use `git add .` or enable --auto-stage."
                )
                return
            raise ValidationError(
                message="No staged changes to commit.",
                hint="Use `git add .`",
                code="NO_STAGED_CHANGES",
            )

    def ensure_commit_validation_provider(self) -> CommitValidationProvider:
        """Resolve and validate the configured commit-message provider.

        ``auto`` enables Commitizen only when the project has recognizable
        configuration and the executable is available. Optional discovery
        failures fall back to Custy's built-in validator unless strict mode is
        requested.

        Returns:
            Effective provider used after discovery and fallback handling.

        Raises:
            ValidationError: If an explicitly required Commitizen integration
                is missing or malformed.
        """

        requested = self.commit_validation_settings.provider
        strict = self.commit_validation_settings.require_tool

        if requested in {
            CommitValidationProvider.CUSTY,
            CommitValidationProvider.GIT,
        }:
            self.commit_validation_provider = requested
            logger.debug("Commit validation provider: %s", requested.value)
            return requested

        inspection = self.commitizenHelper.inspect()

        if inspection.config_error:
            if requested == CommitValidationProvider.COMMITIZEN or strict:
                raise ValidationError(
                    message="Commitizen configuration is invalid.",
                    hint="Correct the detected Commitizen configuration or use "
                    'provider = "custy".',
                    code="COMMITIZEN_CONFIGURATION_INVALID",
                    context={
                        "file": str(inspection.config_path),
                        "error": inspection.config_error,
                    },
                )
            logger.warning(
                "⚠️ Commitizen configuration in [dim]%s[/dim] is invalid; "
                "using Custy's built-in commit validation. Detail: %s",
                inspection.config_path,
                inspection.config_error,
            )
            self.commit_validation_provider = CommitValidationProvider.CUSTY
            return self.commit_validation_provider

        if not inspection.configured:
            if requested == CommitValidationProvider.COMMITIZEN:
                raise ValidationError(
                    message="Commitizen validation was requested but the project "
                    "has no Commitizen configuration.",
                    hint="Add .cz.toml or [tool.commitizen] in pyproject.toml, "
                    'or use provider = "custy".',
                    code="COMMITIZEN_NOT_CONFIGURED",
                )
            self.commit_validation_provider = CommitValidationProvider.CUSTY
            logger.debug(
                "No Commitizen project configuration detected; using Custy validation."
            )
            return self.commit_validation_provider

        if not inspection.available:
            if requested == CommitValidationProvider.COMMITIZEN or strict:
                raise ValidationError(
                    message="Commitizen validation is configured but 'cz' is not "
                    "available.",
                    hint='Install `custy[commitizen]` or set provider = "custy".',
                    code="COMMITIZEN_NOT_AVAILABLE",
                    context={"file": str(inspection.config_path)},
                )
            logger.warning(
                "⚠️ Commitizen configuration detected in [dim]%s[/dim], but "
                "'cz' is unavailable; using Custy's built-in validation.",
                inspection.config_path,
            )
            self.commit_validation_provider = CommitValidationProvider.CUSTY
            return self.commit_validation_provider

        self.commit_validation_provider = CommitValidationProvider.COMMITIZEN
        logger.info(
            "🧪 Commit validation: Custy + Commitizen ([dim]%s[/dim])",
            inspection.config_path,
        )
        return self.commit_validation_provider

    def ensure_commitizen_convention(self) -> None:
        """Backward-compatible alias for provider preflight validation."""

        self.ensure_commit_validation_provider()

    def ensure_commit_hook_policy(self) -> GitHookPlan:
        """Resolve commit-hook behavior before the workflow mutates files.

        Returns:
            Safe native or direct pre-commit execution plan.

        Raises:
            ValidationError: If a configured or detected hook cannot be
                executed safely in the current environment.
        """

        try:
            plan = self.gitHookService.inspect()
        except GitHookPolicyError as error:
            raise ValidationError(
                message="Git commit hooks are not runnable in this environment.",
                hint=(
                    "Repair the hook, install `custy[hooks]`, use the production "
                    "image with hook support, or select native mode only when "
                    "the installed hooks are compatible."
                ),
                code="GIT_HOOK_POLICY_INVALID",
                context={"detail": str(error)},
            ) from error

        self.commit_hook_plan = plan
        if plan.execution is HookExecution.PRE_COMMIT:
            logger.info("🪝 Commit hooks: direct pre-commit execution")
            logger.info("[dim]%s[/dim]", plan.reason)
        else:
            logger.debug("Commit hooks: native Git execution. %s", plan.reason)
        return plan

    def ensure_commit_message_file_exists(self) -> None:
        """
        Ensure commit message file exists before editing.

        This file is required for:
        - commit message generation
        - user editing phase

        Raises:
            ValidationError: If file is missing.
        """

        if not self.commit_message_file:
            raise ValidationError(
                message="Commit message file path is not provided.",
                hint="Use --message-file or run `custy init templates`.",
                code="COMMIT_MSG_PATH_MISSING",
            )

        if not self.commit_message_file.exists():
            raise ValidationError(
                message=f"Commit message file not found: {self.commit_message_file}",
                hint="Run `custy init templates` to initialize required files.",
                code="COMMIT_MSG_FILE_NOT_FOUND",
                context={"path": str(self.commit_message_file)},
            )

    def ensure_tag_message_file_exists(self) -> None:
        """
        Ensure tag message file exists before editing.

        Raises:
            ValidationError: If file is missing.
        """

        if not self.tag_message_file:
            raise ValidationError(
                message="Tag message file path is not provided.",
                hint="Use --tag-message-file or run `custy init templates`.",
                code="TAG_MSG_PATH_MISSING",
            )

        if not self.tag_message_file.exists():
            raise ValidationError(
                message=f"Tag message file not found: {self.tag_message_file}",
                hint="Run `custy init templates` to initialize required files.",
                code="TAG_MSG_FILE_NOT_FOUND",
                context={"path": str(self.tag_message_file)},
            )

    def prepare_version_tag(self) -> None:
        """
        Determine the next version tag based on input or strategy.

        Priority:
        1. Explicit tag input (--tag)
        2. Strategy-based generation

        Side Effects:
            - sets self.tag
        """

        if self.tag_input:
            self.tag = self.tag_input

        elif self.strategy_input == StrategyChoices.SEMVER:
            self.tag = SemverStrategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                build_meta=self.meta,
                no_debug=self.no_debug,
            ).get_next_tag()

        elif self.strategy_input == StrategyChoices.PEP440:
            self.tag = PEP440Strategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                post_release=self.post_release,
                dev_release=self.dev_release,
                local=self.meta,
                epoch=self.epoch,
                no_debug=self.no_debug,
            ).get_next_tag()

        elif self.is_commitizen_auto():
            self.tag = CommitizenStrategy(self.pre_release).get_next_tag()

        elif self.strategy_input == StrategyChoices.DATE:
            self.tag = DateStrategy().get_next_tag()

        elif self.strategy_input == StrategyChoices.GIT_COUNT:
            self.tag = GitCountStrategy().get_next_tag()

        else:
            raise ValidationError(
                message="Invalid versioning configuration.",
                hint="Provide --tag or use --strategy with --bump.",
                code="INVALID_VERSION_INPUT",
            )

        logger.info(f"🔖 Next version: {self.tag}")

    def initialize_workflow(self) -> None:
        """
        Validate and execute branch workflow transition.

        Requires:
            - self.tag already resolved

        Flow:
            1. Detect workflow case
            2. Confirm with user
            3. Execute initial workflow actions
        """

        if self.skip_checks:
            if not self.dry_run:
                input(
                    f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n"
                )
            return

        self.branchWorkflowManager = BranchWorkflowManager(
            no_debug=self.no_debug,
            sync_backup=self.sync_backup,
            dry_run=self.dry_run,
        )

        self.workflow_case = self.branchWorkflowManager.check_transition(
            to_tag=self.tag
        )

        if not self.dry_run:
            input(
                f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n"
            )

        self.branchWorkflowManager.run_initial_workflow(
            case=self.workflow_case,
            to_tag=self.tag,
        )

    def prepare_tag_message(self) -> None:
        """
        Resolve or initialize tag message.

        Priority:
        1. CLI input (--tag-msg)
        2. File (--tag-msg-file)
        3. Default template

        Side Effects:
            - sets self.tag_message
            - may create tag message file
        """

        if self.tag_message_input:
            self.tag_message = self.tag_message_input
            logger.info("✅ Using tag message from CLI.")
            return

        tag_msg_path = Path(self.tag_message_file or CUSTY_TAG_MESSAGE_TEMPLATE)

        if not tag_msg_path.exists():
            default_content = (
                f"Release {self.tag}\n\n# Write additional tag notes below\n"
            )

            if self.dry_run:
                logger.info(
                    "[dry_run](dry-run)[/dry_run] "
                    f"Would create tag message template: {tag_msg_path}"
                )
            else:
                tag_msg_path.parent.mkdir(parents=True, exist_ok=True)
                tag_msg_path.write_text(default_content, encoding="utf-8")

                logger.info(f"📝 Created tag message template: {tag_msg_path}")

        self.tag_message_file = tag_msg_path

    def generate_release_artifacts(self) -> None:
        """
        Generate missing or empty release message files.

        Uses:
            - GitService for tag retrieval
            - ReleaseNoteBuilder for structured output

        Side Effects:
            - writes empty or missing commit-message.txt
            - writes empty or missing tag-message.txt

        Notes:
            Existing non-empty files are user-owned reviewed input and are
            preserved. Custy never replaces them with generic release text.
        """

        version = self.tag
        logger.debug("Generating release artifacts for version %s", version)
        version_type = VersionType.detect(version)

        all_tags = self.gitService.get_all_tags()
        sorted_tags = get_sorted_tags(all_tags)

        version_prefix = version.removeprefix("v")

        # Find prerelease tags
        prereleases = [
            t
            for t in sorted_tags
            if t.startswith(version_prefix) and re.search(r"(a|b|rc|dev)", t)
        ]
        prereleases = list(reversed(prereleases))
        latest_pre = prereleases[0] if prereleases else None

        # Detect changes since RC
        has_changes = True
        if version_type == VersionType.FINAL and latest_pre:
            rc_tags = [tag for tag in prereleases if re.search(r"rc\d+", tag.lower())]
            has_changes = len(rc_tags) > 1

        info = ReleaseInfo(
            version=version,
            version_type=version_type,
            app_name=detect_project_name(),
            prerelease_tags=prereleases,
            latest_prerelease=latest_pre,
            has_changes_since_rc=has_changes,
        )

        builder = ReleaseNoteBuilder(info)

        # Write commit message only when no reviewed content exists.
        if self.commit_message_file:
            commit_content = builder.build_commit_msg()
            self._write_release_artifact(
                self.commit_message_file,
                commit_content,
                label="commit message",
            )

        # Write tag message only when no reviewed content exists.
        if self.tag_message_file:
            tag_content = builder.build_tag_msg()
            self._write_release_artifact(
                Path(self.tag_message_file),
                tag_content,
                label="tag message",
            )

    def _write_release_artifact(
        self,
        path: Path,
        content: str,
        *,
        label: str,
    ) -> None:
        """Write generated content without replacing reviewed user input.

        Args:
            path: Configured release-message path.
            content: Generated fallback content.
            label: Human-readable artifact label used in terminal output.
        """

        if path.is_file():
            try:
                if path.read_text(encoding="utf-8").strip():
                    logger.info(
                        "📝 Preserving existing %s: [dim]%s[/dim]",
                        label,
                        path,
                    )
                    return
            except (OSError, UnicodeError) as error:
                raise ValidationError(
                    message=f"Unable to read the configured {label} file.",
                    hint="Check the file encoding and permissions before retrying.",
                    code="RELEASE_ARTIFACT_READ_FAILED",
                    context={"file": str(path), "error": str(error)},
                ) from error

        if self.dry_run:
            logger.info(
                "[dry_run](dry-run)[/dry_run] Would generate release "
                f"{label}: {path}"
            )
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        logger.info("📝 Generated %s: [dim]%s[/dim]", label, path)

    def edit_release_files(self, *, include_tag: bool = True) -> None:
        """
        Open the message files required by the active workflow.

        Args:
            include_tag: Open the tag-message file after the commit-message file.
                Set this to ``False`` for commit-only development workflows.

        Order:
            1. commit message file
            2. tag message file

        Behavior:
            - Skips missing files
            - Uses environment and platform-aware editor discovery
            - Respects dry-run mode
        """

        if self.commit_message_file:
            self.open_editor(self.commit_message_file, label="commit message")

        if include_tag and self.tag_message_file:
            self.open_editor(self.tag_message_file, label="tag message")

    def open_editor(self, path: Path, label: str = "file") -> None:
        """
        Open a file in an external editor for user modification.

        Args:
            path (Path): File to open.
            label (str): Human-friendly name (for logging).

        Behavior:
            - Honors VISUAL and EDITOR before platform defaults
            - Blocks execution until the selected editor exits
            - Supports terminal editors in interactive Linux containers
            - Respects dry-run mode

        Raises:
            ValidationError: If no editor could be launched.
        """

        # # The validating done on validating steps
        # self.ensure_commit_message_file_exists()
        # self.ensure_tag_message_file_exists()

        # logger.info(f"📝 Opening {label}: {path}")

        # logger.info(f"📝 Opening {label}: {path} — save and close the file to continue.")

        logger.info(
            f"📝 Opening [bright_cyan]{label}[/bright_cyan]: "
            f"[dim]{path}[/dim] — "
            f"[dim white]save and close the file to continue.[/dim white]"
        )

        self.editorService.open_file(
            Path(path),
            label=label,
            dry_run=self.dry_run,
        )

    def validate_edited_files(self) -> None:
        """
        Validate user-edited files and determine tagging behavior.
        """

        provider = (
            self.commit_validation_provider or self.ensure_commit_validation_provider()
        )

        if provider == CommitValidationProvider.GIT:
            validate_commit_message_file(self.commit_message_file)
            logger.info(
                "🧪 Commit validation: basic Git message-file safety checks only."
            )
            return

        commit_type = validate_commit_message_format(self.commit_message_file)

        if provider == CommitValidationProvider.COMMITIZEN:
            result = self.commitizenHelper.check_commit(self.commit_message_file)
            if not result.success:
                detail = (result.stderr or result.stdout).strip()
                raise ValidationError(
                    message="Commit message failed Commitizen validation.",
                    hint="Update the message to match the project's Commitizen "
                    'rules, or choose provider = "custy".',
                    code="COMMITIZEN_CHECK_FAILED",
                    context={
                        "file": str(self.commit_message_file),
                        "exit_code": result.returncode,
                        "detail": detail or "Commitizen did not provide output.",
                    },
                )

        self.evaluate_tagging_eligibility(commit_type)

    def evaluate_tagging_eligibility(self, commit_type: str) -> None:
        """
        Decide whether tagging should proceed based on commit type.

        Rules:
        - If commit type is not allowed → skip tag (unless forced)
        - If forced → allow but warn

        Side Effects:
            - sets self.skip_tag
            - may override self.tag
        """

        if self.skip_tag:
            logger.info("⏭️ Tagging remains disabled by push configuration.")
            return

        if commit_type not in ALLOWED_COMMIT_TYPES:
            if self.force_tag:
                logger.warning(
                    f"⚠️ Forcing tag despite disallowed commit type: {commit_type}"
                )
                return

            logger.warning(
                f"🚫 Skipping tag: commit type '{commit_type}' is not allowed."
            )
            logger.debug(f"Allowed types: {sorted(ALLOWED_COMMIT_TYPES)}")

            self.skip_tag = True

            # 👇 replace _maybe_use_latest_tag
            self.tag = self.gitService.get_latest_tag()

            logger.warning(f"Using latest tag instead: {self.tag}")

    def apply_version_updates(self) -> None:
        """
        Apply all version-related updates before staging and commit.

        This includes:
        - updating Python version file (__version__.py)
        - updating project config files (pyproject.toml, package.json)

        This step prepares the repository state for commit.

        Logic:
            1. Detect project type (python / semver / others)
            2. If Python project:
                - Force PEP440 version format (conversion if needed)
                - Update python version file
                - Update cz.toml
                - Update ONLY python-related files
            3. If non-python (e.g. Node / SemVer):
                - Skip python-specific updates
                - Update ONLY relevant project files

        Notes:
            - This method overrides strategy ONLY for version update phase
            - Does NOT affect tagging strategy
        """

        logger.info("🔧 Applying version updates...")

        layout = detect_project_layout()
        version_to_use = self.tag

        if layout.is_python and self.strategy_input == StrategyChoices.PEP440:
            if "-" in self.tag:
                converted = VersionBridge.semver_to_pep440(self.tag)
                if converted:
                    logger.debug(
                        "Converted SemVer to PEP 440 for Python metadata: %s -> %s",
                        self.tag,
                        converted,
                    )
                    version_to_use = converted

            self.commitizenHelper.update_cz_toml_version(new_version=version_to_use)

        if self.dry_run:
            targets = []
            if self.version_file:
                targets.append(str(self.version_file))
            if layout.is_python:
                targets.append("pyproject.toml")
            if layout.is_node:
                targets.append("package.json")

            if targets:
                logger.info(
                    "(dry-run) Would update project version metadata: %s",
                    ", ".join(dict.fromkeys(targets)),
                )
            else:
                logger.info(
                    "(dry-run) No project version metadata detected; "
                    "Git tags would remain the version source."
                )
            return

        updated = False

        if self.version_file and self.version_file.suffix.lower() == ".py":
            updated |= update_version_target(
                self.version_file,
                version_to_use,
            )

        project_type = None
        if layout.is_python and not layout.is_node:
            project_type = "python"
        elif layout.is_node and not layout.is_python:
            project_type = "node"

        updated |= update_version_universal(
            root=layout.root,
            new_version=version_to_use,
            project_type=project_type,
        )

        standard_targets = {
            (layout.root / "pyproject.toml").resolve(),
            (layout.root / "package.json").resolve(),
        }
        if (
            self.version_file
            and self.version_file.suffix.lower() != ".py"
            and self.version_file.resolve() not in standard_targets
        ):
            updated |= update_version_target(
                self.version_file,
                version_to_use,
            )

        if not updated:
            logger.info(
                "No supported project version metadata was changed; "
                "using Git-tag-only versioning."
            )

    def update_python_version_file(
        self, version_override: Optional[str] = None
    ) -> None:
        """
        Update Python version file (e.g. __version__.py).

        Behavior:
            - writes version string
            - respects dry-run
            - validates file existence

        Args:
            version_override (str | None): override version (used for PEP440 conversion)
        """

        if not self.version_file:
            logger.debug("No version file configured → skipping.")
            return

        if not self.version_file.exists():
            raise ValidationError(
                message=f"Version file not found: {self.version_file}",
                hint="Ensure version file exists or configure it properly.",
                code="VERSION_FILE_NOT_FOUND",
            )

        version = version_override or self.tag

        if self.dry_run:
            logger.info(f"(dry-run) Would update {self.version_file} → {version}")
            return

        update_version_target(self.version_file, version)

        logger.info(
            f"✅ [dim]{self.version_file}[/dim] [green]updated[/green] → {version}"
        )

    def update_project_versions(
        self,
        version_override: Optional[str] = None,
        project_type: Optional[str] = None,
    ) -> None:
        """
        Update project-level version files.

        Supported:
            - pyproject.toml
            - package.json (Node)
            - other supported formats

        Args:
            version_override (str | None): version to apply
            project_type (str): 'python' | 'node' | None

        Behavior:
            - python → update pyproject.toml only
            - node → update package.json only
            - None → fallback to universal

        Uses:
            update_version_universal()
        """

        version = version_override or self.tag

        if self.dry_run:
            logger.info("(dry-run) Would update project version files.")
            return

        updated = update_version_universal(
            root=".",
            new_version=version,
            project_type=project_type,
        )

        if not updated:
            logger.debug("No project version files updated.")

    def generate_changelog_if_needed(self) -> None:
        """
        Generate changelog file if version is eligible.

        Rules:
            - Only for final releases (unless forced)
            - Uses ChangelogGenerator

        Side Effects:
            - writes CHANGELOG.md
        """

        if not maybe_assert_is_final(
            self.tag,
            context="changelog",
            force=self.force_changelog,
        ):
            logger.debug("Skipping changelog generation (not final version).")
            return

        logger.info("[blue]📜 Generating changelog...[/blue]")

        rendered = self.changelogGenerator.generate()

        # print("rendered ", rendered)

        self.changelogGenerator.write_to_file(
            content=rendered,
            path=CHANGELOG_PATH,
        )

        if self.dry_run:
            logger.info(
                "[dry_run](dry-run)[/dry_run] Changelog preview generated; "
                f"{CHANGELOG_PATH} was not changed."
            )
        else:
            logger.info(f"✅ {CHANGELOG_PATH} updated.")

    def stage_changes(self) -> None:
        """
        Stage files before commit.

        Behavior:
            - respects stage_mode
            - uses GitService abstraction
            - validates final staged state
        """

        logger.info("[blue]📦 Staging changes...[/blue]")

        # =========================
        # Mode: NONE / MANUAL
        # =========================
        if self.stage_mode in [StageModeChoices.NONE, StageModeChoices.MANUAL]:
            logger.info("[yellow]⚠️ Skipping auto staging (manual mode).[/yellow]")

            if not self.gitService.has_staged_files():
                if self.dry_run:
                    logger.warning(
                        "[dry_run](dry-run)[/dry_run] No staged files are "
                        "currently present; an actual run in manual mode "
                        "would require staging first."
                    )
                    return

                raise ValidationError(
                    message="No staged files detected.",
                    hint="Stage files manually using `git add`.",
                    code="NO_STAGED_FILES",
                )
            return

        # =========================
        # Mode: ALL
        # =========================
        if self.stage_mode == StageModeChoices.ALL:
            logger.info("[cyan]→ git add .[/cyan]")

            if self.dry_run:
                logger.info("(dry-run) Would stage all files.")
            else:
                self.gitService.auto_stage_all()

        # =========================
        # Mode: UPDATE
        # =========================
        elif self.stage_mode == StageModeChoices.UPDATE:
            logger.info("[cyan]→ git add --update[/cyan]")

            if self.dry_run:
                logger.info("(dry-run) Would stage modified files.")
            else:
                self.gitService.auto_stage_update()

        else:
            raise ValidationError(
                message=f"Invalid stage mode: {self.stage_mode}",
                hint="Use one of: all, update, manual, none",
                code="INVALID_STAGE_MODE",
            )

        if self.dry_run:
            logger.info(
                "[dry_run](dry-run)[/dry_run] Staging was simulated; "
                "post-stage validation was not applied to the unchanged index."
            )
            return

        # =========================
        # Final Validation
        # =========================
        self._validate_staged_result()

    def _validate_staged_result(self) -> None:
        """
        Ensure files are staged after staging operation.

        Raises:
            ValidationError if no files are staged.
        """

        if self.gitService.has_staged_files():
            staged_files = self.gitService.list_staged_files()

            if staged_files:
                logger.info("[green]✅ Staged files:[/green]")
                for f in staged_files:
                    logger.info(f"[dim]  - {f}[/dim]")
            return

        if self.force_commit:
            logger.warning(
                "[yellow]⚠️ No staged files, but proceeding due to --force-commit[/yellow]"
            )
            return

        raise ValidationError(
            message="No files staged after staging step.",
            hint="Check your changes or use `git add .`.",
            code="STAGING_FAILED",
        )

    def backup_commit_message_file(self) -> None:
        """
        Backup commit message file.

        Responsibilities:
        - Backup commit message file (if exists)
        - Store backup in commit backup directory

        Side Effects:
        - creates timestamped backup
        - registers backup file for staging
        """

        if not self.commit_message_file:
            return

        logger.info("[blue]🗂️ Backing up commit message file...[/blue]")

        backup_dir = Path(self.commit_message_backup_dir or CUSTY_BACKUP_COMMIT_DIR)

        self._backup_file(
            source=self.commit_message_file,
            backup_dir=backup_dir,
            label="commit message",
        )

    def backup_tag_message_file(self) -> None:
        """
        Resolve and backup tag message file.

        Responsibilities:
        - Resolve tag message from file (if needed)
        - Backup tag message file (if exists)

        Side Effects:
        - updates self.tag_message (via resolver)
        - creates timestamped backup
        - registers backup file for staging
        """

        logger.info("[blue]🗂️ Processing tag message file...[/blue]")

        # Resolve first (important dependency)
        self._resolve_tag_message_from_file()

        if not self.tag_message_file:
            return

        logger.info("[blue]🗂️ Backing up tag message file...[/blue]")

        backup_dir = Path(self.tag_message_backup_dir or CUSTY_BACKUP_TAG_DIR)

        self._backup_file(
            source=self.tag_message_file,
            backup_dir=backup_dir,
            label="tag message",
        )

    def backup_release_files(self) -> None:
        """
        Backup all release-related files.

        This is a high-level orchestration method that delegates
        to more granular backup methods.

        Responsibilities:
        - Backup commit message file
        - Backup tag message file

        Side Effects:
        - creates timestamped backups
        - registers backup files for staging
        """

        logger.info("[blue]🗂️ Backing up release files...[/blue]")

        self.backup_commit_message_file()
        self.backup_tag_message_file()

    def _resolve_tag_message_from_file(self) -> None:
        """
        Resolve tag message content from file or fallback.

        Priority:
            1. tag_message_file content
            2. fallback to tag value

        Side Effects:
            - sets self.tag_message
        """

        if self.tag_message_file and self.tag_message_file.exists():
            self.tag_message = self.tag_message_file.read_text(encoding="utf-8").strip()
            logger.info(f"[dim]📄 Using tag message from {self.tag_message_file}[/dim]")
        else:
            self.tag_message = self.tag
            logger.warning(
                f"[yellow]ℹ️ No tag message file found → using tag as message: {self.tag}[/yellow]"
            )

    def _backup_file(
        self,
        source: Path,
        backup_dir: Path,
        label: str = "file",
    ) -> None:
        """
        Backup a file with timestamp and register it for staging.

        Args:
            source (Path): File to backup
            backup_dir (Path): Destination directory
            label (str): Human-friendly name for logging

        Behavior:
            - creates timestamped backup
            - prunes old backups
            - registers backup files for staging
        """

        if not source.exists():
            logger.debug(f"[dim]Skipping backup (missing {label}): {source}[/dim]")
            return

        # print("backup_dir", backup_dir)

        backup_dir = Path(backup_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_path = backup_dir / f"{source.stem}_{timestamp}.bak.txt"

        try:
            if self.dry_run:
                logger.info(f"(dry-run) Would backup {label}: {source} → {backup_path}")
                return

            backup_dir.mkdir(parents=True, exist_ok=True)

            content = source.read_text(encoding="utf-8")
            backup_path.write_text(content, encoding="utf-8")

            logger.info(
                f"🗂️ [dim]{label}[/dim] backed up → [green]{backup_path}[/green]"
            )

            # Register new backup for staging
            self.changes_to_staged.append(backup_path)

            # Prune old backups
            old_files = self.backupManager._prune_old_backups(
                backup_dir=backup_dir,
                stem=source.stem,
            )

            if old_files:
                self.changes_to_staged.extend(old_files)
                logger.debug(f"Pruned old backups: {old_files}")

        except Exception as e:
            logger.error(f"[red]⚠️ Failed to backup {label}: {e}[/red]")

    def execute_commit_phase(self) -> None:
        """
        Execute commit phase based on strategy.

        Flow:
            - Default → use internal commit logic
            - Commitizen (auto) → delegate to Commitizen

        After this step, pipeline continues normally.
        """

        logger.info("[blue]🧾 Executing commit phase...[/blue]")

        # =========================================================
        # Commitizen Flow
        # =========================================================
        if self.is_commitizen_auto():
            logger.info("[cyan]→ Using Commitizen workflow[/cyan]")

            if self.dry_run:
                logger.info(
                    "[cyan](dry-run)[/cyan] Would run Commitizen commit + check"
                )
                return

            try:
                commit_result = self.commitizenHelper.commit()
                if not commit_result.success:
                    raise RuntimeError(
                        (commit_result.stderr or commit_result.stdout).strip()
                        or "Commitizen commit command failed."
                    )
                logger.info("[green]✅ Commitizen commit created[/green]")

                check_result = self.commitizenHelper.check_commit()
                if not check_result.success:
                    raise RuntimeError(
                        (check_result.stderr or check_result.stdout).strip()
                        or "Commitizen check command failed."
                    )
                logger.info("[green]✅ Commit message validated by Commitizen[/green]")

            except Exception as e:
                raise ValidationError(
                    message="Commitizen commit failed.",
                    hint="Check Commitizen configuration and commit rules.",
                    code="COMMITIZEN_FAILED",
                    context={"error": str(e)},
                ) from e

            return

        # =========================================================
        # Default Flow
        # =========================================================
        logger.debug("[dim]Using default commit flow[/dim]")
        self.create_commit()

    def create_commit(self) -> None:
        """
        Create a Git commit using either:
        - inline message (--commit-message)
        - commit message file (commit-message.txt)

        Behavior:
            - prefers inline message over file
            - validates staged state (unless --force-commit)
            - supports dry-run
            - uses GitService abstraction

        Raises:
            ValidationError:
                - if no message source is provided
                - if commit fails
        """

        logger.info("[blue]🧾 Creating commit...[/blue]")

        # =========================================================
        # Determine commit message source
        # =========================================================
        message = None
        message_file = None

        if self.commit_message_input:
            message = self.commit_message_input
            logger.info("[dim]Using inline commit message (--commit-message)[/dim]")

        elif self.commit_message_file:
            message_file = str(self.commit_message_file)
            logger.info(
                f"[dim]Using commit message file: {self.commit_message_file}[/dim]"
            )

        else:
            raise ValidationError(
                message="No commit message provided.",
                hint="Use --commit-message or ensure commit-message file exists.",
                code="COMMIT_MESSAGE_MISSING",
            )

        if self.dry_run:
            logger.info(
                "[dry_run](dry-run)[/dry_run] Would run commit "
                + ("with inline message" if message else f"with file {message_file}")
            )
            return

        # =========================================================
        # Handle empty commit scenario
        # =========================================================
        has_staged = self.gitService.has_staged_files()

        if not has_staged:
            if not self.force_commit:
                raise ValidationError(
                    message="No staged changes to commit.",
                    hint="Stage files or use --force-commit to allow empty commit.",
                    code="NO_STAGED_CHANGES",
                )

            logger.warning(
                "[yellow]⚠️ No staged changes → creating empty commit (--force-commit)[/yellow]"
            )

        # =========================================================
        # Execute commit
        # =========================================================
        no_verify = self._execute_commit_hooks(
            message=message,
            message_file=message_file,
        )

        try:
            self.gitService.commit(
                message=message,
                message_file=message_file,
                no_verify=no_verify,
            )

            logger.info("[green]✅ Commit created successfully.[/green]")

        except GitOperationError as error:
            detail = error.detail
            normalized_detail = detail.lower().replace("\\", "/")
            hook_failure = any(
                marker in normalized_detail
                for marker in (
                    ".git/hooks/",
                    "pre-commit",
                    "commit-msg hook",
                    "hook failed",
                    "files were modified by this hook",
                )
            )
            raise ValidationError(
                message=(
                    "Git commit was rejected by a repository hook."
                    if hook_failure
                    else "Git failed to create the commit."
                ),
                hint=(
                    "Run the failing hook in the same environment and repair or "
                    "reinstall it. For a Windows-created pre-commit hook mounted "
                    "into Linux Docker, install the hook inside that environment."
                    if hook_failure
                    else "Review the captured Git output, commit message, staged "
                    "files, and repository state."
                ),
                code=("GIT_HOOK_FAILED" if hook_failure else "GIT_COMMIT_FAILED"),
                context={
                    "exit_code": error.returncode,
                    "detail": detail or "Git did not provide diagnostic output.",
                },
            ) from error
        except Exception as e:
            raise ValidationError(
                message="Failed to create commit.",
                hint="Check your commit message and repository state.",
                code="COMMIT_FAILED",
                context={"error": str(e)},
            ) from e

    def _execute_commit_hooks(
        self,
        *,
        message: str | None,
        message_file: str | None,
    ) -> bool:
        """Run a safe direct pre-commit plan before creating a Git commit.

        Args:
            message: Optional inline commit message.
            message_file: Optional configured commit-message file.

        Returns:
            ``True`` only when Git should use ``--no-verify`` because every
            bypassed pre-commit-managed stage already succeeded directly.

        Raises:
            ValidationError: If direct hook execution fails or cannot be
                prepared safely.
        """

        plan = self.commit_hook_plan or self.ensure_commit_hook_policy()
        if plan.execution is HookExecution.NATIVE:
            return False

        temporary_directory: tempfile.TemporaryDirectory[str] | None = None
        hook_message_file = Path(message_file) if message_file else None
        try:
            if "commit-msg" in plan.stages and message is not None:
                temporary_directory = tempfile.TemporaryDirectory(
                    prefix="custy-commit-message-"
                )
                hook_message_file = Path(temporary_directory.name) / "message.txt"
                hook_message_file.write_text(
                    message.rstrip() + "\n",
                    encoding="utf-8",
                )

            result = self.gitHookService.run(
                plan,
                message_file=hook_message_file,
            )
        except GitHookPolicyError as error:
            raise ValidationError(
                message="Custy could not prepare the configured commit hooks.",
                hint="Review tool.custy.git.hooks and the repository hook files.",
                code="GIT_HOOK_EXECUTION_INVALID",
                context={"detail": str(error)},
            ) from error
        finally:
            if temporary_directory is not None:
                temporary_directory.cleanup()

        if not result.success:
            detail = (result.stderr or result.stdout).strip()
            raise ValidationError(
                message="A pre-commit hook rejected the staged changes.",
                hint=(
                    "Run `pre-commit run --hook-stage pre-commit`, repair the "
                    "reported files or checks, stage the result, and retry."
                ),
                code="PRE_COMMIT_HOOK_FAILED",
                context={
                    "exit_code": result.returncode,
                    "detail": detail or "pre-commit did not provide output.",
                },
            )

        output = (result.stdout or result.stderr).strip()
        if output:
            logger.info("%s", output)
        logger.info("✅ Pre-commit hooks completed successfully.")
        return plan.requires_no_verify

    def is_commitizen_auto(self) -> bool:
        return (
            self.strategy_input == StrategyChoices.COMMITIZEN
            and self.bump_level == BumpChoices.AUTO
        )

    def create_tag(self) -> None:
        """
        Create an annotated Git tag.

        Message source priority:
            1. inline tag message (--tag-message)
            2. tag message file (--tag-message-file)
            3. fallback → use tag name

        Behavior:
            - respects skip_tag flag
            - supports dry-run
            - uses GitService abstraction

        Raises:
            ValidationError:
                - if tag creation fails
        """

        # =========================================================
        # Skip condition
        # =========================================================
        if getattr(self, "skip_tag", False):
            logger.info("[yellow]⏭️ Tag step skipped.[/yellow]")
            return

        if not self.tag:
            raise ValidationError(
                message="Tag value is not defined.",
                hint="Ensure version tag is generated before tagging.",
                code="TAG_MISSING",
            )

        logger.info(f"[blue]🏷️ Creating tag:[/blue] [bold]{self.tag}[/bold]")

        # =========================================================
        # Resolve tag message
        # =========================================================
        message = None
        message_file = None

        if self.tag_message_input:
            message = self.tag_message_input
            logger.info("[dim]Using inline tag message (--tag-message)[/dim]")

        elif self.tag_message_file:
            message_file = str(self.tag_message_file)
            logger.info(f"[dim]Using tag message file: {self.tag_message_file}[/dim]")

        else:
            message = self.tag
            logger.warning(
                "[yellow]ℹ️ No tag message provided → using tag as message[/yellow]"
            )

        # =========================================================
        # Dry-run
        # =========================================================
        if self.dry_run:
            logger.info(
                f"[cyan](dry-run)[/cyan] Would create tag [bold]{self.tag}[/bold]"
            )
            return

        # =========================================================
        # Execute tag creation
        # =========================================================
        try:
            self.gitService.tag(
                tag=self.tag,
                message=message,
                message_file=message_file,
            )

            logger.info(
                f"[green]✅ Tag created successfully:[/green] [bold]{self.tag}[/bold]"
            )

        except Exception as e:
            raise ValidationError(
                message=f"Failed to create tag '{self.tag}'.",
                hint="Check tag format and repository state.",
                code="TAG_CREATION_FAILED",
                context={"error": str(e), "tag": self.tag},
            ) from e

    def cleanup_backups(self) -> None:
        """
        Cleanup old backup files after backup phase.
        """

        cleaner = HandleCleanupBackups(
            target=self.cleanup_backup_type,
            keep=self.backup_retention_count,
            dry_run=self.dry_run,
        )

        cleaner.cleanup()

    def push_changes(self, *, include_tag: bool = True) -> None:
        """
        Push commits and tags to the resolved remote groups.

        Args:
            include_tag: Push an eligible resolved tag after each branch push.
                Commit-only development workflows set this to ``False``.

        Selection priority:
            1. An explicit remote supplied by the CLI.
            2. All configured groups when all_remote is enabled.
            3. The configured push_to group.
            4. Optional backup synchronization for a main-group push.

        Branch Rules:
            Backup push is skipped for branches starting with:
                - feature/
                - ci/
                - sandbox/
        """

        logger.info("[blue]🚀 Pushing changes...[/blue]")

        current_branch = self.gitService.get_current_branch()
        logger.debug(f"Current branch: {current_branch}")

        main_remotes, backup_remotes = self._resolve_push_remote_groups(
            current_branch=current_branch
        )

        if not self.dry_run and os.getenv("CUSTY_CONTAINER"):
            logger.info(
                "[yellow]ℹ️ Container push authentication uses credentials "
                "available inside the container. Host credential-manager "
                "sessions are not inherited automatically.[/yellow]"
            )

        if main_remotes:
            self._push_to_remotes(
                main_remotes,
                label="main",
                include_tag=include_tag,
            )

        if backup_remotes:
            self._push_to_remotes(
                backup_remotes,
                label="backup",
                include_tag=include_tag,
            )

    def _resolve_main_remotes(self) -> list[str]:
        """
        Resolve main remotes list.

        Priority:
            1. self.main_remotes
            2. self.default_remote
        """

        remotes = self._deduplicate_remotes(self.main_remotes or [])
        if remotes:
            return remotes

        if self.default_remote is not None and not isinstance(self.default_remote, str):
            raise ValidationError(
                message="The configured default_remote must be a string.",
                hint="Set tool.custy.git.default_remote to a Git remote name.",
                code="INVALID_REMOTE_CONFIG",
                context={"field": "default_remote"},
            )

        default_remote = (self.default_remote or "").strip()
        if default_remote:
            logger.info(f"[dim]Using default remote: {default_remote}[/dim]")
            return [default_remote]

        raise ValidationError(
            message="No valid main remote found.",
            hint="Configure tool.custy.git.main_remotes or default_remote.",
            code="MAIN_REMOTE_MISSING",
        )

    def _resolve_backup_remotes(self) -> list[str]:
        """
        Resolve backup remotes list.

        Empty backup groups remain optional unless push_to explicitly selects
        the backup group.
        """

        remotes = self._deduplicate_remotes(self.backup_remotes or [])
        if remotes:
            return remotes

        return []

    @staticmethod
    def _deduplicate_remotes(remotes: list[str]) -> list[str]:
        """Normalize remote names while preserving configuration order."""

        if not isinstance(remotes, list):
            raise ValidationError(
                message="Configured Git remote groups must be arrays of names.",
                hint='Use TOML arrays such as main_remotes = ["origin"].',
                code="INVALID_REMOTE_CONFIG",
            )

        normalized: list[str] = []
        for remote in remotes:
            if not isinstance(remote, str):
                raise ValidationError(
                    message="Every configured Git remote name must be a string.",
                    hint="Remove non-string values from the configured remote arrays.",
                    code="INVALID_REMOTE_CONFIG",
                    context={"remote": remote},
                )

            remote = remote.strip()
            if remote and remote not in normalized:
                normalized.append(remote)

        return normalized

    def _resolve_push_remote_groups(
        self,
        current_branch: str | None = None,
    ) -> tuple[list[str], list[str]]:
        """
        Resolve the main and backup remote groups for the current push.

        An explicit CLI remote always wins. Otherwise all_remote overrides the
        push_to strategy. sync_backup adds configured backups to a main push.
        Backup targets remain protected on non-critical branches.
        """

        explicit_remote = (self.remote or "").strip()
        if explicit_remote:
            return [explicit_remote], []

        if self.push_to is not None and not isinstance(self.push_to, str):
            raise ValidationError(
                message="The configured push_to value must be a string.",
                hint="Set tool.custy.git.push_to to main, backup, or all.",
                code="INVALID_PUSH_TARGET",
                context={"push_to": self.push_to},
            )

        push_to = (self.push_to or "main").strip().lower()
        if push_to not in {"main", "backup", "all"}:
            raise ValidationError(
                message=f"Unsupported Git push target: '{self.push_to}'.",
                hint="Set tool.custy.git.push_to to main, backup, or all.",
                code="INVALID_PUSH_TARGET",
                context={"push_to": self.push_to},
            )

        select_main = self.all_remote or push_to in {"main", "all"}
        select_backup = self.all_remote or push_to in {"backup", "all"}

        main_remotes = self._resolve_main_remotes() if select_main else []
        backup_remotes = self._resolve_backup_remotes() if select_backup else []

        if self.sync_backup and select_main and not select_backup:
            backup_remotes = self._resolve_backup_remotes()
            if not backup_remotes:
                logger.warning(
                    "[yellow]⚠️ Backup synchronization was requested, "
                    "but no backup remotes are configured.[/yellow]"
                )

        if push_to == "backup" and not self.all_remote and not backup_remotes:
            raise ValidationError(
                message="The backup push target has no configured remotes.",
                hint="Configure tool.custy.git.backup_remotes or select push_to = main.",
                code="BACKUP_REMOTE_MISSING",
            )

        if (
            backup_remotes
            and current_branch
            and any(
                current_branch.startswith(prefix) for prefix in NON_CRITICAL_BRANCHES
            )
        ):
            logger.warning(
                f"[yellow]⛔ Skipping backup push for branch '{current_branch}'[/yellow]"
            )
            backup_remotes = []

        main_remotes = self._deduplicate_remotes(main_remotes)
        main_remote_names = set(main_remotes)
        backup_remotes = [
            remote
            for remote in self._deduplicate_remotes(backup_remotes)
            if remote not in main_remote_names
        ]

        if not main_remotes and not backup_remotes:
            raise ValidationError(
                message="No Git remotes were selected for push.",
                hint="Configure a default, main, or backup Git remote.",
                code="PUSH_REMOTE_MISSING",
            )

        return main_remotes, backup_remotes

    def _push_to_remotes(
        self,
        remotes: list[str],
        label: str,
        *,
        include_tag: bool = True,
    ) -> None:
        """
        Push commit and tag to given remotes.

        Args:
            remotes: list of remote names
            label: "main" or "backup"
            include_tag: Push an eligible resolved tag after the branch push.

        Raises:
            ValidationError on failure
        """

        for remote in remotes:
            logger.info(f"[cyan]→ Pushing to {remote} ({label})[/cyan]")

            # =========================================================
            # Dry-run
            # =========================================================
            if self.dry_run:
                logger.info(f"(dry-run) Would push HEAD to {remote}")
                if include_tag and not getattr(self, "skip_tag", False) and self.tag:
                    logger.info(f"(dry-run) Would push tag {self.tag} to {remote}")
                continue

            # =========================
            # Push commit (HEAD)
            # =========================
            try:
                self.gitService.push(remote=remote, ref="HEAD")
                logger.info(f"[green]✅ Commit pushed to {remote}[/green]")

            except Exception as e:
                context = self._push_failure_context(e, remote=remote)
                raise ValidationError(
                    message=f"Failed to push commit to {remote}.",
                    hint=self._push_failure_hint(e),
                    code="PUSH_FAILED",
                    context=context,
                ) from e

            # =========================
            # Push tag (if allowed)
            # =========================
            if not include_tag or getattr(self, "skip_tag", False) or not self.tag:
                logger.info(f"[dim]⏭️ Tag skipped for {remote}[/dim]")
                continue

            try:
                self.gitService.push_tag(remote=remote, tag=self.tag)
                logger.info(f"[green]🏷️ Tag pushed to {remote}[/green]")

            except Exception as e:
                context = self._push_failure_context(
                    e,
                    remote=remote,
                    tag=self.tag,
                )
                raise ValidationError(
                    message=f"Failed to push tag to {remote}.",
                    hint=self._push_failure_hint(e, is_tag=True),
                    code="PUSH_TAG_FAILED",
                    context=context,
                ) from e

    @staticmethod
    def _push_failure_hint(error: Exception, *, is_tag: bool = False) -> str:
        """Return an actionable hint for a Git push failure.

        Authentication failures are called out separately because a Docker
        container does not automatically share the host credential manager.
        Other failures retain the normal remote, network, and tag guidance.

        Args:
            error: Exception raised by the Git service.
            is_tag: Whether the failed operation was a tag push.

        Returns:
            A user-facing recovery hint.
        """

        detail = error.detail if isinstance(error, GitOperationError) else str(error)
        normalized = detail.lower()
        authentication_markers = (
            "authentication failed",
            "could not read username",
            "could not read password",
            "invalid username or password",
            "permission denied (publickey)",
            "terminal prompts disabled",
        )
        if any(marker in normalized for marker in authentication_markers):
            return (
                "Authenticate Git inside the current execution environment. "
                "Docker does not inherit the host credential-manager session; "
                "use SSH, allow the interactive prompt, or run "
                "'custy configure credentials' to configure Custy's optional "
                "external token fallback. Tokens are never stored in config.toml."
            )

        if is_tag:
            return "Ensure the tag exists and the remote is reachable and writable."

        return (
            "Check the remote URL, network connection, permissions, and branch policy."
        )

    @staticmethod
    def _push_failure_context(
        error: Exception,
        *,
        remote: str,
        tag: str | None = None,
    ) -> dict[str, object]:
        """Build structured push diagnostics without discarding Git output.

        Args:
            error: Exception raised by the Git service.
            remote: Remote name being processed.
            tag: Optional tag involved in the failed operation.

        Returns:
            Context suitable for the CLI validation-error renderer.
        """

        context: dict[str, object] = {
            "remote": remote,
            "error": str(error),
        }
        if tag:
            context["tag"] = tag
        if isinstance(error, GitOperationError):
            if error.returncode is not None:
                context["exit_code"] = error.returncode
            if error.detail:
                context["detail"] = error.detail

        return context

    def execute_post_workflow(self) -> None:
        """
        Execute post-release workflow transitions.

        This step runs after:
            - commit
            - tag
            - push

        Responsibilities:
            - finalize branch transitions (e.g. release → main)
            - cleanup temporary branches
            - apply workflow rules

        Behavior:
            - skipped if --skip-checks is enabled
            - executed only if workflow context is available
            - pauses for user confirmation if actions were performed
        """

        if self.skip_checks:
            logger.debug("[dim]Skipping post-workflow (skip_checks enabled)[/dim]")
            return

        # if not hasattr(self, "workflow_manager") or not hasattr(self, "workflow_case"):
        if not hasattr(self, "branchWorkflowManager") or not hasattr(
            self, "workflow_case"
        ):
            logger.debug("[dim]No workflow context → skipping post-workflow[/dim]")
            return

        logger.info("[blue]🔄 Executing post-release workflow...[/blue]")

        try:
            executed = self.branchWorkflowManager.run_final_workflow(
                case=self.workflow_case,
                to_tag=self.tag,
            )

            if executed:
                if self.dry_run:
                    logger.info(
                        "[dry_run](dry-run)[/dry_run] Workflow transition "
                        "mutations were simulated."
                    )
                else:
                    logger.info("[green]✅ Workflow transitions completed.[/green]")

                # input(
                #     "[dim]Press Enter to continue...[/dim]"
                # )

                if not self.dry_run:
                    input(
                        f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n"
                    )
            else:
                logger.debug("[dim]No post-workflow actions executed[/dim]")

        except Exception as e:
            raise ValidationError(
                message="Post-release workflow failed.",
                hint="Check branch state and workflow rules.",
                code="POST_WORKFLOW_FAILED",
                context={"error": str(e)},
            ) from e

    def run(self) -> None:
        """
        Execute full release workflow pipeline.

        This is the main orchestration method.

        Pipeline:
            0. Validation
            1. Version preparation
            2. Workflow initialization
            3. Message preparation
            4. Artifact generation
            5. User editing
            6. Post-edit validation
            7. Version updates
            8. Backup
            9. Cleanup
            10. Staging
            11. Commit (strategy-aware)
            12. Tag
            13. Push
            14. Post-workflow transitions
        """

        logger.info("[bold blue]🚀 Starting release workflow...[/bold blue]")

        # =========================================================
        # Phase 0–7
        # =========================================================
        self.validate()
        self.prepare_version_tag()
        self.initialize_workflow()
        self.prepare_tag_message()
        self.generate_release_artifacts()
        self.edit_release_files()
        self.validate_edited_files()

        # Phase 7.1
        self.apply_version_updates()
        # Phase 7.2
        self.generate_changelog_if_needed()

        # =========================================================
        # Phase 8–10
        # =========================================================
        self.backup_release_files()
        self.cleanup_backups()
        self.stage_changes()

        # =========================================================
        # Phase 11 (SPECIAL HANDLING)
        # =========================================================
        self.execute_commit_phase()

        # =========================================================
        # Phase 12–14
        # =========================================================
        self.create_tag()
        self.push_changes()
        self.execute_post_workflow()

        logger.info(
            "[bold green]🎉 Release workflow completed successfully.[/bold green]"
        )

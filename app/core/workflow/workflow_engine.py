# app/core/workflow/workflow_engine.py

from pathlib import Path
from typing import Optional, List

import re
import logging
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style

from app.constants.path import (
    CUSTY_TAG_MESSAGE_TEMPLATE,
    CUSTY_BACKUP_COMMIT_DIR,
    CUSTY_BACKUP_TAG_DIR,
    CHANGELOG_PATH,
)
from app.constants.git_workflow_rules import (
    ALLOWED_COMMIT_TYPES,
    NON_CRITICAL_BRANCHES,
)

from app.cli.constants.enums import (
    StrategyChoices, StageModeChoices, BumpChoices
)

from app.core.git_ops.helper import (
    CommitizenHelper,
    get_sorted_tags,
    maybe_assert_is_final,
    detect_project_strategy,
)
from app.core.git_ops.versioning import (
    ReleaseInfo,
    ReleaseNoteBuilder,
    VersionType,
    VersionBridge,
)
from app.core.git_ops.tag_strategy import (
    CommitizenStrategy,
    DateStrategy,
    GitCountStrategy,
    PEP440Strategy,
    SemverStrategy,
)
from app.core.git_ops.git.factory import create_git_service
from app.core.git_ops.git.service import GitService
from app.core.git_ops.commit.validator import validate_commit_message_format
from app.core.branch_workflow import BranchWorkflowManager
from app.core.changelog.generator import ChangelogGenerator
from app.core.backup import BackupManager
from app.core.exceptions.validation_error import ValidationError  # adjust if needed
from app.core.files.update_files import update_version_universal
from app.core.cleanup.backups.handle_cleanup_backups import HandleCleanupBackups
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

    def __init__(
        self,
        config: WorkflowConfig
    ) -> None:
        # =========================================================
        # 📦 Configuration (immutable input)
        # =========================================================
        self.config = config

        # ===== Inputs =====
        self.commit_message_input = config.commit_message_input
        self.commit_message_file = config.commit_message_file
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
        self.skip_checks = config.skip_checks

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
        self.tag: str = ""
        self.tag_message: str = ""
        self.changes_to_staged: List[str] = []

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
        self.ensure_commitizen_convention()
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
                code="NOT_GIT_REPO"
            )

    def ensure_remote_exists(self, remote: str = "origin"):
        """
        Ensure a required Git remote exists.

        Args:
            remote (str): Remote name to check (default: 'origin').

        Behavior:
            - Uses GitService abstraction
            - Can be skipped via --skip-checks
        """

        if self.skip_checks:
            return

        if not self.gitService.check_remote(remote):
            raise ValidationError(
                message=f"Git remote '{remote}' not found or unreachable.",
                hint=f"Add remote using: git remote add {remote} <url>",
                code="REMOTE_NOT_FOUND",
                context={"remote": remote}
            )

    def ensure_version_file(self):
        """
        Ensure version file exists.
        """

        # print("self.version_file", self.version_file)

        if not self.version_file or not self.version_file.exists():
            raise ValidationError(
                message=f"Version file '{self.version_file}' not found.",
                hint="Run `custy init config`",
                code="VERSION_FILE_NOT_FOUND"
            )

    def ensure_commit_message_file(self):
        """
        Ensure commit message file exists.
        """
        if not self.commit_message_file or not self.commit_message_file.exists():
            raise ValidationError(
                message=f"Commit message file '{self.commit_message_file}' not found.",
                hint="Run `custy init config`",
                code="COMMIT_MSG_FILE_NOT_FOUND"
            )

    def ensure_tag_message_file(self):
        """
        Ensure tag message file exists.
        """
        if not self.tag_message_file or not self.tag_message_file.exists():
            raise ValidationError(
                message=f"Tag message file '{self.tag_message_file}' not found.",
                hint="Run `custy init config`",
                code="TAG_MSG_FILE_NOT_FOUND"
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

        print("self.auto_stage===========",self.auto_stage)

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
                    logger.debug("⚠️ Still no staged files after auto-staging. but proceeding due to --force-commit.")
                    if self.force_commit:
                        logger.warning("⚠️ Proceeding due to --force-commit")
                        return

                    logger.debug("⚠️ [yellow]Warning[/yellow]: Still no staged changes after `git add .`")
                    confirm = input("No staged files. Continue? (y/n): ").strip().lower()
                    if confirm not in ["y", "yes"]:
                        raise ValidationError(
                            message="Aborted due to empty staging.",
                            hint="Stage files using `git add`",
                            code="EMPTY_STAGING_ABORTED"
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
                    code="AUTO_STAGE_FAILED"
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
                code="NO_STAGED_CHANGES"
            )

    def ensure_commitizen_convention(self):
        """
        Ensure commitizen convention.
        """
        if not self.commitizenHelper.check_commit:
            raise ValidationError(
                message=f"Checking commitizen convention '{self.commit_message_file}' not found.",
                hint="Use cz check --commit-msg-file (path)]",
                code="COMMITIZEN_CONVENTION_FAILED"
            )

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
                input(f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n")
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
            input(f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n")

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
        Generate commit and tag message files using ReleaseNoteBuilder.

        Uses:
            - GitService for tag retrieval
            - ReleaseNoteBuilder for structured output

        Side Effects:
            - writes commit-message.txt
            - writes tag-message.txt
        """

        version = self.tag
        print("version", version)
        version_type = VersionType.detect(version)

        all_tags = self.gitService.get_all_tags()
        sorted_tags = get_sorted_tags(all_tags)

        version_prefix = version.removeprefix("v")

        # Find prerelease tags
        prereleases = [
            t for t in sorted_tags
            if t.startswith(version_prefix)
            and re.search(r"(a|b|rc|dev)", t)
        ]
        prereleases = list(reversed(prereleases))
        latest_pre = prereleases[0] if prereleases else None

        # Detect changes since RC
        has_changes = True
        if version_type == VersionType.FINAL and latest_pre:
            rc_tags = [
                tag for tag in prereleases
                if re.search(r"rc\d+", tag.lower())
            ]
            has_changes = len(rc_tags) > 1

        info = ReleaseInfo(
            version=version,
            version_type=version_type,
            app_name="Custy",
            prerelease_tags=prereleases,
            latest_prerelease=latest_pre,
            has_changes_since_rc=has_changes,
        )

        builder = ReleaseNoteBuilder(info)

        # Write commit message
        if self.commit_message_file:
            commit_content = builder.build_commit_msg()

            if self.dry_run:
                logger.info(
                    "[dry_run](dry-run)[/dry_run] Would update release "
                    f"commit message: {self.commit_message_file}"
                )
            else:
                self.commit_message_file.write_text(
                    commit_content,
                    encoding="utf-8",
                )

        # Write tag message
        if self.tag_message_file:
            tag_content = builder.build_tag_msg()

            if self.dry_run:
                logger.info(
                    "[dry_run](dry-run)[/dry_run] Would update release "
                    f"tag message: {self.tag_message_file}"
                )
            else:
                Path(self.tag_message_file).write_text(
                    tag_content,
                    encoding="utf-8",
                )

    def edit_release_files(self) -> None:
        """
        Open commit and tag message files for user editing.

        Order:
            1. commit message file
            2. tag message file

        Behavior:
            - Skips missing files
            - Uses system editor (VSCode, Notepad fallback)
            - Respects dry-run mode
        """

        if self.commit_message_file:
            self.open_editor(self.commit_message_file, label="commit message")

        if self.tag_message_file:
            self.open_editor(self.tag_message_file, label="tag message")

    def open_editor(self, path: Path, label: str = "file") -> None:
        """
        Open a file in an external editor for user modification.

        Args:
            path (Path): File to open.
            label (str): Human-friendly name (for logging).

        Behavior:
            - Tries multiple editors (VSCode → Notepad fallback)
            - Blocks execution until editor is closed (if supported)
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

        editors = [
            ["code", "--wait"],   # VSCode
            ["notepad"],          # Windows fallback
        ]

        for editor_cmd in editors:
            try:
                if self.dry_run:
                    logger.info(f"(dry-run) Would open editor: {' '.join(editor_cmd)} {path}")
                    return

                result = self.gitService.executor.runner.run(
                    command=editor_cmd + [str(path)],
                    shell=True,
                    check=True,
                )

                if result is not None:
                    logger.info(f"✅ Finished editing {label}.")
                    return

            except Exception as e:
                logger.debug(f"Editor failed: {editor_cmd} → {e}")
                continue

        # ❌ If all editors fail
        raise ValidationError(
            message="Unable to open editor automatically.",
            hint="Please open and edit the file manually.",
            code="EDITOR_LAUNCH_FAILED",
            context={"file": str(path)},
        )

    def validate_edited_files(self) -> None:
        """
        Validate user-edited files and determine tagging behavior.
        """

        commit_type = validate_commit_message_format(self.commit_message_file)

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

        self.skip_tag = False

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

            logger.warning(
                f"Using latest tag instead: {self.tag}"
            )

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

        # =========================================================
        # Detect project type
        # =========================================================
        project_strategy = detect_project_strategy(
            cli_value=None,
            no_debug=self.no_debug,
        )

        logger.debug(f"Detected project strategy: {project_strategy}")

        # =========================================================
        # CASE 1: Python Project (PEP440 enforced here)
        # =========================================================
        if project_strategy == StrategyChoices.PEP440:
            logger.info("🐍 Python project detected → using PEP440 for version updates")

            version_to_use = self.tag

            # Convert if current tag is SemVer-like
            if "-" in self.tag:
                converted = VersionBridge.semver_to_pep440(self.tag)
                if converted:
                    logger.debug(f"Converted SemVer → PEP440: {self.tag} → {converted}")
                    version_to_use = converted

            # ---- Python version file ----
            self.update_python_version_file(version_override=version_to_use)

            # ---- cz.toml ----
            self.commitizenHelper.update_cz_toml_version(
                new_version=version_to_use
            )

            # ---- Project files (ONLY python) ----
            self.update_project_versions(
                version_override=version_to_use,
                project_type="python",
            )

        # =========================================================
        # CASE 2: Non-Python (SemVer / JS / etc.)
        # =========================================================
        else:
            logger.info("🌐 Non-Python project → skipping Python-specific updates")

            # Only update project files (Node / etc.)
            self.update_project_versions(
                version_override=self.tag,
                project_type="node",
            )

        # # If project type == python
        # self.update_python_version_file()
        # self.commitizenHelper.update_cz_toml_version(new_version=self.tag)

        # self.update_project_versions()
        # # self.generate_changelog_if_needed()

    def update_python_version_file(self, version_override: Optional[str] = None) -> None:
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

        content = f'# {self.version_file.name}\n\n__version__ = "{version}"\n'

        if self.dry_run:
            logger.info(f"(dry-run) Would update {self.version_file} → {version}")
            return

        self.version_file.write_text(content, encoding="utf-8")

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

        rendered = (
            self.changelogGenerator.generate()
        )

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
            backup_dir=CUSTY_BACKUP_TAG_DIR,
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
            logger.error(
                f"[red]⚠️ Failed to backup {label}: {e}[/red]"
            )

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
                logger.info("[cyan](dry-run)[/cyan] Would run Commitizen commit + check")
                return

            try:
                self.commitizenHelper.commit()
                logger.info("[green]✅ Commitizen commit created[/green]")

                self.commitizenHelper.check_commit()
                logger.info("[green]✅ Commit message validated by Commitizen[/green]")

            except Exception as e:
                raise ValidationError(
                    message="Commitizen commit failed.",
                    hint="Check Commitizen configuration and commit rules.",
                    code="COMMITIZEN_FAILED",
                    context={"error": str(e)},
                )

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
            logger.info(f"[dim]Using commit message file: {self.commit_message_file}[/dim]")

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
        try:
            self.gitService.commit(
                message=message,
                message_file=message_file,
            )

            logger.info("[green]✅ Commit created successfully.[/green]")

        except Exception as e:
            raise ValidationError(
                message="Failed to create commit.",
                hint="Check your commit message and repository state.",
                code="COMMIT_FAILED",
                context={"error": str(e)},
            )

    def is_commitizen_auto(self) -> bool:
        return self.strategy_input == StrategyChoices.COMMITIZEN and self.bump_level == BumpChoices.AUTO

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
                "[cyan](dry-run)[/cyan] Would create tag "
                f"[bold]{self.tag}[/bold]"
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
            )

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

    def push_changes(self) -> None:
        """
        Push commits and tags to configured remotes.

        Behavior:
            - uses user-provided remotes if available
            - Optionally pushes to backup remote(s)
            - falls back to 'origin' / 'backup' with confirmation
            - skips backup for non-critical branches
            - Respects skip_tag flag
            - Uses GitService abstraction

        Branch Rules:
            Backup push is skipped for branches starting with:
                - feature/
                - ci/
                - sandbox/
        """

        logger.info("[blue]🚀 Pushing changes...[/blue]")

        current_branch = self.gitService.get_current_branch()
        logger.debug(f"Current branch: {current_branch}")

        # =========================================================
        # Resolve main remotes
        # =========================================================
        main_remotes = self._resolve_main_remotes()

        # =========================================================
        # Resolve backup remotes
        # =========================================================
        backup_remotes = []

        if self.sync_backup:
            if any(current_branch.startswith(p) for p in NON_CRITICAL_BRANCHES):
                logger.warning(
                    f"[yellow]⛔ Skipping backup push for branch '{current_branch}'[/yellow]"
                )
            else:
                backup_remotes = self._resolve_backup_remotes()

        # =========================================================
        # Push main
        # =========================================================
        self._push_to_remotes(main_remotes, label="main")

        # =========================================================
        # Push backup
        # =========================================================
        if backup_remotes:
            self._push_to_remotes(backup_remotes, label="backup")

    def _resolve_main_remotes(self) -> list[str]:
        """
        Resolve main remotes list.

        Priority:
            1. self.main_remotes
            2. fallback to 'origin'
        """

        if self.main_remotes:
            return self.main_remotes

        # fallback to origin
        if self.gitService.check_remote("origin"):
            confirm = input(
                "No main remote provided. Use 'origin'? (y/n): "
            ).strip().lower()

            if confirm in ("y", "yes"):
                logger.info("[dim]Using default remote: origin[/dim]")
                return ["origin"]

        raise ValidationError(
            message="No valid main remote found.",
            hint="Provide --main-remotes or configure 'origin'.",
            code="MAIN_REMOTE_MISSING",
        )

    def _resolve_backup_remotes(self) -> list[str]:
        """
        Resolve backup remotes list.

        Priority:
            1. self.backup_remotes
            2. fallback to 'backup'
        """

        if self.backup_remotes:
            return self.backup_remotes

        if self.gitService.check_remote("backup"):
            confirm = input(
                "No backup remote provided. Use 'backup'? (y/n): "
            ).strip().lower()

            if confirm in ("y", "yes"):
                logger.info("[dim]Using default remote: backup[/dim]")
                return ["backup"]

        logger.warning("[yellow]⚠️ No backup remote configured.[/yellow]")
        return []

    def _push_to_remotes(self, remotes: list[str], label: str) -> None:
        """
        Push commit and tag to given remotes.

        Args:
            remotes: list of remote names
            label: "main" or "backup"

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
                if not getattr(self, "skip_tag", False) and self.tag:
                    logger.info(f"(dry-run) Would push tag {self.tag} to {remote}")
                continue

            # =========================
            # Push commit (HEAD)
            # =========================
            try:
                self.gitService.push(remote=remote, ref="HEAD")
                logger.info(f"[green]✅ Commit pushed to {remote}[/green]")

            except Exception as e:
                raise ValidationError(
                    message=f"Failed to push commit to {remote}.",
                    hint="Check remote or network connection.",
                    code="PUSH_FAILED",
                    context={"remote": remote, "error": str(e)},
                )

            # =========================
            # Push tag (if allowed)
            # =========================
            if getattr(self, "skip_tag", False) or not self.tag:
                logger.info(f"[dim]⏭️ Tag skipped for {remote}[/dim]")
                continue

            try:
                self.gitService.push_tag(remote=remote, tag=self.tag)
                logger.info(f"[green]🏷️ Tag pushed to {remote}[/green]")

            except Exception as e:
                raise ValidationError(
                    message=f"Failed to push tag to {remote}.",
                    hint="Ensure tag exists and remote is accessible.",
                    code="PUSH_TAG_FAILED",
                    context={"remote": remote, "tag": self.tag, "error": str(e)},
                )

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
        if (
            not hasattr(self, "branchWorkflowManager")
            or not hasattr(self, "workflow_case")
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
                    input(f"\n{Style.DIM}{Fore.LIGHTWHITE_EX}Press Enter to continue...\n{Style.RESET_ALL}\n")
            else:
                logger.debug("[dim]No post-workflow actions executed[/dim]")

        except Exception as e:
            raise ValidationError(
                message="Post-release workflow failed.",
                hint="Check branch state and workflow rules.",
                code="POST_WORKFLOW_FAILED",
                context={"error": str(e)},
            )

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

        logger.info("[bold green]🎉 Release workflow completed successfully.[/bold green]")

# app\git_commit_tagger.py
""" """

import re
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from colorama import Fore, Style
from termcolor import colored

from .utils import (ALLOWED_COMMIT_TYPES, BackupManager, ChangelogGenerator,
                    CommitizenHelper, CommitizenStrategy, DateStrategy,
                    GitCountStrategy, GitHelper, PEP440Strategy, ReleaseInfo,
                    ReleaseNoteBuilder, SemverStrategy, VersionType,
                    WorkflowManager, classify_commit_type, get_last_tag_before,
                    get_sorted_tags, maybe_assert_is_final)

# =======================
# 🚀 Main Class
# =======================


class GitCommitTagger:
    """Automates Git commit + tagging flow, with support for bumping, strategy, dry-run, and version file updates."""

    NON_CRITICAL_BRANCHES = ("feature/", "ci/", "sandbox/")

    def __init__(
        self,
        message_file: str,
        tag: str | None,
        tag_msg: str | None,
        tag_msg_file: str | None,
        strategy: str | None,
        bump: str | None,
        pre_release: str | None = None,
        post_release: bool | None = False,
        dev_release: bool | None = False,
        meta: str | None = None,
        epoch: int | None = None,
        force_tag: bool | None = False,
        dry_run: bool = False,
        version_file: str | None = None,
        auto_stage: bool | None = False,
        stage_mode: str | None = "all",
        force_changelog: bool | None = False,
        force_commit: bool | None = False,
        sync_backup: bool | None = False,
        skip_checks: bool | None = False,
        no_debug: bool | None = False,
    ) -> None:
        self.message_path: Path = Path(message_file)
        self.tag_input: str | None = tag
        self.tag_msg_input: str | None = tag_msg
        self.tag_msg_file: Path | None = Path(tag_msg_file)
        self.strategy_input: str | None = strategy
        self.bump_level: str | None = bump
        self.pre_release: str | None = pre_release
        self.post_release: bool | None = post_release
        self.dev_release: bool | None = dev_release
        self.meta: str | None = meta
        self.epoch: int | None = epoch
        self.force_tag: bool | None = force_tag
        self.dry_run: bool = dry_run
        self.version_file: str | None = Path(version_file) if version_file else None
        self.auto_stage: bool | None = auto_stage
        self.stage_mode: str | None = stage_mode
        self.force_changelog: bool | None = force_changelog
        self.force_commit: bool | None = force_commit
        self.sync_backup = sync_backup
        self.skip_checks = skip_checks
        self.no_debug = no_debug

        self.tag: str = ""
        self.tag_msg: str = ""
        self.backup_commit_message_path: Path = None
        self.backup_tag_message_path: Path = None
        self.changes_to_staged: list = []

        self.git = GitHelper(dry_run=dry_run)
        self.cz = CommitizenHelper(dry_run=dry_run)
        self.changelog_generator = ChangelogGenerator(dry_run=dry_run)
        self.backup_manager = BackupManager(keep=10)
        self.workflow_manager = WorkflowManager(
            no_debug=self.no_debug,
            sync_backup=self.sync_backup,
            dry_run=self.dry_run,
        )

        if self.no_debug:
            self.git.runner.set_silent(True)
            self.cz.runner.set_silent(True)
            self.changelog_generator.runner.set_silent(True)
            print("🐞  No Debug")

    # =======================
    # Public API
    # =======================

    def execute_commit_tag_bump(self) -> None:
        """(If not using commitizen)
        Main execution pipeline (Template Method pattern).

        1. Validate git repository, files, etc
        2. Add stage if needed
        3. Open editor for commit message
        4. Check commit message
        5. Determine next version (tag)
        6. Update __version__.py with that tag
        7. Update cz.toml version with that tag
        8. Stage and commit all changes (including version bump)
        9. Tag that commit
        """
        if self.strategy_input == "commitizen" and self.bump_level == "auto":
            self._handle_commitizen_only()
        else:
            self._handle_manual_or_semver()
        print(f"\n✅ Success: Commit, tag '{self.tag}, and bump'.\n")

    def execute_all(self) -> None:
        """(If not using commitizen)
        Main execution pipeline (Template Method pattern).

        1. Validate git repository, files, etc
        2. Add stage if needed
        3. Open editor for commit message
        4. Check commit message
        5. Determine next version (tag)
        6. Update __version__.py with that tag
        7. Update cz.toml version with that tag
        8. Stage and commit all changes (including version bump)
        9. Tag that commit
        10. Push commit and tag
        11. generate CHANGELOG.md
        12. Commit and push CHANGELOG.md
        13. backup commit message. Not the commit message for  changelog.md changes
        """
        self.execute_commit_tag_bump()
        print(f"\n{Fore.LIGHTCYAN_EX}[*] Push changes...{Style.RESET_ALL}\n")
        self.push_changes()
        self._generate_changelog()

        self.finalize_workflow()

        print(f"\n✅ Success: Commit, tag '{self.tag}', bump and pushed.\n")

    def validate_workflow_transition(self):
        """
        Validates that the current branch and tag match the expected project strategy
        transition rules (e.g. develop → release → main).
        """
        if not self.skip_checks:
            self.workflow_manager = WorkflowManager(
                no_debug=self.no_debug,
                sync_backup=self.sync_backup,
                dry_run=self.dry_run,
            )
            self.workflow_case = self.workflow_manager.check_transition(to_tag=self.tag)
            input(f"{Fore.LIGHTWHITE_EX}Press Enter to continue...{Style.RESET_ALL}")
            self.workflow_manager.run_initial_workflow(
                case=self.workflow_case,
                to_tag=self.tag,
            )
        else:
            input(f"{Fore.LIGHTWHITE_EX}Press Enter to continue...{Style.RESET_ALL}")

    def finalize_workflow(self):
        """
        Executes the final workflow steps after tagging and pushing,
        such as merging hotfixes or cleaning up release branches.
        """
        executed = False
        if not self.skip_checks:
            if hasattr(self, "workflow_case") and hasattr(self, "workflow_manager"):
                executed = self.workflow_manager.run_final_workflow(
                    case=self.workflow_case,
                    to_tag=self.tag,
                )

        if executed:
            input(f"{Fore.LIGHTWHITE_EX}Press Enter to exit...{Style.RESET_ALL}")

    def validate(self) -> None:
        self._ensure_git_repo()

        if not self.message_path.exists():
            print(f"❌ ERROR: Message file '{self.message_path}' not found.")
            sys.exit(1)

        self._ensure_staged_changes()

    def push_changes(self):
        """
        Pushes commits and tags to the origin remote, and optionally to the backup remote.

        This method always pushes to 'origin'. If `sync_backup` is enabled, it also pushes
        to 'backup', unless the current branch matches a non-critical pattern (e.g., feature/, ci/, sandbox/).

        Branches excluded from backup push:
        - feature/*
        - ci/*
        - sandbox/*
        """
        self._push("origin")

        # Only push to backup if allowed
        if getattr(self, "sync_backup", False):
            current_branch = self.git.get_current_branch()

            # Don't sync backup if on feature/*, ci/*, sandbox/*
            if any(
                current_branch.startswith(prefix)
                for prefix in self.NON_CRITICAL_BRANCHES
            ):
                print(
                    f"⛔ Skipping backup push and branch '{current_branch}' (not critical) on backup remote",
                )
                return

            self._push("backup")

    # =======================
    # Private
    # =======================

    def _generate_changelog(self):
        # Enforce final version before generating changelog
        if maybe_assert_is_final(
            self.tag,
            context="changelog",
            force=self.force_changelog,
        ):
            # Generate and push changelog
            print(f"\n{Fore.BLUE}[*] Generating changelog...{Style.RESET_ALL}\n")
            rendered = self.changelog_generator.generate()
            self.changelog_generator.write_to_files(
                content=rendered,
                path="CHANGELOG.md",
            )
            remotes = ["origin"]
            if getattr(self, "sync_backup", False):
                remotes.append("backup")
            self.git.commit_and_push_changelog(remotes=remotes)

    def _handle_commitizen_only(self):
        self.validate()
        self.git.check_remote_origin()
        self._resolve_tag()
        self._update_version_file()
        self._backup_commit_message()
        self._stage_pre_commit()
        self.cz.commit()
        self.cz.check_commit()
        self._tag()

    def _handle_manual_or_semver(self):
        print(f"\n{Fore.LIGHTYELLOW_EX}[*] Begin validation...{Style.RESET_ALL}\n")
        self.validate()
        self.git.check_remote_origin()
        self._resolve_tag()
        self.validate_workflow_transition()
        print(f"\n{Fore.CYAN}[*] Opening editor...{Style.RESET_ALL}\n")
        self._generate_release_notes()
        # self._prepare_and_edit_release_message_if_final()
        self._open_editor(self.tag_msg_file)
        print(f"📋 Allowed commit types: {', '.join(sorted(ALLOWED_COMMIT_TYPES))}")
        self._open_editor(self.message_path)
        print(f"\n{Fore.LIGHTBLUE_EX}[*] Validating messages...{Style.RESET_ALL}\n")
        self._validate_commit_type_for_tagging()
        self._maybe_use_latest_tag()
        # self.cz.check_commit(path=self.message_path,)  # Use the format  agreed upon with Commitizen.
        self.git.check_commit_message_file(self.message_path)
        print(f"\n{Fore.MAGENTA}[*] Writing version to files...{Style.RESET_ALL}\n")
        self._update_version_file()
        self.cz.update_cz_toml_version(new_version=self.tag)
        print(f"\n{Fore.LIGHTYELLOW_EX}[*] Backup phase...{Style.RESET_ALL}\n")
        self._backup_tag_message_with_check()
        self._backup_commit_message()
        print(f"\n{Fore.GREEN}[*] Commit & tag operation...{Style.RESET_ALL}\n")
        self._stage_pre_commit()
        self._commit()
        self._tag()

    def _resolve_tag(self) -> None:
        # if self.bump_level:
        #     current_tag = self.get_latest_tag()
        #     self.tag = self.bump_version(current_tag, self.bump_level)
        # elif self.tag_input:
        #     self.tag = self.tag_input
        if self.tag_input:
            self.tag = self.tag_input
        # elif self.strategy_input == "semver" and self.bump_level:
        elif self.strategy_input == "semver":
            self.tag = SemverStrategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                build_meta=self.meta,
                no_debug=self.no_debug,
            ).get_next_tag()
        # elif self.strategy_input == "pep440" and self.bump_level:
        elif self.strategy_input == "pep440":
            self.tag = PEP440Strategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                post_release=self.post_release,
                dev_release=self.dev_release,
                local=self.meta,
                epoch=self.epoch,
                no_debug=self.no_debug,
            ).get_next_tag()
        elif self.strategy_input == "commitizen" and self.bump_level == "auto":
            self.tag = CommitizenStrategy(self.pre_release).get_next_tag()
        elif self.strategy_input == "date":
            self.tag = DateStrategy().get_next_tag()
        elif self.strategy_input == "gitcount":
            self.tag = GitCountStrategy().get_next_tag()
        else:
            print("❌ ERROR: Provide either --tag or use  --strategy with --bump.")
            sys.exit(1)

        print(f"🔖  Next version: {self.tag}")

        # self.tag_msg = self.tag_msg_input or self.tag
        self._resolve_tag_message()

    def _resolve_tag_message(self) -> None:
        """
        Resolve tag message: use CLI --tag-msg, or fallback to tag-msg.txt or tag name.
        1. CLI argument --tag-msg (self.tag_msg_input)
        2. CLI argument --tag-msg-file (self.tag_msg_file) (Open editor if file doesn't exist)
        3. Fallback to default: 'Release vX.Y.Z'
        """
        if self.tag_msg_input:
            self.tag_msg = self.tag_msg_input
            print("✅ Using tag message from --tag-msg CLI input.")
            return

        tag_msg_path = Path(self.tag_msg_file or "templates/tag-msg.txt")

        if not tag_msg_path.exists():
            # Create file with default content
            default_content = (
                f"Release {self.tag}\n\n# Write additional tag notes below\n"
            )
            tag_msg_path.parent.mkdir(parents=True, exist_ok=True)
            tag_msg_path.write_text(default_content, encoding="utf-8")
            print(f"📝 Created default tag message file: {tag_msg_path}")

    def _backup_tag_message_with_check(self):
        # Read edited content
        if self.tag_msg_file.exists():
            self.tag_msg = self.tag_msg_file.read_text(encoding="utf-8").strip()
            print(f"📄 Using tag message from: {self.tag_msg_file}")
            self._backup_tag_message()
        else:
            self.tag_msg = self.tag
            print(
                f"ℹ️ No tag message provided. Using tag name as message: '{self.tag_msg}'",
            )

    def _maybe_use_latest_tag(self):
        if getattr(self, "skip_tag", False):
            self.tag = self.git.get_latest_tag()
            print(
                f"🚫 Skipping tag resolution due to disallowed commit type. Using current tag instead: {self.tag}",
            )
            return

    def _update_version_file(self) -> None:
        if not self.version_file:
            return

        content = f'__version__ = "{self.tag}"\n'

        if self.dry_run:
            print(f"(dry-run) Would write to {self.version_file}: {content.strip()}")
            # print(f"(dry-run) Would generate tag: {self.tag}")
        else:
            if not self.version_file.exists():
                print(f"❌ ERROR: Version file '{self.version_file}' not found.")
                sys.exit(1)
            self.version_file.write_text(content)
            print(f"✅ Updated version file: {self.version_file}")

    def _stage_pre_commit(self):
        """
        Stage all relevant files before committing.
        Includes version file, .cz.toml, and optional backup file.
        """
        self.changes_to_staged.append(".cz.toml")
        if self.version_file:
            self.changes_to_staged.append(self.version_file)

        # Optionally deduplicate and remove falsy values
        files_to_stage = list({f for f in self.changes_to_staged if f})

        self.git.stage_files(files_to_stage)

    def _open_editor(self, path: Path) -> None:
        print(f"📝 Opening {path} for editing...")
        editors = [["code", "--wait"], ["notepad"]]
        for editor_cmd in editors:
            try:
                if not self.dry_run:
                    self.git.runner.run(
                        command=editor_cmd + [str(path)],
                        shell=True,
                        check=True,
                    )
                return
            except Exception:
                continue
        print("❌ ERROR: Could not open editor. Please edit the message file manually.")
        sys.exit(1)

    def _validate_commit_type_for_tagging(self) -> None:
        """
        Check if commit message matches an allowed type for tagging.
        If not and --force-tag is not used, set skip_tag=True.
        """
        commits_msg = self.message_path.read_text(encoding="utf-8")
        first_line = commits_msg.strip().splitlines()[0] if commits_msg.strip() else ""
        commit_type = classify_commit_type(first_line=first_line)

        if commit_type:
            if commit_type not in ALLOWED_COMMIT_TYPES:
                if not self.force_tag:
                    print(
                        f"🚫 Skipping tag: commit types `{commit_type}` is not allowed.",
                    )
                    print(f"ℹ️ Allowed types: {sorted(ALLOWED_COMMIT_TYPES)}")
                    print("ℹ️ Use --force-tag to override.")
                    print(
                        "💡 Note: Don't forget to manually update the version in commit-msg.txt",
                    )
                    print(
                        "           → Use the current latest tag or whatever version you determine.",
                    )
                    print("ℹ️ Use --force-tag to override.")
                    input(
                        f"{Fore.LIGHTWHITE_EX}Press Enter to continue...{Style.RESET_ALL}",
                    )
                    self.skip_tag = True
                else:
                    print(
                        f"⚠️ Forcing tag despite disallowed commit type `{commit_type}`.",
                    )
        elif not self.force_tag:
            print(
                "🚫 Skipping tag: could not detect valid commit type.",
            )
            print(f"ℹ️ Allowed types: {sorted(ALLOWED_COMMIT_TYPES)}")
            print("ℹ️ Use --force-tag to override.")
            input(
                f"{Fore.LIGHTWHITE_EX}Press Enter to continue...{Style.RESET_ALL}",
            )
            self.skip_tag = True
        else:
            print("⚠️ Forcing tag despite unrecognized commit type.")

    def _ensure_staged_changes(self) -> None:
        if self.git.has_staged_files():
            return  # ✅ All good

        if self.auto_stage:
            print("⚠️ No staged changes detected.")
            print("📦 Auto-running: git add .")

            if self.stage_mode == "update":
                self.git.auto_stage_update()
            else:
                self.git.auto_stage_all()

            if not self.dry_run:
                # 🔁 Re-check after auto-staging
                if not self.git.has_staged_files():
                    if self.force_commit:
                        print(
                            "⚠️ Still no staged files after auto-staging. but proceeding due to --force-commit.",
                        )
                        return
                    self._error_exit("Still no staged changes after `git add .`")

            staged_files = self.git.list_staged_files()
            if staged_files:
                print(colored("📝 File staged for commit:", "cyan"))
                for file in staged_files:
                    print(colored(f"  -{file}", "green"))
            else:
                print("⚠️ No files were staged.")
                if self.force_commit:
                    print("⚠️ Proceeding with empty due to --force-commit.")
                    return
                self._error_exit("No files staged after auto-stage.")
        elif self.force_commit:
            print("⚠️ No staged files, but proceeding due to --force-commit.")
            return
        else:
            print("❌ Error: No staged changes to commit.")
            print("💡 Hint: Stage files using `git add <file>` or `git add .`")
            sys.exit(1)

    def _ensure_git_repo(self):
        if not self.git.is_get_repo():
            print("❌ ERROR: Not a Git repository.")
            print("💡 Hint: Initialize git repository using `git init`")
            sys.exit(1)

    def _commit(self) -> None:
        command = ["git", "commit", "-F", str(self.message_path)]
        if self.force_commit and not self.git.has_staged_files():
            command.append("--allow-empty")

        self.git.runner.run(
            command=command,
            check=True,
            on_error=lambda: self._error_exit("Failed to commit."),
        )

    def _tag(self) -> None:
        if not getattr(self, "skip_tag", False) and self.tag:
            self.git.runner.run(
                command=["git", "tag", "-a", self.tag, "-m", self.tag_msg],
                check=True,
                on_error=lambda: self._error_exit(
                    f"Failed to create tag '{self.tag}'.",
                ),
            )
        else:
            print("⏭️ Tag step skipped.")

    def _push(self, remote: str = "origin") -> None:
        """
        Pushes the current commit and optionally the tag to the specified remote.

        Args:
            remote (str): The Git remote to push to (default: "origin")

        Behavior:
            - Always pushes the current HEAD commit.
            - Pushes the tag only if tagging is enabled and `self.tag` is set.
            - Skips tag push if `skip_tag` is True or `self.tag` is not set.

        """
        print(f"🔁 Pushing to {remote} remote...")
        self.git.runner.run(
            command=["git", "push", remote, "HEAD"],
            check=True,
            on_error=lambda: self._error_exit(
                f"Failed to push commit to {remote} remote.",
            ),
        )
        # Push tag only if tagging wasn't skipped
        if not getattr(self, "skip_tag", False) and self.tag:
            self.git.runner.run(
                command=["git", "push", remote, self.tag],
                check=True,
                on_error=lambda: self._error_exit(
                    f"Failed to push tag '{self.tag} to {remote} remote'.",
                ),
            )
        else:
            print(f"⏭️ Tag push to {remote} remote skipped.")

    def _error_exit(self, message: str) -> None:
        print(f"❌ ERROR: {message}")
        sys.exit(1)

    def _backup_commit_message(self) -> None:
        if not self.message_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.message_path.parent / "backups" / "commit"
        backup_dir.mkdir(exist_ok=True)

        # backup_path = backup_dir / self.message_path.with_name(f"{self.message_path.stem}_{timestamp}.bak.txt")
        self.backup_commit_message_path = (
            backup_dir / f"{self.message_path.stem}_{timestamp}.bak.txt"
        )

        try:
            self.backup_commit_message_path.write_text(self.message_path.read_text())
            print(f"🗂️ Commit message backed up to: {self.backup_commit_message_path}")
            old_files = self.backup_manager._prune_old_backups(
                backup_dir=backup_dir,
                stem=self.message_path.stem,
            )

            if self.backup_commit_message_path:
                self.changes_to_staged.append(self.backup_commit_message_path)
            if old_files:
                self.changes_to_staged += old_files

        except Exception as e:
            print(f"⚠️ Failed to backup commit message: {e}")

    def _backup_tag_message(self) -> None:
        """
        Backup the tag message file with a timestamp
        """
        if not self.tag_msg_file:
            return

        tag_msg_path = Path(self.tag_msg_file)
        if not tag_msg_path.exists():
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = self.message_path.parent / "backups" / "tag"
            backup_dir.mkdir(exist_ok=True)

            self.backup_tag_message_path = (
                backup_dir / f"{tag_msg_path.stem}_{timestamp}.bak.txt"
            )
            content = tag_msg_path.read_text(encoding="utf-8")
            self.backup_tag_message_path.write_text(content, encoding="utf-8")
            print(f"🗂️ Tag message backed up to: {self.backup_tag_message_path}")
            old_files = self.backup_manager._prune_old_backups(
                backup_dir=backup_dir,
                stem=tag_msg_path.stem,
            )

            if self.backup_tag_message_path:
                self.changes_to_staged.append(self.backup_tag_message_path)
            if old_files:
                self.changes_to_staged += old_files

        except Exception as e:
            print(f"⚠️ Failed to backup tag commit message: {e}")

    def _prepare_release_message_from_prereleases(self, version: str) -> str:
        """ """
        version_prefix = version.removeprefix("v")  # handle both v1.3.4 abd 1.3.4
        all_tags = (
            self.git.get_all_tags()
        )  # expects list[str], e.g. ['1.3.4a1', '1.3.4b2', '1.3.3', ...]
        sorted_tags = get_sorted_tags(all_tags)

        # Find matching pre-release tags for this version, e.g., 1.3.4a1, b1, rc1...
        prerelease_tags = [
            t
            for t in sorted_tags
            if t.startswith(version_prefix) and re.search(r"(a|b|rc|dev)\d*", t)
        ]
        prerelease_tags = list(reversed(prerelease_tags))  # Newest tag first

        if not prerelease_tags:
            return f"Release v{version}\n\n---\n\n_No pre-release tags found for {version}_"

        sections = []

        for i, tag in enumerate(prerelease_tags):
            # Find previous tag to compute commit range
            if i + 1 < len(prerelease_tags):
                prev_tag = prerelease_tags[i + 1]
            else:
                prev_tag = get_last_tag_before(tag, sorted_tags)

            commits = self.git.get_commits_between_tags(prev_tag, tag)

            if not commits:
                continue

            section_lines = [f"### 🔹 from tag: {tag}\n"]

            for c in commits:
                sha = c["sha"][:7]
                author = c["author"]
                date = datetime.strptime(c["date"], "%a %b %d %H:%M:%S %Y %z")
                header = c["header"]
                body = self._clean_commit_body(c["body"])

                commit_block = dedent(f"""
                    -  **{header}**
                    _SHA: {sha}_
                    _Author: {author}_
                    _Date: {date}_

                    {body.strip()}
                """).strip()

                section_lines.append(commit_block)

            sections.append("\n\n".join(section_lines))

        final_output = f"Release v{version}\n\n---\n\n" + "\n\n---\n\n".join(sections)
        return final_output

    def _clean_commit_body(self, body: str) -> str:
        """
        Remove 'Changelog: handled separately' from footer/body
        """
        lines = body.strip().splitlines()
        cleaned = [
            line for line in lines if "Changelog: handled separately" not in line
        ]
        return "\n".join(cleaned).strip()

    def _write_template_to_message_file(self, content: str):
        """
        Write prefilled message content to both commit-msg.txt and tag-msg.txt
        """
        if self.message_path:
            self.message_path.write_text(content.strip(), encoding="utf-8")
        if self.tag_msg_file:
            Path(self.tag_msg_file).write_text(content.strip(), encoding="utf-8")

    def _is_pre_release(self, version: str) -> bool:
        return bool(re.search(r"(a|b|rc|dev)\d*", version))

    def _prepare_and_edit_release_message_if_final(self):
        """
        If this is a final release (not pre-release), aggregate commits
        and prefill both commit and tag message files before opening editor.
        """
        if not self._is_pre_release(self.tag) and self.pre_release is None:
            notes = self._prepare_release_message_from_prereleases(self.tag)
            self._write_template_to_message_file(notes)
        self._open_editor(self.message_path)

    def _generate_release_notes(self):
        """
        Generate commit-msg.txt and tag-msg.txt using ReleaseNoteBuilder.
        """
        version = self.tag
        version_type = VersionType.detect(version)
        all_tags = self.git.get_all_tags()
        sorted_tags = get_sorted_tags(all_tags)
        version_prefix = version.removeprefix("v")

        # Find pre-release tags this version (e.g. v1.4.0a1, rc1, etc.)
        prereleases = [
            t
            for t in sorted_tags
            if t.startswith(version_prefix) and re.search(r"(a|b|rc|dev)", t)
        ]
        prereleases = list(reversed(prereleases))
        latest_pre = prereleases[0] if prereleases else None

        # Determine if there are any changes since last RC/prerelease
        has_changes = True
        if version_type == VersionType.FINAL and latest_pre:
            # changes = self.git.get_commits_between_tags(latest_pre, version)
            rc_tags = [tag for tag in prereleases if re.search(r"rc\d+", tag.lower())]
            # has_changes = bool(changes)
            has_changes = len(rc_tags) > 1

        # Build structured release info
        info = ReleaseInfo(
            version=version,
            version_type=version_type,
            app_name="Custy",
            prerelease_tags=prereleases,
            latest_prerelease=latest_pre,
            has_changes_since_rc=has_changes,
        )

        builder = ReleaseNoteBuilder(info)

        # Write commit-msg.txt
        if self.message_path:
            self.message_path.write_text(builder.build_commit_msg(), encoding="utf-8")

        # Write tag-msg.txt
        if self.tag_msg_file:
            Path(self.tag_msg_file).write_text(
                builder.build_tag_msg(),
                encoding="utf-8",
            )

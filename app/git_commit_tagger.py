# tools\git_commit\git_commit_tagger.py
""" """

import sys
from datetime import datetime
from pathlib import Path

from termcolor import colored

from .utils import (ChangelogGenerator, CommitizenHelper, CommitizenStrategy,
                    DateStrategy, GitCountStrategy, GitHelper, SemverStrategy)

# =======================
# 🚀 Main Class
# =======================


class GitCommitTagger:
    """Automates Git commit + tagging flow, with support for bumping, strategy, dry-run, and version file updates."""

    def __init__(
        self,
        message_file: str,
        tag: str | None,
        tag_msg: str | None,
        strategy: str | None,
        bump: str | None,
        pre_release: str | None = None,
        post_release: bool | None = False,
        dev_release: bool | None = False,
        local: str | None = None,
        epoch: int | None = None,
        dry_run: bool = False,
        version_file: str | None = None,
        auto_stage: bool | None = False,
        stage_mode: str | None = "all",
    ) -> None:
        self.message_path: Path = Path(message_file)
        self.tag_input: str | None = tag
        self.tag_msg_input: str | None = tag_msg
        self.strategy_input: str | None = strategy
        self.bump_level: str | None = bump
        self.pre_release: str | None = pre_release
        self.post_release: bool | None = post_release
        self.dev_release: bool | None = dev_release
        self.local: str | None = local
        self.epoch: int | None = epoch
        self.dry_run: bool = dry_run
        self.version_file: str | None = Path(version_file) if version_file else None
        self.auto_stage: bool | None = auto_stage
        self.stage_mode: str | None = stage_mode

        self.tag: str = ""
        self.tag_msg: str = ""
        self.backup_path: Path = None

        self.git = GitHelper(dry_run=dry_run)
        self.cz = CommitizenHelper(dry_run=dry_run)
        self.changelog_generator = ChangelogGenerator(dry_run=dry_run)

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
        self.push()
        rendered = self.changelog_generator.generate()
        self.changelog_generator.write_to_files(rendered)
        self.git.commit_and_push_changelog()

        print(f"\n✅ Success: Commit, tag '{self.tag}', bump and pushed.\n")

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
        self.validate()
        self.git.check_remote_origin()
        self._resolve_tag()
        self._open_editor()
        #self.cz.check_commit(path=self.message_path,)  # Use the format  agreed upon with Commitizen.
        self.git.check_commit_message_file(self.message_path)
        self._update_version_file()
        self.cz.update_cz_toml_version(new_version=self.tag)
        self._backup_commit_message()
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
        elif self.strategy_input == "semver" and self.bump_level:
            self.tag = SemverStrategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                post_release=self.post_release,
                dev_release=self.dev_release,
                local=self.local,
                epoch=self.epoch,
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

        print(self.tag)

        self.tag_msg = self.tag_msg_input or self.tag

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

        files_to_stage = [".cz.toml"]
        if self.version_file:
            files_to_stage.append(self.version_file)
        if self.backup_path:
            files_to_stage.append(self.backup_path)

        # Optionally deduplicate and remove falsy values
        files_to_stage = list({f for f in files_to_stage if f})

        self.git.stage_files(files_to_stage)

    def _open_editor(self) -> None:
        print(f"📝 Opening {self.message_path} for editing...")
        editors = [["code", "--wait"], ["notepad"]]
        for editor_cmd in editors:
            try:
                if not self.dry_run:
                    self.git.runner.run(
                        command=editor_cmd + [str(self.message_path)],
                        shell=True,
                        check=True,
                    )
                return
            except Exception:
                continue
        print("❌ ERROR: Could not open editor. Please edit the message file manually.")
        sys.exit(1)

    def validate(self) -> None:
        self._ensure_git_repo()

        if not self.message_path.exists():
            print(f"❌ ERROR: Message file '{self.message_path}' not found.")
            sys.exit(1)

        self._ensure_staged_changes()

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

            # 🔁 Re-check after auto-staging
            if not self.git.has_staged_files():
                self._error_exit("Still no staged changes after `git add .`")

            staged_files = self.git.list_staged_files()
            if staged_files:
                print(colored("📝 File staged for commit:", "cyan"))
                for file in staged_files:
                    print(colored(f"  -{file}", "green"))
            else:
                print("⚠️ No files were staged.")
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
        self.git.runner.run(
            command=["git", "commit", "-F", str(self.message_path)],
            check=True,
            on_error=lambda: self._error_exit("Failed to commit."),
        )

    def _tag(self) -> None:
        self.git.runner.run(
            command=["git", "tag", "-a", self.tag, "-m", self.tag_msg],
            check=True,
            on_error=lambda: self._error_exit(f"Failed to create tag '{self.tag}'."),
        )

    def push(self) -> None:
        self.git.runner.run(
            command=["git", "push", "origin", "HEAD"],
            check=True,
            on_error=lambda: self._error_exit("Failed to push commit."),
        )
        self.git.runner.run(
            command=["git", "push", "origin", self.tag],
            check=True,
            on_error=lambda: self._error_exit(f"Failed to push tag '{self.tag}'."),
        )

    def _error_exit(self, message: str) -> None:
        print(f"❌ ERROR: {message}")
        sys.exit(1)

    def _backup_commit_message(self) -> None:
        if not self.message_path.exists():
            return

        timestamp = datetime.now().strftime("%%Y%m%d_%H%M%S")
        backup_dir = self.message_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)

        # backup_path = backup_dir / self.message_path.with_name(f"{self.message_path.stem}_{timestamp}.bak.txt")
        self.backup_path = backup_dir / f"{self.message_path.stem}_{timestamp}.bak.txt"

        try:
            self.backup_path.write_text(self.message_path.read_text())
            print(f"🗂️ commit message backed up to: {self.backup_path}")
        except Exception as e:
            print(f"⚠️ Failed to backup commit message: {e}")

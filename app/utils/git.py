# tools\utils\git.py

"""
Utilities Class (Git)
"""

import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from ..errors.validation_error import ValidationError
from .dry_run_support import DryRunSupport

# =======================
# 🔧 Utilities CLass
# =======================


class GitHelper(DryRunSupport):
    """
    Helper class for Git-related operations.
    """

    def _on_error(self, context: str) -> Callable:
        """
        Returns a reusable error handler for subprocess errors.

        Args:
            context: (str): Description of the failed operation.

        Returns:
            Callable: Function to call n error.

        """

        def handler():
            print(f"❌ ERROR: failed to {context}.")
            print(
                "💡 Make sure this is a valid Git repository and you're on the correct branch.",
            )
            sys.exit(1)

        return handler

    def _error_exit(self, message: str) -> None:
        print(f"❌ ERROR: {message}")
        sys.exit(1)

    def is_get_repo(self) -> bool:
        """Git rev-parse --is-inside-work-tree"""
        command = ["git", "rev-parse", "--is-inside-work-tree"]
        return (
            Path(".git").exists()
            or self.runner.run(
                command=command,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode
            == 0
        )

    def has_staged_files(self) -> bool:
        """
        Check if there are any staged (tracked) files to commit.
        """
        """git diff --cached --quiet"""
        try:
            result = self.runner.run(
                ["git", "diff", "--cached", "--quiet"],
                check=False,
            )
            return result.returncode != 0
        except Exception:
            return False

    def auto_stage_all(self) -> None:
        """
        Run `git add .` to stage all changes
        Stage all modified, deleted, and untracked files.
        """
        self.runner.run(
            ["git", "add", "."],
            check=True,
            on_error=lambda: self._error_exit("Failed to stage files with `git add .`"),
        )

    def auto_stage_update(self) -> None:
        """
        Run `git add --update`
        Stage only modified and deleted tracked files (not new files).
        """
        self.runner.run(
            ["git", "add", "--update"],
            check=True,
            on_error=lambda: self._error_exit(
                "Failed to stage files with `git add --update",
            ),
        )

    def stage_files(self, files: list[Path]) -> None:
        """
        Stage specific files using `git add <file1> <file2> ...`

        Args:
            files: list[Path]: List of file paths to stage.
        """
        self.runner.run(
            ["git", "add", *files],
            check=True,
            on_error=lambda: self._error_exit(f"Failed to stage files: {', '.join(files)}`"),
        )

    def list_staged_files(self) -> list[str]:
        """
        Returns a list of staged files.
        """
        result = self.runner.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
            on_error=lambda: print("❌ERROR: Failed to list staged files."),
        )
        if result and result.stdout:
            return result.stdout.strip().splitlines()
        return []

    def check_commit_message_file(self, file_path: Path):
        """
        Validates a commit message from a file using Conventional Commit rules.
        Validates a structured commit message (header + optional body/footer).

        Args:
            file_path (Path): Path to the commit message file.
        """

        CONVENTIONAL_TYPES = {
            "feat", "fix", "docs", "style", "refactor",
            "perf", "test", "chore", "ci", "build", "release"
        }
        HEADER_REGEX = re.compile(
            r"(?P<type>\w+)(\((?P<scope>[^\)]+)\))?!?: (?P<summary>.+)$"
        )
        try:
            if not file_path.exists() or not file_path.is_file():
                raise ValidationError(f"❌ Commit message file not found: {file_path}")

            lines = file_path.read_text(encoding="utf-8").strip().splitlines()
            if not lines:
                raise ValidationError(f"❌ Commit message is empty.")

            header = lines[0].strip()
            match = HEADER_REGEX.match(header)
            if not match:
                raise ValidationError(f"❌ Invalid format. Expected: type(scope?): description")

            commit_type = match.group("type")
            if commit_type not in CONVENTIONAL_TYPES:
                raise ValidationError(f"❌ Invalid type '{commit_type}'. Must be one of: {', '.join(CONVENTIONAL_TYPES)}")

            summary = match.group("summary").strip()
            if not summary:
                raise ValidationError(f"❌ Summary is empty.")

            # Optional: check body exists and is not blank if present
            if len(lines) > 1:
                body_lines = lines[1:]
                if all(not line.strip() for line in body_lines):
                    print("⚠️ Warning: Commit body exists but is empty.")
                else:
                    print("✅ Body and/or footer detected.")

            print("✅ Commit message is valid.")
        except ValidationError as e:
            self._error_exit(str(e))

    def check_remote_origin(self) -> None:
        """
        Verify that the 'origin' remote exists and is reachable.
        """
        """git remote get-url origin"""
        try:
            result = self.runner.run(
                ["git", "remote", "get-url", "origin"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("❌ Error: Remote 'origin' not found or unreachable.")
            print("💡 Tip: Add a remote with:")
            print("   get remote add origin <url>")
            sys.exit(1)

    def has_changelog_changed(self) -> bool:
        """Check if CHANGELOG.md is modified in git diff."""
        """git diff --name-only"""
        result = self.runner.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
        )
        return "CHANGELOG.md" in result.stdout

    def get_current_branch(self) -> str:
        """Git rev-parse --abbrev-ref HEAD"""
        result = self.runner.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def commit_and_push_changelog(self) -> None:
        if not self.has_changelog_changed():
            print("⚠️ No changes in CHANGELOG.md. Skipping commit.")
            return

        print("💾 Committing generated CHANGELOG.md...")
        try:
            subprocess.run(["git", "add", "CHANGELOG.md"], check=True)
            subprocess.run(
                ["git", "commit", "-m", "docs(changelog): update changelog"],
                check=True,
            )
            branch = self.get_current_branch()
            subprocess.run(
                ["git", "push", "--set-upstream", "origin", branch],
                check=True,
            )
            print("✅ Changelog committed and pushed successfully.")
        except subprocess.CalledProcessError as e:
            print("❌ ERROR: Failed to commit or push CHANGELOG.md")
            print(f"🔍 Detail: {e}")
            sys.exit(1)

    def get_latest_tag(self) -> str:
        """Get the most recent Git tag (semantic versioning format expected).
        Returns 'v0.0.0' if no tags are found.
        """
        """git describe --tags --abbrev=0"""
        try:
            command = ["git", "describe", "--tags", "--abbrev=0"]
            output = self.runner.check_output(
                command=command,
                text=True,
            )
            return output.strip() if output else "v0.0.0"
            # return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("⚠️ No existing tags found. Starting form v0.0.0")
            return "v0.0.0"

    def get_tags(self) -> list[str]:
        """
        Return sorted list of tags (latest first)
        """
        result = self.runner.run(
            ["git", "tag"],
            capture_output=True,
            text=True,
            check=True,
            on_error=self._on_error("fetch git tags"),
        )
        return (
            sorted(result.stdout.strip().splitlines(), reverse=True) if result else []
        )

    def get_commits_between(self, ref_start: str, ref_end: str) -> list[str]:
        """
        Return commit messages between two Git refs.add.

        Args:
            ref_start (str): Older tag or empty string.
            ref_end (str): Newer tag.

        Returns:
            list[str]: List of raw commit messages.

        """
        # cmd = ["git", "log", f"{ref_start}..{ref_end}", "--pretty=format:%B"]
        cmd = ["git", "log", f"{ref_start}..{ref_end}", "--pretty=format:%H"]
        result = self.runner.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            on_error=self._on_error(f"get commits between {ref_start} and {ref_end}"),
        )
        if not result:
            return []

        commit_hashes = result.stdout.strip().splitlines()

        commits = []
        for sha in commit_hashes:
            show_cmd = ["git", "show", "-s", "--format=%B", sha]
            show_result = self.runner.run(
                show_cmd,
                capture_output=True,
                text=True,
                check=True,
                on_error=self._on_error(f"read commit {sha}"),
            )
            if show_result:
                commits.append(show_result.stdout.strip())

        return commits

    def get_tag_date(self, tag: str) -> str:
        """
        Get the commit date of the given tag

        Args:
            tag (str): Git tag name.

        Returns:
            str: Date in YYYY-MM-DD format.

        """
        cmd = ["git", "log", "-1", "--format=%ad", "--date=short", tag]
        result = self.runner.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            on_error=self._on_error(f"get date for {tag}"),
        )
        return result.stdout.strip() if result else "unknown"

    def parse_commit(self, msg: str) -> dict:
        """
        Parse a conventional commit message into structured data.

        Args:
            msg (str): Full commit message.

        Returns:
            dict: Parsed structure: type, scope, subject, body.

        """
        # pattern = r'(?P<type>\w+)(\((?P<scope>[^)]+)\)): (?P<subject>[^\n]+)(\n(?P<body>[\s\S]+))?'
        lines = msg.strip().splitlines()
        first_line = lines[0] if lines else ""
        body_lines = lines[1:]

        pattern = r"(?P<type>\w+)(\((?P<scope>[^)]+)\))?: (?P<subject>.+)"
        match = re.match(pattern, first_line)

        if match:
            return {
                "type": match.group("type") or "other",
                "scope": match.group("scope") or "general",
                "subject": match.group("subject").strip(),
                "body": "\n".join(body_lines).strip() if body_lines else None,
            }
        return {
            "type": "other",
            "scope": "general",
            "subject": first_line.strip(),
            "body": "\n".join(body_lines).strip() if body_lines else None,
        }

    def bump_version(
            self,
            current: str,
            level: str,
            pre: str | None = None,
            dev: bool = False,
            post: bool = False,
            local: str | None = None,
            epoch: int | None = None,
            ) -> str:
        """
        Bump the given semantic version based on the specified level (patch, minor, major).
        Bumps a semver string like v1.2.3 to the next version.
        Handles pre-releases like alpha, beta, rc.
        Bump version using full PEP 440 format:
        [Epoch!]MAJOR.MINOR.PATCH[Pre-release][Post-release][Development][+Local]
        """

        # Match full version wit optional epoch 'v' prefix
        # Remove pre-release suffix if present
        # base_tag = re.match(r"v?(\d+)\.(\d+)\.(\d+)", current)
        base_tag = re.match(r"(?:(\d+)!)?v?(\d+)\.(\d+)\.(\d+)", current)
        # Matches: v1.2.3, 1.2.3 1.2.3-alpha.1, 1.2.3-beta.9
        # and extract:
        # group (1) = major = 1
        # group (2) = minor = 2
        # group (3) = patch = 3
        # pre_tag = re.search(r"-(\w+)\.(\d+)", current)
        pre_tag = re.search(r"(a|b|rc)(\d+)", current)
        # Matches: -alpha.1, -beta.2, -rc.5
        # and extract:
        # group (1) = label = alpha, beta, or rc
        # group (2) = number = 1, 2, etc
        post_tag = re.search(r"post(\d+)", current)
        dev_tag = re.search(r"dev(\d+)", current)
        local_tag = re.search(r"\+(.*)", current)

        if not base_tag:
            print(f"❌ Invalid tag format: '{current}' (expected) [N!]X.Y.Z or vX.Y.Z")
            sys.exit(1)

        epoch_val, major, minor, patch = base_tag.groups()
        major, minor, patch = map(int, [major, minor, patch])
        epoch_val = int(epoch_val) if epoch_val else None

        # Apply bump level
        if level == "patch":
            patch += 1
        elif level == "minor":
            minor += 1
            patch = 0
        elif level == "major":
            major += 1
            minor = 0
            patch = 0
        else:
            print("❌ Invalid bump level. Use: Patch, minor, or major.")
            sys.exit(1)

        version = f"{major}.{minor}.{patch}"

        # Pre-release
        if pre:
            pre_letter = {"alpha": "a", "beta": "b", "rc": "rc"}.get(pre.lower(), pre.lower())
            if pre_tag and pre_tag.group(1) == pre_letter:
                pre_num = int(pre_tag.group(2)) + 1
            else:
                pre_num = 1
            version += f"{pre_letter}{pre_num}"

        # Post-release
        if post:
            post_num = int(post_tag.group(1)) + 1 if post_tag else 1
            version += f".post{post_num}"

        # Development-release
        if dev:
            dev_num = int(dev_tag.group(1)) + 1 if dev_tag else 1
            version += f".dev{dev_num}"

        # Local version metadata
        if local:
            version += f"+{local}"

        # Add epoch
        if epoch and epoch > 0:
            version = f"{epoch}!{version}"

        return version

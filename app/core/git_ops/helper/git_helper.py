# app/core/git_ops/helper/git_helper.py

"""
Utilities Class (Git)
"""

import logging
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from app.core.dry_run import DryRunSupport
from app.errors.validation import ValidationError

logger = logging.getLogger(__name__)

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

    def _run_git(self, args: list[str]) -> str:
        try:
            result = self.runner.run(
                ["git"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                encoding="utf-8",
            )
            if result is None:
                print(f"⚠️ Dry-run or command skipped: git {' '.join(args)}")
                # return "" # ✅ fix: always return string, never None
                return None
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ GIt command failed: git {' '.join(args)}")
            print(e.stderr)
            return ""

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

        Returns:
            bool: True if there are staged changes, False otherwise.

        Notes:
            Uses:
                git diff --cached --quiet

            Return code:
                0 → no changes
                1 → changes exist
        """
        try:
            result = self.runner.run(
                ["git", "diff", "--cached", "--quiet"],
                check=False,
            )

            has_changes = result.returncode != 0

            if has_changes:
                print("📦 Staged changes detected.")
            else:
                print("⚠️ No staged changes found.")

            return has_changes

        except Exception as e:
            print(f"❌ Failed to check staged files: {e}")
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
        if not files:
            print("⚠️ No files provided to stage.")
            return

        existing_files = [f for f in files if isinstance(f, Path) and f.exists()]
        if not existing_files:
            print("⚠️ No exists to stage.")
            return

        files_str = [str(f) for f in files]

        self.runner.run(
            ["git", "add", *files_str],
            check=True,
            on_error=lambda: self._error_exit(
                f"Failed to stage files: {', '.join(files_str)}`",
            ),
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
            "feat",
            "fix",
            "docs",
            "style",
            "refactor",
            "perf",
            "test",
            "chore",
            "ci",
            "build",
            "release",
        }
        HEADER_REGEX = re.compile(
            r"(?P<type>\w+)(\((?P<scope>[^\)]+)\))?!?: (?P<summary>.+)$",
        )
        try:
            if not file_path.exists() or not file_path.is_file():
                raise ValidationError(f"❌ Commit message file not found: {file_path}")

            lines = file_path.read_text(encoding="utf-8").strip().splitlines()
            if not lines:
                raise ValidationError("❌ Commit message is empty.")

            header = lines[0].strip()
            match = HEADER_REGEX.match(header)
            if not match:
                raise ValidationError(
                    "❌ Invalid format. Expected: type(scope?): description",
                )

            commit_type = match.group("type")
            if commit_type not in CONVENTIONAL_TYPES:
                raise ValidationError(
                    f"❌ Invalid type '{commit_type}'. Must be one of: {', '.join(CONVENTIONAL_TYPES)}",
                )

            summary = match.group("summary").strip()
            if not summary:
                raise ValidationError("❌ Summary is empty.")

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
            self.runner.run(
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

    def has_commit(self):
        """
        Check if the repository has at least one commit.

        Command:
            git rev-parse --verify HEAD
        """
        try:
            result = self.runner.run(
                ["git", "rev-parse", "--verify", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            )
            return bool(result and result.returncode == 0)
        except Exception as e:
            # Failed to check commits
            print(f"⚠️ Unable to verify HEAD: {e}")
            return False

    def get_current_branch(self) -> str:
        """
        Safely determine the current branch.
        Handles:
        - new repository (no commits yet)
        - detached HEAD state
        - git failure

        Commands used:
            git rev-parse --abbrev-ref HEAD
            git symbolic-ref --short HEAD
        """
        try:
            # Case 1: repository has no commits yet
            if not self.has_commit():
                print("🆕 New repository detected (no commits yet).")

                result = self.runner.run(
                    ["git", "symbolic-ref", "--short", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                if result and result.stdout:
                    return result.stdout.strip()

                # fallback default branch
                return "main"

            # Case 2: normal case with commits
            result = self.runner.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )

            if result and result.stdout:
                branch = result.stdout.strip()

                if branch == "HEAD":
                    print("⚠️ Detached HEAD state detected.")

                return branch

        except Exception as e:
            print(f"⚠️ Failed to determine current branch: {e}")

        return "unknown"

    def commit_and_push_changelog(self, remotes: list[str] | None = None) -> None:
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
            print("00000000000000000000000")
            for remote in remotes or []:
                self._push(remote=remote, branch=branch)

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
                encoding="utf-8",
                check=True,
                on_error=self._on_error(f"read commit {sha}"),
            )
            if show_result and show_result.stdout:
                commits.append(show_result.stdout.strip())
            else:
                print(f"⚠️ Skipping commit {sha}: no output or command failed.")

        return commits

    def get_commits_between_tags(self, from_tag: str, to_tag: str) -> list[dict]:
        """
        Returns commits between two tags in chronological order (oldest → newest)
        Each commit: {sha, header, body, author, date}
        """
        format_str = "%H%n%s%n%an%n%ad%n%B%n---END---"
        rev_range = f"{from_tag}..{to_tag}" if from_tag else to_tag
        raw = self._run_git(
            ["log", "--reverse", "--pretty=format:" + format_str, rev_range],
        )

        if not raw:
            print(f"⚠️ Skipped log retrieval: {from_tag}..{to_tag} (dry-run?)")
            return []

        commits = []
        for chunk in raw.strip().split("---END---"):
            if not chunk.strip():
                continue
            # lines = chunk.strip()
            # sha, header, author, date = lines[0:4]
            lines = chunk.strip().splitlines()
            if len(lines) < 4:
                continue  # or log error and skip
            sha, header, author, date = lines[0:4]
            body = "\n".join(lines[4:]).strip()
            commits.append(
                {
                    "sha": sha,
                    "header": header,
                    "author": author,
                    "date": date,
                    "body": body,
                },
            )
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

    # def parse_commit(self, msg: str) -> dict:
    #     """
    #     Parse a conventional commit message into structured data.

    #     Args:
    #         msg (str): Full commit message.

    #     Returns:
    #         dict: Parsed structure: type, scope, subject, body.

    #     """
    #     # pattern = r'(?P<type>\w+)(\((?P<scope>[^)]+)\)): (?P<subject>[^\n]+)(\n(?P<body>[\s\S]+))?'
    #     lines = msg.strip().splitlines()
    #     first_line = lines[0] if lines else ""
    #     body_lines = lines[1:]

    #     pattern = r"(?P<type>\w+)(\((?P<scope>[^)]+)\))?: (?P<subject>.+)"
    #     match = re.match(pattern, first_line)

    #     if match:
    #         return {
    #             "type": match.group("type") or "other",
    #             "scope": match.group("scope") or "general",
    #             "subject": match.group("subject").strip(),
    #             "body": "\n".join(body_lines).strip() if body_lines else None,
    #         }
    #     return {
    #         "type": "other",
    #         "scope": "general",
    #         "subject": first_line.strip(),
    #         "body": "\n".join(body_lines).strip() if body_lines else None,
    #     }

    # def parse_commit(self, msg: str) -> dict:
    #     lines = msg.strip().splitlines()
    #     if not lines:
    #         return {}

    #     header = lines[0].strip()
    #     body_lines = lines[1:]

    #     # 🚫 Ignore merge commits early
    #     if header.lower().startswith("merge"):
    #         return {"type": "merge", "skip": True}

    #     pattern = r"(?P<type>\w+)(\((?P<scope>[^)]+)\))?: (?P<subject>.+)"
    #     match = re.match(pattern, header)

    #     commit_type = "other"
    #     scope = "general"
    #     subject = header

    #     if match:
    #         commit_type = match.group("type")
    #         scope = match.group("scope") or "general"
    #         subject = match.group("subject").strip()

    #     return {
    #         "type": commit_type,
    #         "scope": scope,
    #         "subject": subject,
    #         "body": "\n".join(body_lines).strip(),
    #         "raw_body_lines": body_lines,
    #     }

    def parse_commit(self, msg: str) -> dict:
        lines = msg.strip().splitlines()
        if not lines:
            return {}

        header = lines[0].strip()
        body_lines = lines[1:]

        # 🚫 Skip merge commits
        if header.lower().startswith("merge"):
            return {"type": "merge", "skip": True}

        pattern = r"(?P<type>\w+)(\((?P<scope>[^)]+)\))?: (?P<subject>.+)"
        match = re.match(pattern, header)

        commit_type = "other"
        scope = "general"
        subject = header

        if match:
            commit_type = match.group("type")
            scope = match.group("scope") or "general"
            subject = match.group("subject").strip()

        return {
            "type": commit_type,
            "scope": scope,
            "subject": subject,
            "body": "\n".join(body_lines).strip(),
            "raw_body_lines": body_lines,
        }

    def get_all_tags(self) -> list[str]:
        """
        Returns a list of all Git tags, sorted by creation date.
        """
        output = self._run_git(["tag", "--sort=creatordate"])
        return output.strip().splitlines() if output else []

    def _push(self, branch: str, remote: str = "origin"):
        subprocess.run(
            ["git", "push", "--set-upstream", remote, branch],
            check=True,
        )

    def branch_exists(self, branch_name: str) -> bool:
        result = self.runner.run(
            command=["git", "rev-parse", "--verify", "--quite", branch_name],
            check=False,
            capture_output=True,
        )
        return result.returncode == 0


def parse_pep440_or_semver(tag: str) -> tuple:
    """
    Parse tag into sortable components supporting both SemVer and PEP 440.

    Examples:
    - 'v1.2.3' -> (1, 2, 3)
    - '2!1.2.3rc1.post2.dev4+sha.abc123' -> (2, 1, 2, 3, 'rc1', 'post2', 'dev4', 'sha.abc123')
    - '1.2.3-alpha.1+meta' -> (1, 2, 3, 'alpha.1', 'meta')

    """
    tag = tag.lstrip("v")

    # Split off epoch
    epoch = 0
    if "!" in tag:
        epoch_str, tag = tag.split("!", 1)
        if epoch_str.isdigit():
            epoch = int(epoch_str)

    # Split pre-release, post, dev, local
    main_version = tag
    pre = post = dev = local = ""

    # local segment
    if "+" in tag:
        main_version, local = tag.split("+", 1)
    if ".post" in main_version:
        main_version, post = main_version.split(".post", 1)
        post = "post" + post
    if ".dev" in main_version:
        main_version, dev = main_version.split(".dev", 1)
        dev = "dev" + dev
    match = re.search(r"(a|b|rc)\d+", main_version)
    if match:
        idx = match.start()
        main_version, pre = main_version[:idx], main_version[idx:]

    parts = tuple(
        [epoch]
        + [int(p) if p.isdigit() else p for p in re.split(r"[^\W]+", main_version) if p]
        + [pre, post, dev, local],
    )
    return parts


def get_last_tag_before(current_tag: str, all_tags: list[str]) -> str:
    """
    Returns the last final (non-prerelease) tag that comes before the given tag.
    A final tag has no a/b/rc/dev suffix.
    """
    clean_current = current_tag.lstrip("v")
    for tag in reversed(all_tags):
        if tag == current_tag:
            continue
        if not re.search(r"(a|b|rc|dev)\d*", tag) and tag < clean_current:
            return tag
    return ""


def get_sorted_tags(tags: list[str]) -> list[str]:
    """
    Sort tags using combined PEP 440 / SemVer logic.
    """
    return sorted(tags, key=parse_pep440_or_semver)

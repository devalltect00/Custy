# app/core/git_ops/git/service.py

#

##### Domain Logic

import re
import logging
from pathlib import Path
from typing import List
from datetime import datetime

from app.config.config_loader import get_config, ConfigLoader
from app.core.git_ops.git.protocol import IGitCommandExecutor
from app.core.decorators.log_decorators import log_execution
from app.core.cleanup.branch.models import (
    BranchInfo,
)
from app.core.git_ops.helper import (
    detect_tag_sorting_strategy,
)
from app.cli.constants.enums import (
    StrategyChoices,
)
from app.core.git_ops.tag_sorter.factory import (
    TagSorterFactory,
)
from app.core.git_ops.tag_sorter.base import (
    TagSorter,
)

logger = logging.getLogger(__name__)


class GitService:
    """
    High-level Git operations (business logic layer).
    Depends on abstraction (IGitCommandExecutor), not implementation.

    This class:
    - orchestrates git commands
    - applies domain logic
    - handles logging decisions
    - provides clean API for CLI / workflow

    It does NOT:
    - directly execute subprocess
    - depend on dry-run implementation
    - depend on specific executor implementation
    """

    def __init__(
        self,
        executor: IGitCommandExecutor,
        config: ConfigLoader | None = None,
        strategy: StrategyChoices | None = None,
    ):
        self.executor = executor
        self.config = config or get_config()
        self.strategy = strategy
        self._tag_sorter: TagSorter | None = None

    def _resolve_tag_sorting_strategy(
        self,
    ) -> StrategyChoices:
        """
        Resolve the strategy used to sort Git tags.

        The strategy passed into GitService has already been resolved by the
        workflow layer. Automatic detection is only used when no strategy was
        provided or when Commitizen is responsible for version generation.

        Returns
        -------
        StrategyChoices
            A strategy supported by TagSorterFactory.
        """

        strategy = self.strategy

        if (
            strategy is None
            or strategy == StrategyChoices.NONE
            or strategy == StrategyChoices.COMMITIZEN
        ):
            detected = detect_tag_sorting_strategy(
                no_debug=self.executor.get_silent(),
            )

            return StrategyChoices(detected)

        if isinstance(strategy, str):
            return StrategyChoices(strategy)

        return strategy

    def _get_tag_sorter(self) -> TagSorter:
        """
        Return the configured TagSorter instance.

        The sorter is created lazily and cached for the lifetime of this
        GitService instance.
        """

        if self._tag_sorter is not None:
            return self._tag_sorter

        strategy = self._resolve_tag_sorting_strategy()

        kwargs: dict[str, object] = {}

        if strategy == StrategyChoices.DATE:
            kwargs["date_format"] = self.config.get(
                "cli",
                "versioning",
                "date_format",
                default="%Y.%m.%d",
            )

        self._tag_sorter = TagSorterFactory.create(
            strategy=strategy,
            **kwargs,
        )

        return self._tag_sorter

    @log_execution
    def get_is_dry_run(self) -> bool:
        """
        Determine whether Git operations are currently executing in
        dry-run mode.

        This method exposes the executor's dry-run state through the
        public Git service API, preventing callers from depending on the
        executor implementation.

        Returns
        -------
        bool
            True when dry-run mode is enabled.
        """

        return self.executor.get_is_dry_run()

    # ============================================
    # Resolve remotes (CORE LOGIC)
    # ============================================
    def resolve_remotes(
        self,
        remotes: list[str] | None = None,
        push_to: str | None = None,
    ) -> list[str]:
        """
        Resolve list of remotes using priority:

        1. Explicit argument (remotes)
        2. Config (.custy.toml)
        3. Default fallback

        Args:
            remotes (list[str] | None): Explicit remotes
            push_to (str | None): 'main' | 'backup' | 'all'

        Returns:
            list[str]: Final resolved remotes
        """

        # 1. Explicit remotes (highest priority)
        if remotes:
            return remotes

        # 2. Resolve push strategy
        push_to = self.config.resolve(
            cli_value=push_to,
            config_keys=["git", "push_to"],
            default="main",
        )

        main_remotes = self.config.get("git", "main_remotes", default=["origin"])
        backup_remotes = self.config.get("git", "backup_remotes", default=[])

        if push_to == "main":
            return main_remotes

        if push_to == "backup":
            return backup_remotes

        if push_to == "all":
            return list(dict.fromkeys(main_remotes + backup_remotes))

        # fallback safety
        return main_remotes

    def resolve_default_remote(self, remote: str | None = None) -> str:
        """
        Resolve single remote with priority:
            1. Explicit argument
            2. Config
            3. Default 'origin'
        """
        return self.config.resolve(
            cli_value=remote,
            config_keys=["git", "default_remote"],
            default="origin",
        )

    # =========================================================
    # ===================== REPOSITORY =========================
    # =========================================================

    @log_execution
    def is_git_repo(self) -> bool:
        """
        Check whether current directory is a Git repository.

        Logic:
            - check `.git` folder existence
            - fallback to `git rev-parse --is-inside-work-tree`

        Args:
            None

        Returns:
            bool:
                True  → inside a git repository
                False → not a git repository

        Raises:
            None
        """
        if Path(".git").exists():
            return True

        result = self.executor.rev_parse_inside_work_tree()
        return result.success

    @log_execution
    def has_commit(self) -> bool:
        """
        Check if repository has at least one commit.

        Logic:
            git rev-parse --verify HEAD

        Args:
            None

        Returns:
            bool:
                True  → repository has commits
                False → no commits yet

        Raises:
            None
        """
        result = self.executor.rev_parse_head()
        return result.success

    @log_execution
    def branch_exists(self, branch: str) -> bool:
        """
        Check whether a Git branch exists.

        Logic:
            git rev-parse --verify --quiet <branch>

        Args:
            branch (str): Branch name

        Returns:
            bool:
                True  → branch exists
                False → branch does not exist

        Raises:
            None
        """
        # result = self.executor.branch_exists(branch)
        # return result.returncode == 0
        return self.executor.branch_exists(branch).success

    # =========================================================
    # ===================== STAGING ============================
    # =========================================================

    @log_execution
    def has_staged_files(self) -> bool:
        """
        Check if there are staged changes.

        Logic:
            git diff --cached --quiet

        Args:
            None

        Returns:
            bool:
                True  → staged changes exist
                False → no staged changes

        Raises:
            None
        """
        result = self.executor.diff_cached_quiet()

        if result.skipped:
            logger.warning(
                "\n⚠️ Staged-state inspection was skipped; "
                "treating the index as unchanged."
            )
            return False

        if result.has_changes:
            logger.info("\n📦 Staged changes detected.")
            return True

        logger.info("\n⚠️ No staged changes found.")
        return False

    @log_execution
    def auto_stage_all(self) -> None:
        """
        Stage all files (including untracked).

        Logic:
            git add .

        Args:
            None

        Returns:
            None

        Raises:
            RuntimeError:
                If staging fails
        """
        result = self.executor.add_all()

        if not result.success:
            raise RuntimeError("Failed to stage files with `git add .`")

    @log_execution
    def auto_stage_update(self) -> None:
        """
        Stage only modified and deleted tracked files.

        Logic:
            git add --update

        Args:
            None

        Returns:
            None

        Raises:
            RuntimeError:
                If staging fails
        """
        result = self.executor.add_update()

        if not result.success:
            raise RuntimeError("Failed to stage files with `git add --update`")

    @log_execution
    def stage_files(self, files: List[Path]) -> None:
        """
        Stage specific files.

        Logic:
            git add <files>

        Args:
            files (List[Path]): Files to stage

        Returns:
            None

        Raises:
            RuntimeError:
                If staging fails
        """
        if not files:
            logger.warning("\n⚠️ No files provided to stage.")
            return

        valid_files = [str(f) for f in files if f.exists()]

        if not valid_files:
            logger.warning("\n⚠️ No valid files to stage.")
            return

        result = self.executor.add_files(valid_files)

        if not result.success:
            raise RuntimeError(f"Failed to stage files: {valid_files}")

    @log_execution
    def list_staged_files(self) -> List[str]:
        """
        Get list of staged files.

        Logic:
            git diff --cached --name-only

        Args:
            None

        Returns:
            List[str]:
                List of staged file paths

        Raises:
            None
        """
        result = self.executor.list_staged_files()

        if result.stdout:
            return result.stdout.strip().splitlines()

        return []

    # =========================================================
    # ===================== BRANCH =============================
    # =========================================================

    @log_execution
    def get_current_branch(self) -> str:
        """
        Determine and get current branch safely.

        Handles:
        - new repo (no commits)
        - detached HEAD

        Logic:
            - use symbolic-ref if no commits
            - fallback to rev-parse

        Args:
            None

        Returns:
            str:
                Current branch name

        Raises:
            None
        """
        if not self.has_commit():
            res = self.executor.symbolic_head()
            return res.stdout.strip() if res.stdout else "main"

        result = self.executor.current_branch()

        if result.stdout:
            branch = result.stdout.strip()
            if branch == "HEAD":
                logger.warning("\n⚠️ Detached HEAD state detected.")

        # res = self.executor.current_branch()
        return result.stdout.strip() if result.stdout else "unknown"

    @log_execution
    def list_branches(self) -> list[BranchInfo]:
        """
        Retrieve branch metadata.

        Returns
        -------
        list[BranchInfo]
            Local branches with metadata required by the cleanup
            workflow.
        """

        metadata_result = self.executor.list_branch_metadata()
        merged_result = self.executor.list_merged_branches()

        merged = {
            name.strip()
            for name in merged_result.stdout.splitlines()
            if name.strip()
        }

        branches: list[BranchInfo] = []

        for line in metadata_result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            name, timestamp = line.split("|", maxsplit=1)

            branches.append(
                BranchInfo(
                    name=name,
                    last_commit=datetime.fromtimestamp(
                        int(timestamp)
                    ),
                    merged=name in merged,
                    remote_exists=self.remote_branch_exists(name),
                )
            )

        return branches

    @log_execution
    def remote_branch_exists(
        self,
        branch: str,
        remote: str | None = None,
    ) -> bool:
        """
        Determine whether a branch exists on a remote repository.
        """

        remote = self.resolve_default_remote(remote)

        result = self.executor.remote_branch_exists(
            remote,
            branch,
        )

        return bool(result.stdout.strip())

    @log_execution
    def delete_local_branch(
        self,
        branch: str,
        force: bool = False,
    ) -> None:
        """
        Delete a local branch.
        """

        result = self.executor.delete_local_branch(
            branch,
            force=force,
        )

        if not result.success:
            raise RuntimeError(
                f"Failed to delete local branch '{branch}'."
            )

    @log_execution
    def delete_remote_branch(
        self,
        branch: str,
        remote: str | None = None,
    ) -> None:
        """
        Delete a remote branch.
        """

        remote = self.resolve_default_remote(remote)

        result = self.executor.delete_remote_branch(
            remote,
            branch,
        )

        if not result.success:
            raise RuntimeError(
                (
                    f"Failed to delete remote branch "
                    f"'{branch}' from '{remote}'."
                )
            )

    # =========================================================
    # ===================== REMOTE =============================
    # =========================================================

    @log_execution
    def get_remote_url(self, remote: str = "origin") -> str | None:
        """
        Get remote repository URL.

        Logic:
            git remote get-url <remote>

        Args:
            remote (str): Remote name

        Returns:
            str | None:
                Remote URL if exists, else None

        Raises:
            None
        """
        result = self.executor.remote_get_url(remote)
        return result.stdout.strip() if result.success else None

    @log_execution
    def check_remote(self, remote: str = "origin") -> bool:
        """
        Check whether a given Git remote exists and is reachable.

        Logic:
            git remote get-url <remote>

        Args:
            remote (str): Name of the remote (e.g., 'origin', 'backup').

        Returns:
            bool:
                True  → remote exists and accessible
                False → remote not found or error occurred

        Raises:
            None
        """
        result = self.executor.remote_get_url(remote)
        return result.success

    # =========================================================
    # ===================== DIFF ===============================
    # =========================================================

    @log_execution
    def get_modified_files(self) -> List[str]:
        """
        Get list of modified (unstaged) files.

        Logic:
            git diff --name-only

        Args:
            None

        Returns:
            List[str]:
                Modified file paths

        Raises:
            None
        """
        result = self.executor.diff_name_only()
        return result.stdout.strip().splitlines() if result.stdout else []

    # =========================================================
    # ===================== COMMITS ============================
    # =========================================================

    @log_execution
    def commit(
        self,
        message: str | None = None,
        message_file: str | None = None,
    ) -> None:
        """
        Create a Git commit.

        Logic:
            git commit (-m | -F)

        Args:
            message (str | None): Inline commit message
            message_file (str | None): File containing message

        Returns:
            None

        Raises:
            RuntimeError:
                If commit fails
        """

        if not self.executor.commit(message, message_file).success:
            raise RuntimeError("Git commit failed")

    @log_execution
    def get_commit_message(self, sha: str) -> str:
        """
        Get full commit message.

        Logic:
            git show -s --format=%B <sha>

        Args:
            sha (str): Commit hash

        Returns:
            str:
                Full commit message

        Raises:
            None
        """
        result = self.executor.show_commit(sha)
        return result.stdout.strip() if result.stdout else ""

    @log_execution
    def get_commit_hashes(self, ref_range: str) -> list[str]:
        """
        Retrieve commit hashes within a given Git revision range.
        Get commit hashes within a range.

        Logic:
            git log <range> --pretty=format:%H

        Args:
            ref_range (str): Git revision range (e.g., 'v1.0.0..v1.1.0').

        Returns:
            list[str]:
                List of commit hashes (SHA).

        Raises:
            None
        """
        result = self.executor.log_between(ref_range, "%H")
        return result.stdout.strip().splitlines() if result.stdout else []

    @log_execution
    def get_raw_log(
        self,
        ref_range: str,
        pretty_format: str = "%H",
        reverse: bool = False,
    ) -> List[str]:
        """
        Execute raw git log command.

        Logic:
            git log <range> --pretty=format:<format>

        Args:
            ref_range (str): Git revision range
            pretty_format (str): Format string
            reverse (bool): Reverse order

        Returns:
            List[str]:
                Raw log output lines

        Raises:
            None
        """
        result = self.executor.log_between(ref_range, pretty_format, reverse)
        return result.stdout.strip().splitlines() if result.stdout else []

    @log_execution
    def get_commit_count(self) -> int:
        """
        Get total commit count in the repository.

        Logic:
            git rev-list --count HEAD

        Args:
            None

        Returns:
            int: Total number of commits

        Raises:
            RuntimeError: If command execution fails
        """
        result = self.executor.get_commit_count()

        if not result.success:
            raise RuntimeError("Failed to get commit count")

        try:
            return int(result.stdout.strip())
        except ValueError as e:
            raise RuntimeError(f"Invalid commit count output: {result.stdout}") from e

    # =========================================================
    # ===================== TAGS ===============================
    # =========================================================

    @log_execution
    def tag(
        self,
        tag: str,
        message: str | None = None,
        message_file: str | None = None,
    ) -> None:
        """
        Create Git tag.

        Logic:
            git tag -a <tag>

        Args:
            tag (str): Tag name
            message (str | None): Inline message
            message_file (str | None): File message

        Returns:
            None

        Raises:
            RuntimeError:
                If tag creation fails
        """
        if not self.executor.tag(tag, message, message_file).success:
            raise RuntimeError(f"Failed to create tag {tag}. git tag {tag} failed")

    @log_execution
    def get_latest_tag(self) -> str:
        """
        Get latest Git tag.

        Logic:
            git describe --tags --abbrev=0

        Args:
            None

        Returns:
            str:
                Latest tag or fallback 'v0.0.0'

        Raises:
            None
        """
        result = self.executor.describe_latest_tag()
        if not result.stdout:
            logger.warning("\n⚠️ No existing tags found. Defaulting to v0.0.0")
        return result.stdout.strip() if result.stdout else "v0.0.0"

    @log_execution
    def get_tags(self) -> List[str]:
        """
        Get all version tags sorted from newest to oldest.

        Logic:
            git tag
            strategy-aware sorting

        Args:
            None

        Returns:
            List[str]:
                Version tags ordered from newest to oldest.

        Raises:
            None
        """

        result = self.executor.get_tags()

        if not result.stdout:
            return []

        tags = result.stdout.strip().splitlines()

        # return sorted(result.stdout.strip().splitlines(), reverse=True) if result.stdout else []
        return self._get_tag_sorter().sort(
            tags,
            reverse=True,
        )

    @log_execution
    def get_latest_version_tag(self) -> str | None:
        """
        Return the highest version tag according to the configured
        versioning strategy.

        Returns
        -------
        str | None
            Latest version tag, or None if no tags exist.
        """

        tags = self.get_tags()

        if not tags:
            return None

        return self._get_tag_sorter().latest(tags)

    @log_execution
    def get_oldest_version_tag(self) -> str | None:
        """
        Return the oldest version tag according to the configured
        versioning strategy.

        Returns
        -------
        str | None
            Oldest version tag, or None if no tags exist.
        """

        tags = self.get_tags()

        if not tags:
            return None

        return self._get_tag_sorter().oldest(tags)

    @log_execution
    def get_all_tags(self) -> List[str]:
        """
        Get all tags sorted by creation date.

        Logic:
            git tag --sort=creatordate

        Args:
            None

        Returns:
            List[str]:
                Sorted tags

        Raises:
            None
        """
        result = self.executor.get_all_tags()
        return result.stdout.strip().splitlines() if result.stdout else []

    @log_execution
    def get_tag_date(self, tag: str) -> str:
        """
        Retrieve the commit date associated with a Git tag.
        Get date of a tag.

        Logic:
            git log -1 --format=%ad --date=short <tag>

        Args:
            tag (str): Tag name.

        Returns:
            str: Date in 'YYYY-MM-DD' format, or 'unknown' if unavailable.
        """
        result = self.executor.get_tag_date(tag)
        return result.stdout.strip() if result.stdout else "unknown"

    # =========================================================
    # ===================== PUSH ===============================
    # =========================================================

    @log_execution
    def push(
        self,
        remote: str | None = None,
        remotes: list[str] | None = None,
        ref: str = "HEAD",
        push_to: str | None = None,
    ) -> None:
        """
        Push to one or multiple remotes.

        Priority:
            1. remotes list
            2. single remote
            3. config (main/backup/all)

        Args:
            remote (str | None): single remote
            remotes (list[str] | None): multiple remotes
            ref (str): branch or ref
            push_to (str): strategy ('main', 'backup', 'all')
        """

        # Resolve remotes
        if remotes:
            target_remotes = remotes
        elif remote:
            target_remotes = [remote]
        else:
            target_remotes = self.resolve_remotes(push_to=push_to)

        if not target_remotes:
            logger.warning("\n⚠️ No remotes resolved. Skipping push.")
            return

        for r in target_remotes:
            logger.info(f"\n🚀 Pushing to {r}:{ref}")
            result = self.executor.push(remote=r, ref=ref)

            if not result.success:
                raise RuntimeError(f"Failed to push to {r}")

    @log_execution
    def push_tag(
        self,
        tag: str,
        remote: str | None = None,
        remotes: list[str] | None = None,
        push_to: str | None = None,
    ) -> None:
        """
        Push tag to remotes.
        """

        if remotes:
            target_remotes = remotes
        elif remote:
            target_remotes = [remote]
        else:
            target_remotes = self.resolve_remotes(push_to=push_to)

        for r in target_remotes:
            logger.info(f"\n🏷️ Pushing tag {tag} to {r}")
            result = self.executor.push_tag(r, tag)

            if not result.success:
                raise RuntimeError(f"Failed to push tag to {r}")

    # =========================================================
    # ===================== ADVANCED ===========================
    # =========================================================

    @log_execution
    def get_commits_between(self, ref_start: str, ref_end: str) -> List[str]:
        """
        Get commit messages between two refs.

        Args:
            ref_start (str): older ref
            ref_end (str): newer ref

        Returns:
            List[str]: commit messages
        """
        ref_range = f"{ref_start}..{ref_end}" if ref_start else ref_end

        result = self.executor.log_between(ref_range)

        if not result.stdout:
            return []

        hashes = result.stdout.strip().splitlines()
        commits = []

        for sha in hashes:
            commit_result = self.executor.show_commit(sha)

            if commit_result.stdout:
                commits.append(commit_result.stdout.strip())

        return commits

    @log_execution
    def get_commits_between_tags(self, from_tag: str, to_tag: str) -> list[dict]:
        """
        Retrieve structured commit data between two tags.

        Each commit includes:
            - sha
            - header (subject)
            - author
            - date
            - body

        Args:
            from_tag (str): Starting tag (exclusive).
            to_tag (str): Ending tag (inclusive).

        Returns:
            list[dict]: Structured commit entries.
        """
        result = self.executor.get_commits_between_tags(from_tag, to_tag)

        if not result.stdout:
            return []

        commits = []

        for chunk in result.stdout.strip().split("---END---"):
            if not chunk.strip():
                continue

            lines = chunk.strip().splitlines()

            if len(lines) < 4:
                continue

            sha, header, author, date = lines[:4]
            body = "\n".join(lines[4:]).strip()

            commits.append({
                "sha": sha,
                "header": header,
                "author": author,
                "date": date,
                "body": body,
            })

        return commits

    # =========================================================
    # ===================== PARSER =============================
    # =========================================================

    @log_execution
    def parse_commit(self, msg: str) -> dict:
        """
        Parse a commit message into structured components.

        Supports conventional commit format:
            type(scope): subject

        Args:
            msg (str): Full commit message.

        Returns:
            dict:
                {
                    "type": str,
                    "scope": str,
                    "subject": str,
                    "body": str,
                    "raw_body_lines": list[str],
                    "skip": bool (optional for merge commits)
                }
        """
        lines = msg.strip().splitlines()
        if not lines:
            return {}

        header = lines[0].strip()
        body_lines = lines[1:]

        # Skip merge commits
        if header.lower().startswith("merge"):
            return {"type": "merge", "skip": True}

        pattern = r"(?P<type>\w+)(\((?P<scope>[^\)]+)\))?: (?P<subject>.+)"
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

    # ======================
    # Changelog helpers
    # ======================

    @log_execution
    def has_changelog_changed(self) -> bool:
        """
        Check if CHANGELOG.md has been modified.

        Returns:
            bool
        """
        result = self.executor.diff_name_only()
        return "CHANGELOG.md" in result.stdout

# app/core/git_ops/git/protocol.py

#

##### Type-safe interface (Protocol)

from typing import Optional, Protocol

from app.core.git_ops.git.result import CommandResult


class IGitCommandExecutor(Protocol):
    """
    Structural interface for Git command execution.
    Any class implementing these methods is accepted.

    Protocol for Git command execution layer.

    Defines all low-level Git operations with flexible parameters.
    """

    def get_silent(self) -> bool: ...
    def set_silent(self, is_silent: bool) -> None: ...
    def get_is_dry_run(self) -> bool: ...
    def set_is_dry_run(self, is_dry_run: bool) -> None: ...

    # ======================
    # Core
    # ======================

    # ----------------------
    # Staging
    # ----------------------

    def diff_cached_quiet(self) -> CommandResult: ...

    def add_all(self) -> CommandResult: ...
    def add_update(self) -> CommandResult: ...
    def add_files(self, files: list[str]) -> CommandResult: ...
    def list_staged_files(self) -> CommandResult: ...

    # ----------------------
    # Repository
    # ----------------------

    def rev_parse_inside_work_tree(self) -> CommandResult: ...
    def rev_parse_head(self) -> CommandResult: ...

    # ----------------------
    # Branch
    # ----------------------

    def current_branch(self) -> CommandResult: ...
    def symbolic_head(self) -> CommandResult: ...

    def branch_exists(self, branch_name: str) -> CommandResult: ...

    def list_local_branches(
        self,
    ) -> CommandResult:
        """
        Retrieve every local Git branch.

        Returns
        -------
        CommandResult
            Branch names separated by newlines.
        """
        ...

    def list_merged_branches(
        self,
    ) -> CommandResult:
        """
        Retrieve merged local branches.

        Returns
        -------
        CommandResult
            Branch names separated by newlines.
        """
        ...

    def list_branch_metadata(
        self,
    ) -> CommandResult:
        """
        Retrieve branch metadata.

        Returns
        -------
        CommandResult
            Metadata in the following format:

            branch|unix_timestamp
        """
        ...

    # ======================
    # Remote
    # ======================

    def remote_get_url(self, remote: str) -> CommandResult: ...

    def remote_branch_exists(
        self,
        remote: str,
        branch: str,
    ) -> CommandResult:
        """
        Determine whether a branch exists on a remote.

        Returns
        -------
        CommandResult
        """
        ...

    def delete_local_branch(
        self,
        branch: str,
        force: bool = False,
    ) -> CommandResult:
        """
        Delete a local branch.

        Returns
        -------
        CommandResult
        """
        ...

    def delete_remote_branch(
        self,
        remote: str,
        branch: str,
    ) -> CommandResult:
        """
        Delete a remote branch.

        Returns
        -------
        CommandResult
        """
        ...

    # ======================
    # Log / Commit inspection
    # ======================

    def log_between(
        self,
        ref_range: str,
        pretty_format: str = "%H",
        reverse: bool = False,
    ) -> CommandResult: ...

    def show_commit(
        self,
        sha: str,
        pretty_format: str = "%B",
    ) -> CommandResult: ...

    def get_commits_between_tags(
        self,
        from_tag: str,
        to_tag: str,
    ) -> CommandResult: ...

    def get_commit_count(self) -> CommandResult: ...

    def get_tag_date(self, tag: str) -> CommandResult: ...

    def get_all_tags(self) -> CommandResult: ...

    def get_tags(self) -> CommandResult: ...

    def diff_name_only(self) -> CommandResult: ...
    def describe_latest_tag(self) -> CommandResult: ...

    # ======================
    # Commit / Tag / Push
    # ======================
    def commit(
        self,
        message: Optional[str] = None,
        message_file: Optional[str] = None,
    ) -> CommandResult: ...

    def tag(
        self,
        tag: str,
        message: Optional[str] = None,
        message_file: Optional[str] = None,
        annotated: bool = True,
    ) -> CommandResult: ...

    def push(
        self,
        remote: str,
        ref: str,
        set_upstream: bool = False,
    ) -> CommandResult: ...

    def push_tag(self, remote: str, tag: str) -> CommandResult: ...

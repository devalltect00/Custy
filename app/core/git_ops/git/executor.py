# app/core/git_ops/git/executor.py

#

##### Infrastructure

import subprocess
from typing import Optional

from app.core.dry_run import DryRunSupport
from app.core.git_ops.git.result import CommandResult


class GitCommandExecutor(DryRunSupport):
    """
    Low-level Git command executor.

    This class is responsible ONLY for executing Git commands and returning
    normalized results via CommandResult.

    Flexible, parameterized, and reusable.

    It does NOT:
    - contain business logic
    - perform logging decisions
    - raise high-level domain errors

    It DOES:
    - execute git commands via Runner
    - handle dry-run behavior
    - normalize subprocess results into CommandResult
    """

    def __init__(self, dry_run: bool = False, is_silent: bool = False) -> None:
        """
        Initialize GitCommandExecutor.

        Args:
            dry_run (bool): Whether to simulate commands.
            is_silent (bool): Whether to suppress debug output.
        """
        super().__init__(dry_run=dry_run, is_silent=is_silent)

    def get_silent(self) -> bool:
        return self.runner.get_silent()

    def set_silent(self, is_silent: bool) -> None:
        self.runner.set_silent(is_silent)

    def get_is_dry_run(self) -> bool:
        return self.runner.get_is_dry_run()

    def set_is_dry_run(self, is_dry_run: bool) -> None:
        self.runner.set_is_dry_run(is_dry_run)

    #####

    def _run(
        self,
        args: list[str],
        check: bool = False,
        *,
        read_only: bool = False,
    ) -> CommandResult:
        """
        Execute a git command.

        Args:
            args (List[str]): Git command arguments (excluding 'git').
            check (bool): If True, subprocess will raise on non-zero exit.
            read_only (bool): Execute discovery during dry-run mode.

        Returns:
            CommandResult: Normalized result of execution.
        """
        result = self.runner.run(
            ["git"] + args,
            check=check,
            read_only=read_only,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )

        if result is None:
            if self.runner.get_is_dry_run() and not read_only:
                return CommandResult.dry_run()

            return CommandResult(
                returncode=1,
                stderr="Git command did not complete successfully.",
            )

        return CommandResult.from_completed(result)

    # ======================
    # Core Git commands
    # ======================

    def diff_cached_quiet(self) -> CommandResult:
        """
        Check if there are staged changes.

        Command:
            git diff --cached --quiet

        Returns:
            CommandResult:
                returncode:
                    0 → no changes
                    1 → changes exist
        """
        return self._run(
            ["diff", "--cached", "--quiet"],
            check=False,
            read_only=True,
        )

    def add_all(self) -> CommandResult:
        """
        Stage all changes (including untracked files).

        Command:
            git add .

        Returns:
            CommandResult
        """
        return self._run(["add", "."], check=True)

    def add_update(self) -> CommandResult:
        """
        Stage only modified and deleted tracked files.

        Command:
            git add --update

        Returns:
            CommandResult
        """
        return self._run(["add", "--update"], check=True)

    def add_files(self, files: list[str]) -> CommandResult:
        """
        Stage specific files.

        Args:
            files (List[str]): List of file paths.

        Command:
            git add <files>

        Returns:
            CommandResult
        """
        return self._run(["add", *files], check=True)

    def list_staged_files(self) -> CommandResult:
        """
        List staged files.

        Command:
            git diff --cached --name-only

        Returns:
            CommandResult with stdout containing file list
        """
        return self._run(
            ["diff", "--cached", "--name-only"],
            check=True,
            read_only=True,
        )

    def rev_parse_inside_work_tree(self) -> CommandResult:
        """
        Check if inside a git repository.

        Command:
            git rev-parse --is-inside-work-tree

        Returns:
            CommandResult
        """
        return self._run(
            ["rev-parse", "--is-inside-work-tree"],
            check=False,
            read_only=True,
        )

    def rev_parse_head(self) -> CommandResult:
        """
        Check if repository has at least one commit.

        Command:
            git rev-parse --verify HEAD

        Returns:
            CommandResult
        """
        return self._run(
            ["rev-parse", "--verify", "HEAD"],
            check=False,
            read_only=True,
        )

    # =========================================================
    # Branch inspection
    # =========================================================

    def current_branch(self) -> CommandResult:
        """
        Get current branch name.

        Command:
            git rev-parse --abbrev-ref HEAD

        Returns:
            CommandResult
        """
        return self._run(
            ["rev-parse", "--abbrev-ref", "HEAD"],
            check=False,
            read_only=True,
        )

    def symbolic_head(self) -> CommandResult:
        """
        Get current branch (fallback for new repo without commits).

        Command:
            git symbolic-ref --short HEAD

        Returns:
            CommandResult
        """
        return self._run(
            ["symbolic-ref", "--short", "HEAD"],
            check=False,
            read_only=True,
        )

    def branch_exists(self, branch_name: str) -> CommandResult:
        """
        Check if branch exists.
        """
        return self._run(
            ["rev-parse", "--verify", "--quiet", branch_name],
            check=False,
            read_only=True,
        )

    def list_local_branches(self) -> CommandResult:
        """
        Retrieve all local branches.

        This method uses Git's plumbing command
        ``git for-each-ref`` instead of ``git branch`` because
        it provides machine-readable output that is easier to
        parse and extend.

        Command
        -------
        git for-each-ref refs/heads
            --format=%(refname:short)

        Returns
        -------
        CommandResult
            Command output containing one branch name per line.
        """

        return self._run(
            [
                "for-each-ref",
                "refs/heads",
                "--format=%(refname:short)",
            ],
            check=True,
            read_only=True,
        )

    def list_merged_branches(self) -> CommandResult:
        """
        Retrieve merged local branches.

        Command
        -------
        git for-each-ref refs/heads
            --merged
            --format=%(refname:short)

        Returns
        -------
        CommandResult
            Branch names, one per line.
        """

        return self._run(
            [
                "for-each-ref",
                "refs/heads",
                "--merged",
                "--format=%(refname:short)",
            ],
            check=True,
            read_only=True,
        )

    def list_branch_metadata(self) -> CommandResult:
        """
        Retrieve local branch metadata.

        Command
        -------
        git for-each-ref refs/heads

        Format
        ------
        <branch>|<unix_timestamp>

        Returns
        -------
        CommandResult
            Structured branch metadata.
        """

        return self._run(
            [
                "for-each-ref",
                "refs/heads",
                "--format=%(refname:short)|%(committerdate:unix)",
            ],
            check=True,
            read_only=True,
        )

    def remote_branch_exists(
        self,
        remote: str,
        branch: str,
    ) -> CommandResult:
        """
        Check whether a remote branch exists.

        Command
        -------
        git ls-remote --heads <remote> <branch>

        Returns
        -------
        CommandResult
        """

        return self._run(
            [
                "ls-remote",
                "--heads",
                remote,
                branch,
            ],
            check=False,
            read_only=True,
        )

    def delete_local_branch(
        self,
        branch: str,
        force: bool = False,
    ) -> CommandResult:
        """
        Delete a local branch.

        Parameters
        ----------
        branch:
            Branch name.

        force:
            Use ``-D`` instead of ``-d``.

        Returns
        -------
        CommandResult
        """

        return self._run(
            [
                "branch",
                "-D" if force else "-d",
                branch,
            ],
            check=True,
        )

    def delete_remote_branch(
        self,
        remote: str,
        branch: str,
    ) -> CommandResult:
        """
        Delete a branch from a remote repository.

        Command
        -------
        git push <remote> --delete <branch>

        Returns
        -------
        CommandResult
        """

        return self._run(
            [
                "push",
                remote,
                "--delete",
                branch,
            ],
            check=True,
        )

    # ======================
    # Remote
    # ======================

    def remote_get_url(self, remote: str = "origin") -> CommandResult:
        """
        Get remote URL dynamically.

        Args:
            remote (str): Remote name (origin, backup, etc.)

        Command:
            git remote get-url <remote>

        Returns:
            CommandResult
        """
        return self._run(
            ["remote", "get-url", remote],
            check=True,
            read_only=True,
        )

    # ======================
    # Log / Commit inspection
    # ======================

    def log_between(
        self,
        ref_range: str,
        pretty_format: str = "%H",
        reverse: bool = False,
    ) -> CommandResult:
        """
        Get commit hashes between refs.

        Flexible git log.

        Args:
            ref_range (str): e.g. 'v1.0.0..v1.1.0' or 'v1..v2'
            pretty_format (str): git pretty format string
            reverse (bool): chronological order

        Command:
            git log <range> --pretty=format:<format> <'--reverse' (optional)>

        Returns:
            CommandResult
        """
        cmd = ["log", ref_range, f"--pretty=format:{pretty_format}"]

        if reverse:
            cmd.insert(1, "--reverse")

        return self._run(cmd, check=True, read_only=True)

    def show_commit(
        self,
        sha: str,
        pretty_format: str = "%B",
    ) -> CommandResult:
        """
        Get full commit message.

        Show commit with flexible format.

        Args:
            format (str): format.
            sha (str): Commit hash.

        Command:
            git show -s --format=<format> <sha>

        Returns:
            CommandResult
        """
        return self._run(
            ["show", "-s", f"--format={pretty_format}", sha],
            check=True,
            read_only=True,
        )

    def get_commit_count(self) -> CommandResult:
        """
        Get total commit count.

        Command:
            git rev-list --count HEAD

        Returns:
            CommandResult with stdout containing commit count
        """
        return self._run(
            ["rev-list", "--count", "HEAD"],
            check=True,
            read_only=True,
        )

    # ======================
    # Advanced helpers
    # ======================

    def get_commits_between_tags(
        self,
        from_tag: str,
        to_tag: str,
    ) -> CommandResult:
        """
        Raw log output for parsing at service level.
        """
        format_str = "%H%n%s%n%an%n%ad%n%B%n---END---"
        rev_range = f"{from_tag}..{to_tag}" if from_tag else to_tag

        return self.log_between(
            ref_range=rev_range,
            pretty_format=format_str,
            reverse=True,
        )

    def get_tag_date(self, tag: str) -> CommandResult:
        """
        Get tag date.
        """
        return self._run(
            ["log", "-1", "--format=%ad", "--date=short", tag],
            check=True,
            read_only=True,
        )

    def get_all_tags(self) -> CommandResult:
        """
        Get all tags sorted by creation date.
        """
        return self._run(
            ["tag", "--sort=creatordate"],
            check=True,
            read_only=True,
        )

    # //====================

    def diff_name_only(self) -> CommandResult:
        """
        List modified files.

        Command:
            git diff --name-only

        Returns:
            CommandResult
        """
        return self._run(
            ["diff", "--name-only"],
            check=False,
            read_only=True,
        )

    def get_tags(self) -> CommandResult:
        """
        Get all tags.

        Command:
            git tag

        Returns:
            CommandResult
        """
        return self._run(["tag"], check=True, read_only=True)

    def describe_latest_tag(self) -> CommandResult:
        """
        Get latest tag.

        Command:
            git describe --tags --abbrev=0

        Returns:
            CommandResult
        """
        return self._run(
            ["describe", "--tags", "--abbrev=0"],
            check=False,
            read_only=True,
        )

    # ======================
    # Commit / Tag / Push
    # ======================

    def commit(
        self,
        message: Optional[str] = None,
        message_file: Optional[str] = None,
        *,
        no_verify: bool = False,
    ) -> CommandResult:
        """
        Create commit.

        Args:
            message: commit message (-m)
            message_file: file path (-F)
            no_verify: Skip Git's pre-commit and commit-msg wrappers after
                Custy has already executed recognized pre-commit stages.
        """
        cmd = ["commit"]

        if no_verify:
            cmd.append("--no-verify")

        if message_file:
            cmd += ["-F", message_file]
        elif message:
            cmd += ["-m", message]
        else:
            raise ValueError("Either message or message_file must be provided")

        return self._run(cmd, check=True)

    def tag(
        self,
        tag: str,
        message: Optional[str] = None,
        message_file: Optional[str] = None,
        annotated: bool = True,
    ) -> CommandResult:
        """
        Create tag.

        Args:
            tag: tag name
            message: inline message
            message_file: message file
            annotated: use -a
        """
        cmd = ["tag"]

        if annotated:
            cmd.append("-a")

        cmd.append(tag)

        if message_file:
            cmd += ["-F", message_file]
        elif message:
            cmd += ["-m", message]

        return self._run(cmd, check=True)

    def push(
        self,
        remote: str = "origin",
        ref: str = "HEAD",
        set_upstream: bool = False,
    ) -> CommandResult:
        """
        Push to remote.

        Args:
            remote: remote name
            ref: branch or tag
            set_upstream: add --set-upstream
        """
        cmd = ["push"]

        if set_upstream:
            cmd.append("--set-upstream")

        cmd += [remote, ref]

        return self._run(cmd, check=True)

    def push_tag(self, remote: str, tag: str) -> CommandResult:
        """
        Push specific tag.
        """
        return self._run(["push", remote, tag], check=True)

# app/core/cleanup/branch/models.py

"""
Branch cleanup domain models.

This module defines the data models used by the branch cleanup
workflow.

These models provide strongly typed contracts between the CLI,
handler, service, Git layer, and UI. Keeping the cleanup workflow
based on explicit request and result models makes the implementation
easier to test, extend, and maintain.

Models
------

BranchInfo
    Metadata describing a Git branch.

BranchCleanupRequest
    Input parameters controlling a branch cleanup operation.

BranchCleanupResult
    Summary of a completed cleanup operation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.cli.constants.enums import MergeStatusChoices


DEFAULT_PROTECTED_BRANCHES = (
    "main",
    "master",
    "develop",
)

@dataclass(slots=True)
class BranchInfo:
    """
    Metadata describing a Git branch.

    Instances of this class are created by the Git service and passed
    through the cleanup workflow. Using a structured object instead of
    raw strings allows future features such as sorting, filtering,
    reporting, exporting, and richer terminal output without changing
    the public API.

    Attributes
    ----------
    name:
        Branch name.

    last_commit:
        Timestamp of the latest commit reachable from the branch.

    merged:
        Indicates whether the branch has already been merged into the
        current target branch.

    remote_exists:
        Indicates whether the branch also exists on the configured
        remote repository.
    """

    name: str

    last_commit: datetime

    merged: bool

    remote_exists: bool = True

    @property
    def age(self) -> timedelta:
        """
        Return the current age of the branch.

        Returns
        -------
        timedelta
            Elapsed time since the branch's latest commit.
        """
        return datetime.now() - self.last_commit


@dataclass(slots=True)
class BranchCleanupRequest:
    """
    Configuration for a branch cleanup operation.

    This model contains every option required by the cleanup service.

    It is intentionally independent from Typer, configuration loading,
    and Git execution so it can be reused by tests and future APIs.

    Attributes
    ----------
    include_prefixes:
        Only branches beginning with one of these prefixes will be
        considered for cleanup.

        When ``None`` or empty, all branch prefixes are accepted.

    merge_status:
        Determines whether all, merged, or unmerged branches should be
        considered.

    max_age:
        Relative age filter.

        Only branches older than the supplied duration will be
        considered.

        -----

        Maximum allowed branch age.

        Branches newer than this duration will be skipped.

        -----

        This filter is mutually exclusive with ``before``.

        When ``None``, no relative age filter is applied.

    before:
        Absolute date filter.

        Only branches whose latest commit occurred before the
        supplied date will be considered.

        This filter is mutually exclusive with ``max_age``.

        When ``None``, no absolute date filter is applied.

    delete_local:
        Delete local branches.

    delete_remote:
        Delete remote branches.

    remote:
        Target Git remote used for remote branch deletion.

    protected_branches:
        Branches that must never be deleted.
    """

    include_prefixes: list[str] = field(default_factory=list)

    merge_status: MergeStatusChoices = MergeStatusChoices.MERGED

    max_age: timedelta | None = None

    before: datetime | None = None

    delete_local: bool = True

    delete_remote: bool = True

    remote: str = "origin"

    protected_branches: list[str] = field(
        default_factory=lambda: list(DEFAULT_PROTECTED_BRANCHES)
    )


@dataclass(slots=True)
class BranchCleanupResult:
    """
    Result of a completed branch cleanup operation.

    The cleanup service returns this model after processing every
    branch. The UI layer is responsible for presenting the result to
    the user.

    Attributes
    ----------
    scanned:
        Total number of branches evaluated.

    deleted_local:
        Names of successfully deleted local branches. In dry-run mode,
        these are local branches that would be deleted.

    deleted_remote:
        Names of successfully deleted remote branches. In dry-run mode,
        these are remote branches that would be deleted.

    skipped:
        Names of skipped branches.

    failed:
        Mapping of branch names to failure messages.

    dry_run:
        Indicates whether the cleanup was executed in dry-run mode.
    """

    scanned: int = 0

    deleted_local: list[str] = field(default_factory=list)

    deleted_remote: list[str] = field(default_factory=list)

    skipped: list[str] = field(default_factory=list)

    failed: dict[str, str] = field(default_factory=dict)

    dry_run: bool = False

    @property
    def deleted_count(self) -> int:
        """
        Return the number of deleted or planned local branches.

        Returns
        -------
        int
            Number of deleted local branches, or deletion candidates during
            dry-run mode.
        """
        return len(self.deleted_local)

    @property
    def skipped_count(self) -> int:
        """
        Return the number of skipped branches.

        Returns
        -------
        int
            Number of skipped branches.
        """
        return len(self.skipped)

    @property
    def failed_count(self) -> int:
        """
        Return the number of failed branch deletions.

        Returns
        -------
        int
            Number of failures.
        """
        return len(self.failed)

    @property
    def success(self) -> bool:
        """
        Determine whether the cleanup completed without failures.

        Returns
        -------
        bool
            True when no deletion failures occurred.
        """
        return self.failed_count == 0

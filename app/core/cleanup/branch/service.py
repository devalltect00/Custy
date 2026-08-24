# app/core/cleanup/branch/service.py

"""
Branch cleanup service.

This module contains the business logic responsible for identifying,
filtering, and deleting Git branches.

The service is intentionally independent from:

- Typer
- Rich
- subprocess
- logging presentation

All Git operations are delegated to ``GitService`` while terminal output
is delegated to ``BranchCleanupDisplay``.
"""

from __future__ import annotations

from datetime import datetime

from app.cli.constants.enums import MergeStatusChoices
from app.core.cleanup.branch.models import (
    BranchCleanupRequest,
    BranchCleanupResult,
    BranchInfo,
)
from app.core.git_ops.git.service import GitService


class BranchCleanupService:
    """
    Service responsible for branch cleanup.

    This class orchestrates the cleanup workflow while delegating Git
    operations to ``GitService``.

    Responsibilities
    ----------------

    - Retrieve branch metadata
    - Apply cleanup filters
    - Delete matching branches
    - Produce a cleanup result

    The service contains no UI logic and performs no direct subprocess
    execution.
    """

    def __init__(
        self,
        git_service: GitService,
    ) -> None:
        """
        Initialize the cleanup service.

        Parameters
        ----------
        git_service:
            Git service used for all Git operations.
        """

        self.git = git_service

    def cleanup(
        self,
        request: BranchCleanupRequest,
    ) -> BranchCleanupResult:
        """
        Execute a branch cleanup operation.

        Parameters
        ----------
        request:
            Cleanup request.

        Returns
        -------
        BranchCleanupResult
            Cleanup summary.
        """

        result = BranchCleanupResult(
            dry_run=self.git.executor.get_is_dry_run(),
        )

        branches = self.git.list_branches()

        result.scanned = len(branches)

        for branch in branches:

            if not self._should_delete(
                branch,
                request,
            ):
                result.skipped.append(branch.name)
                continue

            if request.delete_local:
                self.git.delete_local_branch(branch.name)
                result.deleted_local.append(branch.name)

            if request.delete_remote and branch.remote_exists:
                self.git.delete_remote_branch(
                    branch.name,
                    remote=request.remote,
                )
                result.deleted_remote.append(branch.name)

        return result

    def _should_delete(
        self,
        branch: BranchInfo,
        request: BranchCleanupRequest,
    ) -> bool:
        """
        Determine whether a branch satisfies every cleanup filter.

        Parameters
        ----------
        branch:
            Branch metadata.

        request:
            Cleanup request.

        Returns
        -------
        bool
            True when the branch should be deleted.
        """

        if branch.name in request.protected_branches:
            return False

        if not request.include_prefixes:
            return False

        if not any(
            branch.name.startswith(prefix)
            for prefix in request.include_prefixes
        ):
            return False

        if request.merge_status is MergeStatusChoices.MERGED:

            if not branch.merged:
                return False

        elif request.merge_status is MergeStatusChoices.UNMERGED:

            if branch.merged:
                return False

        if request.max_age is not None:

            if branch.age < request.max_age:
                return False

        if request.before is not None:

            if branch.last_commit >= request.before:
                return False

        return True

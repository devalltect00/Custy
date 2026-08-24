# app/core/cleanup/branch/handler.py

"""
Branch cleanup handler.

This module provides the entry point for branch cleanup operations.

The handler is responsible for coordinating the cleanup workflow by
connecting the request model, Git service, cleanup service, and display
layer.

Unlike the cleanup service, the handler contains no business rules.
Its responsibility is orchestration only.
"""

from __future__ import annotations

from app.core.cleanup.branch.display import BranchCleanupDisplay
from app.core.cleanup.branch.models import (
    BranchCleanupRequest,
    BranchCleanupResult,
)
from app.core.cleanup.branch.service import BranchCleanupService
from app.core.git_ops.git.factory import create_git_service


class BranchCleanupHandler:
    """
    Coordinate branch cleanup operations.

    The handler creates the required services, executes the cleanup
    workflow, and forwards the result to the display layer.

    Responsibilities
    ----------------

    - Create GitService
    - Create BranchCleanupService
    - Create BranchCleanupDisplay
    - Execute cleanup
    - Display results

    The handler intentionally contains no cleanup logic.
    """

    def __init__(
        self,
        request: BranchCleanupRequest,
        *,
        dry_run: bool = False,
        silent: bool = False,
    ) -> None:
        """
        Initialize the branch cleanup handler.

        Parameters
        ----------
        dry_run:
            Enable dry-run mode.

        silent:
            Suppress Git command output.
        """

        self.git_service = create_git_service(
            dry_run=dry_run,
            no_debug=silent,
        )

        self.cleanup_service = BranchCleanupService(
            self.git_service,
        )

        self.display = BranchCleanupDisplay()

        self.request = request

    def clean(
        self,
    ) -> BranchCleanupResult:
        """
        Execute a branch cleanup workflow.

        Parameters
        ----------
        request:
            Branch cleanup request.

        Returns
        -------
        BranchCleanupResult
            Completed cleanup result.
        """

        self.display.show_start()

        # print("self.request",self.request)

        if not self.request.include_prefixes:
            self.display.show_no_prefixes()

            return BranchCleanupResult(
                dry_run=self.git_service.get_is_dry_run(),
            )

        result = self.cleanup_service.cleanup(
            self.request,
        )

        if result.scanned == 0:
            self.display.show_no_branches()
            return result

        self.display.show_summary(result)

        return result

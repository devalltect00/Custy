# app/core/cleanup/branch/display.py

"""
Branch cleanup display helpers.

This module is responsible for presenting branch cleanup results to the
terminal.

Unlike the cleanup service, this module contains no business logic.
Its only responsibility is converting domain models into user-friendly
terminal output using the shared UI components.

Presentation responsibilities include:

- Progress messages
- Summary panels
- Cleanup tables
- Informational messages
- Warning messages
"""

from __future__ import annotations

from app.core.cleanup.branch.models import BranchCleanupResult
from app.ui.console import console
from app.ui.panels import (
    info_panel,
    success_panel,
    warning_panel,
)
from app.ui.tables import branch_cleanup_table


class BranchCleanupDisplay:
    """
    Display helper for branch cleanup operations.

    This class centralizes every piece of terminal output produced by
    the branch cleanup workflow.

    Keeping Rich rendering isolated from the cleanup service makes the
    business logic easier to test while ensuring a consistent user
    experience across commands.
    """

    def show_start(self) -> None:
        """
        Display the cleanup start message.
        """

        console.print(
            info_panel(
                "Scanning Git branches..."
            )
        )

    def show_no_branches(self) -> None:
        """
        Display a message when no branches match the requested filters.
        """

        console.print(
            warning_panel(
                (
                    "No branches matched the supplied cleanup "
                    "criteria."
                )
            )
        )

    def show_no_prefixes(self) -> None:
        """
        Display a message when no branch prefixes are configured.

        Branch cleanup intentionally skips execution when no prefixes are
        provided to prevent accidental deletion of non-protected branches.
        """

        console.print(
            warning_panel(
                (
                    "No branch prefixes were configured.\n\n"
                    "Branch cleanup was skipped to prevent accidental "
                    "deletion.\n\n"
                    "Configure one or more prefixes using:\n"
                    "• config.toml\n"
                    "• --prefix"
                )
            )
        )

    def show_summary(
        self,
        result: BranchCleanupResult,
    ) -> None:
        """
        Display the cleanup summary.

        Parameters
        ----------
        result:
            Completed cleanup result.
        """

        console.print(
            branch_cleanup_table(result)
        )

        deletion_label = "Would delete" if result.dry_run else "Deleted"

        message = (
            f"Scanned      : {result.scanned}\n"
            f"{deletion_label:<12} : {result.deleted_count}\n"
            f"Remote  : {len(result.deleted_remote)}\n"
            f"Skipped : {result.skipped_count}\n"
            f"Failed  : {result.failed_count}"
        )

        if result.dry_run:
            message += (
                "\n\nDry-run mode enabled. No local or remote branches "
                "were deleted."
            )

        console.print(
            success_panel(message)
        )

# app/core/initialize/presenters/initialization_presenter.py

"""
Initialization presentation helpers.

Responsible for rendering initialization results
using Rich UI components.
"""

from rich.table import Table

from app.core.initialize.models.initialization_result import (
    InitializationResult,
)


class InitializationPresenter:
    """
    Render initialization summaries.
    """

    def render(
        self,
        result: InitializationResult,
    ) -> Table:
        """
        Render initialization summary table.

        Parameters
        ----------
        result:
            Initialization execution result.

        Returns
        -------
        Table
            Rich table ready for console rendering.
        """

        table = Table(
            title="Initialization Summary",
        )

        table.add_column(
            "Property",
            style="cyan",
        )

        table.add_column(
            "Value",
        )

        table.add_row(
            "Mode",
            str(result.mode).title(),
        )

        action = "Would Create" if result.dry_run else "Created"
        copy_action = "Would Copy" if result.dry_run else "Copied"

        table.add_row(
            f"{action} Files",
            str(result.created_files),
        )

        table.add_row(
            f"{copy_action} Files",
            str(result.copied_files),
        )

        table.add_row(
            "Skipped Files",
            str(result.skipped_files),
        )

        table.add_row(
            f"{action} Directories",
            str(result.created_directories),
        )

        table.add_row(
            "Dry Run",
            "Yes" if result.dry_run else "No",
        )

        return table

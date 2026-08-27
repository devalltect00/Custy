# tests/core/initialize/models/test_initialization_presenter.py

"""
tests/core/initialize/test_initialization_presenter.py

Unit tests for the initialization presenter.

These tests verify that InitializationPresenter converts initialization
results into a Rich table suitable for console rendering.
"""

from rich.table import Table

from app.core.initialize.models.initialization_result import (
    InitializationResult,
)
from app.core.initialize.presenters.initialization_presenter import (
    InitializationPresenter,
)


class TestInitializationPresenter:
    """Tests for InitializationPresenter."""

    def test_render_returns_rich_table(self):
        """Renders an initialization summary as a Rich table."""

        presenter = InitializationPresenter()

        result = InitializationResult(
            mode="all",
            created_files=10,
            copied_files=5,
            skipped_files=2,
            created_directories=4,
        )

        table = presenter.render(result)

        assert isinstance(table, Table)

    def test_render_uses_expected_table_title(self):
        """Uses the expected table title."""

        presenter = InitializationPresenter()

        table = presenter.render(InitializationResult(mode="config"))

        assert table.title == "Initialization Summary"

    def test_render_creates_expected_columns(self):
        """Creates the expected table columns."""

        presenter = InitializationPresenter()

        table = presenter.render(InitializationResult(mode="config"))

        assert len(table.columns) == 2

        assert table.columns[0].header == "Property"
        assert table.columns[1].header == "Value"

    def test_render_creates_expected_number_of_rows(self):
        """Creates one row for each reported statistic."""

        presenter = InitializationPresenter()

        table = presenter.render(InitializationResult(mode="config"))

        assert len(table.rows) == 6

    def test_render_populates_all_statistics(self):
        """Populates every statistic from the execution result."""

        presenter = InitializationPresenter()

        result = InitializationResult(
            mode="templates",
            created_files=1,
            copied_files=2,
            skipped_files=3,
            created_directories=4,
        )

        table = presenter.render(result)

        cells = []

        for column in table.columns:
            cells.append(list(column.cells))

        assert cells[0] == [
            "Mode",
            "Created Files",
            "Copied Files",
            "Skipped Files",
            "Created Directories",
            "Dry Run",
        ]

        assert cells[1] == [
            "Templates",
            "1",
            "2",
            "3",
            "4",
            "No",
        ]

    def test_render_uses_planned_labels_for_dry_run(self):
        """Dry-run summaries distinguish planned from applied changes."""

        table = InitializationPresenter().render(
            InitializationResult(
                mode="all",
                created_files=1,
                copied_files=2,
                created_directories=3,
                dry_run=True,
            )
        )

        labels = list(table.columns[0].cells)

        assert "Would Create Files" in labels
        assert "Would Copy Files" in labels
        assert "Would Create Directories" in labels
        assert list(table.columns[1].cells)[-1] == "Yes"

# tests/ui/test_tables.py

"""
tests/ui/test_tables.py

Unit tests for reusable Rich table helpers.

These tests verify that configuration_table() builds a Rich table with
the expected columns and configuration values.
"""

from pathlib import Path

from rich.table import Table

from app.core.cleanup.branch.models import BranchCleanupResult
from app.ui.tables import branch_cleanup_table, configuration_table


class TestConfigurationTable:
    """Tests for configuration_table()."""

    def test_returns_rich_table(self):
        """Creates a Rich table."""

        table = configuration_table(
            target_directory=Path("/project"),
            profile="default",
            smart_mode=True,
            max_depth=5,
            show_files=False,
            collapse_dirs={"build", "__pycache__"},
            project_type="python",
        )

        assert isinstance(table, Table)

    def test_uses_expected_table_title(self):
        """Uses the expected table title."""

        table = configuration_table(
            target_directory=Path("/project"),
            profile="default",
            smart_mode=True,
            max_depth=5,
            show_files=False,
            collapse_dirs=set(),
            project_type=None,
        )

        assert table.title == "Configuration"

    def test_creates_expected_columns(self):
        """Creates the expected table columns."""

        table = configuration_table(
            target_directory=Path("/project"),
            profile="default",
            smart_mode=True,
            max_depth=5,
            show_files=False,
            collapse_dirs=set(),
            project_type=None,
        )

        assert len(table.columns) == 2

        assert table.columns[0].header == "Setting"
        assert table.columns[1].header == "Value"

    def test_creates_expected_rows(self):
        """Creates one row for each configuration value."""

        table = configuration_table(
            target_directory=Path("/project"),
            profile="release",
            smart_mode=False,
            max_depth=10,
            show_files=True,
            collapse_dirs={"src", "tests"},
            project_type="python",
        )

        assert len(table.rows) == 7

        columns = [list(column.cells) for column in table.columns]

        assert columns[0] == [
            "Target Directory",
            "Profile",
            "Smart Mode",
            "Max Depth",
            "Show Files",
            "Project Type",
            "Collapse Directories",
        ]

        # assert columns[1][0] == "/project"
        assert columns[1][0] == str(Path("/project"))
        assert columns[1][1] == "release"
        assert columns[1][2] == "False"
        assert columns[1][3] == "10"
        assert columns[1][4] == "True"
        assert columns[1][5] == "python"

        collapse = columns[1][6]

        assert collapse in (
            "src, tests",
            "tests, src",
        )

    def test_displays_dash_when_no_collapsed_directories(self):
        """Displays '-' when no collapsed directories are configured."""

        table = configuration_table(
            target_directory=Path("/project"),
            profile="default",
            smart_mode=True,
            max_depth=5,
            show_files=False,
            collapse_dirs=set(),
            project_type=None,
        )

        values = list(table.columns[1].cells)

        assert values[-1] == "-"


class TestBranchCleanupTable:
    """Tests dry-run labeling for branch cleanup summaries."""

    def test_dry_run_uses_planned_deletion_labels(self):
        """Preview tables never describe simulated deletions as applied."""

        table = branch_cleanup_table(
            BranchCleanupResult(
                deleted_local=["feature/demo"],
                deleted_remote=["feature/demo"],
                dry_run=True,
            )
        )

        labels = list(table.columns[0].cells)

        assert table.title == "Branch Cleanup Preview"
        assert "Would Delete (Local)" in labels
        assert "Would Delete (Remote)" in labels

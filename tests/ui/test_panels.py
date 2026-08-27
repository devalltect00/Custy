# tests/ui/test_panels.py

"""
tests/ui/test_panels.py

Unit tests for reusable Rich panel helpers.

These tests verify that the panel helper functions create Rich panels
with the expected titles, styles, and rendered content.
"""

import pytest
from rich.panel import Panel

from app.ui import panels


class TestPanels:
    """Tests for Rich panel helper functions."""

    # ==========================================================
    # Standard Panels
    # ==========================================================

    @pytest.mark.parametrize(
        ("factory", "title", "border_style"),
        [
            (
                panels.success_panel,
                "Success",
                "green",
            ),
            (
                panels.info_panel,
                "Info",
                "cyan",
            ),
            (
                panels.warning_panel,
                "Warning",
                "yellow",
            ),
            (
                panels.error_panel,
                "Error",
                "red",
            ),
        ],
    )
    def test_creates_standard_panel(
        self,
        factory,
        title,
        border_style,
    ):
        """Creates a panel using the expected title and border style."""

        panel = factory("Hello World")

        assert isinstance(panel, Panel)
        assert panel.title == title
        assert str(panel.border_style) == border_style
        assert panel.renderable == "Hello World"

    # ==========================================================
    # Success Summary
    # ==========================================================

    def test_creates_success_summary_panel(self):
        """Creates a success panel including elapsed execution time."""

        panel = panels.success_summary_panel(
            message="Completed",
            elapsed_time=12.345,
        )

        assert isinstance(panel, Panel)
        assert panel.title == "Success"
        assert str(panel.border_style) == "green"

        assert "Completed" in panel.renderable
        assert "Completed in 12.35 seconds" in panel.renderable

    # ==========================================================
    # Summary Panel
    # ==========================================================

    def test_creates_summary_panel(self):
        """Creates a generic summary panel."""

        panel = panels.summary_panel(
            title="Configuration",
            message="Finished",
        )

        assert isinstance(panel, Panel)
        assert panel.title == "Configuration"
        assert str(panel.border_style) == "blue"
        assert panel.renderable == "Finished"

# tests/ui/test_exceptions.py

"""
tests/ui/test_exceptions.py

Unit tests for exception presentation helpers.

These tests verify that user-facing error messages are rendered using
the shared console and error panel helper.
"""

from unittest.mock import MagicMock

from app.ui import exceptions


class TestExceptions:
    """Tests for exception presentation helpers."""

    def test_show_error_prints_error_panel(
        self,
        monkeypatch,
    ):
        """Displays an error panel using the shared console."""

        panel = object()

        error_panel = MagicMock(
            return_value=panel,
        )

        console_print = MagicMock()

        monkeypatch.setattr(
            exceptions,
            "error_panel",
            error_panel,
        )

        monkeypatch.setattr(
            exceptions.console,
            "print",
            console_print,
        )

        exceptions.show_error(
            "Something went wrong.",
        )

        error_panel.assert_called_once_with(
            "Something went wrong.",
        )

        console_print.assert_called_once_with(
            panel,
        )

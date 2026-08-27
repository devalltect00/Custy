# tests/utils/test_logging_formatter.py

"""
tests/utils/test_logging_formatter.py

Unit tests for the custom logging formatter.

These tests verify that SeparatorFormatter removes Rich markup,
formats separator lines, and preserves standard log messages.
"""

import logging

import pytest

from app.utils.logging import SeparatorFormatter


class TestSeparatorFormatter:
    """Tests for SeparatorFormatter."""

    def _record(
        self,
        message: str,
    ) -> logging.LogRecord:
        """Create a LogRecord for testing."""

        return logging.LogRecord(
            name="custy",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg=message,
            args=(),
            exc_info=None,
        )

    # ==========================================================
    # Standard Formatting
    # ==========================================================

    def test_formats_normal_message(self):
        """Formats a normal log message unchanged."""

        formatter = SeparatorFormatter("%(message)s")

        result = formatter.format(
            self._record("Hello World"),
        )

        assert result == "Hello World"

    # ==========================================================
    # Rich Markup
    # ==========================================================

    @pytest.mark.parametrize(
        ("message", "expected"),
        [
            (
                "[green]Hello[/green]",
                "Hello",
            ),
            (
                "[bold]Custy[/bold]",
                "Custy",
            ),
            (
                "[cyan]One[/cyan] [red]Two[/red]",
                "One Two",
            ),
        ],
    )
    def test_removes_rich_markup(
        self,
        message,
        expected,
    ):
        """Removes Rich markup tags."""

        formatter = SeparatorFormatter("%(message)s")

        result = formatter.format(
            self._record(message),
        )

        assert result == expected

    # ==========================================================
    # Empty Messages
    # ==========================================================

    @pytest.mark.parametrize(
        "message",
        [
            "",
            " ",
            "   ",
            "[green][/green]",
        ],
    )
    def test_empty_message_becomes_separator(
        self,
        message,
    ):
        """Converts empty messages into a separator."""

        formatter = SeparatorFormatter("%(message)s")

        result = formatter.format(
            self._record(message),
        )

        assert result == (SeparatorFormatter.COMMON_SEPARATOR)

    # ==========================================================
    # CLI Command Header
    # ==========================================================

    def test_cli_command_message_becomes_title_block(self):
        """Formats CLI command headers."""

        formatter = SeparatorFormatter("%(message)s")

        result = formatter.format(
            self._record(
                "CLI COMMAND: custy release",
            ),
        )

        assert SeparatorFormatter.TITLE_SEPARATOR in result

        assert "CLI COMMAND" in result

        assert result.startswith("\n")

        assert result.endswith(SeparatorFormatter.TITLE_SEPARATOR + "\n")

# tests/logging/test_logging.py

"""
tests/logging/test_logging.py

Unit tests for logging utilities.
"""

import logging

from app.utils.logging import SeparatorFormatter


class TestSeparatorFormatter:

    def test_empty_message_becomes_separator(self):
        formatter = SeparatorFormatter("%(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="",
            args=(),
            exc_info=None,
        )

        assert formatter.format(record) == formatter.COMMON_SEPARATOR

    def test_rich_tags_are_removed(self):
        formatter = SeparatorFormatter("%(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="[cyan]Hello[/cyan]",
            args=(),
            exc_info=None,
        )

        assert formatter.format(record) == "Hello"

    def test_cli_command_adds_title_separator(self):
        formatter = SeparatorFormatter("%(message)s")

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="CLI COMMAND: custy run release",
            args=(),
            exc_info=None,
        )

        output = formatter.format(record)

        assert formatter.TITLE_SEPARATOR in output
        assert "CLI COMMAND" in output

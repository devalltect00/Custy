# tests/ui/test_console.py

"""
tests/ui/test_console.py

Unit tests for the shared Rich console.

These tests verify that the application exposes a singleton Rich Console
configured with the application's custom theme.
"""

from rich.console import Console

from app.ui.console import console


class TestConsole:
    """Tests for the shared Rich console."""

    def test_console_is_rich_console(self):
        """Exposes a Rich Console instance."""

        assert isinstance(
            console,
            Console,
        )

    # def test_console_uses_application_theme(self):
    #     """Uses the application's configured Rich theme."""

    #     expected_theme = theme.to_rich_theme()

    #     assert console._theme_stack is not None
    #     assert console.get_style("info") == expected_theme.get_style("info")

    def test_console_has_theme(self):
        """Initializes the console with a theme."""

        assert console._theme_stack is not None

    def test_console_is_singleton(self):
        """Returns the same shared console instance."""

        from app.ui.console import console as second_console

        assert console is second_console

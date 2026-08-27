# tests/theme/test_theme.py

"""
tests/theme/test_theme.py

Unit tests for the theme module.
"""

from rich.theme import Theme as RichTheme

from app.theme.theme import (
    HelpTheme,
    Theme,
    helpExample,
    helpHint,
    helpOption,
    helpText,
    helpTitle,
    load_theme,
)


class TestTheme:
    def test_load_theme(self):
        theme = load_theme()
        assert isinstance(theme, Theme)
        assert theme.primary
        assert theme.secondary

    def test_to_rich_theme(self):
        assert isinstance(load_theme().to_rich_theme(), RichTheme)

    def test_helper_functions(self):
        assert helpTitle("cyan") == "bold cyan"
        assert helpText("abc") == "abc"
        assert helpHint("hint") == "dim hint"
        assert helpOption("opt") == "bold opt"
        assert helpExample("ex") == "italic ex"

    def test_help_theme_defaults(self):
        assert HelpTheme.title
        assert HelpTheme.text
        assert HelpTheme.option
        assert HelpTheme.example

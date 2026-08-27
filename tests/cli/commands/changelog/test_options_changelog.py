# tests/cli/commands/changelog/test_options_changelog.py

"""
tests/cli/commands/changelog/test_options.py

Tests for CLI option declarations of the changelog command.
"""

from app.cli.commands.changelog import options


class TestChangelogOptions:
    """Validate Typer option definitions."""

    def test_commit_message_option_exists(self):
        assert options.CommitMessageFileOption is not None

    def test_force_option_exists(self):
        assert options.ForceOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "CommitMessageFileOption",
            "ForceOption",
        )

        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_have_metadata(self):
        for option in (
            options.CommitMessageFileOption,
            options.ForceOption,
        ):
            assert getattr(option, "__metadata__", None) is not None

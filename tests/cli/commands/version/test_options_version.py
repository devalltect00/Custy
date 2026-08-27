# tests/cli/commands/version/test_options_version.py

"""
tests/cli/commands/version/test_options.py

Tests for CLI option declarations of the version command.
"""

from app.cli.commands.version import options


class TestVersionOptions:
    """Validate Typer option definitions."""

    def test_version_file_option_exists(self):
        assert options.VersionFileOption is not None

    def test_strategy_option_exists(self):
        assert options.StrategyOption is not None

    def test_bump_option_exists(self):
        assert options.BumpOption is not None

    def test_tag_option_exists(self):
        assert options.TagOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "VersionFileOption",
            "StrategyOption",
            "BumpOption",
            "TagOption",
        )
        for symbol in expected:
            assert hasattr(options, symbol)

    def test_option_metadata_is_available(self):
        for option in (
            options.VersionFileOption,
            options.StrategyOption,
            options.BumpOption,
            options.TagOption,
        ):
            assert getattr(option, "__metadata__", None) is not None

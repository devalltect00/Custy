# tests/cli/commands/init/test_options.py

"""
tests/cli/commands/init/test_options.py

Tests for CLI option declarations used by the init command.
"""

from typing import get_args

from app.cli.commands.init import options


class TestInitOptions:
    """Validate option objects are exposed correctly."""

    def test_mode_option_exists(self):
        assert options.ModeOption is not None

    def test_force_option_exists(self):
        assert options.ForceOption is not None

    def test_ask_option_exists(self):
        assert options.AskOption is not None

    def test_option_module_exports_expected_symbols(self):
        assert hasattr(options, "ModeOption")
        assert hasattr(options, "ForceOption")
        assert hasattr(options, "AskOption")

    def test_option_help_strings_are_defined(self):
        # Typer OptionInfo objects expose help metadata.
        for opt in (
            options.ModeOption,
            options.ForceOption,
            options.AskOption,
        ):
            # assert getattr(opt, "help", None)

            metadata = get_args(opt)

            option_info = next(item for item in metadata if hasattr(item, "help"))

            assert option_info.help

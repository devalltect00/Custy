# tests/cli/commands/validate/test_options_validate.py

"""
tests/cli/commands/validate/test_options.py

Tests for CLI option declarations of the validate command.
"""

from app.cli.commands.validate import options


class TestValidateOptions:
    """Validate Typer option definitions."""

    def test_commit_message_option_exists(self):
        assert options.CommitMessageFileOption is not None

    def test_tag_message_option_exists(self):
        assert options.TagMessageFileOption is not None

    def test_version_file_option_exists(self):
        assert options.VersionFileOption is not None

    def test_auto_stage_option_exists(self):
        assert options.AutoStageOption is not None

    def test_stage_mode_option_exists(self):
        assert options.StageModeOption is not None

    def test_check_cz_option_exists(self):
        assert options.CheckCzOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "CommitMessageFileOption",
            "TagMessageFileOption",
            "VersionFileOption",
            "AutoStageOption",
            "StageModeOption",
            "CheckCzOption",
        )

        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_have_help_metadata(self):
        for option in (
            options.CommitMessageFileOption,
            options.TagMessageFileOption,
            options.VersionFileOption,
            options.AutoStageOption,
            options.StageModeOption,
            options.CheckCzOption,
        ):
            assert getattr(option, "__metadata__", None) is not None

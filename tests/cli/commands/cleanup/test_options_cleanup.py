# tests/cli/commands/cleanup/test_options_cleanup.py

"""
tests/cli/commands/cleanup/test_options.py

Tests for CLI option declarations of the cleanup command.
"""

from app.cli.commands.cleanup import options


class TestCleanupOptions:
    """Validate Typer option definitions."""

    def test_backup_options_exist(self):
        assert options.TypeOption is not None
        assert options.KeepOption is not None

    def test_branch_options_exist(self):
        assert options.IncludePrefixesOption is not None
        assert options.MergeStatusOption is not None
        assert options.MaxAgeOption is not None
        assert options.BeforeOption is not None

    def test_directory_options_exist(self):
        assert options.CommitMessageBackupDirOption is not None
        assert options.TagMessageBackupDirOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "TypeOption",
            "KeepOption",
            "IncludePrefixesOption",
            "MergeStatusOption",
            "MaxAgeOption",
            "BeforeOption",
            "CommitMessageBackupDirOption",
            "TagMessageBackupDirOption",
        )
        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_have_metadata(self):
        for option in (
            options.TypeOption,
            options.KeepOption,
            options.IncludePrefixesOption,
            options.MergeStatusOption,
            options.MaxAgeOption,
            options.BeforeOption,
            options.CommitMessageBackupDirOption,
            options.TagMessageBackupDirOption,
        ):
            assert getattr(option, "__metadata__", None) is not None

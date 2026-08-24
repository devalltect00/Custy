# tests/cli/commands/backup/test_options_backup.py

"""
tests/cli/commands/backup/test_options.py

Tests for CLI option declarations of the backup command.
"""

from app.cli.commands.backup import options


class TestBackupOptions:
    """Validate Typer option definitions."""

    def test_commit_message_file_option_exists(self):
        assert options.CommitMessageFileOption is not None

    def test_commit_backup_dir_option_exists(self):
        assert options.CommitMessageBackupDirOption is not None

    def test_tag_message_file_option_exists(self):
        assert options.TagMessageFileOption is not None

    def test_tag_backup_dir_option_exists(self):
        assert options.TagMessageBackupDirOption is not None

    def test_expected_symbols_are_exported(self):
        expected = (
            "CommitMessageFileOption",
            "CommitMessageBackupDirOption",
            "TagMessageFileOption",
            "TagMessageBackupDirOption",
        )
        for symbol in expected:
            assert hasattr(options, symbol)

    def test_options_have_metadata(self):
        for option in (
            options.CommitMessageFileOption,
            options.CommitMessageBackupDirOption,
            options.TagMessageFileOption,
            options.TagMessageBackupDirOption,
        ):
            assert getattr(option, "__metadata__", None) is not None

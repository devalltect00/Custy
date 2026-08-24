# tests/cli/commands/backup/test_models_backup.py

"""
tests/cli/commands/backup/test_models.py

Unit tests for backup argument models.
"""

from pathlib import Path

from app.cli.commands.backup.models import (
    BackupCommitArgs,
    BackupTagArgs,
    BackupAllArgs,
)


class TestBackupModels:

    def test_backup_commit_args(self):
        args = BackupCommitArgs(
            commit_message_file=Path("commit.txt"),
            commit_message_backup_dir=Path("backups/commit"),
        )
        assert args.commit_message_file == Path("commit.txt")
        assert args.commit_message_backup_dir == Path("backups/commit")

    def test_backup_tag_args(self):
        args = BackupTagArgs(
            tag_message_file=Path("tag.txt"),
            tag_message_backup_dir=Path("backups/tag"),
        )
        assert args.tag_message_file == Path("tag.txt")
        assert args.tag_message_backup_dir == Path("backups/tag")

    def test_backup_all_args(self):
        args = BackupAllArgs(
            commit_message_file=Path("commit.txt"),
            tag_message_file=Path("tag.txt"),
            commit_message_backup_dir=Path("backups/commit"),
            tag_message_backup_dir=Path("backups/tag"),
        )
        assert args.commit_message_file == Path("commit.txt")
        assert args.tag_message_file == Path("tag.txt")
        assert args.commit_message_backup_dir == Path("backups/commit")
        assert args.tag_message_backup_dir == Path("backups/tag")

    def test_dataclass_equality(self):
        assert BackupCommitArgs(None, None) == BackupCommitArgs(None, None)
        assert BackupTagArgs(None, None) == BackupTagArgs(None, None)
        assert BackupAllArgs(None, None, None, None) == BackupAllArgs(None, None, None, None)

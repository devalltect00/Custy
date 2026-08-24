# tests/cli/commands/backup/test_resolver_backup.py

"""
tests/cli/commands/backup/test_resolver.py

Unit tests for backup resolvers.
"""

from pathlib import Path

from app.cli.commands.backup import resolver
from app.cli.commands.backup.models import (
    BackupCommitArgs,
    BackupTagArgs,
    BackupAllArgs,
)


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(self, **kwargs):
        self.commit_message_file = kwargs.get("commit_message_file")
        self.tag_message_file = kwargs.get("tag_message_file")
        self.commit_message_backup_dir = kwargs.get("commit_message_backup_dir")
        self.tag_message_backup_dir = kwargs.get("tag_message_backup_dir")


class TestBackupResolvers:

    def test_resolve_backup_commit_args_defaults(self):
        args = resolver.resolve_backup_commit_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, BackupCommitArgs)

    def test_resolve_backup_commit_args_preserves_values(self):
        commit = Path("commit.txt")
        backup = Path("backups/commit")

        args = resolver.resolve_backup_commit_args(
            DummyConfig(),
            DummyCliArgs(
                commit_message_file=commit,
                commit_message_backup_dir=backup,
            ),
        )

        assert args.commit_message_file == commit
        assert args.commit_message_backup_dir == backup

    def test_resolve_backup_tag_args_defaults(self):
        args = resolver.resolve_backup_tag_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, BackupTagArgs)

    def test_resolve_backup_tag_args_preserves_values(self):
        tag = Path("tag.txt")
        backup = Path("backups/tag")

        args = resolver.resolve_backup_tag_args(
            DummyConfig(),
            DummyCliArgs(
                tag_message_file=tag,
                tag_message_backup_dir=backup,
            ),
        )

        assert args.tag_message_file == tag
        assert args.tag_message_backup_dir == backup

    def test_resolve_backup_all_args(self):
        args = resolver.resolve_backup_all_args(
            DummyConfig(),
            DummyCliArgs(
                commit_message_file=Path("commit.txt"),
                tag_message_file=Path("tag.txt"),
                commit_message_backup_dir=Path("backups/commit"),
                tag_message_backup_dir=Path("backups/tag"),
            ),
        )

        assert isinstance(args, BackupAllArgs)
        assert args.commit_message_file == Path("commit.txt")
        assert args.tag_message_file == Path("tag.txt")

# tests/cli/commands/cleanup/test_resolver_cleanup.py

"""Unit tests for cleanup argument resolvers."""

from datetime import datetime, timedelta
from pathlib import Path

from app.cli.commands.cleanup import resolver
from app.cli.commands.cleanup.models import (
    CleanupAllArgs,
    CleanupBackupArgs,
    CleanupBranchesArgs,
)
from app.cli.constants import CleanupTypeChoices, MergeStatusChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


class DummyCliArgs:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.keep = kwargs.get("keep")
        self.include_prefixes = kwargs.get("include_prefixes")
        self.merge_status = kwargs.get("merge_status")
        self.max_age = kwargs.get("max_age")
        self.before = kwargs.get("before")
        self.commit_message_backup_dir = kwargs.get("commit_message_backup_dir")
        self.tag_message_backup_dir = kwargs.get("tag_message_backup_dir")


class TestCleanupResolvers:
    def test_resolve_cleanup_backup_args_defaults(self):
        args = resolver.resolve_cleanup_backup_args(
            DummyConfig(),
            DummyCliArgs(),
        )
        assert isinstance(args, CleanupBackupArgs)
        assert args.type == CleanupTypeChoices.ALL
        assert args.keep == 10

    def test_resolve_cleanup_backup_args_preserves_values(self):
        args = resolver.resolve_cleanup_backup_args(
            DummyConfig(),
            DummyCliArgs(
                type=CleanupTypeChoices.TAG,
                keep=5,
                commit_message_backup_dir=Path("commit"),
                tag_message_backup_dir=Path("tag"),
            ),
        )

        assert args.type == CleanupTypeChoices.TAG
        assert args.keep == 5
        assert args.commit_message_backup_dir == Path("commit")
        assert args.tag_message_backup_dir == Path("tag")

    def test_resolve_cleanup_branches_args(self):
        args = resolver.resolve_cleanup_branches_args(
            DummyConfig(),
            DummyCliArgs(
                include_prefixes=["feature/"],
                merge_status=MergeStatusChoices.MERGED,
                max_age="30d",
            ),
        )

        assert isinstance(args, CleanupBranchesArgs)
        assert args.include_prefixes == ["feature/"]
        assert args.merge_status is MergeStatusChoices.MERGED
        assert args.max_age == timedelta(days=30)
        assert args.before is None

    def test_resolve_cleanup_all_args(self):
        args = resolver.resolve_cleanup_all_args(
            DummyConfig(),
            DummyCliArgs(
                type=CleanupTypeChoices.ALL,
                keep=3,
                include_prefixes=["fix/"],
                merge_status=MergeStatusChoices.ALL,
                before="2026-07-01",
            ),
        )

        assert isinstance(args, CleanupAllArgs)
        assert args.keep == 3
        assert args.include_prefixes == ["fix/"]
        assert args.merge_status is MergeStatusChoices.ALL
        assert args.max_age is None
        assert args.before == datetime(2026, 7, 1)

# tests/cli/commands/cleanup/test_models_cleanup.py

"""Unit tests for cleanup argument models."""

from datetime import datetime, timedelta
from pathlib import Path

from app.cli.commands.cleanup.models import (
    CleanupAllArgs,
    CleanupBackupArgs,
    CleanupBranchesArgs,
)
from app.cli.constants import CleanupTypeChoices, MergeStatusChoices


class TestCleanupModels:

    def test_backup_args(self):
        args = CleanupBackupArgs(
            type=CleanupTypeChoices.ALL,
            keep=10,
            commit_message_backup_dir=Path("c"),
            tag_message_backup_dir=Path("t"),
        )
        assert args.type == CleanupTypeChoices.ALL
        assert args.keep == 10

    def test_branch_args(self):
        args = CleanupBranchesArgs(
            include_prefixes=["feature/"],
            merge_status=MergeStatusChoices.MERGED,
            max_age=timedelta(days=30),
            before=None,
        )
        assert args.include_prefixes == ["feature/"]
        assert args.merge_status is MergeStatusChoices.MERGED
        assert args.max_age == timedelta(days=30)
        assert args.before is None

    def test_all_args(self):
        args = CleanupAllArgs(
            type=CleanupTypeChoices.ALL,
            keep=5,
            include_prefixes=["fix/"],
            merge_status=MergeStatusChoices.ALL,
            max_age=None,
            before=datetime(2026, 7, 1),
            commit_message_backup_dir=Path("c"),
            tag_message_backup_dir=Path("t"),
        )
        assert args.keep == 5
        assert args.include_prefixes == ["fix/"]
        assert args.merge_status is MergeStatusChoices.ALL
        assert args.before == datetime(2026, 7, 1)

    def test_dataclass_equality(self):
        left = CleanupBranchesArgs(
            include_prefixes=["feature/"],
            merge_status=MergeStatusChoices.UNMERGED,
        )
        right = CleanupBranchesArgs(
            include_prefixes=["feature/"],
            merge_status=MergeStatusChoices.UNMERGED,
        )

        assert left == right

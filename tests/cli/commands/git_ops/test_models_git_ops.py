# tests/cli/commands/git_ops/test_models_git_ops.py

"""
tests/cli/commands/git_ops/test_models.py

Unit tests for git operation argument models.
"""

from pathlib import Path

from app.cli.commands.git_ops.models import CommitArgs, PushArgs, TagArgs
from app.cli.constants import BumpChoices, StageModeChoices, StrategyChoices


class TestGitOpsModels:
    def test_commit_args(self):
        args = CommitArgs(
            commit_message_file=Path("commit.txt"),
            force_commit=True,
            auto_stage=True,
            stage_mode=StageModeChoices.ALL,
            strategy=StrategyChoices.SEMVER,
            version_file=Path("app/__version__.py"),
            check_cz=True,
            commit_message_backup_dir=Path("backup"),
        )
        assert args.force_commit is True
        assert args.auto_stage is True
        assert args.stage_mode == StageModeChoices.ALL

    def test_tag_args(self):
        args = TagArgs(
            tag_message_file=Path("tag.txt"),
            version_file=Path("app/__version__.py"),
            strategy=StrategyChoices.PEP440,
            bump=BumpChoices.PATCH,
            tag="v1.0.0",
            tag_message="Release",
            pre_release=None,
            post_release=False,
            dev_release=False,
            meta=None,
            epoch=None,
            skip_check=False,
            force_tag=False,
            tag_message_backup_dir=Path("backup"),
        )
        assert args.tag == "v1.0.0"

    def test_push_args(self):
        args = PushArgs(
            all_remote=True,
            remote="origin",
            tag="v1.0.0",
            skip_tag=False,
            sync_backup=True,
        )
        assert args.remote == "origin"

    def test_dataclass_equality(self):
        assert PushArgs(False, None, None, False, False) == PushArgs(
            False, None, None, False, False
        )

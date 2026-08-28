# tests/cli/commands/run/test_models_run.py

"""
tests/cli/commands/run/test_models.py

Unit tests for RunArgs.
"""

from pathlib import Path

from app.cli.commands.run.models import RunArgs
from app.cli.constants import StageModeChoices, StrategyChoices


class TestRunArgs:
    def test_construct(self):
        args = RunArgs(
            steps=["commit", "tag"],
            check_cz=True,
            auto_stage=True,
            stage_mode=StageModeChoices.ALL,
            commit_message_file=Path("commit.txt"),
            force_commit=False,
            commit_message_backup_dir=Path("backup/commit"),
            tag_message_file=Path("tag.txt"),
            version_file=Path("app/__version__.py"),
            strategy=StrategyChoices.SEMVER,
            bump=None,
            tag="v1.0.0",
            tag_message="release",
            pre_release=None,
            post_release=False,
            dev_release=False,
            meta=None,
            epoch=None,
            force_tag=False,
            skip_check=False,
            tag_message_backup_dir=Path("backup/tag"),
            all_remote=True,
            remote="origin",
            default_remote="origin",
            main_remotes=["origin"],
            backup_remotes=["backup"],
            push_to="all",
            skip_tag=False,
            sync_backup=True,
        )

        assert args.steps == ["commit", "tag"]
        assert args.strategy == StrategyChoices.SEMVER
        assert args.remote == "origin"

    def test_dataclass_equality(self):
        # left = RunArgs(
        #     [], False, False, StageModeChoices.ALL,
        #     None, False, None,
        #     None, None, None, None, None, None, None,
        #     False, False, None, None,
        #     False, False, True, "origin", False, False,
        # )

        left = RunArgs(
            steps=[],
            check_cz=False,
            auto_stage=False,
            stage_mode=StageModeChoices.ALL,
            commit_message_file=None,
            force_commit=False,
            commit_message_backup_dir=None,
            tag_message_file=None,
            version_file=None,
            strategy=None,
            bump=None,
            tag=None,
            tag_message=None,
            pre_release=None,
            post_release=False,
            dev_release=False,
            meta=None,
            epoch=None,
            force_tag=False,
            skip_check=False,
            tag_message_backup_dir=None,
            all_remote=True,
            remote="origin",
            default_remote="origin",
            main_remotes=["origin"],
            backup_remotes=[],
            push_to="main",
            skip_tag=False,
            sync_backup=False,
        )

        # right = RunArgs(
        #     [], False, False, StageModeChoices.ALL,
        #     None, False, None,
        #     None, None, None, None, None, None, None,
        #     False, False, None, None,
        #     False, False, True, "origin", False, False,
        # )

        right = RunArgs(
            steps=[],
            check_cz=False,
            auto_stage=False,
            stage_mode=StageModeChoices.ALL,
            commit_message_file=None,
            force_commit=False,
            commit_message_backup_dir=None,
            tag_message_file=None,
            version_file=None,
            strategy=None,
            bump=None,
            tag=None,
            tag_message=None,
            pre_release=None,
            post_release=False,
            dev_release=False,
            meta=None,
            epoch=None,
            force_tag=False,
            skip_check=False,
            tag_message_backup_dir=None,
            all_remote=True,
            remote="origin",
            default_remote="origin",
            main_remotes=["origin"],
            backup_remotes=[],
            push_to="main",
            skip_tag=False,
            sync_backup=False,
        )

        assert left == right

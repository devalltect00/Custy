# tests/cli/commands/git_ops/test_resolver_git_ops.py

"""
tests/cli/commands/git_ops/test_resolver.py

Unit tests for git operation resolvers.
"""

from pathlib import Path

from app.cli.commands.git_ops import resolver
from app.cli.commands.git_ops.models import CommitArgs, TagArgs, PushArgs
from app.cli.constants import StrategyChoices, StageModeChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


# class DummyCliArgs:
#     def __init__(self, **kwargs):
#         self.__dict__.update(kwargs)

class DummyCliArgs:
    def __init__(self, **kwargs):
        defaults = {
            # commit
            "commit_message_file": None,
            "force_commit": None,
            "auto_stage": None,
            "stage_mode": None,
            "strategy": None,
            "version_file": None,
            "check_cz": None,
            "commit_message_backup_dir": None,

            # tag
            "tag_message_file": None,
            "bump": None,
            "tag": None,
            "tag_message": None,
            "pre_release": None,
            "post_release": None,
            "dev_release": None,
            "meta": None,
            "epoch": None,
            "skip_check": None,
            "force_tag": None,
            "tag_message_backup_dir": None,

            # push
            "all_remote": None,
            "remote": None,
            "skip_tag": None,
            "sync_backup": None,
        }

        defaults.update(kwargs)

        for key, value in defaults.items():
            setattr(self, key, value)


class TestGitOpsResolvers:

    def test_resolve_commit_args_defaults(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_commit_args(DummyConfig(), DummyCliArgs())

        assert isinstance(args, CommitArgs)
        assert args.auto_stage is False
        assert args.force_commit is False
        assert args.stage_mode == StageModeChoices.ALL
        assert args.strategy == StrategyChoices.SEMVER

    def test_resolve_commit_args_preserves_values(self):
        args = resolver.resolve_commit_args(
            DummyConfig(),
            DummyCliArgs(
                commit_message_file=Path("commit.txt"),
                force_commit=True,
                auto_stage=True,
                stage_mode=StageModeChoices.UPDATE,
                strategy=StrategyChoices.PEP440,
                version_file=Path("app/__version__.py"),
                check_cz=True,
                commit_message_backup_dir=Path("backup"),
            ),
        )

        assert args.force_commit is True
        assert args.auto_stage is True
        assert args.stage_mode == StageModeChoices.UPDATE

    def test_resolve_tag_args(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_tag_args(
            DummyConfig(),
            DummyCliArgs(tag="v1.0.0"),
        )

        assert isinstance(args, TagArgs)
        assert args.tag == "v1.0.0"

    def test_resolve_push_args(self):
        args = resolver.resolve_push_args(
            DummyConfig(),
            DummyCliArgs(
                remote="origin",
                all_remote=True,
                sync_backup=True,
                skip_tag=False,
                tag="v1.0.0",
            ),
        )

        assert isinstance(args, PushArgs)
        assert args.remote == "origin"
        assert args.sync_backup is True

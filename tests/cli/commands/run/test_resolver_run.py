# tests/cli/commands/run/test_resolver_run.py

"""
tests/cli/commands/run/test_resolver.py

Unit tests for resolve_run_args().
"""

from pathlib import Path

from app.cli.commands.run import resolver
from app.cli.commands.run.models import RunArgs
from app.cli.constants import StageModeChoices, StrategyChoices


class DummyConfig:
    def resolve(self, value, key, default):
        return default if value is None else value


# class DummyCliArgs:
#     def __init__(self, **kwargs):
#         self.__dict__.update(kwargs)


class DummyCliArgs:
    def __init__(self, **kwargs):
        defaults = {
            # pipeline
            "steps": None,
            # commit
            "check_cz": None,
            "auto_stage": None,
            "stage_mode": None,
            "commit_message_file": None,
            "force_commit": None,
            "commit_message_backup_dir": None,
            # tag
            "tag_message_file": None,
            "version_file": None,
            "strategy": None,
            "bump": None,
            "tag": None,
            "tag_message": None,
            "pre_release": None,
            "post_release": None,
            "dev_release": None,
            "meta": None,
            "epoch": None,
            "force_tag": None,
            "skip_check": None,
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


class TestRunResolver:
    def test_returns_run_args(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_run_args(
            DummyConfig(),
            DummyCliArgs(steps=["release"]),
        )

        assert isinstance(args, RunArgs)
        assert args.steps == ["release"]

    def test_default_values_are_used(self, monkeypatch):
        monkeypatch.setattr(
            resolver,
            "detect_project_strategy",
            lambda no_debug=True: StrategyChoices.SEMVER,
        )

        args = resolver.resolve_run_args(
            DummyConfig(),
            DummyCliArgs(steps=["commit"]),
        )

        assert args.auto_stage is False
        assert args.check_cz is False
        assert args.stage_mode == StageModeChoices.ALL
        assert args.strategy == StrategyChoices.SEMVER
        assert args.remote == "origin"
        assert args.all_remote is True

    def test_explicit_values_are_preserved(self):
        args = resolver.resolve_run_args(
            DummyConfig(),
            DummyCliArgs(
                steps=["commit", "tag"],
                auto_stage=True,
                check_cz=True,
                stage_mode=StageModeChoices.UPDATE,
                commit_message_file=Path("commit.txt"),
                force_commit=True,
                commit_message_backup_dir=Path("backup/commit"),
                tag_message_file=Path("tag.txt"),
                version_file=Path("app/__version__.py"),
                strategy=StrategyChoices.PEP440,
                tag="v2.0.0",
                remote="backup",
                all_remote=False,
                skip_tag=True,
                sync_backup=True,
            ),
        )

        assert args.steps == ["commit", "tag"]
        assert args.auto_stage is True
        assert args.check_cz is True
        assert args.stage_mode == StageModeChoices.UPDATE
        assert args.strategy == StrategyChoices.PEP440
        assert args.tag == "v2.0.0"
        assert args.remote == "backup"
        assert args.sync_backup is True

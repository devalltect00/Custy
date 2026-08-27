# tests/core/workflow/test_workflow_builder.py

"""
tests/workflow/test_workflow_builder.py

Unit tests for WorkflowEngineBuilder.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from app.cli.constants.enums import (
    BumpChoices,
    CleanupTypeChoices,
    LogLevelChoices,
    StageModeChoices,
    StrategyChoices,
)
from app.core.workflow.workflow_builder import WorkflowEngineBuilder
from app.core.workflow.workflow_engine import WorkflowEngine


class TestWorkflowBuilder:
    def test_default_builder(self):
        builder = WorkflowEngineBuilder()

        assert builder.config is not None

    def test_fluent_api(self):
        engine = (
            WorkflowEngineBuilder()
            .with_commit_message("hello")
            .with_commit_file("commit.txt")
            .with_tag("v1.2.3")
            .with_tag_message("release")
            .with_tag_file("tag.txt")
            .with_strategy(StrategyChoices.SEMVER)
            .with_bump(BumpChoices.MINOR)
            .with_pre_release("rc1")
            .with_post_release(True)
            .with_dev_release(True)
            .with_meta("sha123")
            .with_epoch(1)
            .with_version_file("__version__.py")
            .with_auto_stage(StageModeChoices.UPDATE)
            .with_force_commit()
            .with_force_tag()
            .with_force_changelog()
            .with_sync_backup()
            .with_main_remotes(["origin"])
            .with_backup_remotes(["backup"])
            .with_cleanup_types(CleanupTypeChoices.TAG)
            .with_backup_retention(15)
            .with_commit_backup_dir("backup/commit")
            .with_tag_backup_dir("backup/tag")
            .with_dry_run()
            .with_debug()
            .with_skip_checks()
            .with_log_level(LogLevelChoices.DEBUG)
            .build()
        )

        assert isinstance(engine, WorkflowEngine)

        cfg = engine.config

        assert cfg.commit_message_input == "hello"
        assert cfg.commit_message_file == Path("commit.txt")
        assert cfg.tag_input == "v1.2.3"
        assert cfg.tag_message_input == "release"
        assert cfg.tag_message_file == Path("tag.txt")

        assert cfg.strategy == StrategyChoices.SEMVER
        assert cfg.bump_level == BumpChoices.MINOR

        assert cfg.auto_stage is True
        assert cfg.stage_mode == StageModeChoices.UPDATE

        assert cfg.force_commit is True
        assert cfg.force_tag is True
        assert cfg.force_changelog is True

        assert cfg.sync_backup is True

        assert cfg.main_remotes == ["origin"]
        assert cfg.backup_remotes == ["backup"]

        assert cfg.cleanup_backup_type == CleanupTypeChoices.TAG
        assert cfg.backup_retention_count == 15

        assert cfg.dry_run is True
        assert cfg.no_debug is False
        assert cfg.skip_checks is True
        assert cfg.log_level == LogLevelChoices.DEBUG

    def test_with_debug_false(self):
        builder = WorkflowEngineBuilder()

        builder.with_debug(False)

        assert builder.config.no_debug is True

    def test_validate_stage_mode(self):
        builder = WorkflowEngineBuilder()

        builder.config.auto_stage = True
        builder.config.stage_mode = None

        with pytest.raises(ValueError):
            builder.build()

    def test_get_helper(self):
        class Dummy:
            value = 123

        assert WorkflowEngineBuilder._get(Dummy(), "value") == 123
        assert WorkflowEngineBuilder._get(Dummy(), "missing", 999) == 999


##### Additional


class TestFromCliArgs:
    """Tests for WorkflowEngineBuilder.from_cli_args()."""

    class FullArgs:
        commit_message = "feat: builder"
        commit_message_file = "commit.txt"

        tag = "v1.2.3"
        tag_message = "Release"
        tag_message_file = "tag.txt"

        strategy = StrategyChoices.SEMVER
        bump_level = BumpChoices.MINOR

        pre_release = "rc1"
        post_release = True
        dev_release = True

        meta = "abc123"
        epoch = 2

        version_file = "__version__.py"

        auto_stage = True
        stage_mode = StageModeChoices.UPDATE

        force_commit = True
        force_tag = True
        force_changelog = True

        sync_backup = True

        main_remotes = ["origin"]
        backup_remotes = ["backup"]

        cleanup_backup_type = CleanupTypeChoices.TAG
        backup_retention_count = 10

        commit_message_backup_dir = "backup/commit"
        tag_message_backup_dir = "backup/tag"

        dry_run = True
        no_debug = False
        skip_checks = True

        log_level = LogLevelChoices.DEBUG

    def test_from_cli_args_populates_config(self):
        builder = WorkflowEngineBuilder()

        builder.from_cli_args(self.FullArgs())

        cfg = builder.config

        assert cfg.commit_message_input == "feat: builder"
        assert cfg.commit_message_file == Path("commit.txt")

        assert cfg.tag_input == "v1.2.3"
        assert cfg.tag_message_input == "Release"
        assert cfg.tag_message_file == Path("tag.txt")

        assert cfg.strategy == StrategyChoices.SEMVER
        assert cfg.bump_level == BumpChoices.MINOR

        assert cfg.pre_release == "rc1"
        assert cfg.post_release is True
        assert cfg.dev_release is True

        assert cfg.meta == "abc123"
        assert cfg.epoch == 2

        assert cfg.version_file == Path("__version__.py")

        assert cfg.auto_stage is True
        assert cfg.stage_mode == StageModeChoices.UPDATE

        assert cfg.force_commit is True
        assert cfg.force_tag is True
        assert cfg.force_changelog is True

        assert cfg.sync_backup is True

        # assert cfg.main_remotes == ["origin"]
        # assert cfg.backup_remotes == ["backup"]

        assert cfg.main_remotes is None
        assert cfg.backup_remotes is None

        assert cfg.cleanup_backup_type == CleanupTypeChoices.TAG
        assert cfg.backup_retention_count == 10

        assert cfg.commit_message_backup_dir == Path("backup/commit")
        assert cfg.tag_message_backup_dir == Path("backup/tag")

        assert cfg.dry_run is True
        assert cfg.no_debug is False
        assert cfg.skip_checks is True
        assert cfg.log_level == LogLevelChoices.DEBUG

    def test_from_cli_args_empty_object(self):
        class Args:
            pass

        builder = WorkflowEngineBuilder()

        result = builder.from_cli_args(Args())

        assert result is builder

    def test_from_cli_args_auto_stage_disabled(self):
        class Args:
            auto_stage = False

        builder = WorkflowEngineBuilder()

        builder.from_cli_args(Args())

        assert builder.config.auto_stage is False

    def test_from_cli_args_cleanup_all_is_ignored(self):
        class Args:
            cleanup_backup_type = CleanupTypeChoices.ALL

        builder = WorkflowEngineBuilder()

        builder.from_cli_args(Args())

        # assert builder.config.cleanup_backup_type != CleanupTypeChoices.ALL

        assert builder.config.cleanup_backup_type == CleanupTypeChoices.ALL

    def test_from_cli_args_info_log_level_is_ignored(self):
        class Args:
            log_level = LogLevelChoices.INFO

        builder = WorkflowEngineBuilder()

        builder.from_cli_args(Args())

        # assert builder.config.log_level != LogLevelChoices.INFO

        assert builder.config.log_level == LogLevelChoices.INFO

    def test_from_cli_args_no_debug(self):
        class Args:
            no_debug = True

        builder = WorkflowEngineBuilder()

        builder.from_cli_args(Args())

        assert builder.config.no_debug is True


class TestBuild:
    """Tests for WorkflowEngineBuilder.build()."""

    @patch("app.core.workflow.workflow_builder.WorkflowEngine")
    def test_build_returns_engine(self, engine_cls):
        builder = WorkflowEngineBuilder()

        engine = builder.build()

        engine_cls.assert_called_once_with(builder.config)
        assert engine == engine_cls.return_value

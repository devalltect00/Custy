# tests/core/workflow/test_workflow_config.py

"""
tests/workflow/test_workflow_config.py

Unit tests for WorkflowConfig.
"""

from pathlib import Path

from app.cli.constants.enums import (
    BumpChoices,
    CleanupTypeChoices,
    LogLevelChoices,
    StageModeChoices,
    StrategyChoices,
)
from app.core.editor import EditorIdentifier, EditorSettings
from app.core.workflow.workflow_config import WorkflowConfig


class TestWorkflowConfig:
    def test_defaults(self):
        config = WorkflowConfig()

        assert config.commit_message_input is None
        assert config.commit_message_file is None

        assert config.tag_input is None
        assert config.tag_message_input is None
        assert config.tag_message_file is None

        assert config.strategy is None
        assert config.bump_level is None

        assert config.pre_release is None
        assert config.post_release is False
        assert config.dev_release is False

        assert config.meta is None
        assert config.epoch is None

        assert config.dry_run is False
        assert config.no_debug is True
        assert config.skip_checks is False

        assert config.log_level == LogLevelChoices.INFO
        assert config.editor_settings == EditorSettings()

        assert config.version_file is None

        assert config.auto_stage is False
        assert config.stage_mode == StageModeChoices.ALL

        assert config.force_tag is False
        assert config.force_commit is False
        assert config.force_changelog is False
        assert config.sync_backup is False
        assert config.skip_tag is False

        assert config.remote is None
        assert config.default_remote == "origin"
        assert config.all_remote is False
        assert config.push_to == "main"
        assert config.main_remotes is None
        assert config.backup_remotes is None

        assert config.commit_message_backup_dir is None
        assert config.tag_message_backup_dir is None

        assert config.cleanup_backup_type == CleanupTypeChoices.ALL
        assert config.backup_retention_count == 10

    def test_custom_values(self):
        config = WorkflowConfig(
            commit_message_input="hello",
            commit_message_file=Path("commit.txt"),
            tag_input="v1.0.0",
            tag_message_input="release",
            tag_message_file=Path("tag.txt"),
            strategy=StrategyChoices.SEMVER,
            bump_level=BumpChoices.MINOR,
            pre_release="rc1",
            post_release=True,
            dev_release=True,
            meta="sha123",
            epoch=2,
            dry_run=True,
            no_debug=False,
            skip_checks=True,
            log_level=LogLevelChoices.DEBUG,
            version_file=Path("__version__.py"),
            auto_stage=True,
            stage_mode=StageModeChoices.UPDATE,
            force_tag=True,
            force_commit=True,
            force_changelog=True,
            sync_backup=True,
            skip_tag=True,
            remote="upstream",
            default_remote="origin",
            all_remote=True,
            push_to="all",
            main_remotes=["origin"],
            backup_remotes=["backup"],
            commit_message_backup_dir=Path("backup/commit"),
            tag_message_backup_dir=Path("backup/tag"),
            cleanup_backup_type=CleanupTypeChoices.TAG,
            backup_retention_count=25,
            editor_settings=EditorSettings(
                windows=(EditorIdentifier.NOTEPAD,),
            ),
        )

        assert config.strategy == StrategyChoices.SEMVER
        assert config.bump_level == BumpChoices.MINOR
        assert config.stage_mode == StageModeChoices.UPDATE
        assert config.log_level == LogLevelChoices.DEBUG
        assert config.skip_tag is True
        assert config.remote == "upstream"
        assert config.all_remote is True
        assert config.push_to == "all"
        assert config.main_remotes == ["origin"]
        assert config.backup_remotes == ["backup"]
        assert config.backup_retention_count == 25
        assert config.editor_settings.windows == (EditorIdentifier.NOTEPAD,)

    def test_dataclass_equality(self):
        left = WorkflowConfig()
        right = WorkflowConfig()

        assert left == right

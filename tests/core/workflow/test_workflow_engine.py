# tests/core/workflow/test_workflow_engine.py

"""
tests/workflow/test_workflow_engine.py

Unit tests for WorkflowEngine.

These tests focus on engine construction, configuration
propagation, helper methods, and lightweight behavior.
Business workflow methods will be covered in later phases.
"""

from pathlib import Path
from unittest.mock import MagicMock, call

from app.cli.constants.enums import (
    BumpChoices,
    LogLevelChoices,
    StageModeChoices,
    StrategyChoices,
)
from app.core.workflow.workflow_config import WorkflowConfig
from app.core.workflow.workflow_engine import WorkflowEngine


class TestWorkflowEngineInitialization:
    def test_default_initialization(self):
        config = WorkflowConfig()

        engine = WorkflowEngine(config)

        assert engine.config is config

        assert engine.commit_message_input is None
        assert engine.tag_input is None

        assert engine.dry_run is False
        assert engine.no_debug is True

        assert engine.tag == ""
        assert engine.tag_message == ""

        assert engine.changes_to_staged == []

    def test_configuration_is_copied(self):
        config = WorkflowConfig(
            commit_message_input="hello",
            commit_message_file=Path("commit.txt"),
            tag_input="v1.0.0",
            strategy=StrategyChoices.SEMVER,
            bump_level=BumpChoices.MINOR,
            stage_mode=StageModeChoices.UPDATE,
            dry_run=True,
            no_debug=False,
            log_level=LogLevelChoices.DEBUG,
        )

        engine = WorkflowEngine(config)

        assert engine.commit_message_input == "hello"
        assert engine.commit_message_file == Path("commit.txt")

        assert engine.tag_input == "v1.0.0"
        assert engine.tag == "v1.0.0"

        assert engine.strategy_input == StrategyChoices.SEMVER
        assert engine.bump_level == BumpChoices.MINOR

        assert engine.stage_mode == StageModeChoices.UPDATE

        assert engine.dry_run is True
        assert engine.no_debug is False
        assert engine.log_level == LogLevelChoices.DEBUG


class TestWorkflowHelpers:
    def test_commitizen_auto_true(self):
        config = WorkflowConfig(
            strategy=StrategyChoices.COMMITIZEN,
            bump_level=BumpChoices.AUTO,
        )

        engine = WorkflowEngine(config)

        assert engine.is_commitizen_auto() is True

    def test_commitizen_auto_false(self):
        config = WorkflowConfig(
            strategy=StrategyChoices.SEMVER,
            bump_level=BumpChoices.MINOR,
        )

        engine = WorkflowEngine(config)

        assert engine.is_commitizen_auto() is False


class TestWorkflowEditorIntegration:
    """Tests the workflow boundary around the editor service."""

    def test_open_editor_delegates_with_current_dry_run(self) -> None:
        """Workflow state is passed to the editor service at call time."""

        engine = WorkflowEngine(WorkflowConfig(dry_run=True))
        engine.editorService = MagicMock()
        message_file = Path("commit-message.txt")

        engine.open_editor(message_file, label="commit message")

        engine.editorService.open_file.assert_called_once_with(
            message_file,
            label="commit message",
            dry_run=True,
        )

    def test_edit_release_files_preserves_commit_then_tag_order(self) -> None:
        """Commit and tag messages are opened in deterministic order."""

        commit_file = Path("commit-message.txt")
        tag_file = Path("tag-message.txt")
        engine = WorkflowEngine(
            WorkflowConfig(
                commit_message_file=commit_file,
                tag_message_file=tag_file,
            )
        )
        engine.editorService = MagicMock()

        engine.edit_release_files()

        assert engine.editorService.open_file.call_args_list == [
            call(commit_file, label="commit message", dry_run=False),
            call(tag_file, label="tag message", dry_run=False),
        ]

    def test_edit_release_files_can_limit_editing_to_commit_message(self) -> None:
        """Development workflows should not open an unused tag-message file."""

        commit_file = Path("commit-message.txt")
        engine = WorkflowEngine(
            WorkflowConfig(
                commit_message_file=commit_file,
                tag_message_file=Path("tag-message.txt"),
            )
        )
        engine.editorService = MagicMock()

        engine.edit_release_files(include_tag=False)

        engine.editorService.open_file.assert_called_once_with(
            commit_file,
            label="commit message",
            dry_run=False,
        )


class TestSilentMode:
    def test_set_silent_mode(self):
        engine = WorkflowEngine(WorkflowConfig())

        engine.gitService.executor = MagicMock()
        engine.gitService.executor.runner = MagicMock()

        engine.commitizenHelper.runner = MagicMock()
        engine.changelogGenerator.runner = MagicMock()

        engine._set_silent_mode()

        engine.gitService.executor.runner.set_silent.assert_called_once_with(True)


class TestValidationEntry:
    def test_validate_calls_all_steps(self):
        engine = WorkflowEngine(WorkflowConfig())

        engine.ensure_git_repo = MagicMock()
        engine.ensure_remote_exists = MagicMock()
        engine.ensure_version_file = MagicMock()
        engine.ensure_commit_message_file = MagicMock()
        engine.ensure_tag_message_file = MagicMock()
        engine.ensure_staged_changes = MagicMock()
        engine.ensure_commit_validation_provider = MagicMock()
        engine.ensure_commit_message_file_exists = MagicMock()
        engine.ensure_tag_message_file_exists = MagicMock()

        engine.validate()

        engine.ensure_git_repo.assert_called_once()
        engine.ensure_remote_exists.assert_called_once()
        engine.ensure_version_file.assert_called_once()
        engine.ensure_commit_message_file.assert_called_once()
        engine.ensure_tag_message_file.assert_called_once()
        engine.ensure_staged_changes.assert_called_once()
        engine.ensure_commit_validation_provider.assert_called_once()
        engine.ensure_commit_message_file_exists.assert_called_once()
        engine.ensure_tag_message_file_exists.assert_called_once()

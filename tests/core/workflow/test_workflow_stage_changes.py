# tests/core/workflow/test_workflow_stage_changes.py

"""
Unit tests for WorkflowEngine.stage_changes().

This module verifies automatic staging behavior, stage mode selection,
dry-run support, and validation of staged files.

Covered behaviors include:

- Manual mode
- None mode
- All mode
- Update mode
- Dry-run
- Invalid stage mode
- Final staged-file validation
"""


from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import StageModeChoices
from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine


# ==========================================================
# Manual / None Modes
# ==========================================================


class TestManualStageModes:
    """
    Tests stage modes that do not automatically stage files.
    """

    @pytest.mark.parametrize(
        "mode",
        [
            StageModeChoices.NONE,
            StageModeChoices.MANUAL,
        ],
    )
    def test_returns_when_files_already_staged(
        self,
        workflow_engine: WorkflowEngine,
        mode,
    ) -> None:
        """
        Manual modes succeed when files are already staged.
        """

        workflow_engine.stage_mode = mode

        workflow_engine.gitService.has_staged_files.return_value = True

        workflow_engine.stage_changes()

        workflow_engine.gitService.auto_stage_all.assert_not_called()
        workflow_engine.gitService.auto_stage_update.assert_not_called()

    @pytest.mark.parametrize(
        "mode",
        [
            StageModeChoices.NONE,
            StageModeChoices.MANUAL,
        ],
    )
    def test_raises_when_no_files_are_staged(
        self,
        workflow_engine: WorkflowEngine,
        mode,
    ) -> None:
        """
        Manual modes require staged files.
        """

        workflow_engine.stage_mode = mode

        workflow_engine.gitService.has_staged_files.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.stage_changes()

        assert exc.value.code == "NO_STAGED_FILES"


# ==========================================================
# Stage All
# ==========================================================


class TestStageAll:
    """
    Tests StageModeChoices.ALL.
    """

    def test_stages_all_files(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Executes git add .
        """

        workflow_engine.stage_mode = StageModeChoices.ALL

        validator = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_validate_staged_result",
            validator,
        )

        workflow_engine.stage_changes()

        workflow_engine.gitService.auto_stage_all.assert_called_once()

        validator.assert_called_once()

    def test_dry_run_skips_git_add(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Dry-run does not execute auto-stage.
        """

        workflow_engine.stage_mode = StageModeChoices.ALL
        workflow_engine.dry_run = True

        validator = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_validate_staged_result",
            validator,
        )

        workflow_engine.stage_changes()

        workflow_engine.gitService.auto_stage_all.assert_not_called()

        validator.assert_not_called()


# ==========================================================
# Stage Update
# ==========================================================


class TestStageUpdate:
    """
    Tests StageModeChoices.UPDATE.
    """

    def test_stages_modified_files(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Executes git add --update.
        """

        workflow_engine.stage_mode = StageModeChoices.UPDATE

        validator = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_validate_staged_result",
            validator,
        )

        workflow_engine.stage_changes()

        workflow_engine.gitService.auto_stage_update.assert_called_once()

        validator.assert_called_once()

    def test_dry_run_skips_update(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Dry-run skips update staging.
        """

        workflow_engine.stage_mode = StageModeChoices.UPDATE
        workflow_engine.dry_run = True

        validator = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_validate_staged_result",
            validator,
        )

        workflow_engine.stage_changes()

        workflow_engine.gitService.auto_stage_update.assert_not_called()

        validator.assert_not_called()

    def test_manual_dry_run_reports_missing_staging_without_raising(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """Manual preview does not require a simulated index mutation."""

        workflow_engine.stage_mode = StageModeChoices.MANUAL
        workflow_engine.dry_run = True
        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine.stage_changes()

        workflow_engine.gitService.has_staged_files.assert_called_once_with()


# ==========================================================
# Invalid Stage Mode
# ==========================================================


class TestInvalidStageMode:
    """
    Tests invalid stage mode handling.
    """

    def test_invalid_stage_mode_raises(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Unknown stage modes are rejected.
        """

        workflow_engine.stage_mode = "invalid"

        with pytest.raises(ValidationError) as exc:
            workflow_engine.stage_changes()

        assert exc.value.code == "INVALID_STAGE_MODE"

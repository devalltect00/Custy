# tests/core/workflow/test_workflow_stage.py

"""
Unit tests for WorkflowEngine staging validation.

This module verifies the staging phase before commit creation.

Covered behaviour:

- existing staged files
- force commit
- dry run
- auto-stage
- empty staging detection
"""

import pytest

from app.cli.constants import StageModeChoices
from app.core.exceptions.validation_error import ValidationError

# ==========================================================
# Staging Validation
# ==========================================================


class TestEnsureStagedChanges:
    """
    Tests for WorkflowEngine.ensure_staged_changes().
    """

    def test_returns_when_files_are_already_staged(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Existing staged files immediately satisfy validation.
        """

        workflow_engine.gitService.has_staged_files.return_value = True

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.has_staged_files.assert_called_once()

    def test_force_commit_skips_validation(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Force commit bypasses staging validation.
        """

        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine.force_commit = True

        workflow_engine.ensure_staged_changes()

        assert workflow_engine.force_commit is True

    def test_dry_run_does_not_raise(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Dry-run reports the issue without raising.
        """

        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine.dry_run = True

        workflow_engine.ensure_staged_changes()

    def test_raises_when_no_staged_files(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Raises ValidationError when staging is empty.
        """

        workflow_engine.gitService.has_staged_files.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_staged_changes()

        assert exc.value.code == "NO_STAGED_CHANGES"

# ==========================================================
# Auto Stage
# ==========================================================


class TestAutoStage:
    """
    Tests automatic staging.
    """

    def test_auto_stage_all(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Auto-stage all files.
        """

        workflow_engine.auto_stage = True

        workflow_engine.gitService.has_staged_files.side_effect = [
            False,
            True,
        ]

        workflow_engine.gitService.list_staged_files.return_value = [
            "a.py",
        ]

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.auto_stage_all.assert_called_once()

    def test_auto_stage_update(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Auto-stage tracked files only.
        """

        workflow_engine.auto_stage = True
        workflow_engine.stage_mode = StageModeChoices.UPDATE

        workflow_engine.gitService.has_staged_files.side_effect = [
            False,
            True,
        ]

        workflow_engine.gitService.list_staged_files.return_value = [
            "main.py",
        ]

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.auto_stage_update.assert_called_once()

    # def test_auto_stage_failure_raises(
    #     self,
    #     workflow_engine: WorkflowEngine,
    # ) -> None:
    #     """
    #     Auto-stage failure raises ValidationError.
    #     """

    #     workflow_engine.auto_stage = True

    #     workflow_engine.gitService.has_staged_files.return_value = False

    #     workflow_engine.gitService.list_staged_files.return_value = []

    #     with pytest.raises(ValidationError) as exc:
    #         workflow_engine.ensure_staged_changes()

    #     assert exc.value.code == "AUTO_STAGE_FAILED"

# ==========================================================
# User Confirmation
# ==========================================================


class TestUserConfirmation:
    """
    Tests interactive confirmation after auto-stage fails.
    """

    def test_abort_when_user_declines(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        User choosing 'no' aborts the workflow.
        """

        workflow_engine.auto_stage = True

        workflow_engine.gitService.has_staged_files.return_value = False
        workflow_engine.gitService.list_staged_files.return_value = []

        monkeypatch.setattr(
            "builtins.input",
            lambda _: "n",
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_staged_changes()

        assert exc.value.code == "EMPTY_STAGING_ABORTED"

    def test_continue_when_user_accepts(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        User choosing 'yes' continues until auto-stage ultimately fails.
        """

        workflow_engine.auto_stage = True

        workflow_engine.gitService.has_staged_files.return_value = False
        workflow_engine.gitService.list_staged_files.return_value = []

        monkeypatch.setattr(
            "builtins.input",
            lambda _: "y",
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_staged_changes()

        assert exc.value.code == "AUTO_STAGE_FAILED"

    def test_force_commit_after_failed_auto_stage(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Force commit bypasses the second validation after auto-stage.
        """

        workflow_engine.auto_stage = True
        workflow_engine.force_commit = True

        workflow_engine.gitService.has_staged_files.return_value = False
        workflow_engine.gitService.list_staged_files.return_value = []

        workflow_engine.ensure_staged_changes()

##### Part 2

# ==========================================================
# Staged File Reporting
# ==========================================================


class TestStagedFileReporting:
    """
    Tests reporting of successfully staged files.
    """

    def test_reports_multiple_staged_files(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Successfully staged files complete validation.
        """

        workflow_engine.auto_stage = True

        workflow_engine.gitService.has_staged_files.side_effect = [
            False,
            True,
        ]

        workflow_engine.gitService.list_staged_files.return_value = [
            "app/main.py",
            "README.md",
            "tests/test_main.py",
        ]

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.auto_stage_all.assert_called_once()

        workflow_engine.gitService.list_staged_files.assert_called_once()

    def test_reports_single_staged_file(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Handles a single staged file.
        """

        workflow_engine.auto_stage = True

        workflow_engine.gitService.has_staged_files.side_effect = [
            False,
            True,
        ]

        workflow_engine.gitService.list_staged_files.return_value = [
            "main.py",
        ]

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.list_staged_files.assert_called_once()

# ==========================================================
# Dry Run Auto Stage
# ==========================================================


class TestAutoStageDryRun:
    """
    Tests auto-stage behaviour during dry-run mode.
    """

    def test_dry_run_skips_second_validation(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Dry-run skips the second staging verification.
        """

        workflow_engine.auto_stage = True
        workflow_engine.dry_run = True

        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.auto_stage_all.assert_called_once()

        workflow_engine.gitService.list_staged_files.assert_not_called()

# ==========================================================
# Force Commit After Auto Stage
# ==========================================================


class TestForceCommitAfterAutoStage:
    """
    Tests force commit after unsuccessful auto-stage.
    """

    def test_force_commit_returns_after_empty_auto_stage(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Continues when auto-stage produces no files but
        force_commit is enabled.
        """

        workflow_engine.auto_stage = True
        workflow_engine.force_commit = True

        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine.gitService.list_staged_files.return_value = []

        workflow_engine.ensure_staged_changes()

        workflow_engine.gitService.auto_stage_all.assert_called_once()

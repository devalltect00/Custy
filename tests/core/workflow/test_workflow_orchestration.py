# tests/core/workflow/test_workflow_orchestration.py

"""
Unit tests for workflow orchestration in WorkflowEngine.

This module verifies the high-level orchestration methods that
coordinate the complete release workflow, including initialization,
post-release workflow execution, and the overall pipeline.

Coverage:
    - initialize_workflow()
    - execute_post_workflow()
    - run()
"""

from unittest.mock import MagicMock, call, patch

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine


# ==========================================================
# initialize_workflow()
# ==========================================================


class TestInitializeWorkflow:
    """Tests for WorkflowEngine.initialize_workflow()."""

    def test_skip_checks_returns_immediately(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Skip-checks mode exits before any workflow initialization.
        """

        workflow_engine.skip_checks = True

        workflow_engine.branchWorkflowManager.check_transition = MagicMock()
        workflow_engine.branchWorkflowManager.run_initial_workflow = MagicMock()

        with patch("builtins.input", return_value=""):
            workflow_engine.initialize_workflow()

        workflow_engine.branchWorkflowManager.check_transition.assert_not_called()
        workflow_engine.branchWorkflowManager.run_initial_workflow.assert_not_called()

    @patch("app.core.workflow.workflow_engine.BranchWorkflowManager")
    def test_creates_branch_workflow_manager(
        self,
        manager_cls,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        A fresh BranchWorkflowManager is created for initialization.
        """

        manager = MagicMock()
        manager.check_transition.return_value = "CASE_1"

        manager_cls.return_value = manager

        workflow_engine.tag = "v1.2.3"

        with patch("builtins.input", return_value=""):
            workflow_engine.initialize_workflow()

        manager_cls.assert_called_once_with(
            no_debug=workflow_engine.no_debug,
            sync_backup=workflow_engine.sync_backup,
            dry_run=workflow_engine.dry_run,
        )

    @patch("app.core.workflow.workflow_engine.BranchWorkflowManager")
    def test_runs_initial_workflow(
        self,
        manager_cls,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Initializes the detected workflow transition.
        """

        manager = MagicMock()
        manager.check_transition.return_value = "CASE_5"

        manager_cls.return_value = manager

        workflow_engine.tag = "v2.0.0"

        with patch("builtins.input", return_value=""):
            workflow_engine.initialize_workflow()

        manager.check_transition.assert_called_once_with(
            to_tag="v2.0.0",
        )

        manager.run_initial_workflow.assert_called_once_with(
            case="CASE_5",
            to_tag="v2.0.0",
        )


# ==========================================================
# execute_post_workflow()
# ==========================================================


class TestExecutePostWorkflow:
    """Tests for WorkflowEngine.execute_post_workflow()."""

    def test_skip_checks_skips_execution(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Skip-checks bypass post workflow execution.
        """

        workflow_engine.skip_checks = True

        workflow_engine.branchWorkflowManager.run_final_workflow = MagicMock()

        workflow_engine.execute_post_workflow()

        workflow_engine.branchWorkflowManager.run_final_workflow.assert_not_called()

    def test_missing_workflow_case_skips_execution(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Missing workflow context skips execution.
        """

        if hasattr(workflow_engine, "workflow_case"):
            delattr(workflow_engine, "workflow_case")

        workflow_engine.branchWorkflowManager.run_final_workflow = MagicMock()

        workflow_engine.execute_post_workflow()

        workflow_engine.branchWorkflowManager.run_final_workflow.assert_not_called()

    def test_executes_post_workflow(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Successful workflow transition requests user confirmation.
        """

        workflow_engine.workflow_case = "CASE_3"
        workflow_engine.tag = "v1.5.0"

        workflow_engine.branchWorkflowManager.run_final_workflow = MagicMock(
            return_value=True,
        )

        with patch("builtins.input", return_value="") as confirm:
            workflow_engine.execute_post_workflow()

        workflow_engine.branchWorkflowManager.run_final_workflow.assert_called_once_with(
            case="CASE_3",
            to_tag="v1.5.0",
        )

        confirm.assert_called_once()

    def test_no_actions_performed(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        No confirmation requested when no workflow actions occur.
        """

        workflow_engine.workflow_case = "CASE_3"

        workflow_engine.branchWorkflowManager.run_final_workflow = MagicMock(
            return_value=False,
        )

        with patch("builtins.input", return_value="") as confirm:
            workflow_engine.execute_post_workflow()

        confirm.assert_not_called()

    def test_wraps_workflow_errors(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Unexpected workflow failures become ValidationError.
        """

        workflow_engine.workflow_case = "CASE_2"

        workflow_engine.branchWorkflowManager.run_final_workflow = MagicMock(
            side_effect=RuntimeError("boom"),
        )

        with pytest.raises(ValidationError):
            workflow_engine.execute_post_workflow()


# ==========================================================
# run()
# ==========================================================


class TestRun:
    """Tests for WorkflowEngine.run()."""

    def test_executes_complete_pipeline(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Executes every workflow phase exactly once.
        """

        methods = [
            "validate",
            "prepare_version_tag",
            "initialize_workflow",
            "prepare_tag_message",
            "generate_release_artifacts",
            "edit_release_files",
            "validate_edited_files",
            "apply_version_updates",
            "generate_changelog_if_needed",
            "backup_release_files",
            "cleanup_backups",
            "stage_changes",
            "execute_commit_phase",
            "create_tag",
            "push_changes",
            "execute_post_workflow",
        ]

        for method in methods:
            setattr(workflow_engine, method, MagicMock())

        workflow_engine.run()

        for method in methods:
            getattr(workflow_engine, method).assert_called_once()

    def test_executes_pipeline_in_order(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Workflow phases execute in the documented order.
        """

        calls = []

        methods = [
            "validate",
            "prepare_version_tag",
            "initialize_workflow",
            "prepare_tag_message",
            "generate_release_artifacts",
            "edit_release_files",
            "validate_edited_files",
            "apply_version_updates",
            "generate_changelog_if_needed",
            "backup_release_files",
            "cleanup_backups",
            "stage_changes",
            "execute_commit_phase",
            "create_tag",
            "push_changes",
            "execute_post_workflow",
        ]

        for method in methods:
            setattr(
                workflow_engine,
                method,
                MagicMock(side_effect=lambda m=method: calls.append(m)),
            )

        workflow_engine.run()

        assert calls == methods

    def test_stops_when_validation_fails(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Validation failure aborts the workflow immediately.
        """

        workflow_engine.validate = MagicMock(
            side_effect=ValidationError(
                message="Validation failed.",
                hint="Fix validation errors.",
                code="VALIDATION_FAILED",
            )
        )

        workflow_engine.prepare_version_tag = MagicMock()

        with pytest.raises(ValidationError):
            workflow_engine.run()

        workflow_engine.prepare_version_tag.assert_not_called()

    def test_stops_when_commit_phase_fails(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Later phases are not executed after commit failure.
        """

        workflow_engine.validate = MagicMock()
        workflow_engine.prepare_version_tag = MagicMock()
        workflow_engine.initialize_workflow = MagicMock()
        workflow_engine.prepare_tag_message = MagicMock()
        workflow_engine.generate_release_artifacts = MagicMock()
        workflow_engine.edit_release_files = MagicMock()
        workflow_engine.validate_edited_files = MagicMock()
        workflow_engine.apply_version_updates = MagicMock()
        workflow_engine.generate_changelog_if_needed = MagicMock()
        workflow_engine.backup_release_files = MagicMock()
        workflow_engine.cleanup_backups = MagicMock()
        workflow_engine.stage_changes = MagicMock()

        workflow_engine.execute_commit_phase = MagicMock(
            side_effect=ValidationError(
                message="Commit failed.",
                hint="Fix commit.",
                code="COMMIT_FAILED",
            )
        )

        workflow_engine.create_tag = MagicMock()
        workflow_engine.push_changes = MagicMock()
        workflow_engine.execute_post_workflow = MagicMock()

        with pytest.raises(ValidationError):
            workflow_engine.run()

        workflow_engine.create_tag.assert_not_called()
        workflow_engine.push_changes.assert_not_called()
        workflow_engine.execute_post_workflow.assert_not_called()

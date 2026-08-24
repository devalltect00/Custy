# tests/core/workflow/test_workflow_stage_validation.py

"""
Unit tests for WorkflowEngine._validate_staged_result().

This module verifies the final staging validation performed after
automatic staging.

Covered behaviors include:

- Successful staging
- Single staged file
- Multiple staged files
- Empty staged file list
- Force commit override
- Validation failure
"""

from typing import List

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine


# ==========================================================
# Successful Validation
# ==========================================================


class TestValidateStagedResultSuccess:
    """
    Tests successful staging validation.
    """

    def test_returns_when_single_file_is_staged(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        A single staged file satisfies validation.
        """

        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.gitService.list_staged_files.return_value = [
            "main.py",
        ]

        workflow_engine._validate_staged_result()

        workflow_engine.gitService.has_staged_files.assert_called_once()
        workflow_engine.gitService.list_staged_files.assert_called_once()

    def test_returns_when_multiple_files_are_staged(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Multiple staged files satisfy validation.
        """

        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.gitService.list_staged_files.return_value = [
            "README.md",
            "app/main.py",
            "tests/test_main.py",
        ]

        workflow_engine._validate_staged_result()

        workflow_engine.gitService.list_staged_files.assert_called_once()

    def test_returns_when_staged_file_list_is_empty(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        An empty staged-file list still succeeds when Git reports
        staged files exist.
        """

        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.gitService.list_staged_files.return_value = []

        workflow_engine._validate_staged_result()

        workflow_engine.gitService.list_staged_files.assert_called_once()


# ==========================================================
# Force Commit
# ==========================================================


class TestValidateStagedResultForceCommit:
    """
    Tests force-commit behavior.
    """

    def test_force_commit_bypasses_failed_validation(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Force commit skips the final staged-file validation.
        """

        workflow_engine.force_commit = True

        workflow_engine.gitService.has_staged_files.return_value = False

        workflow_engine._validate_staged_result()

        workflow_engine.gitService.list_staged_files.assert_not_called()


# ==========================================================
# Validation Failure
# ==========================================================


class TestValidateStagedResultFailure:
    """
    Tests failure scenarios.
    """

    def test_raises_when_no_files_are_staged(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Raises ValidationError when staging ultimately fails.
        """

        workflow_engine.force_commit = False

        workflow_engine.gitService.has_staged_files.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine._validate_staged_result()

        assert exc.value.code == "STAGING_FAILED"

    @pytest.mark.parametrize(
        "value",
        [
            None,
            False,
        ],
    )
    def test_requires_force_commit_to_be_truthy(
        self,
        workflow_engine: WorkflowEngine,
        value,
    ) -> None:
        """
        Only a truthy force_commit bypasses validation.
        """

        workflow_engine.force_commit = value

        workflow_engine.gitService.has_staged_files.return_value = False

        with pytest.raises(ValidationError):
            workflow_engine._validate_staged_result()

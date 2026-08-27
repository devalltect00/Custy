# tests/core/workflow/test_workflow_commit.py

"""
Unit tests for the commit phase of WorkflowEngine.

This module verifies commit creation, commit message handling,
and interactions with GitService during the commit stage.
"""

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine

# ==========================================================
# Commit Creation
# ==========================================================


class TestCreateCommit:
    """
    Tests commit creation behaviour.
    """

    def test_commit_uses_message_file(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Uses the configured commit message file.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat: initial commit")

        workflow_engine.commit_message_file = commit_file

        workflow_engine.gitService.commit.return_value = True

        workflow_engine.create_commit()

        # workflow_engine.gitService.commit.assert_called_once_with(
        #     commit_file,
        # )

        workflow_engine.gitService.commit.assert_called_once_with(
            message=None,
            message_file=str(commit_file),
        )

    def test_commit_skips_during_dry_run(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Dry-run never invokes GitService.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat")

        workflow_engine.commit_message_file = commit_file
        workflow_engine.dry_run = True

        workflow_engine.create_commit()

        workflow_engine.gitService.commit.assert_not_called()

    def test_commit_requires_message_file(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Missing commit message file raises ValidationError.
        """

        workflow_engine.commit_message_file = None

        with pytest.raises(ValidationError):
            workflow_engine.create_commit()


# ==========================================================
# Commit Result
# ==========================================================


class TestCommitResult:
    """
    Tests commit result handling.
    """

    def test_successful_commit_returns(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Successful commit completes normally.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat")

        workflow_engine.commit_message_file = commit_file

        workflow_engine.gitService.commit.return_value = True

        workflow_engine.create_commit()

        workflow_engine.gitService.commit.assert_called_once()

    def test_failed_commit_raises(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        GitService failure propagates.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat")

        workflow_engine.commit_message_file = commit_file

        workflow_engine.gitService.commit.side_effect = ValidationError(
            message="Commit failed",
            hint="Retry",
            code="COMMIT_FAILED",
        )

        with pytest.raises(ValidationError):
            workflow_engine.create_commit()

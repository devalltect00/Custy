# tests/core/pipeline/steps/validation/test_ensure_commit_message_file_exists_step.py

"""
tests/pipeline/steps/validation/test_ensure_commit_message_file_exists_step.py

Unit tests for EnsureCommitMessageFileExistsStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_commit_message_file_exists_step import (
    EnsureCommitMessageFileExistsStep,
)


class TestEnsureCommitMessageFileExistsStep:
    """
    Tests for EnsureCommitMessageFileExistsStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.ensure_commit_message_file_exists().
        """
        ctx = MagicMock()

        step = EnsureCommitMessageFileExistsStep()

        step.execute(ctx)

        ctx.engine.ensure_commit_message_file_exists.assert_called_once_with()

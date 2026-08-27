# tests/core/pipeline/steps/validation/test_ensure_commit_message_file_step.py

"""
tests/pipeline/steps/validation/test_ensure_commit_message_file_step.py

Unit tests for EnsureCommitMessageFileStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_commit_message_file_step import (
    EnsureCommitMessageFileStep,
)


class TestEnsureCommitMessageFileStep:
    """
    Tests for EnsureCommitMessageFileStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_commit_message_file().
        """
        ctx = MagicMock()

        step = EnsureCommitMessageFileStep()

        step.execute(ctx)

        ctx.engine.ensure_commit_message_file.assert_called_once_with()

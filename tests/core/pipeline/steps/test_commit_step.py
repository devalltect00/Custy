# tests/core/pipeline/steps/test_commit_step.py

"""
tests/pipeline/steps/execution/test_commit_step.py

Unit tests for CommitStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.commit_step import (
    CommitStep,
)


class TestCommitStep:
    """
    Tests for CommitStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.execute_commit_phase().
        """
        ctx = MagicMock()

        step = CommitStep()

        step.execute(ctx)

        ctx.engine.execute_commit_phase.assert_called_once_with()

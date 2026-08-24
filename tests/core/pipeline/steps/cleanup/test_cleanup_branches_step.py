# tests/core/pipeline/steps/cleanup/test_cleanup_branches_step.py

"""
tests/pipeline/steps/backup/test_cleanup_branches_step.py

Unit tests for CleanupBranchesStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.cleanup_branches_step import (
    CleanupBranchesStep,
)


class TestCleanupBranchesStep:
    """
    Tests for CleanupBranchesStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.clean().
        """
        ctx = MagicMock()

        step = CleanupBranchesStep()

        step.execute(ctx)

        ctx.engine.clean.assert_called_once_with()

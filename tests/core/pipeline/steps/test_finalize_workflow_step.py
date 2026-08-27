# tests/core/pipeline/steps/test_finalize_workflow_step.py

"""
tests/pipeline/steps/finalization/test_finalize_workflow_step.py

Unit tests for FinalizeWorkflowStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.finalize_workflow_step import (
    FinalizeWorkflowStep,
)


class TestFinalizeWorkflowStep:
    """
    Tests for FinalizeWorkflowStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.execute_post_workflow().
        """
        ctx = MagicMock()

        step = FinalizeWorkflowStep()

        step.execute(ctx)

        ctx.engine.execute_post_workflow.assert_called_once_with()

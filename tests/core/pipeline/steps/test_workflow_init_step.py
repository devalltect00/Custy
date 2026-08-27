# tests/core/pipeline/steps/test_workflow_init_step.py

"""
tests/pipeline/steps/preparation/test_workflow_init_step.py

Unit tests for WorkflowInitStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.workflow_init_step import (
    WorkflowInitStep,
)


class TestWorkflowInitStep:
    """
    Tests for WorkflowInitStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.initialize_workflow().
        """
        ctx = MagicMock()

        step = WorkflowInitStep()

        step.execute(ctx)

        ctx.engine.initialize_workflow.assert_called_once_with()

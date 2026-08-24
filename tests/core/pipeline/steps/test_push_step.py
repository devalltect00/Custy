# tests/core/pipeline/steps/test_push_step.py

"""
tests/pipeline/steps/execution/test_push_step.py

Unit tests for PushStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.push_step import (
    PushStep,
)


class TestPushStep:
    """
    Tests for PushStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.push_changes().
        """
        ctx = MagicMock()

        step = PushStep()

        step.execute(ctx)

        ctx.engine.push_changes.assert_called_once_with()

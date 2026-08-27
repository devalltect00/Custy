# tests/core/pipeline/steps/test_stage_step.py

"""
tests/pipeline/steps/execution/test_stage_step.py

Unit tests for StageStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.stage_step import (
    StageStep,
)


class TestStageStep:
    """
    Tests for StageStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.stage_changes().
        """
        ctx = MagicMock()

        step = StageStep()

        step.execute(ctx)

        ctx.engine.stage_changes.assert_called_once_with()

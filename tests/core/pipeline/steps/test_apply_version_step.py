# tests/core/pipeline/steps/test_apply_version_step.py

"""
tests/pipeline/steps/generation/test_apply_version_step.py

Unit tests for ApplyVersionStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.apply_version_step import (
    ApplyVersionStep,
)


class TestApplyVersionStep:
    """
    Tests for ApplyVersionStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.apply_version_updates().
        """
        ctx = MagicMock()

        step = ApplyVersionStep()

        step.execute(ctx)

        ctx.engine.apply_version_updates.assert_called_once_with()

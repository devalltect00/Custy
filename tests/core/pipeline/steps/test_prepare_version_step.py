# tests/core/pipeline/steps/test_prepare_version_step.py

"""
tests/pipeline/steps/preparation/test_prepare_version_step.py

Unit tests for PrepareVersionStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.prepare_version_step import (
    PrepareVersionStep,
)


class TestPrepareVersionStep:
    """
    Tests for PrepareVersionStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.prepare_version_tag().
        """
        ctx = MagicMock()

        step = PrepareVersionStep()

        step.execute(ctx)

        ctx.engine.prepare_version_tag.assert_called_once_with()

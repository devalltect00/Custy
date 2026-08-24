# tests/core/pipeline/steps/test_tag_step.py

"""
tests/pipeline/steps/execution/test_tag_step.py

Unit tests for TagStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.tag_step import (
    TagStep,
)


class TestTagStep:
    """
    Tests for TagStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.create_tag().
        """
        ctx = MagicMock()

        step = TagStep()

        step.execute(ctx)

        ctx.engine.create_tag.assert_called_once_with()

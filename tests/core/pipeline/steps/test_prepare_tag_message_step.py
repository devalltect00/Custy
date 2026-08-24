# tests/core/pipeline/steps/test_prepare_tag_message_step.py

"""
tests/pipeline/steps/preparation/test_prepare_tag_message_step.py

Unit tests for PrepareTagMessageStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.prepare_tag_message_step import (
    PrepareTagMessageStep,
)


class TestPrepareTagMessageStep:
    """
    Tests for PrepareTagMessageStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.prepare_tag_message().
        """
        ctx = MagicMock()

        step = PrepareTagMessageStep()

        step.execute(ctx)

        ctx.engine.prepare_tag_message.assert_called_once_with()

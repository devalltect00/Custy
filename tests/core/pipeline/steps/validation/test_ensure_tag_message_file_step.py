# tests/core/pipeline/steps/validation/test_ensure_tag_message_file_step.py

"""
tests/pipeline/steps/validation/test_ensure_tag_message_file_step.py

Unit tests for EnsureTagMessageFileStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_tag_message_file_step import (
    EnsureTagMessageFileStep,
)


class TestEnsureTagMessageFileStep:
    """
    Tests for EnsureTagMessageFileStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_tag_message_file().
        """
        ctx = MagicMock()

        step = EnsureTagMessageFileStep()

        step.execute(ctx)

        ctx.engine.ensure_tag_message_file.assert_called_once_with()

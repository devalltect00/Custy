# tests/core/pipeline/steps/validation/test_ensure_tag_message_file_exists_step.py

"""
tests/pipeline/steps/validation/test_ensure_tag_message_file_exists_step.py

Unit tests for EnsureTagMessageFileExistsStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_tag_message_file_exists_step import (
    EnsureTagMessageFileExistsStep,
)


class TestEnsureTagMessageFileExistsStep:
    """
    Tests for EnsureTagMessageFileExistsStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.ensure_tag_message_file_exists().
        """
        ctx = MagicMock()

        step = EnsureTagMessageFileExistsStep()

        step.execute(ctx)

        ctx.engine.ensure_tag_message_file_exists.assert_called_once_with()

# tests/core/pipeline/steps/test_validate_edited_step.py

"""
tests/pipeline/steps/generation/test_validate_edited_step.py

Unit tests for ValidateEditedStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validate_edited_step import (
    ValidateEditedStep,
)


class TestValidateEditedStep:
    """
    Tests for ValidateEditedStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.validate_edited_files().
        """
        ctx = MagicMock()

        step = ValidateEditedStep()

        step.execute(ctx)

        ctx.engine.validate_edited_files.assert_called_once_with()

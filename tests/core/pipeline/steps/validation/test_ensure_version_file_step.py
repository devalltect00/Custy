# tests/core/pipeline/steps/validation/test_ensure_version_file_step.py

"""
tests/pipeline/steps/validation/test_ensure_version_file_step.py

Unit tests for EnsureVersionFileStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_version_file_step import (
    EnsureVersionFileStep,
)


class TestEnsureVersionFileStep:
    """
    Tests for EnsureVersionFileStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_version_file().
        """
        ctx = MagicMock()

        step = EnsureVersionFileStep()

        step.execute(ctx)

        ctx.engine.ensure_version_file.assert_called_once_with()

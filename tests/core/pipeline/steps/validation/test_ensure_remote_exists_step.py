# tests/core/pipeline/steps/validation/test_ensure_remote_exists_step.py

"""
tests/pipeline/steps/validation/test_ensure_remote_exists_step.py

Unit tests for EnsureRemoteExistsStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_remote_exists_step import (
    EnsureRemoteExistsStep,
)


class TestEnsureRemoteExistsStep:
    """
    Tests for EnsureRemoteExistsStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_remote_exists().
        """
        ctx = MagicMock()

        step = EnsureRemoteExistsStep()

        step.execute(ctx)

        ctx.engine.ensure_remote_exists.assert_called_once_with()

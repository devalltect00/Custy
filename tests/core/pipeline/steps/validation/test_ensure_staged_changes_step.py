# tests/core/pipeline/steps/validation/test_ensure_staged_changes_step.py

"""
tests/pipeline/steps/validation/test_ensure_staged_changes_step.py

Unit tests for EnsureStagedChangesStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_staged_changes_step import (
    EnsureStagedChangesStep,
)


class TestEnsureStagedChangesStep:
    """
    Tests for EnsureStagedChangesStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_staged_changes().
        """
        ctx = MagicMock()

        step = EnsureStagedChangesStep()

        step.execute(ctx)

        ctx.engine.ensure_staged_changes.assert_called_once_with()

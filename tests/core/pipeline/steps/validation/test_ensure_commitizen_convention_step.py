# tests/core/pipeline/steps/validation/test_ensure_commitizen_convention_step.py

"""
tests/pipeline/steps/validation/test_ensure_commitizen_convention_step.py

Unit tests for EnsureCommitizenConventionStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_commitizen_convention_step import (
    EnsureCommitizenConventionStep,
)


class TestEnsureCommitizenConventionStep:
    """
    Tests for EnsureCommitizenConventionStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.ensure_commitizen_convention().
        """
        ctx = MagicMock()

        step = EnsureCommitizenConventionStep()

        step.execute(ctx)

        ctx.engine.ensure_commitizen_convention.assert_called_once_with()

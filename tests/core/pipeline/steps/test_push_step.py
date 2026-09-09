# tests/core/pipeline/steps/test_push_step.py

"""
tests/pipeline/steps/execution/test_push_step.py

Unit tests for PushStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.push_step import (
    PushStep,
)


class TestPushStep:
    """
    Tests for PushStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.push_changes().
        """
        ctx = MagicMock()

        step = PushStep()

        step.execute(ctx)

        ctx.engine.push_changes.assert_called_once_with(include_tag=True)

    def test_execute_can_skip_tag_pushes(self):
        """Commit-only workflows must explicitly suppress tag publication."""

        ctx = MagicMock()

        step = PushStep(include_tag=False)

        step.execute(ctx)

        ctx.engine.push_changes.assert_called_once_with(include_tag=False)

    def test_requires_exclusive_terminal(self):
        """Push prompts must not compete with the live progress display."""

        assert PushStep.requires_exclusive_terminal is True

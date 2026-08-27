# tests/core/pipeline/steps/test_generate_changelog_step.py

"""
tests/pipeline/steps/generation/test_generate_changelog_step.py

Unit tests for GenerateChangelogStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.generate_changelog_step import (
    GenerateChangelogStep,
)


class TestGenerateChangelogStep:
    """
    Tests for GenerateChangelogStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.generate_changelog_if_needed().
        """
        ctx = MagicMock()

        step = GenerateChangelogStep()

        step.execute(ctx)

        ctx.engine.generate_changelog_if_needed.assert_called_once_with()

# tests/core/pipeline/steps/test_edit_files_step.py

"""
tests/pipeline/steps/generation/test_edit_files_step.py

Unit tests for EditFilesStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.edit_files_step import (
    EditFilesStep,
)


class TestEditFilesStep:
    """
    Tests for EditFilesStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.edit_release_files().
        """
        ctx = MagicMock()

        step = EditFilesStep()

        step.execute(ctx)

        ctx.engine.edit_release_files.assert_called_once_with(include_tag=True)

    def test_execute_can_skip_tag_message_editing(self):
        """Commit-only workflows must not request the tag-message editor."""

        ctx = MagicMock()

        step = EditFilesStep(include_tag=False)

        step.execute(ctx)

        ctx.engine.edit_release_files.assert_called_once_with(include_tag=False)

    def test_requires_exclusive_terminal(self):
        """Declares that blocking editors need sole terminal ownership."""

        assert EditFilesStep.requires_exclusive_terminal is True

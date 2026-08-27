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

        ctx.engine.edit_release_files.assert_called_once_with()

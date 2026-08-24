# tests/core/pipeline/steps/cleanup/test_cleanup_backups_step.py

"""
tests/pipeline/steps/backup/test_cleanup_backups_step.py

Unit tests for CleanupBackupsStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.cleanup_backups_step import (
    CleanupBackupsStep,
)


class TestCleanupBackupsStep:
    """
    Tests for CleanupBackupsStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.cleanup_backups().
        """
        ctx = MagicMock()

        step = CleanupBackupsStep()

        step.execute(ctx)

        ctx.engine.cleanup_backups.assert_called_once_with()

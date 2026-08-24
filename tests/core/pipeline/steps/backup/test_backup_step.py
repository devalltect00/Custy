# tests/core/pipeline/steps/backup/test_backup_step.py

"""
tests/pipeline/steps/backup/test_backup_step.py

Unit tests for BackupStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.backup_step import BackupStep


class TestBackupStep:
    """
    Tests for BackupStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.backup_release_files().
        """
        ctx = MagicMock()

        step = BackupStep()

        step.execute(ctx)

        ctx.engine.backup_release_files.assert_called_once_with()

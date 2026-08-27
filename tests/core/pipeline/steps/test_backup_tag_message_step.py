# tests/core/pipeline/steps/test_backup_tag_message_step.py

"""
tests/pipeline/steps/backup/test_backup_tag_message_step.py

Unit tests for BackupTagMessageStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.backup.backup_tag_message_step import (
    BackupTagMessageStep,
)


class TestBackupTagMessageStep:
    """
    Tests for BackupTagMessageStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.backup_tag_message_file().
        """
        ctx = MagicMock()

        step = BackupTagMessageStep()

        step.execute(ctx)

        ctx.engine.backup_tag_message_file.assert_called_once_with()

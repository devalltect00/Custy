# tests/core/pipeline/steps/backup/test_backup_commit_message_step.py

"""
tests/pipeline/steps/backup/test_backup_commit_message_step.py

Unit tests for BackupCommitMessageStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.backup.backup_commit_message_step import (
    BackupCommitMessageStep,
)


class TestBackupCommitMessageStep:
    """
    Tests for BackupCommitMessageStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to
        WorkflowEngine.backup_commit_message_file().
        """
        ctx = MagicMock()

        step = BackupCommitMessageStep()

        step.execute(ctx)

        ctx.engine.backup_commit_message_file.assert_called_once_with()

# tests/integration/test_backup_flow.py

"""
tests/integration/test_backup_flow.py

Integration tests for the backup workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline

from app.core.pipeline.steps.backup_step import (
    BackupStep,
)
from app.core.pipeline.steps.backup.backup_commit_message_step import (
    BackupCommitMessageStep,
)
from app.core.pipeline.steps.backup.backup_tag_message_step import (
    BackupTagMessageStep,
)


class TestBackupFlow:
    """
    Integration tests for the backup workflow.
    """

    def test_backup_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = Pipeline(
            [
                BackupStep(),
                BackupCommitMessageStep(),
                BackupTagMessageStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        ctx.engine.backup_release_files.assert_called_once_with()
        ctx.engine.backup_commit_message_file.assert_called_once_with()
        ctx.engine.backup_tag_message_file.assert_called_once_with()

    def test_backup_pipeline_execution_order(self):
        ctx = MagicMock()

        order = []

        ctx.engine.backup_release_files.side_effect = (
            lambda: order.append("release")
        )
        ctx.engine.backup_commit_message_file.side_effect = (
            lambda: order.append("commit")
        )
        ctx.engine.backup_tag_message_file.side_effect = (
            lambda: order.append("tag")
        )

        Pipeline(
            [
                BackupStep(),
                BackupCommitMessageStep(),
                BackupTagMessageStep(),
            ],
            isVisible=False,
        ).run(ctx)

        assert order == [
            "release",
            "commit",
            "tag",
        ]

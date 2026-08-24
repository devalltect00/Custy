# app/core/pipeline/steps/backup/backup_commit_message_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class BackupCommitMessageStep(BaseStep):
    """
    Step 8.a: Backup Commit Message File

    Creates a backup for the commit message file.

    Responsibilities:
    - Backup commit message file (if exists)
    - Store backup in commit backup directory

    This step is optional and can be included in workflows
    where commit message preservation is required.

    Ensures recovery of commit message content if needed.
    """

    @log_step(label="backup-commit-message")
    def execute(self, ctx):
        ctx.engine.backup_commit_message_file()

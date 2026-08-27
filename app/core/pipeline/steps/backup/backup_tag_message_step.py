# app/core/pipeline/steps/backup/backup_tag_message_step.py

from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class BackupTagMessageStep(BaseStep):
    """
    Step 8.b: Backup Tag Message File

    Resolves and creates a backup for the tag message file.

    Responsibilities:
    - Resolve tag message from file (if applicable)
    - Backup tag message file (if exists)
    - Store backup in tag backup directory

    This step is optional and can be included in workflows
    where tag message preservation is required.

    Ensures recovery of tag message content and consistency
    before tagging operations.
    """

    @log_step(label="backup-tag-message")
    def execute(self, ctx):
        ctx.engine.backup_tag_message_file()

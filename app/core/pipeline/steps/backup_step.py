# app/core/pipeline/steps/backup_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class BackupStep(BaseStep):
    """
    Step 8: Backup Release Files

    Creates backups for:
    - commit message file
    - tag message file

    Ensures recovery is possible if needed.
    """

    @log_step(label="backup-files")
    def execute(self, ctx):
        ctx.engine.backup_release_files()

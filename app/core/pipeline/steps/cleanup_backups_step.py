# app/core/pipeline/steps/cleanup_backups_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class CleanupBackupsStep(BaseStep):
    """
    Step 9: Cleanup Backups

    Removes old backup files based on retention policy.

    Keeps recent backups and deletes outdated ones.
    """

    @log_step(label="cleanup-backups")
    def execute(self, ctx):
        ctx.engine.cleanup_backups()

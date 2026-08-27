# app/core/pipeline/steps/validation/ensure_commit_message_file_exists_step.py

from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class EnsureCommitMessageFileExistsStep(BaseStep):
    """
    Step 0.8: Ensure Commit Message File Exists (Strict)

    Double-check commit message file exists before editing.

    Prevents runtime failure during editor step.
    """

    @log_step(label="validate-commit-message-exists")
    def execute(self, ctx):
        ctx.engine.ensure_commit_message_file_exists()

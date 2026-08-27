# app/core/pipeline/steps/validation/ensure_commit_message_file_step.py

from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class EnsureCommitMessageFileStep(BaseStep):
    """
    Step 0.4: Ensure Commit Message File

    Check commit message template exists.

    Required for commit generation.
    """

    @log_step(label="validate-commit-message-file")
    def execute(self, ctx):
        ctx.engine.ensure_commit_message_file()

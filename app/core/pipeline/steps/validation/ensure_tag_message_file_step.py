# app/core/pipeline/steps/validation/ensure_tag_message_file_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureTagMessageFileStep(BaseStep):
    """
    Step 0.5: Ensure Tag Message File

    Check tag message template exists.

    Required for tagging step.
    """

    @log_step(label="validate-tag-message-file")
    def execute(self, ctx):
        ctx.engine.ensure_tag_message_file()

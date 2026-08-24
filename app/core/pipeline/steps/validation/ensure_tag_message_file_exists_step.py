# app/core/pipeline/steps/validation/ensure_tag_message_file_exists_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureTagMessageFileExistsStep(BaseStep):
    """
    Step 0.9: Ensure Tag Message File Exists (Strict)

    Double-check tag message file exists before editing.

    Prevents runtime failure during tag step.
    """

    @log_step(label="validate-tag-message-exists")
    def execute(self, ctx):
        ctx.engine.ensure_tag_message_file_exists()

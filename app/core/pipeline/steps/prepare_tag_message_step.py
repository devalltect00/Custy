# app/core/pipeline/steps/prepare_tag_message_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class PrepareTagMessageStep(BaseStep):
    """
    Step 3: Prepare Tag Message

    Resolves tag message source:

    Priority:
    1. CLI input
    2. File
    3. Default template

    Ensures tag message is ready before tagging.
    """

    @log_step(label="prepare-tag-message")
    def execute(self, ctx):
        ctx.engine.prepare_tag_message()

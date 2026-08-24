# app/core/pipeline/steps/tag_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class TagStep(BaseStep):
    """
    Step 12: Create Tag

    Creates annotated Git tag.

    Uses:
    - tag value
    - tag message (inline or file)

    Skips if tagging is disabled.
    """

    @log_step(label="create-tag")
    def execute(self, ctx):
        ctx.engine.create_tag()

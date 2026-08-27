# app/core/pipeline/steps/push_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class PushStep(BaseStep):
    """
    Step 13: Push Changes

    Pushes:
    - commit (HEAD)
    - tag (if applicable)

    Supports:
    - multiple remotes
    - backup remotes
    """

    @log_step(label="push")
    def execute(self, ctx):
        ctx.engine.push_changes()

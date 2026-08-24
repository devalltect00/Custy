# app/core/pipeline/steps/validation/ensure_remote_exists_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureRemoteExistsStep(BaseStep):
    """
    Step 0.2: Ensure Remote Exists

    Verify that required Git remote (e.g. origin) exists.

    Prevents push failures later.
    """

    @log_step(label="validtion-remote-check")
    def execute(self, ctx):
        ctx.engine.ensure_remote_exists()

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

    The live pipeline display is suspended because Git may request credentials
    from the terminal. Keeping the terminal exclusive makes authentication
    prompts visible instead of allowing the progress bar to redraw over them.
    """

    requires_exclusive_terminal: bool = True

    @log_step(label="push")
    def execute(self, ctx):
        ctx.engine.push_changes()

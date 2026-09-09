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

    def __init__(self, *, include_tag: bool = True) -> None:
        """Configure whether this step may push a resolved release tag.

        Args:
            include_tag: Push an eligible tag after the branch. Development-only
                commit workflows disable this behavior.
        """

        self.include_tag = include_tag

    @log_step(label="push")
    def execute(self, ctx):
        ctx.engine.push_changes(include_tag=self.include_tag)

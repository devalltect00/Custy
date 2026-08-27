# app/core/pipeline/steps/stage_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class StageStep(BaseStep):
    """
    Step 10: Stage Changes

    Stages files before commit.

    Behavior depends on stage mode:
    - all
    - update
    - manual

    Ensures files are ready for commit.
    """

    @log_step(label="stage-changes")
    def execute(self, ctx):
        ctx.engine.stage_changes()

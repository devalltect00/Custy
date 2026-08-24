# app/core/pipeline/steps/commit_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class CommitStep(BaseStep):
    """
    Step 11: Commit Changes

    Creates commit using selected strategy:

    - Default commit
    - Commitizen (if configured)

    Handles validation and commit creation.
    """

    @log_step(label="commit")
    def execute(self, ctx):
        ctx.engine.execute_commit_phase()

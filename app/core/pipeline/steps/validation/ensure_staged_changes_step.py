# app/core/pipeline/steps/validation/ensure_staged_changes_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureStagedChangesStep(BaseStep):
    """
    Step 0.6: Ensure Staged Changes

    Ensure there are staged files before commit.

    Supports:
    - auto-stage
    - force commit
    - dry-run (non-blocking)
    """

    @log_step(label="validate-staged-changes")
    def execute(self, ctx):
        ctx.engine.ensure_staged_changes()

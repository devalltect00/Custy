# app/core/pipeline/steps/validation/ensure_commitizen_convention_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureCommitizenConventionStep(BaseStep):
    """
    Step 0.7: Ensure Commitizen Convention

    Validate commit message format using Commitizen rules.

    Ensures consistency in commit messages.
    """

    @log_step(label="validate-commitizen-check")
    def execute(self, ctx):
        ctx.engine.ensure_commitizen_convention()

# app/core/pipeline/steps/validate_edited_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class ValidateEditedStep(BaseStep):
    """
    Step 6: Validate Edited Files

    Validates user-edited commit message.

    Responsibilities:
    - Ensure commit format is valid
    - Determine if tagging is allowed

    May influence tagging behavior.
    """

    @log_step(label="validate-edited")
    def execute(self, ctx):
        ctx.engine.validate_edited_files()

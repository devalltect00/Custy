# app/core/pipeline/steps/validation/ensure_version_file_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureVersionFileStep(BaseStep):
    """
    Step 0.3: Ensure Version File

    Ensure version file exists and is accessible.

    Required for version updates.
    """

    @log_step(label="validate-version-file")
    def execute(self, ctx):
        ctx.engine.ensure_version_file()

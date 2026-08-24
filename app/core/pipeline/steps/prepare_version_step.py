# app/core/pipeline/steps/prepare_version_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class PrepareVersionStep(BaseStep):
    """
    Step 1: Prepare Version Tag

    Determines the next version tag.

    Sources:
    - CLI input (--tag)
    - Strategy (semver, pep440, commitizen, etc.)

    Result:
    - ctx.engine.tag is set
    """

    @log_step(label="prepare-version")
    def execute(self, ctx):
        ctx.engine.prepare_version_tag()

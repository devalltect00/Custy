# app/core/pipeline/steps/apply_version_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class ApplyVersionStep(BaseStep):
    """
    Step 7.1: Apply Version Updates

    Applies version changes to project:

    - Update version file (__version__.py)
    - Update project configs (pyproject.toml, etc.)
    - Generate changelog (if applicable)

    Prepares repo state before commit.
    """

    @log_step(label="apply-version")
    def execute(self, ctx):
        ctx.engine.apply_version_updates()

# app/core/pipeline/steps/generate_artifacts_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class GenerateArtifactsStep(BaseStep):
    """
    Step 4: Generate Release Artifacts

    Generates:
    - commit message template
    - tag message template

    Based on version and commit history.

    Uses ReleaseNoteBuilder internally.
    """

    @log_step(label="generate-artifacts")
    def execute(self, ctx):
        ctx.engine.generate_release_artifacts()

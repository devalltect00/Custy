# app/core/pipeline/steps/validation/ensure_commit_validation_provider_step.py

"""Pipeline preflight for commit-message validation providers."""

from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class EnsureCommitValidationProviderStep(BaseStep):
    """Resolve optional commit validation before mutating workflow steps."""

    @log_step(label="validate-commit-provider")
    def execute(self, ctx) -> None:
        """Delegate provider discovery and strictness checks to the engine."""

        ctx.engine.ensure_commit_validation_provider()

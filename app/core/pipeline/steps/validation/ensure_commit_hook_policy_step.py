# app/core/pipeline/steps/validation/ensure_commit_hook_policy_step.py

"""Pipeline preflight for safe Git commit-hook execution."""

from app.core.pipeline.decorators.log_step import log_step
from app.core.pipeline.steps.base_step import BaseStep


class EnsureCommitHookPolicyStep(BaseStep):
    """Resolve native or direct pre-commit behavior before file mutations."""

    @log_step(label="validate-commit-hooks")
    def execute(self, ctx) -> None:
        """Delegate cross-platform hook inspection to the workflow engine."""

        ctx.engine.ensure_commit_hook_policy()

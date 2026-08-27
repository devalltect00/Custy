# app/core/pipeline/steps/cleanup_branches_step.py

"""
Pipeline step for Git branch cleanup.

This step executes the configured branch cleanup engine as part of the
Custy pipeline.

The step intentionally contains no cleanup business logic. All cleanup
behavior is delegated to the engine attached to the pipeline context.
"""

from app.core.pipeline.context import GitContext
from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep

# from app.core.cleanup.handle_cleanup_branches import handleCleanupBranches


class CleanupBranchesStep(BaseStep):
    """
    Pipeline step for branch cleanup.

    -----
    (optionally): Cleanup Git branches.
    -----

    This step delegates execution to the cleanup engine stored in the
    pipeline context.

    Business logic is intentionally implemented outside the pipeline step
    to keep pipeline orchestration independent from cleanup
    implementation details.
    """

    @log_step(label="cleanup-branches")
    def execute(
        self,
        ctx: GitContext,
    ) -> None:
        """
        Execute the branch cleanup engine.

        Parameters
        ----------
        ctx:
            Pipeline execution context.
        """
        # handler = handleCleanupBranches(ctx.engine.config)
        # handler.clean()
        engine = ctx.engine
        engine.clean()

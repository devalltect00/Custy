# app/core/pipeline/steps/validation/ensure_git_repo_step.py

from app.core.pipeline.steps.base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class EnsureGitRepoStep(BaseStep):
    """
    Step 0.1: Ensure Git Repository

    Check that current directory is a valid Git repository.

    Prevents running workflow outside Git project.
    """

    @log_step(label="validate-git-repo")
    def execute(self, ctx):
        ctx.engine.ensure_git_repo()

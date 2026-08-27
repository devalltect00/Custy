# app/core/pipeline/steps/finalize_workflow_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class FinalizeWorkflowStep(BaseStep):
    """
    Step 14: Finalize Workflow

    Executes post-release workflow actions:

    - branch transitions (release → main)
    - cleanup temporary branches
    - finalize workflow state

    Last step of the pipeline.
    """

    @log_step(label="finalize-workflow")
    def execute(self, ctx):
        ctx.engine.execute_post_workflow()

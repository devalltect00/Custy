# app/core/pipeline/steps/workflow_init_step.py

from app.core.pipeline.decorators.log_step import log_step

from .base_step import BaseStep


class WorkflowInitStep(BaseStep):
    """
    Step 2: Initialize Workflow

    Handles branch workflow transitions.

    Responsibilities:
    - Detect workflow case (e.g., develop → release)
    - Validate transition
    - Execute initial workflow actions

    Ensures correct Git workflow flow before changes.

    The step owns the terminal while it waits for confirmation so the live
    pipeline display cannot hide or overwrite the prompt.
    """

    requires_exclusive_terminal: bool = True

    @log_step(label="workflow-init")
    def execute(self, ctx):
        ctx.engine.initialize_workflow()

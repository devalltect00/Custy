# app/core/pipeline/steps/workflow_init_step.py

from .base_step import BaseStep
from app.core.pipeline.decorators.log_step import log_step


class WorkflowInitStep(BaseStep):
    """
    Step 2: Initialize Workflow

    Handles branch workflow transitions.

    Responsibilities:
    - Detect workflow case (e.g., develop → release)
    - Validate transition
    - Execute initial workflow actions

    Ensures correct Git workflow flow before changes.
    """

    @log_step(label="workflow-init")
    def execute(self, ctx):
        ctx.engine.initialize_workflow()

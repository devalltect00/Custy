# tests/integration/test_dev_flow.py

"""
tests/integration/test_dev_flow.py

Integration tests for the development workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.commit_step import (
    CommitStep,
)
from app.core.pipeline.steps.prepare_version_step import (
    PrepareVersionStep,
)
from app.core.pipeline.steps.push_step import (
    PushStep,
)
from app.core.pipeline.steps.stage_step import (
    StageStep,
)
from app.core.pipeline.steps.workflow_init_step import (
    WorkflowInitStep,
)


class TestDevFlow:
    """
    Integration tests for the development workflow.
    """

    def test_dev_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = Pipeline(
            [
                PrepareVersionStep(),
                WorkflowInitStep(),
                StageStep(),
                CommitStep(),
                PushStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        ctx.engine.prepare_version_tag.assert_called_once_with()
        ctx.engine.initialize_workflow.assert_called_once_with()

        ctx.engine.stage_changes.assert_called_once_with()
        ctx.engine.execute_commit_phase.assert_called_once_with()
        ctx.engine.push_changes.assert_called_once_with()

        # Development flow should not perform release-only actions.
        ctx.engine.generate_release_artifacts.assert_not_called()
        ctx.engine.generate_changelog_if_needed.assert_not_called()
        ctx.engine.create_tag.assert_not_called()
        ctx.engine.execute_post_workflow.assert_not_called()

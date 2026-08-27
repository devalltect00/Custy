# tests/integration/test_cleanup_flow.py

"""
tests/integration/test_cleanup_flow.py

Integration tests for the cleanup workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.cleanup_backups_step import (
    CleanupBackupsStep,
)
from app.core.pipeline.steps.cleanup_branches_step import (
    CleanupBranchesStep,
)


class TestCleanupFlow:
    """
    Integration tests for the cleanup workflow.
    """

    def test_cleanup_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = Pipeline(
            [
                CleanupBackupsStep(),
                CleanupBranchesStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        ctx.engine.cleanup_backups.assert_called_once_with()
        ctx.engine.clean.assert_called_once_with()

    def test_cleanup_pipeline_execution_order(self):
        ctx = MagicMock()

        order = []

        ctx.engine.cleanup_backups.side_effect = lambda: order.append("cleanup_backups")

        ctx.engine.clean.side_effect = lambda: order.append("cleanup_branches")

        Pipeline(
            [
                CleanupBackupsStep(),
                CleanupBranchesStep(),
            ],
            isVisible=False,
        ).run(ctx)

        assert order == [
            "cleanup_backups",
            "cleanup_branches",
        ]

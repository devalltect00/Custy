# tests/integration/test_release_flow.py

"""
tests/integration/test_release_flow.py

Integration tests for the release workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.apply_version_step import ApplyVersionStep
from app.core.pipeline.steps.backup_step import BackupStep
from app.core.pipeline.steps.commit_step import CommitStep
from app.core.pipeline.steps.edit_files_step import EditFilesStep
from app.core.pipeline.steps.finalize_workflow_step import (
    FinalizeWorkflowStep,
)
from app.core.pipeline.steps.generate_artifacts_step import GenerateArtifactsStep
from app.core.pipeline.steps.generate_changelog_step import GenerateChangelogStep
from app.core.pipeline.steps.prepare_tag_message_step import PrepareTagMessageStep
from app.core.pipeline.steps.prepare_version_step import PrepareVersionStep
from app.core.pipeline.steps.push_step import PushStep
from app.core.pipeline.steps.stage_step import StageStep
from app.core.pipeline.steps.tag_step import TagStep
from app.core.pipeline.steps.validate_edited_step import ValidateEditedStep
from app.core.pipeline.steps.workflow_init_step import WorkflowInitStep


class TestReleaseFlow:
    """
    Integration tests for the complete release pipeline.
    """

    def test_release_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = Pipeline(
            [
                PrepareVersionStep(),
                WorkflowInitStep(),
                PrepareTagMessageStep(),
                GenerateArtifactsStep(),
                EditFilesStep(),
                ValidateEditedStep(),
                ApplyVersionStep(),
                GenerateChangelogStep(),
                BackupStep(),
                StageStep(),
                CommitStep(),
                TagStep(),
                PushStep(),
                FinalizeWorkflowStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        ctx.engine.prepare_version_tag.assert_called_once_with()
        ctx.engine.initialize_workflow.assert_called_once_with()
        ctx.engine.prepare_tag_message.assert_called_once_with()

        ctx.engine.generate_release_artifacts.assert_called_once_with()
        ctx.engine.edit_release_files.assert_called_once_with()
        ctx.engine.validate_edited_files.assert_called_once_with()

        ctx.engine.apply_version_updates.assert_called_once_with()
        ctx.engine.generate_changelog_if_needed.assert_called_once_with()

        ctx.engine.backup_release_files.assert_called_once_with()

        ctx.engine.stage_changes.assert_called_once_with()
        ctx.engine.execute_commit_phase.assert_called_once_with()
        ctx.engine.create_tag.assert_called_once_with()
        ctx.engine.push_changes.assert_called_once_with()

        ctx.engine.execute_post_workflow.assert_called_once_with()

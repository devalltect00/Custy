# tests/integration/test_workflow_flow.py

"""
tests/integration/test_workflow_flow.py

Integration tests for complete workflow orchestration.

These tests verify that the workflow can be resolved, built,
and executed using a supplied WorkflowEngine-like object.
"""

from unittest.mock import MagicMock

from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.command_resolver import CommandResolver


class TestWorkflowFlow:
    """
    End-to-end orchestration tests.
    """

    @staticmethod
    def _engine():
        """
        Create a fully mocked workflow engine.

        Using a mocked engine keeps these tests focused on
        orchestration rather than WorkflowEngine internals.
        """
        return MagicMock()

    def test_release_workflow(self):
        engine = self._engine()

        ctx = MagicMock()
        ctx.engine = engine

        pipeline = PipelineBuilder(
            isVisible=False,
        ).build(CommandResolver().resolve(["release"]))

        pipeline.run(ctx)

        #
        # Validation
        #
        engine.ensure_git_repo.assert_called_once()
        engine.ensure_remote_exists.assert_called_once()
        engine.ensure_version_file.assert_called_once()
        engine.ensure_staged_changes.assert_called_once()
        engine.ensure_commit_validation_provider.assert_called_once()
        engine.ensure_commit_message_file.assert_called_once()
        engine.ensure_commit_message_file_exists.assert_called_once()
        engine.ensure_tag_message_file.assert_called_once()
        engine.ensure_tag_message_file_exists.assert_called_once()

        #
        # Preparation
        #
        engine.prepare_version_tag.assert_called_once()
        engine.initialize_workflow.assert_called_once()
        engine.prepare_tag_message.assert_called_once()

        #
        # Generation
        #
        engine.generate_release_artifacts.assert_called_once()
        engine.edit_release_files.assert_called_once()
        engine.validate_edited_files.assert_called_once()
        engine.apply_version_updates.assert_called_once()
        engine.generate_changelog_if_needed.assert_called_once()

        #
        # Backup
        #
        engine.backup_commit_message_file.assert_called_once()
        engine.backup_tag_message_file.assert_called_once()
        engine.cleanup_backups.assert_called_once()

        #
        # Execution
        #
        engine.stage_changes.assert_called_once()
        engine.execute_commit_phase.assert_called_once()
        engine.create_tag.assert_called_once()
        engine.push_changes.assert_called_once()

    def test_validate_workflow(self):
        engine = self._engine()

        ctx = MagicMock()
        ctx.engine = engine

        pipeline = PipelineBuilder(
            isVisible=False,
        ).build(CommandResolver().resolve(["validate"]))

        pipeline.run(ctx)

        engine.ensure_git_repo.assert_called_once()
        engine.ensure_remote_exists.assert_called_once()
        engine.ensure_version_file.assert_called_once()
        engine.ensure_staged_changes.assert_called_once()
        engine.ensure_commit_validation_provider.assert_called_once()
        engine.ensure_commit_message_file.assert_called_once()
        engine.ensure_commit_message_file_exists.assert_called_once()
        engine.ensure_tag_message_file.assert_called_once()
        engine.ensure_tag_message_file_exists.assert_called_once()

        #
        # Validate profile should stop here.
        #
        engine.prepare_version_tag.assert_not_called()
        engine.stage_changes.assert_not_called()
        engine.execute_commit_phase.assert_not_called()
        engine.create_tag.assert_not_called()
        engine.push_changes.assert_not_called()

    def test_dev_workflow(self):
        engine = self._engine()

        ctx = MagicMock()
        ctx.engine = engine

        pipeline = PipelineBuilder(
            isVisible=False,
        ).build(CommandResolver().resolve(["dev"]))

        pipeline.run(ctx)

        #
        # Dev-specific flow
        #
        engine.ensure_git_repo.assert_called_once()

        engine.prepare_version_tag.assert_called_once()
        engine.initialize_workflow.assert_called_once()

        engine.generate_release_artifacts.assert_called_once()
        engine.edit_release_files.assert_called_once()
        engine.validate_edited_files.assert_called_once()
        engine.generate_changelog_if_needed.assert_called_once()

        engine.backup_commit_message_file.assert_called_once()
        engine.cleanup_backups.assert_called_once()

        engine.stage_changes.assert_called_once()
        engine.execute_commit_phase.assert_called_once()
        engine.push_changes.assert_called_once()

        #
        # Dev profile should not create tags.
        #
        engine.create_tag.assert_not_called()
        engine.backup_tag_message_file.assert_not_called()

# tests/integration/test_dev_flow.py

"""
tests/integration/test_dev_flow.py

Integration tests for the development workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.command_resolver import CommandResolver


class TestDevFlow:
    """
    Integration tests for the development workflow.
    """

    def test_dev_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = PipelineBuilder(isVisible=False).build(
            CommandResolver().resolve(["dev"])
        )

        pipeline.run(ctx)

        ctx.engine.ensure_git_repo.assert_called_once_with()
        ctx.engine.ensure_commit_validation_provider.assert_called_once_with()
        ctx.engine.ensure_commit_hook_policy.assert_called_once_with()
        ctx.engine.ensure_commit_message_file.assert_called_once_with()
        ctx.engine.ensure_commit_message_file_exists.assert_called_once_with()
        ctx.engine.ensure_remote_exists.assert_called_once_with()
        ctx.engine.edit_release_files.assert_called_once_with(include_tag=False)
        ctx.engine.validate_edited_files.assert_called_once_with()
        ctx.engine.backup_commit_message_file.assert_called_once_with()
        ctx.engine.cleanup_backups.assert_called_once_with()
        ctx.engine.stage_changes.assert_called_once_with()
        ctx.engine.execute_commit_phase.assert_called_once_with()
        ctx.engine.push_changes.assert_called_once_with(include_tag=False)

        # Development flow should not perform release-only actions.
        ctx.engine.prepare_version_tag.assert_not_called()
        ctx.engine.initialize_workflow.assert_not_called()
        ctx.engine.generate_release_artifacts.assert_not_called()
        ctx.engine.generate_changelog_if_needed.assert_not_called()
        ctx.engine.apply_version_updates.assert_not_called()
        ctx.engine.create_tag.assert_not_called()
        ctx.engine.backup_tag_message_file.assert_not_called()
        ctx.engine.execute_post_workflow.assert_not_called()

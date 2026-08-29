# tests/integration/test_validate_flow.py

"""
tests/integration/test_validate_flow.py

Integration tests for the validation workflow.
"""

from unittest.mock import MagicMock

from app.core.pipeline.pipeline import Pipeline
from app.core.pipeline.steps.validation.ensure_commit_message_file_exists_step import (
    EnsureCommitMessageFileExistsStep,
)
from app.core.pipeline.steps.validation.ensure_commit_message_file_step import (
    EnsureCommitMessageFileStep,
)
from app.core.pipeline.steps.validation.ensure_commit_validation_provider_step import (
    EnsureCommitValidationProviderStep,
)
from app.core.pipeline.steps.validation.ensure_git_repo_step import (
    EnsureGitRepoStep,
)
from app.core.pipeline.steps.validation.ensure_remote_exists_step import (
    EnsureRemoteExistsStep,
)
from app.core.pipeline.steps.validation.ensure_staged_changes_step import (
    EnsureStagedChangesStep,
)
from app.core.pipeline.steps.validation.ensure_tag_message_file_exists_step import (
    EnsureTagMessageFileExistsStep,
)
from app.core.pipeline.steps.validation.ensure_tag_message_file_step import (
    EnsureTagMessageFileStep,
)
from app.core.pipeline.steps.validation.ensure_version_file_step import (
    EnsureVersionFileStep,
)


class TestValidateFlow:
    """
    Integration tests for the complete validation pipeline.
    """

    def test_validation_pipeline_executes_all_steps(self):
        ctx = MagicMock()

        pipeline = Pipeline(
            [
                EnsureGitRepoStep(),
                EnsureRemoteExistsStep(),
                EnsureVersionFileStep(),
                EnsureCommitMessageFileStep(),
                EnsureTagMessageFileStep(),
                EnsureStagedChangesStep(),
                EnsureCommitValidationProviderStep(),
                EnsureCommitMessageFileExistsStep(),
                EnsureTagMessageFileExistsStep(),
            ],
            isVisible=False,
        )

        pipeline.run(ctx)

        ctx.engine.ensure_git_repo.assert_called_once_with()
        ctx.engine.ensure_remote_exists.assert_called_once_with()
        ctx.engine.ensure_version_file.assert_called_once_with()
        ctx.engine.ensure_commit_message_file.assert_called_once_with()
        ctx.engine.ensure_tag_message_file.assert_called_once_with()
        ctx.engine.ensure_staged_changes.assert_called_once_with()
        ctx.engine.ensure_commit_validation_provider.assert_called_once_with()
        ctx.engine.ensure_commit_message_file_exists.assert_called_once_with()
        ctx.engine.ensure_tag_message_file_exists.assert_called_once_with()

# tests/core/pipeline/steps/validation/test_ensure_git_repo_step.py

"""
tests/pipeline/steps/validation/test_ensure_git_repo_step.py

Unit tests for EnsureGitRepoStep.
"""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_git_repo_step import (
    EnsureGitRepoStep,
)


class TestEnsureGitRepoStep:
    """
    Tests for EnsureGitRepoStep.
    """

    def test_execute_calls_engine(self):
        """
        execute() should delegate to WorkflowEngine.ensure_git_repo().
        """
        ctx = MagicMock()

        step = EnsureGitRepoStep()

        step.execute(ctx)

        ctx.engine.ensure_git_repo.assert_called_once_with()

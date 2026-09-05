# tests/core/pipeline/steps/validation/test_ensure_commit_hook_policy_step.py

"""Tests for the commit-hook policy validation step."""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_commit_hook_policy_step import (
    EnsureCommitHookPolicyStep,
)


def test_delegates_hook_policy_preflight() -> None:
    """The pipeline step resolves hooks before release file mutations."""

    context = MagicMock()

    EnsureCommitHookPolicyStep().execute(context)

    context.engine.ensure_commit_hook_policy.assert_called_once_with()

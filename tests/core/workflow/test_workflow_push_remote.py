# tests/core/workflow/test_workflow_push_remote.py

"""
Unit tests for WorkflowEngine._push_to_remotes().

This module verifies pushing commits and tags to Git remotes,
including dry-run and failure handling.
"""

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.shared import GitOperationError
from app.core.workflow.workflow_engine import WorkflowEngine


class TestPushDryRun:
    """
    Tests dry-run push behavior.
    """

    def test_dry_run_commit_and_tag(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.dry_run = True
        workflow_engine.tag = "v1.0.0"

        workflow_engine._push_to_remotes(
            ["origin"],
            label="main",
        )

        workflow_engine.gitService.push.assert_not_called()

        workflow_engine.gitService.push_tag.assert_not_called()


class TestPushCommit:
    """
    Tests commit pushes.
    """

    def test_push_commit_only_when_tag_skipped(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.skip_tag = True
        workflow_engine.tag = "v1.0.0"

        workflow_engine._push_to_remotes(
            ["origin"],
            label="main",
        )

        workflow_engine.gitService.push.assert_called_once()

        workflow_engine.gitService.push_tag.assert_not_called()

    def test_push_commit_only_when_tag_is_excluded(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """An explicitly commit-only push must ignore a resolved tag."""

        workflow_engine.tag = "v2.1.1"

        workflow_engine._push_to_remotes(
            ["origin"],
            label="main",
            include_tag=False,
        )

        workflow_engine.gitService.push.assert_called_once_with(
            remote="origin",
            ref="HEAD",
        )
        workflow_engine.gitService.push_tag.assert_not_called()


class TestPushCommitAndTag:
    """
    Tests commit and tag pushes.
    """

    def test_pushes_commit_and_tag(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.tag = "v1.0.0"

        workflow_engine._push_to_remotes(
            ["origin"],
            label="main",
        )

        workflow_engine.gitService.push.assert_called_once_with(
            remote="origin",
            ref="HEAD",
        )

        workflow_engine.gitService.push_tag.assert_called_once_with(
            remote="origin",
            tag="v1.0.0",
        )


class TestPushFailures:
    """
    Tests push failure handling.
    """

    def test_wraps_commit_push_failure(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.gitService.push.side_effect = RuntimeError("boom")

        with pytest.raises(ValidationError) as exc:
            workflow_engine._push_to_remotes(
                ["origin"],
                label="main",
            )

        assert exc.value.code == "PUSH_FAILED"

    def test_preserves_authentication_diagnostics(
        self,
        workflow_engine: WorkflowEngine,
    ):
        """Container authentication errors keep Git's actionable detail."""

        workflow_engine.gitService.push.side_effect = GitOperationError(
            "Git push failed",
            operation="push",
            returncode=128,
            stderr=(
                "fatal: could not read Username for 'https://github.com': "
                "terminal prompts disabled"
            ),
        )

        with pytest.raises(ValidationError) as exc_info:
            workflow_engine._push_to_remotes(
                ["origin"],
                label="main",
            )

        error = exc_info.value
        assert error.code == "PUSH_FAILED"
        assert "current execution environment" in error.hint
        assert error.context["exit_code"] == 128
        assert "could not read Username" in error.context["detail"]

    def test_wraps_tag_push_failure(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.tag = "v1.0.0"

        workflow_engine.gitService.push_tag.side_effect = RuntimeError("network")

        with pytest.raises(ValidationError) as exc:
            workflow_engine._push_to_remotes(
                ["origin"],
                label="main",
            )

        assert exc.value.code == "PUSH_TAG_FAILED"

        assert exc.value.context["tag"] == "v1.0.0"

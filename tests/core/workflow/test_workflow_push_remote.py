# tests/core/workflow/test_workflow_push_remote.py

"""
Unit tests for WorkflowEngine._push_to_remotes().

This module verifies pushing commits and tags to Git remotes,
including dry-run and failure handling.
"""


import pytest

from app.core.workflow.workflow_engine import WorkflowEngine
from app.core.exceptions.validation_error import ValidationError


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

    def test_wraps_tag_push_failure(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.tag = "v1.0.0"

        workflow_engine.gitService.push_tag.side_effect = RuntimeError(
            "network"
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine._push_to_remotes(
                ["origin"],
                label="main",
            )

        assert exc.value.code == "PUSH_TAG_FAILED"

        assert exc.value.context["tag"] == "v1.0.0"

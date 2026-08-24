# tests/core/workflow/test_workflow_tag.py

"""
Unit tests for Git tag creation in WorkflowEngine.

This module verifies annotated tag creation, tag message resolution,
dry-run behavior, validation, and Git service error handling.

Covered behaviors include:

- Skip-tag mode
- Missing tag validation
- Inline tag message precedence
- Tag message file usage
- Tag name fallback
- Dry-run execution
- Git service failures
"""


from pathlib import Path

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine


# ==========================================================
# Skip Tag
# ==========================================================


class TestSkipTag:
    """
    Tests skip-tag behavior.
    """

    def test_returns_when_skip_tag_enabled(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Tag creation is skipped when skip_tag is enabled.
        """

        workflow_engine.skip_tag = True
        workflow_engine.tag = "v1.0.0"

        workflow_engine.create_tag()

        workflow_engine.gitService.tag.assert_not_called()


# ==========================================================
# Tag Validation
# ==========================================================


class TestTagValidation:
    """
    Tests tag validation before creation.
    """

    def test_raises_when_tag_missing(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        A version tag must exist before creating a Git tag.
        """

        workflow_engine.tag = ""

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_tag()

        assert exc.value.code == "TAG_MISSING"

        workflow_engine.gitService.tag.assert_not_called()


# ==========================================================
# Tag Message Resolution
# ==========================================================


class TestTagMessageResolution:
    """
    Tests tag message selection priority.
    """

    def test_prefers_inline_tag_message(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Inline tag messages take precedence.
        """

        workflow_engine.tag = "v1.2.3"
        workflow_engine.tag_message_input = "Release notes"

        workflow_engine.create_tag()

        workflow_engine.gitService.tag.assert_called_once_with(
            tag="v1.2.3",
            message="Release notes",
            message_file=None,
        )

    def test_uses_tag_message_file(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """
        Uses the configured tag message file.
        """

        tag_file = tmp_path / "tag-message.txt"
        tag_file.write_text("release")

        workflow_engine.tag = "v2.0.0"
        workflow_engine.tag_message_file = tag_file

        workflow_engine.create_tag()

        workflow_engine.gitService.tag.assert_called_once_with(
            tag="v2.0.0",
            message=None,
            message_file=str(tag_file),
        )

    def test_falls_back_to_tag_name(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Falls back to using the tag itself as the annotation.
        """

        workflow_engine.tag = "v3.0.0"

        workflow_engine.create_tag()

        workflow_engine.gitService.tag.assert_called_once_with(
            tag="v3.0.0",
            message="v3.0.0",
            message_file=None,
        )


# ==========================================================
# Dry Run
# ==========================================================


class TestTagDryRun:
    """
    Tests dry-run behavior.
    """

    def test_dry_run_does_not_create_tag(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Dry-run prevents GitService.tag() from executing.
        """

        workflow_engine.tag = "v4.0.0"
        workflow_engine.dry_run = True

        workflow_engine.create_tag()

        workflow_engine.gitService.tag.assert_not_called()


# ==========================================================
# Tag Failure Handling
# ==========================================================


class TestTagFailure:
    """
    Tests exception handling during tag creation.
    """

    def test_wraps_git_service_exception(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Unexpected GitService exceptions are converted into ValidationError.
        """

        workflow_engine.tag = "v5.0.0"

        workflow_engine.gitService.tag.side_effect = RuntimeError("boom")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_tag()

        assert exc.value.code == "TAG_CREATION_FAILED"

    def test_preserves_error_context(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        ValidationError includes the original exception and tag.
        """

        workflow_engine.tag = "v6.0.0"

        workflow_engine.gitService.tag.side_effect = RuntimeError("network")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_tag()

        assert exc.value.context["tag"] == "v6.0.0"
        assert exc.value.context["error"] == "network"

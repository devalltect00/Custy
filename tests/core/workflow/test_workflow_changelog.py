# tests/core/workflow/test_workflow_changelog.py

"""
Unit tests for changelog generation in WorkflowEngine.

This module verifies changelog generation eligibility,
dry-run behavior, successful generation, and changelog writing.
"""

from unittest.mock import MagicMock

import pytest

from app.constants.path import CHANGELOG_PATH
from app.core.workflow.workflow_engine import WorkflowEngine


class TestGenerateChangelogIfNeeded:
    """
    Tests WorkflowEngine.generate_changelog_if_needed().
    """

    def test_skips_when_version_is_not_final(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Pre-release versions do not generate a changelog.
        """

        checker = MagicMock(return_value=False)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.maybe_assert_is_final",
            checker,
        )

        workflow_engine.generate_changelog_if_needed()

        checker.assert_called_once_with(
            workflow_engine.tag,
            context="changelog",
            force=workflow_engine.force_changelog,
        )

        workflow_engine.changelogGenerator.generate.assert_not_called()

    def test_dry_run_generates_preview_without_persistent_write(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Dry-run renders content and delegates to the generator's safe writer.
        """

        workflow_engine.dry_run = True
        workflow_engine.changelogGenerator.generate.return_value = "# PREVIEW"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.maybe_assert_is_final",
            MagicMock(return_value=True),
        )

        workflow_engine.generate_changelog_if_needed()

        workflow_engine.changelogGenerator.generate.assert_called_once_with()
        workflow_engine.changelogGenerator.write_to_file.assert_called_once_with(
            content="# PREVIEW",
            path=CHANGELOG_PATH,
        )

    def test_generates_and_writes_changelog(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Generates and writes CHANGELOG.md.
        """

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.maybe_assert_is_final",
            MagicMock(return_value=True),
        )

        workflow_engine.changelogGenerator.generate.return_value = "# CHANGELOG"

        workflow_engine.generate_changelog_if_needed()

        workflow_engine.changelogGenerator.generate.assert_called_once()

        workflow_engine.changelogGenerator.write_to_file.assert_called_once_with(
            content="# CHANGELOG",
            path=CHANGELOG_PATH,
        )

    def test_passes_force_flag(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Propagates force_changelog to final-version validation.
        """

        workflow_engine.force_changelog = True

        checker = MagicMock(return_value=False)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.maybe_assert_is_final",
            checker,
        )

        workflow_engine.generate_changelog_if_needed()

        checker.assert_called_once_with(
            workflow_engine.tag,
            context="changelog",
            force=True,
        )

    @pytest.mark.parametrize(
        "content",
        [
            "",
            "# v1.0.0",
            "## Added\n\n- feature",
        ],
    )
    def test_forwards_generated_content(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
        content: str,
    ) -> None:
        """
        Whatever the generator returns is written unchanged.
        """

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.maybe_assert_is_final",
            MagicMock(return_value=True),
        )

        workflow_engine.changelogGenerator.generate.return_value = content

        workflow_engine.generate_changelog_if_needed()

        workflow_engine.changelogGenerator.write_to_file.assert_called_once_with(
            content=content,
            path=CHANGELOG_PATH,
        )

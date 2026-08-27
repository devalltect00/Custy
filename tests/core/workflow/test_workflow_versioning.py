# tests/core/workflow/test_workflow_versioning.py

"""
Unit tests for app.core.workflow.workflow_engine (versioning section).

This module verifies the version preparation phase of WorkflowEngine,
including:

- Commitizen auto detection
- Version strategy selection
- Version tag generation

These tests intentionally isolate WorkflowEngine from external Git
operations by mocking all strategy implementations.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.cli.constants.enums import (
    BumpChoices,
    StrategyChoices,
)
from app.constants.git_workflow_rules import ALLOWED_COMMIT_TYPES
from app.core.exceptions.validation_error import ValidationError
from app.core.git_ops.helper.commitizen import CommitizenHelper
from app.core.workflow.workflow_engine import WorkflowEngine

# ==========================================================
# Commitizen Auto
# ==========================================================


class TestIsCommitizenAuto:
    """
    Tests for WorkflowEngine.is_commitizen_auto().
    """

    def test_returns_true_when_commitizen_and_auto_bump(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Returns True only when Commitizen strategy uses AUTO bump.
        """

        workflow_engine.strategy_input = StrategyChoices.COMMITIZEN
        workflow_engine.bump_level = BumpChoices.AUTO

        assert workflow_engine.is_commitizen_auto() is True

    @pytest.mark.parametrize(
        ("strategy", "bump"),
        [
            (StrategyChoices.SEMVER, BumpChoices.AUTO),
            (StrategyChoices.PEP440, BumpChoices.AUTO),
            (StrategyChoices.DATE, BumpChoices.AUTO),
            (StrategyChoices.GIT_COUNT, BumpChoices.AUTO),
            (StrategyChoices.COMMITIZEN, BumpChoices.MAJOR),
            (StrategyChoices.COMMITIZEN, BumpChoices.MINOR),
            (StrategyChoices.COMMITIZEN, BumpChoices.PATCH),
        ],
    )
    def test_returns_false_for_other_configurations(
        self,
        workflow_engine: WorkflowEngine,
        strategy,
        bump,
    ) -> None:
        """
        Returns False for every non-Commitizen AUTO configuration.
        """

        workflow_engine.strategy_input = strategy
        workflow_engine.bump_level = bump

        assert workflow_engine.is_commitizen_auto() is False


# ==========================================================
# Version Tag Preparation
# ==========================================================


class TestPrepareVersionTag:
    """
    Tests for WorkflowEngine.prepare_version_tag().
    """

    def test_uses_explicit_tag_input(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        CLI tag has the highest priority.
        """

        workflow_engine.tag_input = "v9.9.9"

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "v9.9.9"

    def test_uses_semver_strategy(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Uses SemVer strategy when requested.
        """

        strategy = MagicMock()
        strategy.get_next_tag.return_value = "v2.0.0"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.SemverStrategy",
            MagicMock(return_value=strategy),
        )

        workflow_engine.strategy_input = StrategyChoices.SEMVER

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "v2.0.0"

        strategy.get_next_tag.assert_called_once()

    def test_uses_pep440_strategy(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Uses PEP440 strategy.
        """

        strategy = MagicMock()
        strategy.get_next_tag.return_value = "1.2.3"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.PEP440Strategy",
            MagicMock(return_value=strategy),
        )

        workflow_engine.strategy_input = StrategyChoices.PEP440

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "1.2.3"

        strategy.get_next_tag.assert_called_once()

    def test_uses_commitizen_strategy(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Uses Commitizen strategy when AUTO bump is enabled.
        """

        strategy = MagicMock()
        strategy.get_next_tag.return_value = "v3.0.0"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.CommitizenStrategy",
            MagicMock(return_value=strategy),
        )

        workflow_engine.strategy_input = StrategyChoices.COMMITIZEN
        workflow_engine.bump_level = BumpChoices.AUTO

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "v3.0.0"

        strategy.get_next_tag.assert_called_once()

    def test_uses_date_strategy(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Uses Date strategy.
        """

        strategy = MagicMock()
        strategy.get_next_tag.return_value = "v2026.06.26"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.DateStrategy",
            MagicMock(return_value=strategy),
        )

        workflow_engine.strategy_input = StrategyChoices.DATE

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "v2026.06.26"

        strategy.get_next_tag.assert_called_once()

    def test_uses_git_count_strategy(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Uses Git-count strategy.
        """

        strategy = MagicMock()
        strategy.get_next_tag.return_value = "v105"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.GitCountStrategy",
            MagicMock(return_value=strategy),
        )

        workflow_engine.strategy_input = StrategyChoices.GIT_COUNT

        workflow_engine.prepare_version_tag()

        assert workflow_engine.tag == "v105"

        strategy.get_next_tag.assert_called_once()

    def test_raises_when_configuration_is_invalid(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Raises ValidationError when no valid version source exists.
        """

        workflow_engine.strategy_input = None
        workflow_engine.tag_input = None

        with pytest.raises(ValidationError) as exc:
            workflow_engine.prepare_version_tag()

        assert exc.value.code == "INVALID_VERSION_INPUT"


##### Part 2

# ==========================================================
# Tag Message Preparation
# ==========================================================


class TestPrepareTagMessage:
    """
    Tests for WorkflowEngine.prepare_tag_message().
    """

    def test_uses_cli_tag_message(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        CLI tag message has the highest priority.
        """

        workflow_engine.tag_message_input = "Release from CLI"

        workflow_engine.prepare_tag_message()

        assert workflow_engine.tag_message == "Release from CLI"

    def test_uses_existing_tag_message_file(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Existing tag message files are reused.
        """

        tag_file = tmp_path / "tag-message.txt"
        tag_file.write_text("Existing tag message")

        workflow_engine.tag = "v1.2.3"
        workflow_engine.tag_message_file = tag_file

        workflow_engine.prepare_tag_message()

        assert workflow_engine.tag_message_file == tag_file
        assert tag_file.read_text() == "Existing tag message"

    def test_creates_default_tag_message_template(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Missing tag message files are automatically created.
        """

        tag_file = tmp_path / "tag-message.txt"

        workflow_engine.tag = "v2.0.0"
        workflow_engine.tag_message_file = tag_file

        workflow_engine.prepare_tag_message()

        assert tag_file.exists()

        content = tag_file.read_text(encoding="utf-8")

        assert "Release v2.0.0" in content
        assert "Write additional tag notes below" in content

        assert workflow_engine.tag_message_file == tag_file

    def test_creates_parent_directory_when_missing(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Parent directories are created automatically.
        """

        nested = tmp_path / "templates" / "messages" / "tag.txt"

        workflow_engine.tag = "v5.0.0"
        workflow_engine.tag_message_file = nested

        workflow_engine.prepare_tag_message()

        assert nested.exists()
        assert nested.parent.exists()

    def test_dry_run_does_not_create_missing_tag_message(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Tag-message creation is reported but not applied in dry-run."""

        tag_file = tmp_path / "missing" / "tag-message.txt"
        workflow_engine.tag = "v2.0.0"
        workflow_engine.tag_message_file = tag_file
        workflow_engine.dry_run = True

        workflow_engine.prepare_tag_message()

        assert workflow_engine.tag_message_file == tag_file
        assert not tag_file.exists()
        assert not tag_file.parent.exists()


class TestGenerateReleaseArtifacts:
    """Tests release-message generation and filesystem safety."""

    def test_dry_run_builds_content_without_overwriting_files(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Release messages are computed in memory during a preview."""

        commit_file = tmp_path / "commit-message.txt"
        tag_file = tmp_path / "tag-message.txt"
        commit_file.write_text("original commit")
        tag_file.write_text("original tag")

        workflow_engine.tag = "v2.0.0"
        workflow_engine.commit_message_file = commit_file
        workflow_engine.tag_message_file = tag_file
        workflow_engine.dry_run = True
        workflow_engine.gitService.get_all_tags.return_value = []

        builder = MagicMock()
        builder.build_commit_msg.return_value = "planned commit"
        builder.build_tag_msg.return_value = "planned tag"
        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.ReleaseNoteBuilder",
            MagicMock(return_value=builder),
        )

        workflow_engine.generate_release_artifacts()

        assert commit_file.read_text() == "original commit"
        assert tag_file.read_text() == "original tag"
        builder.build_commit_msg.assert_called_once_with()
        builder.build_tag_msg.assert_called_once_with()


# ==========================================================
# Tagging Eligibility
# ==========================================================


class TestEvaluateTaggingEligibility:
    """
    Tests for WorkflowEngine.evaluate_tagging_eligibility().
    """

    def test_allows_supported_commit_type(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Allowed commit types proceed normally.
        """

        workflow_engine.evaluate_tagging_eligibility("feat")

        assert workflow_engine.skip_tag is False

        workflow_engine.gitService.get_latest_tag.assert_not_called()

    @pytest.mark.parametrize(
        "commit_type",
        [
            # "docs",
            # "style",
            # "build",
            # "ci",
            # "unknown",
            "foobar",
            "invalid",
            "my-custom-type",
            "not-supported",
        ],
    )
    def test_skips_unsupported_commit_types(
        self,
        workflow_engine: WorkflowEngine,
        commit_type: str,
    ) -> None:
        """
        Unsupported commit types skip tagging.
        """

        workflow_engine.gitService.get_latest_tag.return_value = "v1.5.0"

        workflow_engine.evaluate_tagging_eligibility(commit_type)

        assert workflow_engine.skip_tag is True
        assert workflow_engine.tag == "v1.5.0"

        assert commit_type not in ALLOWED_COMMIT_TYPES

        workflow_engine.gitService.get_latest_tag.assert_called_once()

    def test_force_tag_overrides_commit_type(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Force-tag bypasses commit-type restrictions.
        """

        workflow_engine.force_tag = True

        workflow_engine.evaluate_tagging_eligibility("docs")

        assert workflow_engine.skip_tag is False

        workflow_engine.gitService.get_latest_tag.assert_not_called()

    @pytest.mark.parametrize(
        "commit_type",
        [
            "feat",
            "fix",
            "perf",
            "refactor",
        ],
    )
    def test_allowed_commit_types_never_replace_tag(
        self,
        workflow_engine: WorkflowEngine,
        commit_type: str,
    ) -> None:
        """
        Allowed commit types never replace the prepared tag.
        """

        workflow_engine.tag = "v9.0.0"

        workflow_engine.evaluate_tagging_eligibility(commit_type)

        assert workflow_engine.tag == "v9.0.0"

        workflow_engine.gitService.get_latest_tag.assert_not_called()


##### Part 3

# ==========================================================
# Python Version File
# ==========================================================


class TestUpdatePythonVersionFile:
    """
    Tests for WorkflowEngine.update_python_version_file().
    """

    def test_skips_when_version_file_not_configured(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        No action is performed when no version file is configured.
        """

        workflow_engine.version_file = None

        workflow_engine.update_python_version_file()

    def test_raises_when_version_file_does_not_exist(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Raises ValidationError for a missing version file.
        """

        workflow_engine.version_file = Path("missing_version.py")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.update_python_version_file()

        assert exc.value.code == "VERSION_FILE_NOT_FOUND"

    def test_updates_version_file_using_tag(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Writes the prepared tag into the version file.
        """

        version_file = tmp_path / "__version__.py"
        version_file.write_text("old")

        workflow_engine.version_file = version_file
        workflow_engine.tag = "v2.5.0"

        workflow_engine.update_python_version_file()

        content = version_file.read_text(encoding="utf-8")

        assert '__version__ = "2.5.0"' in content

    def test_uses_version_override(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Explicit version overrides the prepared tag.
        """

        version_file = tmp_path / "__version__.py"
        version_file.write_text("old")

        workflow_engine.version_file = version_file
        workflow_engine.tag = "v1.0.0"

        workflow_engine.update_python_version_file(
            version_override="9.9.9",
        )

        content = version_file.read_text(encoding="utf-8")

        assert '__version__ = "9.9.9"' in content

    def test_dry_run_does_not_modify_file(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """
        Dry-run never writes to disk.
        """

        version_file = tmp_path / "__version__.py"
        version_file.write_text("original")

        workflow_engine.version_file = version_file
        workflow_engine.tag = "v8.0.0"
        workflow_engine.dry_run = True

        before = version_file.read_text()

        workflow_engine.update_python_version_file()

        after = version_file.read_text()

        assert before == after


# ==========================================================
# Project Version Files
# ==========================================================


class TestUpdateProjectVersions:
    """
    Tests for WorkflowEngine.update_project_versions().
    """

    def test_updates_project_version(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Updates project version files using the prepared tag.
        """

        updater = MagicMock(return_value=True)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.update_version_universal",
            updater,
        )

        workflow_engine.tag = "v4.0.0"

        workflow_engine.update_project_versions()

        updater.assert_called_once_with(
            root=".",
            new_version="v4.0.0",
            project_type=None,
        )

    def test_uses_explicit_version_override(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Explicit version overrides the prepared tag.
        """

        updater = MagicMock(return_value=True)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.update_version_universal",
            updater,
        )

        workflow_engine.tag = "v1.0.0"

        workflow_engine.update_project_versions(
            version_override="2.3.4",
        )

        updater.assert_called_once_with(
            root=".",
            new_version="2.3.4",
            project_type=None,
        )

    @pytest.mark.parametrize(
        "project_type",
        [
            "python",
            "node",
            None,
        ],
    )
    def test_passes_project_type(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
        project_type,
    ) -> None:
        """
        Passes project type through to the updater.
        """

        updater = MagicMock(return_value=True)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.update_version_universal",
            updater,
        )

        workflow_engine.tag = "v7.0.0"

        workflow_engine.update_project_versions(
            project_type=project_type,
        )

        updater.assert_called_once_with(
            root=".",
            new_version="v7.0.0",
            project_type=project_type,
        )

    def test_skips_when_dry_run(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Dry-run never calls the universal updater.
        """

        updater = MagicMock()

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.update_version_universal",
            updater,
        )

        workflow_engine.tag = "v5.0.0"
        workflow_engine.dry_run = True

        workflow_engine.update_project_versions()

        updater.assert_not_called()

    def test_handles_no_updated_files(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Handles the case where no project files were updated.
        """

        updater = MagicMock(return_value=False)

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.update_version_universal",
            updater,
        )

        workflow_engine.tag = "v6.0.0"

        workflow_engine.update_project_versions()

        updater.assert_called_once()


class TestCommitizenHelper:
    """Tests Commitizen helper behavior used during version updates."""

    def test_dry_run_does_not_update_cz_toml(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Commitizen metadata remains unchanged during previews."""

        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".cz.toml"
        config_file.write_text('version = "1.0.0"\n')

        CommitizenHelper(dry_run=True).update_cz_toml_version("v2.0.0")

        assert config_file.read_text() == 'version = "1.0.0"\n'

    def test_normal_run_updates_cz_toml(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Normal execution replaces the configured Commitizen version."""

        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".cz.toml"
        config_file.write_text('version = "1.0.0"\n', encoding="utf-8")

        CommitizenHelper().update_cz_toml_version("v2.0.0")

        assert config_file.read_text(encoding="utf-8") == ('version = "2.0.0"\n')

    def test_missing_cz_toml_is_ignored(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Missing optional Commitizen metadata does not fail a workflow."""

        monkeypatch.chdir(tmp_path)

        CommitizenHelper().update_cz_toml_version("v2.0.0")

        assert not (tmp_path / ".cz.toml").exists()

    def test_missing_version_field_preserves_cz_toml(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Malformed Commitizen metadata is reported without rewriting it."""

        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".cz.toml"
        config_file.write_text(
            '[tool.commitizen]\nname = "cz_conventional_commits"\n',
            encoding="utf-8",
        )

        CommitizenHelper().update_cz_toml_version("v2.0.0")

        assert config_file.read_text(encoding="utf-8") == (
            '[tool.commitizen]\nname = "cz_conventional_commits"\n'
        )

    def test_commit_check_is_read_only_during_dry_run(self, tmp_path) -> None:
        """Commit validation executes as safe discovery in dry-run mode."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("feat(core): preview")
        helper = CommitizenHelper(dry_run=True)
        helper.runner = MagicMock()

        helper.check_commit(message_file)

        helper.runner.run.assert_called_once_with(
            ["cz", "check", "--commit-msg-file", str(message_file)],
            check=True,
            read_only=True,
        )

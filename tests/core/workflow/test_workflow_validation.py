# tests/core/workflow/test_workflow_validation.py

"""
tests/core/workflow/test_workflow_validation.py

Unit tests for WorkflowEngine validation.

These tests verify that WorkflowEngine validates the execution
environment before starting the release workflow.

Covered responsibilities:

- Git repository validation
- Remote validation
- Version file validation
- Commit message file validation
- Tag message file validation
- Commitizen validation
- Validation pipeline ordering
"""

from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.git_ops.commit.settings import (
    CommitValidationProvider,
    CommitValidationSettings,
)
from app.core.git_ops.helper import CommitizenCommandResult, CommitizenInspection
from app.core.workflow.workflow_config import WorkflowConfig
from app.core.workflow.workflow_engine import WorkflowEngine


@pytest.fixture
def workflow_engine():
    """
    Create a WorkflowEngine with mocked collaborators.

    Every external dependency is replaced so each test focuses only
    on WorkflowEngine behaviour.
    """

    engine = WorkflowEngine(WorkflowConfig())

    engine.gitService = MagicMock()
    engine.commitizenHelper = MagicMock()
    engine.commitizenHelper.inspect.return_value = CommitizenInspection(None, None)
    engine.changelogGenerator = MagicMock()
    engine.backupManager = MagicMock()
    engine.branchWorkflowManager = MagicMock()

    return engine


class TestValidate:
    """Tests for WorkflowEngine.validate()."""

    def test_runs_validation_steps_in_order(
        self,
        workflow_engine,
        monkeypatch,
    ):
        """Runs every validation step exactly once."""

        calls = []

        def record(name):
            return lambda: calls.append(name)

        monkeypatch.setattr(
            workflow_engine,
            "ensure_git_repo",
            record("git"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_remote_exists",
            record("remote"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_version_file",
            record("version"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_commit_message_file",
            record("commit_file"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_tag_message_file",
            record("tag_file"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_staged_changes",
            record("staged"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_commit_validation_provider",
            record("commit_provider"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_commit_message_file_exists",
            record("commit_exists"),
        )

        monkeypatch.setattr(
            workflow_engine,
            "ensure_tag_message_file_exists",
            record("tag_exists"),
        )

        workflow_engine.validate()

        assert calls == [
            "git",
            "remote",
            "version",
            "commit_file",
            "tag_file",
            "staged",
            "commit_provider",
            "commit_exists",
            "tag_exists",
        ]


class TestEnsureGitRepo:
    """Tests for ensure_git_repo()."""

    def test_accepts_git_repository(
        self,
        workflow_engine,
    ):
        """Succeeds when inside a Git repository."""

        workflow_engine.gitService.is_git_repo.return_value = True

        workflow_engine.ensure_git_repo()

        workflow_engine.gitService.is_git_repo.assert_called_once_with()

    def test_raises_when_not_git_repository(
        self,
        workflow_engine,
    ):
        """Raises ValidationError when not inside a Git repository."""

        workflow_engine.gitService.is_git_repo.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_git_repo()

        error = exc.value

        assert error.code == "NOT_GIT_REPO"
        assert "Git repository" in error.message


class TestEnsureRemoteExists:
    """Tests for ensure_remote_exists()."""

    def test_accepts_existing_remote(
        self,
        workflow_engine,
    ):
        """Succeeds when the requested remote exists."""

        workflow_engine.gitService.check_remote.return_value = True

        workflow_engine.ensure_remote_exists("origin")

        workflow_engine.gitService.check_remote.assert_called_once_with("origin")

    def test_skip_checks_bypasses_validation(
        self,
        workflow_engine,
    ):
        """Skips remote validation when skip_checks is enabled."""

        workflow_engine.skip_checks = True

        workflow_engine.ensure_remote_exists()

        workflow_engine.gitService.check_remote.assert_not_called()

    def test_raises_when_remote_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError when remote is unavailable."""

        workflow_engine.gitService.check_remote.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_remote_exists("origin")

        error = exc.value

        assert error.code == "REMOTE_NOT_FOUND"
        assert error.context["remote"] == "origin"

    def test_validates_every_selected_remote(
        self,
        workflow_engine,
    ):
        """Checks all effective main and backup destinations."""

        workflow_engine.all_remote = True
        workflow_engine.main_remotes = ["origin", "github"]
        workflow_engine.backup_remotes = ["mirror"]
        workflow_engine.gitService.get_current_branch.return_value = "main"
        workflow_engine.gitService.check_remote.return_value = True

        workflow_engine.ensure_remote_exists()

        assert workflow_engine.gitService.check_remote.call_args_list == [
            call("origin"),
            call("github"),
            call("mirror"),
        ]


class TestEnsureVersionFile:
    """Tests for ensure_version_file()."""

    def test_accepts_existing_version_file(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Succeeds when the configured version file exists."""

        version = tmp_path / "__version__.py"
        version.write_text("__version__='1.0.0'")

        workflow_engine.version_file = version

        workflow_engine.ensure_version_file()

    def test_accepts_git_tag_only_project(
        self,
        workflow_engine,
    ):
        """Allows repositories without supported project version metadata."""

        workflow_engine.version_file = None

        workflow_engine.ensure_version_file()

    def test_raises_when_version_file_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError for an explicitly configured missing file."""

        workflow_engine.version_file = Path("missing.py")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_version_file()

        assert exc.value.code == "VERSION_FILE_NOT_FOUND"


class TestEnsureCommitMessageFile:
    """Tests for ensure_commit_message_file()."""

    def test_accepts_existing_commit_message_file(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Succeeds when the commit message template exists."""

        path = tmp_path / "commit.txt"
        path.write_text("feat: test")

        workflow_engine.commit_message_file = path

        workflow_engine.ensure_commit_message_file()

    def test_raises_when_commit_message_file_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError for a missing commit message file."""

        workflow_engine.commit_message_file = Path("missing.txt")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commit_message_file()

        assert exc.value.code == "COMMIT_MSG_FILE_NOT_FOUND"


class TestEnsureTagMessageFile:
    """Tests for ensure_tag_message_file()."""

    def test_accepts_existing_tag_message_file(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Succeeds when the tag message template exists."""

        path = tmp_path / "tag.txt"
        path.write_text("release")

        workflow_engine.tag_message_file = path

        workflow_engine.ensure_tag_message_file()

    def test_raises_when_tag_message_file_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError for a missing tag message file."""

        workflow_engine.tag_message_file = Path("missing.txt")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_tag_message_file()

        assert exc.value.code == "TAG_MSG_FILE_NOT_FOUND"


class TestEnsureCommitValidationProvider:
    """Tests for provider discovery and strict optional integration."""

    def test_auto_without_project_configuration_uses_custy(
        self,
        workflow_engine,
    ):
        """Tool absence and configuration absence keep Custy universal."""

        assert (
            workflow_engine.ensure_commit_validation_provider()
            == CommitValidationProvider.CUSTY
        )

    def test_auto_ignores_installed_tool_without_configuration(
        self,
        workflow_engine,
    ):
        """A globally installed executable alone does not activate Commitizen."""

        workflow_engine.commitizenHelper.inspect.return_value = CommitizenInspection(
            None,
            "cz",
        )

        assert (
            workflow_engine.ensure_commit_validation_provider()
            == CommitValidationProvider.CUSTY
        )

    def test_auto_with_configuration_and_tool_uses_commitizen(
        self,
        workflow_engine,
    ):
        """Auto mode enables Commitizen only when both signals are present."""

        workflow_engine.commitizenHelper.inspect.return_value = CommitizenInspection(
            Path(".cz.toml"),
            "cz",
        )

        assert (
            workflow_engine.ensure_commit_validation_provider()
            == CommitValidationProvider.COMMITIZEN
        )

    def test_auto_missing_tool_falls_back_to_custy(
        self,
        workflow_engine,
    ):
        """Optional auto mode warns and falls back when ``cz`` is unavailable."""

        workflow_engine.commitizenHelper.inspect.return_value = CommitizenInspection(
            Path(".cz.toml"),
            None,
        )

        assert (
            workflow_engine.ensure_commit_validation_provider()
            == CommitValidationProvider.CUSTY
        )

    def test_explicit_commitizen_requires_configuration(
        self,
        workflow_engine,
    ):
        """Explicit Commitizen mode fails before mutation without configuration."""

        workflow_engine.commit_validation_settings = CommitValidationSettings(
            provider=CommitValidationProvider.COMMITIZEN,
            require_tool=True,
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commit_validation_provider()

        assert exc.value.code == "COMMITIZEN_NOT_CONFIGURED"

    def test_strict_auto_requires_detected_tool(
        self,
        workflow_engine,
    ):
        """Strict auto mode rejects detected integration without ``cz``."""

        workflow_engine.commit_validation_settings = CommitValidationSettings(
            provider=CommitValidationProvider.AUTO,
            require_tool=True,
        )
        workflow_engine.commitizenHelper.inspect.return_value = CommitizenInspection(
            Path(".cz.toml"),
            None,
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commit_validation_provider()

        assert exc.value.code == "COMMITIZEN_NOT_AVAILABLE"

    def test_invalid_explicit_configuration_is_actionable(
        self,
        workflow_engine,
    ):
        """Malformed strict configuration retains its parser diagnostic."""

        workflow_engine.commit_validation_settings = CommitValidationSettings(
            provider=CommitValidationProvider.COMMITIZEN,
            require_tool=True,
        )
        workflow_engine.commitizenHelper.inspect.return_value = CommitizenInspection(
            Path(".cz.toml"),
            "cz",
            "invalid TOML",
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commit_validation_provider()

        assert exc.value.code == "COMMITIZEN_CONFIGURATION_INVALID"
        assert exc.value.context["error"] == "invalid TOML"


class TestValidateEditedCommitMessage:
    """Tests for final provider-aware validation after editor completion."""

    def test_custy_provider_uses_internal_rules(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Custy validates conventional syntax without optional tools."""

        message = tmp_path / "commit.txt"
        message.write_text("fix(core): preserve diagnostics\n", encoding="utf-8")
        workflow_engine.commit_message_file = message
        workflow_engine.commit_validation_provider = CommitValidationProvider.CUSTY
        workflow_engine.evaluate_tagging_eligibility = MagicMock()

        workflow_engine.validate_edited_files()

        workflow_engine.evaluate_tagging_eligibility.assert_called_once_with("fix")
        workflow_engine.commitizenHelper.check_commit.assert_not_called()

    def test_git_provider_accepts_non_conventional_message(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Git mode applies only required file safety checks."""

        message = tmp_path / "commit.txt"
        message.write_text("A project-specific message\n", encoding="utf-8")
        workflow_engine.commit_message_file = message
        workflow_engine.commit_validation_provider = CommitValidationProvider.GIT
        workflow_engine.evaluate_tagging_eligibility = MagicMock()

        workflow_engine.validate_edited_files()

        workflow_engine.evaluate_tagging_eligibility.assert_not_called()

    def test_commitizen_failure_preserves_tool_output(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Commitizen rejection is reported with its exact diagnostic."""

        message = tmp_path / "commit.txt"
        message.write_text("fix(core): preserve diagnostics\n", encoding="utf-8")
        workflow_engine.commit_message_file = message
        workflow_engine.commit_validation_provider = CommitValidationProvider.COMMITIZEN
        workflow_engine.commitizenHelper.check_commit.return_value = (
            CommitizenCommandResult(
                returncode=1,
                stderr="subject does not match project rules",
            )
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.validate_edited_files()

        assert exc.value.code == "COMMITIZEN_CHECK_FAILED"
        assert "subject does not match" in exc.value.context["detail"]


class TestEnsureCommitMessageFileExists:
    """Tests for ensure_commit_message_file_exists()."""

    def test_raises_when_path_is_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError when no path is configured."""

        workflow_engine.commit_message_file = None

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commit_message_file_exists()

        assert exc.value.code == "COMMIT_MSG_PATH_MISSING"

    def test_accepts_existing_file(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Succeeds for an existing commit message file."""

        path = tmp_path / "commit.txt"
        path.write_text("feat: test")

        workflow_engine.commit_message_file = path

        workflow_engine.ensure_commit_message_file_exists()


class TestEnsureTagMessageFileExists:
    """Tests for ensure_tag_message_file_exists()."""

    def test_raises_when_path_is_missing(
        self,
        workflow_engine,
    ):
        """Raises ValidationError when no path is configured."""

        workflow_engine.tag_message_file = None

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_tag_message_file_exists()

        assert exc.value.code == "TAG_MSG_PATH_MISSING"

    def test_accepts_existing_file(
        self,
        workflow_engine,
        tmp_path,
    ):
        """Succeeds for an existing tag message file."""

        path = tmp_path / "tag.txt"
        path.write_text("Release")

        workflow_engine.tag_message_file = path

        workflow_engine.ensure_tag_message_file_exists()

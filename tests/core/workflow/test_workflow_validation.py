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
from unittest.mock import MagicMock

import pytest

from app.core.exceptions.validation_error import ValidationError
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
            "ensure_commitizen_convention",
            record("commitizen"),
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
            "commitizen",
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

        workflow_engine.gitService.check_remote.assert_called_once_with(
            "origin"
        )

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

    @pytest.mark.parametrize(
        "path",
        [
            None,
            Path("missing.py"),
        ],
    )
    def test_raises_when_version_file_missing(
        self,
        workflow_engine,
        path,
    ):
        """Raises ValidationError for a missing version file."""

        workflow_engine.version_file = path

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


class TestEnsureCommitizenConvention:
    """Tests for ensure_commitizen_convention()."""

    def test_accepts_valid_commitizen_configuration(
        self,
        workflow_engine,
    ):
        """Succeeds when Commitizen validation is available."""

        workflow_engine.commitizenHelper.check_commit = True

        workflow_engine.ensure_commitizen_convention()

    def test_raises_when_commitizen_validation_fails(
        self,
        workflow_engine,
    ):
        """Raises ValidationError when Commitizen validation fails."""

        workflow_engine.commitizenHelper.check_commit = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.ensure_commitizen_convention()

        assert exc.value.code == "COMMITIZEN_CONVENTION_FAILED"


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

# tests/core/workflow/test_workflow_backup.py

"""
Unit tests for backup-related behavior in WorkflowEngine.

This module verifies backup creation, tag-message resolution,
release-file backup orchestration, and low-level backup handling.
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.core.workflow.workflow_engine import WorkflowEngine


class FixedDatetime:
    """Deterministic datetime replacement for timestamped backups."""

    @staticmethod
    def now() -> datetime:
        """Return a fixed timestamp for predictable backup filenames."""

        return datetime(2026, 6, 26, 12, 34, 56)


# ==========================================================
# Commit Message Backups
# ==========================================================


class TestBackupCommitMessageFile:
    """Tests for WorkflowEngine.backup_commit_message_file()."""

    def test_returns_when_commit_message_file_is_missing(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """Skips backup when no commit message file is configured."""

        workflow_engine.commit_message_file = None

        workflow_engine.backup_commit_message_file()

        workflow_engine.backupManager._prune_old_backups.assert_not_called()

    def test_uses_configured_commit_backup_directory(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Uses the configured commit backup directory."""

        source = tmp_path / "commit-message.txt"
        source.write_text("feat: add backup tests", encoding="utf-8")

        backup_dir = tmp_path / "commit-backups"

        workflow_engine.commit_message_file = source
        workflow_engine.commit_message_backup_dir = backup_dir

        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.datetime",
            FixedDatetime,
        )

        try:
            workflow_engine.backupManager._prune_old_backups.return_value = []

            workflow_engine.backup_commit_message_file()

            assert workflow_engine.changes_to_staged
        finally:
            monkeypatch.undo()


# ==========================================================
# Tag Message Resolution
# ==========================================================


class TestResolveTagMessageFromFile:
    """Tests for WorkflowEngine._resolve_tag_message_from_file()."""

    def test_uses_tag_message_file_content(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Loads tag message content from the file when available."""

        tag_file = tmp_path / "tag-message.txt"
        tag_file.write_text("Release notes", encoding="utf-8")

        workflow_engine.tag_message_file = tag_file
        workflow_engine.tag = "v1.2.3"

        workflow_engine._resolve_tag_message_from_file()

        assert workflow_engine.tag_message == "Release notes"

    def test_falls_back_to_tag_when_file_missing(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """Falls back to the tag name when no file exists."""

        workflow_engine.tag_message_file = None
        workflow_engine.tag = "v9.9.9"

        workflow_engine._resolve_tag_message_from_file()

        assert workflow_engine.tag_message == "v9.9.9"


class TestBackupTagMessageFile:
    """Tests for WorkflowEngine.backup_tag_message_file()."""

    def test_returns_when_tag_message_file_is_missing(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """Skips backup when no tag message file is configured."""

        workflow_engine.tag_message_file = None
        workflow_engine.tag = "v1.0.0"

        workflow_engine._resolve_tag_message_from_file = MagicMock()
        workflow_engine._backup_file = MagicMock()

        workflow_engine.backup_tag_message_file()

        workflow_engine._resolve_tag_message_from_file.assert_called_once()
        workflow_engine._backup_file.assert_not_called()

    def test_uses_existing_tag_message_file(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Backs up the configured tag message file."""

        tag_file = tmp_path / "tag-message.txt"
        tag_file.write_text("release", encoding="utf-8")

        workflow_engine.tag_message_file = tag_file
        workflow_engine.tag_message_backup_dir = tmp_path / "tag-backups"
        workflow_engine.tag = "v1.0.0"

        workflow_engine._resolve_tag_message_from_file = MagicMock()
        workflow_engine._backup_file = MagicMock()

        workflow_engine.backup_tag_message_file()

        workflow_engine._resolve_tag_message_from_file.assert_called_once()

        workflow_engine._backup_file.assert_called_once_with(
            source=tag_file,
            backup_dir=tmp_path / "tag-backups",
            label="tag message",
        )


# ==========================================================
# Release Backup Orchestration
# ==========================================================


class TestBackupReleaseFiles:
    """Tests for WorkflowEngine.backup_release_files()."""

    def test_calls_commit_and_tag_backup(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """Calls both backup methods in order."""

        commit_backup = MagicMock()
        tag_backup = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "backup_commit_message_file",
            commit_backup,
        )
        monkeypatch.setattr(
            workflow_engine,
            "backup_tag_message_file",
            tag_backup,
        )

        workflow_engine.backup_release_files()

        commit_backup.assert_called_once()
        tag_backup.assert_called_once()


# ==========================================================
# Low-Level Backup Helper
# ==========================================================


class TestBackupFile:
    """Tests for WorkflowEngine._backup_file()."""

    def test_returns_when_source_missing(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Skips backup when the source file does not exist."""

        source = tmp_path / "missing.txt"
        backup_dir = tmp_path / "backups"

        workflow_engine._backup_file(
            source=source,
            backup_dir=backup_dir,
            label="commit message",
        )

        assert workflow_engine.changes_to_staged == []

    def test_creates_backup_and_registers_it(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Creates a backup file and registers it for staging."""

        source = tmp_path / "commit-message.txt"
        source.write_text("feat: backup", encoding="utf-8")

        backup_dir = tmp_path / "backups"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.datetime",
            FixedDatetime,
        )

        workflow_engine.backupManager._prune_old_backups = MagicMock(return_value=[])

        workflow_engine._backup_file(
            source=source,
            backup_dir=backup_dir,
            label="commit message",
        )

        expected = backup_dir / "commit-message_20260626_123456.bak.txt"

        assert expected.exists()
        assert expected in workflow_engine.changes_to_staged

    def test_dry_run_does_not_create_backup_directory(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
    ) -> None:
        """Previewing a backup leaves its destination absent."""

        source = tmp_path / "commit-message.txt"
        source.write_text("feat: backup", encoding="utf-8")
        backup_dir = tmp_path / "missing" / "backups"
        workflow_engine.dry_run = True

        workflow_engine._backup_file(
            source=source,
            backup_dir=backup_dir,
            label="commit message",
        )

        assert not backup_dir.exists()
        assert workflow_engine.changes_to_staged == []
        workflow_engine.backupManager._prune_old_backups.assert_not_called()

    def test_prunes_old_backups(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path,
        monkeypatch,
    ) -> None:
        """Adds pruned files to the staging list when pruning occurs."""

        source = tmp_path / "tag-message.txt"
        source.write_text("release", encoding="utf-8")

        backup_dir = tmp_path / "backups"

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.datetime",
            FixedDatetime,
        )

        old_file = backup_dir / "tag-message_20240101_000000.bak.txt"
        workflow_engine.backupManager._prune_old_backups = MagicMock(
            return_value=[old_file]
        )

        workflow_engine._backup_file(
            source=source,
            backup_dir=backup_dir,
            label="tag message",
        )

        assert old_file in workflow_engine.changes_to_staged
        workflow_engine.backupManager._prune_old_backups.assert_called_once()

# tests/core/cleanup/backups/test_handle_cleanup_backups.py

"""Unit tests for backup-cleanup coordination."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

import app.core.cleanup.backups.handle_cleanup_backups as cleanup_module
from app.cli.constants.enums import CleanupTypeChoices
from app.core.cleanup.backups.handle_cleanup_backups import HandleCleanupBackups


class TestInitialization:
    """Tests backup-cleanup configuration."""

    def test_builds_dry_run_backup_manager(self):
        """Retention and dry-run state reach the filesystem manager."""

        handler = HandleCleanupBackups(
            target=CleanupTypeChoices.TAG,
            keep=4,
            dry_run=True,
        )

        assert handler.target is CleanupTypeChoices.TAG
        assert handler.keep == 4
        assert handler.dry_run is True
        assert handler.backup_manager.keep == 4
        assert handler.backup_manager.dry_run is True


class TestCleanupRouting:
    """Tests cleanup-target routing."""

    @pytest.mark.parametrize(
        ("target", "expected_labels"),
        [
            (CleanupTypeChoices.COMMIT, ["commit backups"]),
            (CleanupTypeChoices.TAG, ["tag backups"]),
            (
                CleanupTypeChoices.ALL,
                ["commit backups", "tag backups"],
            ),
        ],
    )
    def test_routes_selected_directories(self, target, expected_labels):
        """Each target invokes only its configured backup categories."""

        handler = HandleCleanupBackups(target=target)
        handler._cleanup_directory = MagicMock()

        handler.cleanup()

        assert [
            call.kwargs["label"] for call in handler._cleanup_directory.call_args_list
        ] == expected_labels


class TestCleanupDirectory:
    """Tests cleanup behavior for one backup directory."""

    def test_missing_directory_is_skipped(self, tmp_path):
        """A missing optional backup directory requires no pruning."""

        handler = HandleCleanupBackups()
        handler.backup_manager = MagicMock()

        handler._cleanup_directory(
            tmp_path / "missing",
            "commit backups",
            "commit-msg",
        )

        handler.backup_manager._prune_old_backups.assert_not_called()

    def test_delegates_existing_directory(self, tmp_path):
        """An existing directory is delegated with its matching stem."""

        handler = HandleCleanupBackups(keep=2)
        handler.backup_manager = MagicMock()
        handler.backup_manager._prune_old_backups.return_value = [
            tmp_path / "commit-msg_old.bak.txt",
        ]

        handler._cleanup_directory(
            tmp_path,
            "commit backups",
            "commit-msg",
        )

        handler.backup_manager._prune_old_backups.assert_called_once_with(
            backup_dir=tmp_path,
            stem="commit-msg",
        )

    def test_pruning_failure_is_contained(self, tmp_path, monkeypatch):
        """Filesystem pruning failures are logged without escaping."""

        handler = HandleCleanupBackups()
        handler.backup_manager = MagicMock()
        handler.backup_manager._prune_old_backups.side_effect = OSError(
            "permission denied"
        )
        logged = MagicMock()
        monkeypatch.setattr(cleanup_module.logger, "error", logged)

        handler._cleanup_directory(
            Path(tmp_path),
            "commit backups",
            "commit-msg",
        )

        logged.assert_called_once()

# tests/core/backup/test_backup_manager.py

"""
Tests for app.core.backup.backup_manager.

Covers:
- constructor
- _prune_old_backups()
"""

from pathlib import Path

import pytest

from app.core.backup.backup_manager import BackupManager


class TestInitialization:
    """
    Tests BackupManager construction.
    """

    def test_default_keep(self):
        manager = BackupManager()

        assert manager.keep == 10

    def test_custom_keep(self):
        manager = BackupManager(keep=5)

        assert manager.keep == 5


class TestPruneOldBackups:
    """
    Tests BackupManager._prune_old_backups().
    """

    def test_directory_missing(self, tmp_path, capsys):
        """
        Missing directory returns an empty candidate list.
        """
        manager = BackupManager()

        backup_dir = tmp_path / "missing"

        result = manager._prune_old_backups(
            backup_dir,
            "commit",
        )

        assert result == []

        captured = capsys.readouterr()

        assert "Backup directory not found" in captured.out

    def test_no_files(self, tmp_path):
        """
        Empty directory returns empty list.
        """
        manager = BackupManager()

        result = manager._prune_old_backups(
            tmp_path,
            "commit",
        )

        assert result == []

    def test_keep_all_files(self, tmp_path):
        """
        Nothing is removed when total files <= keep.
        """
        manager = BackupManager(keep=5)

        for i in range(3):
            file = tmp_path / f"commit_{i}.bak.txt"
            file.write_text("data")

        removed = manager._prune_old_backups(
            tmp_path,
            "commit",
        )

        assert removed == []

        assert len(list(tmp_path.glob("*.bak.txt"))) == 3

    def test_remove_old_backups(self, tmp_path):
        """
        Old backups are deleted.
        """
        manager = BackupManager(keep=2)

        files = []

        for i in range(5):
            f = tmp_path / f"commit_{i}.bak.txt"
            f.write_text(str(i))

            # make mtimes different
            f.touch()

            files.append(f)

        removed = manager._prune_old_backups(
            tmp_path,
            "commit",
        )

        assert len(removed) == 3

        remaining = list(tmp_path.glob("*.bak.txt"))

        assert len(remaining) == 2

    def test_ignore_other_stems(self, tmp_path):
        """
        Only matching stem files are considered.
        """
        manager = BackupManager(keep=1)

        (tmp_path / "commit_1.bak.txt").write_text("a")
        (tmp_path / "tag_1.bak.txt").write_text("b")
        (tmp_path / "random.txt").write_text("c")

        removed = manager._prune_old_backups(
            tmp_path,
            "commit",
        )

        assert removed == []

        assert (tmp_path / "tag_1.bak.txt").exists()
        assert (tmp_path / "random.txt").exists()

    def test_dry_run_reports_candidates_without_deleting(self, tmp_path):
        """Dry-run returns old backups while preserving every file."""

        manager = BackupManager(keep=1, dry_run=True)

        for index in range(3):
            path = tmp_path / f"commit_{index}.bak.txt"
            path.write_text(str(index))
            path.touch()

        candidates = manager._prune_old_backups(tmp_path, "commit")

        assert len(candidates) == 2
        assert len(list(tmp_path.glob("*.bak.txt"))) == 3

    # def test_unlink_failure_is_handled(
    #     self,
    #     tmp_path,
    #     monkeypatch,
    #     capsys,
    # ):
    #     """
    #     Failure deleting a backup is handled gracefully.
    #     """
    #     manager = BackupManager(keep=1)

    #     files = []

    #     for i in range(2):
    #         f = tmp_path / f"commit_{i}.bak.txt"
    #         f.write_text("x")
    #         files.append(f)

    #     original_unlink = Path.unlink

    #     def fake_unlink(path):
    #         if path == files[1]:
    #             raise OSError("permission denied")

    #         return original_unlink(path)

    #     monkeypatch.setattr(
    #         Path,
    #         "unlink",
    #         fake_unlink,
    #     )

    #     manager._prune_old_backups(
    #         tmp_path,
    #         "commit",
    #     )

    #     captured = capsys.readouterr()

    #     assert "Failed to delete old backup" in captured.out

    def test_unlink_failure_is_handled(
        self,
        tmp_path,
        monkeypatch,
        capsys,
    ):
        """
        Failure deleting a backup is handled gracefully.
        """
        manager = BackupManager(keep=1)

        for i in range(2):
            (tmp_path / f"commit_{i}.bak.txt").write_text("x")

        def fake_unlink(self):
            raise OSError("permission denied")

        monkeypatch.setattr(
            Path,
            "unlink",
            fake_unlink,
        )

        manager._prune_old_backups(
            tmp_path,
            "commit",
        )

        captured = capsys.readouterr()

        assert "Failed to delete old backup" in captured.out

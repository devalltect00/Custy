# app/core/backup/backup_manager.py
""" """

from pathlib import Path


class BackupManager:
    """Prune timestamped backup files using a retention limit."""

    def __init__(self, keep: int = 10, *, dry_run: bool = False) -> None:
        """Initialize backup retention behavior.

        Args:
            keep:
                Number of newest matching backups to preserve.

            dry_run:
                Report pruning candidates without deleting them.
        """

        self.keep = keep
        self.dry_run = dry_run

    def _prune_old_backups(self, backup_dir: Path, stem: str) -> list[Path]:
        """
        Keep only the most recent N backup files. Delete older ones.
        """
        if not backup_dir.exists():
            print(f"⚠️ Backup directory not found: {backup_dir}")
            return []

        backup = sorted(
            backup_dir.glob(f"{stem}_*.bak.txt"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )

        for old_file in backup[self.keep :]:
            if self.dry_run:
                print(f"(dry-run) Would remove old backup: {old_file}")
                continue

            try:
                old_file.unlink()
                print(f"🗑️ Removed old backup: {old_file}")
            except Exception as e:
                print(f"⚠️ Failed to delete old backup: {e}")

        return backup[self.keep :]

# app/core/cleanup/backups/handle_cleanup_backups.py

import logging
from pathlib import Path
from typing import Literal

from app.cli.constants.enums import CleanupTypeChoices
from app.constants.path import (
    CUSTY_BACKUP_COMMIT_DIR,
    CUSTY_BACKUP_TAG_DIR,
)
from app.core.backup import BackupManager

logger = logging.getLogger(__name__)


CleanupTarget = Literal["commit", "tag", "all"]


class HandleCleanupBackups:
    """
    Cleanup old backup files for commit and/or tag messages.

    This class is responsible for pruning old backup files while keeping
    a specified number of recent backups.

    Parameters:
        target (CleanupTarget):
            Which backups to clean:
                - "commit" → only commit backups
                - "tag"    → only tag backups
                - "all"    → both (default)

        keep (int):
            Number of recent backups to keep per category.
    """

    def __init__(
        self,
        target: CleanupTypeChoices = CleanupTypeChoices.ALL,
        keep: int = 10,
        *,
        dry_run: bool = False,
    ) -> None:
        """Initialize backup cleanup behavior.

        Args:
            target:
                Backup category to inspect.

            keep:
                Number of newest backups to preserve.

            dry_run:
                Report deletion candidates without removing them.
        """

        self.target = target
        self.keep = keep
        self.dry_run = dry_run
        self.backup_manager = BackupManager(
            keep=keep,
            dry_run=dry_run,
        )

    # =========================================================
    # Public API
    # =========================================================
    def cleanup(self) -> None:
        """
        Execute cleanup process based on target.
        """

        logger.info("[blue]🧹 Cleaning up backup files...[/blue]")

        if self.dry_run:
            logger.info(
                "[dry_run](dry-run)[/dry_run] " "Inspecting backup cleanup candidates."
            )

        if self.target in ("commit", "all"):
            self._cleanup_directory(
                backup_dir=CUSTY_BACKUP_COMMIT_DIR,
                label="commit backups",
                stem="commit-msg",
            )

        if self.target in ("tag", "all"):
            self._cleanup_directory(
                backup_dir=CUSTY_BACKUP_TAG_DIR,
                label="tag backups",
                stem="tag-msg",
            )

    # =========================================================
    # Internal Helpers
    # =========================================================
    def _cleanup_directory(self, backup_dir: str | Path, label: str, stem: str) -> None:
        """
        Cleanup a specific backup directory.

        Args:
            backup_dir (Path | str): Directory containing backup files
            label (str): Human-readable label for logging
            stem (str): File stem pattern used for pruning
        """

        path = Path(backup_dir)

        if not path.exists():
            logger.debug(f"[dim]Skipping {label} → directory not found[/dim]")
            return

        logger.info(f"[cyan]→ Cleaning {label}[/cyan] [dim](keeping {self.keep})[/dim]")

        try:
            removed_files = self.backup_manager._prune_old_backups(
                backup_dir=path,
                stem=stem,
            )

            if removed_files:
                for f in removed_files:
                    action = "would remove" if self.dry_run else "removed"
                    logger.info(f"[dim]  {action}: {f}[/dim]")
            else:
                logger.debug(f"[dim]No old backups to remove in {label}[/dim]")

        except Exception as e:
            logger.error(f"[red]⚠️ Failed to clean {label}: {e}[/red]")

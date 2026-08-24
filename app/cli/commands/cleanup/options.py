# app/cli/commands/cleanup/options.py

import typer

from typing import Annotated, Optional
from pathlib import Path

from app.cli.constants import (
  LogLevelChoices,
  CleanupTypeChoices,
  MergeStatusChoices,
  completion_commit_message_backup_dir,
  completion_tag_message_backup_dir,
)

# ---------------------------
# CLEANUP BACKUP OPTIONS
# ---------------------------
TypeOption = Annotated[
    list[CleanupTypeChoices],
    typer.Option(
        "--type", "-t",
        help="""
        [bold]Backup type[/bold]

        Select which backup category should be cleaned.

        [bold yellow]•[/bold yellow] [bold]all[/bold]
        Cleanup commit and tag backups.

        [bold yellow]•[/bold yellow] [bold]commit[/bold]
        Cleanup commit template backups only.

        [bold yellow]•[/bold yellow] [bold]tag[/bold]
        Cleanup tag template backups only.

        [dim blue]Default:[/dim blue] all
        """,
        rich_help_panel="Cleanup Backups Options",
        case_sensitive=False,
    ),
]
KeepOption = Annotated[
    Optional[int],
    typer.Option(
        "--keep", "-k",
        help="""
        [bold]Retention count[/bold]

        Number of recent backups to keep.

        Older backups beyond this limit may be removed.

        [dim blue]Default:[/dim blue] 10

        [dim bright_blue]Example:[/dim bright_blue]

        --keep 5

        Keep only the 5 most recent backups.
        """,
        rich_help_panel="Cleanup Backups Options",
    ),
]

# ---------------------------
# CLEANUP BRANCHES OPTIONS
# ---------------------------
IncludePrefixesOption = Annotated[
    list[str],
    typer.Option(
        "--prefix",
        "-p",
        help="""
        [bold]Branch prefix filter[/bold]

        Only branches beginning with one of the supplied prefixes
        will be considered.

        This option may be specified multiple times.

        Examples:

        --prefix feature/
        --prefix release/
        --prefix hotfix/

        [dim blue]Default:[/dim blue]
        No prefixes.

        When no prefixes are configured,
no branches are eligible for cleanup.
        """,
        rich_help_panel="Cleanup Branches Options",
    ),
]
MergeStatusOption = Annotated[
    MergeStatusChoices,
    typer.Option(
        "--merge-status",
        "-ms",
        help="""
        [bold]Merge status filter[/bold]

        Select which branches should be considered.

        [bold yellow]merged[/bold yellow]
        Only merged branches.

        [bold yellow]unmerged[/bold yellow]
        Only unmerged branches.

        [bold yellow]all[/bold yellow]
        Consider every branch.

        [dim blue]Default:[/dim blue]
        merged
        """,
        rich_help_panel="Cleanup Branches Options",
        case_sensitive=False,
    ),
]
MaxAgeOption = Annotated[
    Optional[str],
    typer.Option(
        "--max-age",
        "-ma",
        help="""
        [bold]Maximum branch age[/bold]

        Only branches older than the supplied duration
        will be considered.

        Supported units:

        • m   minutes
        • h   hours
        • d   days
        • w   weeks
        • mo  months
        • y   years

        Examples:

        30d
        2w
        6mo
        1y

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Cleanup Branches Options",
    ),
]
BeforeOption = Annotated[
    Optional[str],
    typer.Option(
        "--before",
        "-b",
        help="""
        [bold]Latest commit date[/bold]

        Only branches whose latest commit occurred before the
        supplied date will be considered.

        Date format:

        YYYY-MM-DD

        Examples:

        2026-07-01
        2025-12-31

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Cleanup Branches Options",
    ),
]


# =========================================================
# 🟢 COMMIT OPTIONS
# =========================================================
CommitMessageBackupDirOption = Annotated[
    Optional[Path],
    typer.Option(
        "--backup-commit-dir", "-bcd",
        help="""
        [bold]Commit backup directory[/bold]

        Directory where commit template backups are stored.

        [dim blue]Default:[/dim blue]
        tools/custy/templates/backups/commit

        [dim]Behavior:[/dim]
        Created automatically when missing.

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.cli.templates.directory.backups_commit'
        """,
        rich_help_panel="Commit • Backup",
        autocompletion=completion_commit_message_backup_dir,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        writable=True,
    ),
]


# =========================================================
# 🔵 TAG OPTIONS
# =========================================================
TagMessageBackupDirOption = Annotated[
    Optional[Path],
    typer.Option(
        "--backup-tag-dir", "-btd",
        help="""
        [bold]Tag backup directory[/bold]

        Directory where tag template backups are stored.

        [dim blue]Default:[/dim blue]
        tools/custy/templates/backups/tag

        [dim]Behavior:[/dim]
        Created automatically when missing.

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.cli.templates.directory.backups_tag'
        """,
        rich_help_panel="Tag • Backup",
        autocompletion=completion_tag_message_backup_dir,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        writable=True,
    ),
]


# ---------------------------
# EXECUTION OPTIONS
# ---------------------------
DryRunOption = Annotated[
    bool,
    typer.Option(
        "--dry-run/--no-dry-run", "-dr/-Dr",
        help="""
        [bold yellow]Dry run mode[/bold yellow]

        Scan backup files and Git branches without deleting local or remote resources.

        Matching cleanup candidates are reported to the console.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]

# app/cli/commands/backup/options.py

import typer

from typing import Annotated, Optional
from pathlib import Path

from app.cli.constants import (
    LogLevelChoices,
    completion_commit_message_file,
    completion_tag_message_file,
    completion_commit_message_backup_dir,
    completion_tag_message_backup_dir,
)

# =========================================================
# 🟢 COMMIT OPTIONS
# =========================================================
CommitMessageFileOption = Annotated[
    Optional[Path],
    # typer.Argument(
    typer.Option(
        "--commit-msg-file", "-cmsg",
        help="""
        [bold]Commit message template[/bold]

        Path to the commit message template file to back up.

        [dim blue]Default:[/dim blue]
        templates/custy/commit-message.txt

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.cli.templates.file.commit_message'
        """,
        rich_help_panel="Commit • Files",
        autocompletion=completion_commit_message_file,
        exists=True,
        file_okay=True,
        resolve_path=True,
    ),
]
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
TagMessageFileOption = Annotated[
    Optional[Path],
    typer.Option(
        "--tag-msg-file", "-tmsg",
        help="""
        [bold]Tag message template[/bold]

        Path to the tag message template file to back up.

        [dim blue]Default:[/dim blue]
        templates/custy/tag-message.txt

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.cli.templates.file.tag_message'
        """,
        rich_help_panel="Tag • Files",
        autocompletion=completion_tag_message_file,
        exists=True,
        file_okay=True,
        resolve_path=True,
    ),
]
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

        Inspect backup sources and destinations without creating or pruning backup files.

        Planned backup operations are reported to the console.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]

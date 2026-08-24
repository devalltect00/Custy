# app/cli/commands/changelog/options.py

import typer

from typing import Annotated, Optional
from pathlib import Path

from app.cli.constants import (
  LogLevelChoices,
  completion_commit_message_file,
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

        Path to the commit message template used when parsing and classifying commit messages.

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


# =========================================================
# 🟢 CHANGELOG OPTIONS
# =========================================================
ForceOption = Annotated[
    bool,
    typer.Option(
        "--force/--no-force", "-f/-F",
        help="""
        [bold red]Force regeneration[/bold red]

        Force changelog generation even when an existing changelog is already present.

        Useful when:

        • Rebuilding release history

        • Updating templates

        • Regenerating release notes

        [dim blue]Default:[/dim blue] False

        [dim]Variable:[/dim]
        'tool.custy.cli.changelog.force_generation'
        """,
        rich_help_panel="Changelog • Behavior",
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

        Render a changelog preview without writing CHANGELOG.md.

        Git history and configured templates are still read so the preview reflects the current repository.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]

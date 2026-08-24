# app/cli/commands/init/options.py

import typer

from typing import Annotated, Optional
from pathlib import Path

from app.cli.constants.completions import completion_initialization_mode
from app.cli.constants import (
  LogLevelChoices,
)
from app.cli.constants import InitMode

# =========================================================
# 🟢 INITIALIZATION OPTIONS
# =========================================================
ModeOption = Annotated[
    InitMode,
    typer.Option(
        ...,
        "--mode", "-m",
        help="""
        [bold]Initialization Mode[/bold]

        Choose which resources should be generated.

        [bold yellow]•[/bold yellow] [bold]all[/bold]
        Initialize configuration, templates, and examples.

        [bold yellow]•[/bold yellow] [bold]all_no_examples[/bold]
        Initialize configuration and templates only.

        [bold yellow]•[/bold yellow] [bold]config[/bold]
        Initialize configuration files only.

        [bold yellow]•[/bold yellow] [bold]templates[/bold]
        Initialize commit and tag message templates only.

        [bold yellow]•[/bold yellow] [bold]examples[/bold]
        Initialize example resources only.

        [dim bright_green]Recommended:[/dim bright_green] all

        [dim]Useful when setting up a project for the first time.[/dim]
        """,
        rich_help_panel="Initialization • Executions",
        autocompletion=completion_initialization_mode,
        case_sensitive=False,
    ),
]
ForceOption = Annotated[
    bool,
    typer.Option(
        "--force/--no-force", "-f/-F",
        help="""
        [bold red]Force Initialization[/bold red]

        Overwrite existing files and directories without asking for confirmation.

        Use with caution when reinitializing an existing project.
        """,
        rich_help_panel="Initialization • Behavior",
    ),
]
AskOption = Annotated[
    bool,
    typer.Option(
        "--ask", "-a",
        help="""
        [bold yellow]Interactive Mode[/bold yellow]

        Prompt before creating or overwriting files and directories.

        Useful when reviewing initialization changes manually.

        """,
        rich_help_panel="Initialization • Behavior",
    ),
]

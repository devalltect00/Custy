# app/cli/commands/main/options.py

import typer

from typing import Annotated, Optional, List
from pathlib import Path

from app.cli.constants import LogLevelChoices
from app.cli.utils import version_callback

# ---------------------------
# 🧩 APPLICATION OPTIONS
# ---------------------------
NoBannerOption = Annotated[
    bool,
    typer.Option(
        "--no-banner",
        help="""
        [bold]Disable startup banner[/bold]

        Hide the Custy banner during command execution.

        Useful for:

        • CI/CD environments
        • Automated scripts
        • Cleaner console output

        [dim blue]Default:[/dim blue] False
        """,
    ),
]
HelpOption = Annotated[
    bool,
    typer.Option(
        "--help", "-h",
        help="Show help",
    ),
]
VersionOption = Annotated[
    bool | None,
    typer.Option(
        "--version", "-v",
        help="Display the installed Custy version and exit.",
        callback=version_callback,
    ),
]


# ---------------------------
# ⚙️ EXECUTION OPTIONS
# ---------------------------
DryRunOption = Annotated[
    bool,
    typer.Option(
        "--dry-run/--no-dry-run", "-dr/-Dr",
        help="""
        [bold yellow]Dry run mode[/bold yellow]

        Preview the command without applying its intended project, Git, or remote changes.

        Read-only discovery may still run, including file inspection, Git queries, and configured remote queries.

        File writes, deletions, editor launches, Git mutations, and remote mutations are simulated.

        Useful for:

        • Testing workflows
        • Verifying release pipelines
        • Debugging command execution

        [dim]Normal diagnostic logs may still be written.[/dim]

        [dim blue]Default:[/dim blue] False
        """,
        rich_help_panel="Global • Execution",
    ),
]


# ---------------------------
# 📝 LOGGING OPTIONS
# ---------------------------
DebugOption = Annotated[
    bool,
    typer.Option(
        "--debug/--no-debug", "-dbg/-Dbg",
        help="""
        [bold yellow]Debug mode[/bold yellow]

        Enable detailed diagnostic output.

        Useful when troubleshooting:

        • Workflow execution
        • Pipeline behavior
        • Configuration issues
        • Validation failures
        """,
        rich_help_panel="Global • Debug",
    ),
]
LogLevelOption = Annotated[
    LogLevelChoices,
    typer.Option(
        "--log-level", "-ll",
        help="""
        [bold]Logging level[/bold]

        Control logging verbosity.

        [bold yellow]•[/bold yellow] [bold]critical[/bold]
        Critical errors only

        [bold yellow]•[/bold yellow] [bold]error[/bold]
        Errors only

        [bold yellow]•[/bold yellow] [bold]warning[/bold]
        Warnings and errors

        [bold yellow]•[/bold yellow] [bold]info[/bold]
        General information (default)

        [bold yellow]•[/bold yellow] [bold]debug[/bold]
        Detailed diagnostics

        [dim blue]Default:[/dim blue] info

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.logging.level'
        """,
        rich_help_panel="Global • Debug",
        case_sensitive=False,
    ),
]

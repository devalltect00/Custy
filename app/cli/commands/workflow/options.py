# app/cli/commands/workflow/options.py

from typing import Annotated, Optional

import typer

from app.cli.constants import (
    LogLevelChoices,
    completion_tag,
)
from app.cli.utils import (
    validate_tag,
)

# ---------------------------
# BRANCH WORKFLOW OPTIONS
# ---------------------------
EnforceOption = Annotated[
    bool,
    typer.Option(
        "--enforce",
        "-enf",
        help="""
        [bold red]Enforce workflow policies[/bold red]

        Enforce Branch and Tag Strategy.

        Apply configured branch and version workflow rules.

        When enabled, Custy may reject transitions that violate workflow policies.

        [dim blue]Default:[/dim blue] False

        [dim yellow]HINT:[/dim yellow]
        Use validation mode first before enabling enforcement.
        """,
    ),
]
CheckTransitionOption = Annotated[
    bool,
    typer.Option(
        "--check_transition",
        "-ct",
        help="""
        [bold]Validate transitions[/bold]

        Validate branch and version transitions without enforcing workflow actions.

        Useful for testing workflow rules and release readiness.

        [dim blue]Default:[/dim blue] False
        """,
    ),
]
FromBranchOption = Annotated[
    Optional[str],
    typer.Option(
        "--from-branch",
        "-fb",
        help="""
        [bold]Source branch override[/bold]

        Manually specify the source branch used during transition validation.

        Examples:

        develop
        release
        main

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Tag and Branch Override Options",
    ),
]
ToBranchOption = Annotated[
    Optional[str],
    typer.Option(
        "--to-branch",
        "-tb",
        help="""
        [bold]Target branch override[/bold]

        Manually specify the destination branch used during transition validation.

        Examples:

        release
        main

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Tag and Branch Override Options",
    ),
]
FromTagOption = Annotated[
    Optional[str],
    typer.Option(
        "--from-tag",
        "-ft",
        help="""
        [bold]Source version override[/bold]

        Manually specify the starting version used during transition validation.

        Examples:

        v1.2.0
        1.2.0rc1

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Tag and Branch Override Options",
        metavar="X.Y.Z",
        callback=validate_tag,
        autocompletion=completion_tag,
    ),
]
ToTagOption = Annotated[
    Optional[str],
    typer.Option(
        "--to-tag",
        "-tt",
        help="""
        [bold]Target version override[/bold]

        Manually specify the destination version used during transition validation.

        Examples:

        v1.3.0
        1.3.0rc1

        [dim]Optional.[/dim]
        """,
        rich_help_panel="Tag and Branch Override Options",
        metavar="X.Y.Z",
        callback=validate_tag,
        autocompletion=completion_tag,
    ),
]

# ---------------------------
# SYNC and BACKUPS OPTIONS
# ---------------------------
SyncBackupOption = Annotated[
    bool,
    typer.Option(
        "--sync-backup",
        "-sb",
        help="""
        [bold]Synchronize backup remotes[/bold]

        Push workflow-related updates to configured backup remotes.

        Useful when maintaining mirrored repositories.

        [dim blue]Default:[/dim blue] False

        [dim]Variable:[/dim]
        'tool.custy.workflow.sync_backup'
        """,
    ),
]

# ---------------------------
# EXECUTION OPTIONS
# ---------------------------
DryRunOption = Annotated[
    bool,
    typer.Option(
        "--dry-run/--no-dry-run",
        "-dr/-Dr",
        help="""
        [bold yellow]Dry run mode[/bold yellow]

        Preview workflow transitions without applying branch, tag, merge, push, or cleanup mutations.

        Read-only transition discovery and validation may still run.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]
DebugOption = Annotated[
    bool,
    typer.Option(
        "--debug/--no-debug",
        "-dbg/-Dbg",
        help="""
        [bold yellow]Debugging mode[/bold yellow]

        [green]Show[/green]/[blue]Hide[/blue] debug message.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]
LogLevelOption = Annotated[
    LogLevelChoices,
    typer.Option(
        "--log-level",
        "-ll",
        help="""
        [bold]Logging level[/bold]

        Control verbosity of logs

        [bold yellow]•[/bold yellow] [bold]critical[/bold] → only critical errors\n
        [bold yellow]•[/bold yellow] [bold]error[/bold]    → errors only\n
        [bold yellow]•[/bold yellow] [bold]warning[/bold]  → warnings + errors\n
        [bold yellow]•[/bold yellow] [bold]info[/bold]     → general info (default\n
        [bold yellow]•[/bold yellow] [bold]debug[/bold]    → detailed debugging\n

        [dim blue]Default:[/dim blue] info

        [dim yellow]HINT:[/dim yellow] better using .custy.toml configuration.
        [dim]Variable:[/dim] 'tool.custy.logging.level'
        """,
        rich_help_panel="CLI and Execution Options",
        case_sensitive=False,
    ),
]

# app/cli/commands/version/options.py

from pathlib import Path
from typing import Annotated, Optional

import typer

from app.cli.constants import (
    BumpChoices,
    StrategyChoices,
    completion_tag,
    completion_version_file,
)
from app.cli.utils import (
    validate_tag,
)

# =========================================================
# 🔵 TAG OPTIONS
# =========================================================
VersionFileOption = Annotated[
    Optional[Path],
    typer.Option(
        "--version-file",
        "-vf",
        help="""
        [bold]Version file[/bold]

        Path to the version file that will be updated.

        Examples:

        • app/**version**.py
        • src/**version**.py

        [dim blue]Default:[/dim blue]
        app/**version**.py

        [dim yellow]HINT:[/dim yellow]
        Prefer configuring this in config.toml.

        [dim]Variable:[/dim]
        'tool.custy.cli.paths.version_file'
        """,
        rich_help_panel="Tag • Files",
        autocompletion=completion_version_file,
        exists=True,
        file_okay=True,
        resolve_path=True,
    ),
]
StrategyOption = Annotated[
    Optional[StrategyChoices],
    typer.Option(
        "--strategy",
        help="""
        [bold]Versioning strategy[/bold]

        Determine how versions are generated.

        Supported strategies:

        [bold yellow]•[/bold yellow] [bold]semver[/bold]
        Semantic Versioning (v1.2.3)

        [bold yellow]•[/bold yellow] [bold]pep440[/bold]
        Python PEP 440 versions (1.2.3rc1)

        [bold yellow]•[/bold yellow] [bold]date[/bold]
        Date-based versions

        [bold yellow]•[/bold yellow] [bold]gitcount[/bold]
        Versions derived from commit count

        [bold yellow]•[/bold yellow] [bold]commitizen[/bold]
        Versions inferred from commit history

        [dim bright_blue]Note:[/dim bright_blue]
        CLI values override configuration and auto-detection.

        [dim bright_green]Suggested:[/dim bright_green]
        Use project auto-detection when possible.
        """,
        rich_help_panel="Tag • Versioning",
        case_sensitive=False,
    ),
]
BumpOption = Annotated[
    Optional[BumpChoices],
    typer.Option(
        "--bump",
        help="""
        [bold]Version bump level[/bold]

        Auto bump from latest tag. Version bump level (Semver bump level when using --strategy=semver. use 'auto' only with --strategy=commitizen)

        [bold yellow]•[/bold yellow] [bold]patch[/bold] [yellow]→[/yellow] bug fixes\n
        [bold yellow]•[/bold yellow] [bold]minor[/bold] [yellow]→[/yellow] new features\n
        [bold yellow]•[/bold yellow] [bold]major[/bold] [yellow]→[/yellow] breaking changes\n
        [bold yellow]•[/bold yellow] [bold]auto[/bold]  [yellow]→[/yellow] auto-detect (commitizen only)

        [dim]Used with:[/dim] --strategy=semver
        """,
        rich_help_panel="Tag • Versioning",
        case_sensitive=False,
    ),
]
TagOption = Annotated[
    Optional[str],
    typer.Option(
        "--tag",
        help=(
            "Manually specify a stable or lifecycle tag "
            "[magenta]([dim]e.g.[/dim] v1.2.3, v1.2.3-rc.1, or 1.2.3rc1)[/magenta]"
        ),
        rich_help_panel="Tag • Versioning",
        metavar="VERSION",
        callback=validate_tag,
        autocompletion=completion_tag,
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

        Resolve the intended version without updating project files or version metadata.

        Read-only project and Git discovery may still run.
        """,
        rich_help_panel="CLI and Execution Options",
    ),
]

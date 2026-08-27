# app/cli/commands/validate/options.py

from pathlib import Path
from typing import Annotated, Optional

import typer

from app.cli.constants import (
    StageModeChoices,
    completion_commit_message_file,
    completion_tag_message_file,
    completion_version_file,
)

# =========================================================
# 🟢 COMMIT OPTIONS
# =========================================================
CheckCzOption = Annotated[
    bool,
    typer.Option(
        "--check-cz",
        "-cz",
        help="""
        [bold]Commitizen Validation[/bold]

        Validate Commitizen configuration and integration.

        Useful when using Commitizen-based versioning workflows.

        [dim blue]Default:[/dim blue] False

        [dim bright_blue]Requirements:[/dim bright_blue]
        Commitizen must be installed and configured.

        [dim yellow]HINT:[/dim yellow]
        Enable this only if your project uses Commitizen.

        [dim]Variable:[/dim]
        'tool.custy.cli.execution.check_cz'
        """,
        rich_help_panel="Commit • Validation",
    ),
]
AutoStageOption = Annotated[
    bool,
    typer.Option(
        "--auto-stage",
        "-as",
        help="""
        [bold]Auto Stage[/bold]

        Automatically stage files before validation workflows when required.

        Useful when validation depends on staged changes.

        [dim blue]Default:[/dim blue] False

        [dim yellow]HINT:[/dim yellow]
        Most users can leave this disabled.

        [dim]Variable:[/dim]
        'tool.custy.cli.execution.auto_stage'
        """,
        rich_help_panel="Commit • Staging",
    ),
]
StageModeOption = Annotated[
    Optional[StageModeChoices],
    typer.Option(
        "--stage-mode",
        "-sm",
        help="""
        [bold]Stage Mode[/bold]

        Defines how files are auto-staged. Mode:

        [bold yellow]•[/bold yellow] [bold]all[/bold]       [yellow]→[/yellow] [italic black on white]git add .[/italic black on white] [dim]Tip:[/dim] (stage all changes including new files)\n
        [bold yellow]•[/bold yellow] [bold]update[/bold]    [yellow]→[/yellow] [italic black on white]git add --update`[/italic black on white] [dim]Tip:[/dim] (stage only modified/deleted tracked files)

        [dim blue]Default:[/dim blue] all

        [dim]Used only when auto-stage is enabled.[/dim]

        [dim bright_blue]Note:[/dim bright_blue]
        Optional.

        [dim bright_blue]Note:[/dim bright_blue] This is optional.
        """,
        rich_help_panel="Commit • Staging",
        case_sensitive=False,
    ),
]
CommitMessageFileOption = Annotated[
    Optional[Path],
    # typer.Argument(
    typer.Option(
        "--commit-msg-file",
        "-cmsg",
        help="""
        [bold]Commit message file[/bold]

        Path to the file used for commit message.

        [dim blue]Default:[/dim blue] templates/custy/commit-message.txt
        [dim]Tip:[/dim] Will open in editor before commit

        [dim yellow]HINT:[/dim yellow] better using .custy.toml configuration.
        [dim]Variable:[/dim] 'tool.custy.cli.templates.commit_message'
        """,
        rich_help_panel="Commit • Files",
        autocompletion=completion_commit_message_file,
        exists=True,
        file_okay=True,
        resolve_path=True,
    ),
]


# =========================================================
# 🔵 TAG OPTIONS
# =========================================================
TagMessageFileOption = Annotated[
    Optional[Path],
    typer.Option(
        "--tag-msg-file",
        "-tmsg",
        help="""
        [bold]Tag message file[/bold]

        File used as tag annotation message.
        Path to the file used for create tag with message.

        [dim blue]Default:[/dim blue] templates/custy/tag-message.txt
        [dim]Tip:[/dim] Will open in editor before create tag

        [dim yellow]HINT:[/dim yellow] better using .custy.toml configuration.
        [dim]Variable:[/dim] 'tool.custy.cli.templates.tag_message'
        """,
        rich_help_panel="Tag • Files",
        autocompletion=completion_tag_message_file,
        exists=True,
        file_okay=True,
        resolve_path=True,
    ),
]
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

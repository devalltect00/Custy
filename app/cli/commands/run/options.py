# app/cli/commands/run/options.py

from pathlib import Path
from typing import Annotated, Optional

import typer

from app.cli.constants import (
    BumpChoices,
    StageModeChoices,
    StepChoices,
    StrategyChoices,
    completion_commit_message_backup_dir,
    completion_commit_message_file,
    completion_meta,
    completion_remote_name,
    completion_steps,
    completion_tag,
    completion_tag_message,
    completion_tag_message_backup_dir,
    completion_tag_message_file,
    completion_version_file,
)
from app.cli.utils import (
    validate_steps,
    validate_tag,
)

# =========================================================
# 🧠 STEPS ARGUMENT (CRITICAL UX ENTRY POINT)
# =========================================================
StepsArgument = Annotated[
    Optional[list[StepChoices]],
    typer.Argument(
        ...,
        help="""
        [bold]Workflow Steps / Profiles[/bold]

        Select one or more workflow steps, or use a predefined profile.

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]🚀 Workflow Profiles[/bold yellow]

        [green]dev[/green]

        → Daily development workflow

        → commit + push

        [yellow]release[/yellow]

        → Standard release workflow

        → commit + tag + push

        [bold red]full[/bold red]

        → Complete release lifecycle

        → release + changelog + backups + cleanup + workflow actions

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]🔹 Core Steps[/bold yellow]

        [green]validate[/green]
        → Validate project readiness

        [green]commit[/green]
        → Create structured commit

        [green]tag[/green]
        → Generate release tag

        [green]push[/green]
        → Push commits and tags

        [green]changelog[/green]
        → Generate CHANGELOG.md

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]📦 Backup Steps[/bold yellow]

        [yellow]backup-commit[/yellow]
        → Backup commit template

        [yellow]backup-tag[/yellow]
        → Backup tag template

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]🧹 Cleanup Steps[/bold yellow]

        [magenta]cleanup-backups[/magenta]
        → Remove old template backups

        [magenta]cleanup-branches[/magenta]
        → Remove stale branches

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]⚙ Workflow Step[/bold yellow]

        [cyan]workflow[/cyan]

        → Execute workflow transition logic

        [dim]
        Experimental / under active development.
        Behavior may change between releases.
        [/dim]

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [bold yellow]⚡ Examples[/bold yellow]

        custy run dev

        custy run release

        custy run full

        custy run commit tag

        custy run commit tag push

        custy run validate commit tag push changelog

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        [dim]Notes:[/dim]

        • Steps execute sequentially

        • Profiles expand into predefined step lists

        • Validation is included automatically where required

        • Profiles are recommended for most users

        [dim]Tip:[/dim]

        Use [cyan]dev[/cyan] for daily work and [yellow]release[/yellow] for releases.
        """,
        autocompletion=completion_steps,
        callback=validate_steps,
    ),
]


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

        Check commit and tag message using commitizen

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

        Auto run `git add` command

        [dim blue]Default:[/dim blue] False

        [dim yellow]HINT:[/dim yellow] better using .custy.toml configuration.
        [dim]Variable:[/dim] 'tool.custy.cli.execution.auto_stage'
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
        [bold]Commit message template[/bold]

        Path to the commit message template file used for commit message.

        [dim blue]Default:[/dim blue]
        templates/custy/commit-message.txt

        [dim]Tip:[/dim]
        Will open in editor before commit

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
ForceCommitOption = Annotated[
    bool,
    typer.Option(
        "--allow-empty-commit/--no-allow-empty-commit",
        "-aec/-Aec",
        help="""
        [bold red]Force commit[/bold red]

        Allow commit even if:
        - No staged changes

        Creates an empty commit if needed.

        [dim yellow]HINT:[/dim yellow] Useful for repo with no commit (first commit)
        """,
        rich_help_panel="Commit • Behavior",
    ),
]
CommitMessageBackupDirOption = Annotated[
    Optional[Path],
    typer.Option(
        "--backup-commit-dir",
        "-bcd",
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
        "--tag-msg-file",
        "-tmsg",
        help="""
        [bold]Tag message template[/bold]

        Path to the template used when generating annotated Git tags.

        [dim blue]Default:[/dim blue]
        templates/custy/tag-message.txt

        [dim]Tip:[/dim]
        Will open in editor before create tag

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
        help="Manually specify tag [magenta]([dim]e.g.[/dim] v1.2.3 or 1.2.3)[/magenta]",
        rich_help_panel="Tag • Versioning",
        metavar="X.Y.Z",
        callback=validate_tag,
        autocompletion=completion_tag,
    ),
]
TagMessageOption = Annotated[
    Optional[str],
    typer.Option(
        "--tag-message",
        help="Message for the Git tag [bright_blue]([dim blue]Default:[/dim blue] same as tag name)[/bright_blue]",
        rich_help_panel="Tag • Versioning",
        autocompletion=completion_tag_message,
    ),
]
PreReleaseOption = Annotated[
    Optional[str],
    typer.Option(
        "--pre",
        help="Optional Pre-release label [magenta]([dim]e.g.[/dim] alpha, beta, rc, dev, next, preview, etc)[/magenta]",
        rich_help_panel="Tag • Versioning",
    ),
]
PostReleaseOption = Annotated[
    bool,
    typer.Option(
        "--post",
        help="Mark this version as post-release",
        rich_help_panel="Tag • Versioning",
    ),
]
DevReleaseOption = Annotated[
    bool,
    typer.Option(
        "--dev",
        help="Mark this version as development release",
        rich_help_panel="Tag • Versioning",
    ),
]
MetaOption = Annotated[
    Optional[str],
    typer.Option(
        "--meta",
        help="Meta version label [magenta]([dim]e.g.[/dim] sha.abc123)[/magenta]",
        rich_help_panel="Tag • Versioning",
        autocompletion=completion_meta,
    ),
]
EpochOption = Annotated[
    int,
    typer.Option(
        "--epoch",
        help="Set version epoch [magenta]([dim]e.g.[/dim] 1!1.2.3)[/magenta]",
        rich_help_panel="Tag • Versioning",
    ),
]
ForceTagOption = Annotated[
    bool,
    typer.Option(
        "--force-tag/--no-force-tag",
        "-ft/-Ft",
        help="""
        [bold red]Force tag creation[/bold red]

        Allow tag creation even when validation checks would normally prevent it.

        Use with caution.

        [dim blue]Default:[/dim blue] False

        [dim]Variable:[/dim]
        'tool.custy.cli.execution.force_tag'
        """,
        rich_help_panel="Tag • Behavior",
    ),
]
SkipChecksOption = Annotated[
    bool,
    typer.Option(
        "--skip-checks",
        help="Skip branching[yellow]→[/yellow]tag transition validation (for advanced users).",
        rich_help_panel="Tag • Behavior",
    ),
]
TagMessageBackupDirOption = Annotated[
    Optional[Path],
    typer.Option(
        "--backup-tag-dir",
        "-btd",
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


# =========================================================
# 🔴 PUSH OPTIONS
# =========================================================
AllRemoteOption = Annotated[
    bool,
    typer.Option(
        "--all-remote",
        "-ar",
        help="""
        [bold]Push to all configured remotes.[/bold]

        When enabled, Custy pushes commits and eligible tags to the
        de-duplicated main and backup remote groups.

        [dim blue]Default:[/dim blue]
        Configured from config.toml

        [dim]Variable:[/dim]
        'tool.custy.cli.push.all_remote'

        [dim yellow]HINT:[/dim yellow]
        An explicit --remote value takes priority over this option.
        """,
        rich_help_panel="Push • Execution",
    ),
]
RemoteOption = Annotated[
    Optional[str],
    typer.Option(
        "--remote",
        "-r",
        help="""
        [bold]Remote Name[/bold]

        Select exactly one remote. This overrides --all-remote, push_to,
        and the configured remote groups.

        [dim blue]Default:[/dim blue]
        Resolved from tool.custy.git.default_remote and the configured groups.
        """,
        rich_help_panel="Push • Execution",
        autocompletion=completion_remote_name,
    ),
]
SkipTagOption = Annotated[
    bool,
    typer.Option(
        "--skip-tag",
        "-st",
        help="""
        [bold]Skip Tag[/bold]

        Push HEAD without creating or pushing a tag in combined workflows.

        [dim blue]Default:[/dim blue] False

        [dim yellow]HINT:[/dim yellow] Configure the default in config.toml.
        [dim]Variable:[/dim] 'tool.custy.cli.push.skip_tag'
        """,
        rich_help_panel="Push • Behavior",
    ),
]
SyncBackupOption = Annotated[
    bool,
    typer.Option(
        "--sync-backup",
        "-sb",
        help="""
        [bold]Sync Backup Remote[/bold]

        Add configured backup remotes to a main-group push. Backup targets
        remain skipped on non-critical feature, CI, and sandbox branches.

        [dim blue]Default:[/dim blue] False

        [dim yellow]HINT:[/dim yellow] Configure backup remotes before enabling.
        [dim]Variable:[/dim] 'tool.custy.cli.push.sync_backup'
        """,
        rich_help_panel="Push • Behavior",
    ),
]

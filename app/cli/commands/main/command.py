# app/cli/commands/main/command.py

import logging
import sys

import typer
import typer.rich_utils

from app.cli.commands.main.options import (
    DebugOption,
    DryRunOption,
    HelpOption,
    LogLevelOption,
    NoBannerOption,
    VersionOption,
)
from app.cli.commands.main.resolver import resolve_main_args
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context

# from app.cli.commands import push, misc
from app.cli.utils import banner
from app.config.config_loader import get_config
from app.utils import setup_logging


def main(
    ctx: typer.Context,
    no_banner: NoBannerOption = None,
    help: HelpOption = None,
    version: VersionOption = None,
    dry_run: DryRunOption = None,
    debug: DebugOption = None,
    log_level: LogLevelOption = None,
):
    """
    🚀 [bold cyan]Custy — Release Automation Platform[/bold cyan]

    Automate versioning, changelog generation, release workflows,
    Git operations, project initialization, validation, backups,
    cleanup tasks, and workflow orchestration.

    [dim]Built for consistent releases, automation, and developer productivity.[/dim]

    ────────────────────────────────────────

    ⚡ [bold]Quick Start[/bold]

    1. Initialize your project

       [yellow]custy init[/yellow]

    2. Validate your setup

       [yellow]custy validate[/yellow]

    3. Run your first workflow

       [yellow]custy run release[/yellow]

    ────────────────────────────────────────

    🚀 [bold]Recommended Commands[/bold]

    [green]custy run dev[/green]

    ```
      Daily development workflow

      commit → push
    ```

    [green]custy run release[/green]

    ```
      Standard release workflow

      commit → tag → push
    ```

    [green]custy run full[/green]

    ```
      Complete release lifecycle

      release → changelog → backup → cleanup
    ```

    ────────────────────────────────────────

    📦 [bold]Core Commands[/bold]

    [yellow]custy init[/yellow]
    Initialize configuration, templates, and examples

    [yellow]custy validate[/yellow]
    Validate project readiness

    [yellow]custy commit[/yellow]
    Create a structured commit

    [yellow]custy tag[/yellow]
    Create release tags

    [yellow]custy push[/yellow]
    Push commits and tags

    [yellow]custy run[/yellow]
    Execute workflow pipelines

    ────────────────────────────────────────

    🧩 [bold]Release Management[/bold]

    [yellow]custy version[/yellow]
    Synchronize project versions

    [yellow]custy changelog[/yellow]
    Generate release notes and CHANGELOG.md

    ────────────────────────────────────────

    🛠️ [bold]Project Maintenance[/bold]

    [yellow]custy backup[/yellow]
    Backup message templates

    [yellow]custy cleanup[/yellow]
    Remove stale backups and branches

    ────────────────────────────────────────

    ⚙️ [bold]Advanced Features[/bold]

    [yellow]custy workflow[/yellow]

    ```
      Branch and release workflow management

      ⚠ Experimental / Beta
    ```

    ────────────────────────────────────────

    🌐 [bold]Global Options[/bold]

    Global options are specified before commands.

    [yellow]custy --dry-run run release[/yellow]

    ```
      Preview the workflow without applying its intended project,
      Git, or remote changes. Read-only discovery may still run.
    ```

    [yellow]custy --debug commit[/yellow]

    [yellow]custy --log-level debug tag[/yellow]

    ────────────────────────────────────────

    ❓ [bold]Need Help?[/bold]

    View command help:

    ```
      [yellow]custy run --help[/yellow]

      [yellow]custy tag --help[/yellow]

      [yellow]custy workflow --help[/yellow]
    ```

    ────────────────────────────────────────

    💡 [bold]Tip[/bold]

    Most users should use:

    ```
      [green]custy run release[/green]
    ```

    instead of executing commit, tag, and push manually.
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        no_banner=no_banner,
        help=help,
        version=version,
        dry_run=dry_run,
        debug=debug,
        log_level=log_level,
    )

    args = resolve_main_args(config=config, cli_args=cli_args)

    # if debug == None:
    #     temp_debug=False
    # else:
    #     temp_debug=not args.no_debug
    # setup_logging(debug=False)

    # ctx.obj = AppContext()
    # ctx.obj.dry_run = args.dry_run
    # if debug:
    #     ctx.obj.debug = not args.no_debug

    # store global flags into context
    app_ctx = get_context(ctx=ctx)
    app_ctx.dry_run = args.dry_run
    # app_ctx.debug = not args.no_debug if debug else args.no_debug
    app_ctx.debug = not args.no_debug
    app_ctx.log_level = args.log_level

    setup_logging(level=args.log_level, debug=app_ctx.debug)

    ctx.obj = app_ctx

    # print("app_ctx",app_ctx)

    if help:
        if not no_banner:
            banner.show()
        # typer.echo(ctx.get_help())
        # command = get_command(app)
        # console.print(command.get_help(ctx))
        # console.print(command.get_help(ctx))
        typer.echo(ctx.get_help())
        raise typer.Exit(
            code=0,
        )

    if not no_banner:
        banner.show()

    if ctx.invoked_subcommand is None:
        # console.print(ctx.get_help())
        typer.echo(ctx.get_help())
        raise typer.Exit(
            code=0,
        )

    full_command = " ".join(sys.argv[1:])
    logger = logging.getLogger("main")
    logger.debug("[cyan]CLI COMMAND[/cyan] | [dim]custy %s[/dim]", full_command)

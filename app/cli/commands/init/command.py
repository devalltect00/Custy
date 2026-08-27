# app/cli/commands/init/command.py

from types import SimpleNamespace

import typer

from app.cli.commands.init.options import (
    AskOption,
    ForceOption,
    ModeOption,
)

# from app.core.initialize.generate import ScaffoldGenerator
from app.cli.commands.init.resolver import resolve_init_args
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.pipeline.builder import SimplePipelineBuilder

# from app.services import InitService
from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.step_registry import register_all_steps

app = typer.Typer()


class InitContext:
    def __init__(self, args):
        self.args = args

        # minimal engine compatibility
        self.engine = SimpleNamespace(no_debug=not getattr(args, "debug", False))


def _run_init_pipeline(args, commands: list[str]):
    """
    Shared cleanup branch pipeline runner.
    """

    register_all_steps()

    resolver = CommandResolver()

    # 🔥 Single unified step
    pipeline_config = resolver.resolve(commands)

    ctx_obj = InitContext(args)

    pipeline = SimplePipelineBuilder(useCompletedMessage=False).build(pipeline_config)
    pipeline.run(ctx_obj)


@app.callback(
    rich_help_panel="Initialization",
)

# @app.command("init")
def init(
    ctx: typer.Context,
    mode: ModeOption = None,
    force_init: ForceOption = None,
    ask: AskOption = None,
):
    """
    Initialize a project for Custy

    🚀 [bold cyan]Initialize your project[/bold cyan]

    Create the files and folders required to start using Custy.

    This command generates configuration files, templates, and optional example resources used throughout the Custy workflow.

    [dim]Safe to run multiple times. Existing files are preserved unless force mode is enabled.[/dim]

    ────────────────────────────────────────

    📦 [bold]What gets initialized:[/bold]

      • [green]Configuration files[/green]
        Create Custy configuration files.

      • [green]Templates[/green]
        Create commit and tag message templates.

      • [green]Examples[/green]
        Create example resources and sample files.

    ────────────────────────────────────────

    ⚙️ [bold]Initialization Modes:[/bold]

      [cyan]all[/cyan]
        Initialize configuration, templates, and examples.

      [cyan]all_no_examples[/cyan]
        Initialize everything except examples.

      [cyan]config[/cyan]
        Initialize configuration files only.

      [cyan]templates[/cyan]
        Initialize commit and tag templates only.

      [cyan]examples[/cyan]
        Initialize example resources only.

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy init[/yellow]
        Initialize configuration, templates, and examples.

      [yellow]custy init --mode all_no_examples[/yellow]
        Initialize configuration and templates only.

      [yellow]custy init --mode config[/yellow]
        Generate configuration files only.

      [yellow]custy init --mode templates[/yellow]
        Generate commit and tag templates only.

      [yellow]custy init --mode examples[/yellow]
        Generate example resources only.

      [yellow]custy init --force[/yellow]
        Overwrite existing files without prompting.

      [yellow]custy init --ask[/yellow]
        Prompt before overwriting existing files.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

    Global options are specified before the command.

      [yellow]custy --dry-run init[/yellow]
        Build and display the initialization plan without creating,
        copying, or overwriting project files and directories.

      [yellow]custy --debug init[/yellow]
        Show detailed execution logs.

      [yellow]custy --log-level debug init[/yellow]
        Enable verbose logging output.

    ────────────────────────────────────────

    💡 [bold]Recommended Workflow:[/bold]

      1. Run [cyan]custy init[/cyan]
      2. Review generated configuration files
      3. Adjust templates if needed
      4. Validate your project setup
      5. Start using Custy workflows

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy validate[/cyan]
        Validate project readiness.

      [cyan]custy run[/cyan]
        Execute workflow pipelines.

      [cyan]custy version[/cyan]
        Manage project versions.

    ────────────────────────────────────────

    💡 [bold]Tips:[/bold]

      • Safe to run multiple times
      • Use [yellow]custy --dry-run[/yellow] before applying changes
      • Use [yellow]custy init --mode[/yellow] to initialize specific parts only
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        mode=mode,
        force_init=force_init,
        ask=ask,
    )

    args = resolve_init_args(config=config, cli_args=cli_args)

    # ctx.obj = get_context()

    # # store global flags into context
    # ctx.obj.dry_run = args.dry_run
    # ctx.obj.debug = not args.no_debug if debug else args.no_debug
    # ctx.obj.log_level = args.log_level

    app_ctx = get_context(ctx)
    # app_ctx = AppContext()
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # initService = InitService(dry_run=args.dry_run, no_debug=not args.no_debug,)
    # generator = ScaffoldGenerator(force=args.force_init, interactive=args.ask,)

    # initService.run_init(ctx=ctx, generator=generator, mode=mode)
    # initService.run_init(ctx=app_ctx, generator=generator, mode=args.mode)

    combined_args = SimpleNamespace(
        **vars(args),
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
    )

    _run_init_pipeline(combined_args, ["init"])

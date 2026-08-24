# app/cli/commands/version/command.py

import typer
from types import SimpleNamespace

from app.config.config_loader import get_config
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context

from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.builder import SimplePipelineBuilder
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder

from app.cli.commands.version.resolver import resolve_version_args
from app.cli.commands.version.options import (
    VersionFileOption,
    StrategyOption,
    BumpOption,
    TagOption,
)

app = typer.Typer()

@app.callback(
    # rich_help_panel="(still in development)"
)
def callback():
    """
Version synchronization

🔄 [bold cyan]Version synchronization[/bold cyan]

Keep version references consistent across your project.

This command group manages version synchronization after tags or releases are created.

[dim]Version synchronization ensures that project files, version files, and release metadata all reference the same version.[/dim]

────────────────────────────────────────

📦 [bold]Available Commands:[/bold]

  [green]update[/green]
    Synchronize project version across configured files.

────────────────────────────────────────

🧩 [bold]Common Use Cases:[/bold]

  • Sync version after creating a tag
  • Update version files automatically
  • Keep release metadata consistent
  • Maintain version references across project files

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy version update[/yellow]
    Synchronize version using detected settings.

  [yellow]custy version update --tag v1.2.3[/yellow]
    Apply a specific version.

────────────────────────────────────────

💡 [bold]Recommended Workflow:[/bold]

  1. Create a tag
  2. Synchronize project versions
  3. Generate changelog
  4. Push changes

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy tag[/cyan]
    Create version tags.

  [cyan]custy changelog[/cyan]
    Generate release notes.

  [cyan]custy run release[/cyan]
    Execute a complete release workflow.
"""

@app.command("update")
def update(
    ctx: typer.Context,
    version_file: VersionFileOption = None,
    strategy: StrategyOption = None,
    bump: BumpOption = None,
    tag: TagOption = None,
):
    """
Synchronize project versions

🔄 [bold cyan]Synchronize project versions[/bold cyan]

Update version references across project files using a single version source.

This command is commonly used after creating a new tag to ensure all version references remain consistent.

[dim]Supports automatic strategy detection, manual version overrides, and project-specific version files.[/dim]

────────────────────────────────────────

🧩 [bold]What gets updated:[/bold]

  • [green]Version file[/green]
    Example: app/**version**.py

  • [green]Project metadata[/green]
    Example: pyproject.toml

  • [green]Version-related configuration[/green]
    Example: Commitizen configuration

────────────────────────────────────────

⚙️  [bold]Version Sources:[/bold]

  [cyan]--tag[/cyan]

    Use a specific version.

    Example:
      v1.2.3
      1.2.3

  [cyan]--strategy[/cyan]

    Generate version using a versioning strategy.

    Supported:
      • semver
      • pep440
      • date
      • gitcount
      • commitizen

  [cyan]--bump[/cyan]

    Generate the next version automatically.

    Supported:
      • patch
      • minor
      • major
      • auto

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy version update[/yellow]
    Synchronize versions using detected settings.

  [yellow]custy version update --tag v1.2.3[/yellow]
    Apply version v1.2.3.

  [yellow]custy version update --strategy semver --bump patch[/yellow]
    Generate the next patch version.

  [yellow]custy version update --strategy semver --bump minor[/yellow]
    Generate the next minor version.

  [yellow]custy version update --strategy commitizen --bump auto[/yellow]
    Determine the next version from commit history.

  [yellow]custy version update --version-file app/**version**.py[/yellow]
    Use a custom version file.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

Global options are specified before the command.

  [yellow]custy --dry-run version update[/yellow]
    Resolve the intended version and inspect project state without
    updating version files or project metadata.

  [yellow]custy --debug version update[/yellow]
    Show detailed execution logs.

  [yellow]custy --log-level debug version update[/yellow]
    Enable verbose logging output.

────────────────────────────────────────

💡 [bold]Recommended Usage:[/bold]

Version synchronization is commonly performed after:

  • Creating a tag
  • Completing a release
  • Updating release metadata
  • Preparing changelog generation

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy tag[/cyan]
    Create version tags.

  [cyan]custy changelog generate[/cyan]
    Generate release notes.

  [cyan]custy run release[/cyan]
    Execute a complete release workflow.
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        version_file=version_file,
        tag=tag,
        strategy=strategy,
        bump=bump,
    )

    args = resolve_version_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # =========================================
    # Merge args
    # =========================================
    combined_args = SimpleNamespace(
        **vars(args),  # ValidateArgs
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
    )

    # ✅ 1. Register steps (VERY IMPORTANT)
    register_all_steps()

    # ✅ 2. Resolve commands → pipeline config
    resolver = CommandResolver()
    config = resolver.resolve(["apply_version"])

    # ✅ 3. Create engine (inject CLI args here later)
    engine = (
        WorkflowEngineBuilder()
        # .from_cli_args(app_ctx)
        .from_cli_args(combined_args)
        .build())

    # ✅ 4. Create context
    ctx_obj = GitContext(engine)

    # ✅ 5. Build pipeline
    pipeline = SimplePipelineBuilder().build(config)

    # ✅ 6. Execute pipeline
    pipeline.run(ctx_obj)

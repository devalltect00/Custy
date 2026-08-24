# app/cli/commands/changelog/command.py

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

from app.cli.commands.changelog.resolver import resolve_changelog_args
from app.cli.commands.changelog.options import (
    CommitMessageFileOption,
    ForceOption,
)

app = typer.Typer()

@app.callback()
def callback():
    """
Changelog generation

📜 [bold cyan]Changelog generation[/bold cyan]

Generate release notes and update your project's changelog from Git history and structured commit messages.

Custy analyzes commits between releases and groups them into organized sections for easier release tracking.

────────────────────────────────────────

📦 [bold]Available Commands:[/bold]

  [green]generate[/green]
    Generate or update the changelog.

────────────────────────────────────────

🧩 [bold]Generated Content:[/bold]

  • Release notes

  • Version summaries

  • Features

  • Fixes

  • Refactors

  • Other supported commit categories

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy changelog generate[/yellow]
    Generate or update the changelog.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run changelog generate[/yellow]
    Read Git history and render the changelog preview without
    writing CHANGELOG.md.

  [yellow]custy --debug changelog generate[/yellow]
    Show detailed execution logs.

────────────────────────────────────────

💡 [bold]Recommended Usage:[/bold]

Generate changelogs after:

  • Creating a release tag

  • Synchronizing versions

  • Completing release workflows

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy tag[/cyan]
    Create release tags.

  [cyan]custy version update[/cyan]
    Synchronize versions.

  [cyan]custy run release[/cyan]
    Execute a complete release workflow.
"""

@app.command(
    "generate",
    rich_help_panel="Execution",
    )
def generate(
    ctx: typer.Context,
    commit_message_file: CommitMessageFileOption = None,
    force_changelog: ForceOption = None,
):
    """
Generate changelog

📄 [bold cyan]Generate changelog[/bold cyan]

Generate or update the project's changelog using Git history, release tags, and structured commit messages.

The generated changelog summarizes changes between releases and organizes commits into meaningful categories.

────────────────────────────────────────

🧩 [bold]What this command does:[/bold]

  • Read Git history

  • Analyze release boundaries

  • Parse structured commit messages

  • Group commits by category

  • Generate release notes

  • Update CHANGELOG.md

────────────────────────────────────────

📦 [bold]Supported Commit Categories:[/bold]

  • Features

  • Fixes

  • Performance improvements

  • Refactors

  • Documentation updates

  • Other supported commit types

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy changelog generate[/yellow]
    Generate or update CHANGELOG.md.

  [yellow]custy changelog generate --force[/yellow]
    Regenerate changelog even when an existing changelog is present.

  [yellow]custy changelog generate --commit-msg-file templates/custy/commit-message.txt[/yellow]
    Use a custom commit message template.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run changelog generate[/yellow]
    Read Git history and render the generated Markdown without
    writing CHANGELOG.md.

  [yellow]custy --debug changelog generate[/yellow]
    Show detailed execution logs.

  [yellow]custy --log-level debug changelog generate[/yellow]
    Enable verbose logging output.

────────────────────────────────────────

💡 [bold]Recommended Workflow:[/bold]

  1. Create a release tag
  2. Synchronize versions
  3. Generate changelog
  4. Push changes

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy tag[/cyan]

  [cyan]custy version update[/cyan]

  [cyan]custy run release[/cyan]

  [cyan]custy run full[/cyan]
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        commit_message_file=commit_message_file,
        force_changelog=force_changelog,
    )

    args = resolve_changelog_args(config=config, cli_args=cli_args)

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
    # config = [{"name": "generate_artifacts"}]
    config = resolver.resolve(["changelog"])

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

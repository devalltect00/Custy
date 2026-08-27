# app/cli/commands/backup/command.py

from types import SimpleNamespace

import typer

from app.cli.commands.backup.options import (
    CommitMessageBackupDirOption,
    CommitMessageFileOption,
    TagMessageBackupDirOption,
    TagMessageFileOption,
)
from app.cli.commands.backup.resolver import (
    resolve_backup_all_args,
    resolve_backup_commit_args,
    resolve_backup_tag_args,
)
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder


# def _run_backup_pipeline(app_ctx):
def _run_backup_pipeline(args, commands: list[str]):
    """
    Shared backup pipeline runner.
    """

    register_all_steps()

    resolver = CommandResolver()

    # 🔥 Single unified step
    # config = [{"name": "backup"}]
    config = resolver.resolve(commands)

    engine = WorkflowEngineBuilder().from_cli_args(args).build()

    ctx_obj = GitContext(engine)

    pipeline = PipelineBuilder().build(config)
    pipeline.run(ctx_obj)


app = typer.Typer()


@app.callback()
def callback():
    """
    Backup template files

    💾 [bold cyan]Backup template files[/bold cyan]

    Create backups of Custy's commit and tag message templates.

    Backups help preserve previous template versions before making changes,
    upgrading configurations, or preparing releases.

    [dim]Backup files can later be removed using cleanup commands.[/dim]

    ────────────────────────────────────────

    📦 [bold]Available Commands:[/bold]

      [green]commit[/green]
        Backup the commit message template.

      [green]tag[/green]
        Backup the tag message template.

      [green]all[/green]
        Backup both commit and tag message templates.

    ────────────────────────────────────────

    🧩 [bold]What gets backed up:[/bold]

      • Commit message templates

      • Tag message templates

      • Custom template locations configured in
      [cyan]config.toml[/cyan]

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy backup commit[/yellow]
        Backup the commit template.

      [yellow]custy backup tag[/yellow]
        Backup the tag template.

      [yellow]custy backup all[/yellow]
        Backup all message templates.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

    Global options are specified before the command.

      [yellow]custy --dry-run backup all[/yellow]
        Inspect backup sources and report planned copies and pruning
        without changing backup directories.

      [yellow]custy --debug backup commit[/yellow]
        Show detailed execution logs.

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Create backups before:

      • Editing templates
      • Running release workflows
      • Updating configuration
      • Migrating projects
      • Upgrading Custy

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy init[/cyan]
        Generate template files.

      [cyan]custy cleanup[/cyan]
        Remove old backup files.

      [cyan]custy run release[/cyan]
        Execute a release workflow.
    """


@app.command("commit")
def commit_message(
    ctx: typer.Context,
    commit_message_file: CommitMessageFileOption = None,
    commit_message_backup_dir: CommitMessageBackupDirOption = None,
):
    """
    Backup commit message template

    💾 [bold cyan]Backup commit message template[/bold cyan]

    Create a backup copy of the configured commit message template.

    Useful before modifying commit templates or experimenting with new commit formats.

    ────────────────────────────────────────

    📦 [bold]Source:[/bold]

    Commit message template file

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy backup commit[/yellow]
        Backup the configured commit template.

      [yellow]custy backup commit --commit-msg-file templates/custy/commit-message.txt[/yellow]
        Backup a specific template file.

      [yellow]custy backup commit --backup-commit-dir backups/commit[/yellow]
        Store backups in a custom directory.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run backup commit[/yellow]
        Report the planned commit-template backup without creating or
        pruning files.

      [yellow]custy --debug backup commit[/yellow]
        Show detailed execution logs.

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Run this before:

      • Editing commit templates
      • Customizing commit formats
      • Updating project conventions

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy backup all[/cyan]

      [cyan]custy cleanup backups[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        commit_message_file=commit_message_file,
        commit_message_backup_dir=commit_message_backup_dir,
    )

    args = resolve_backup_commit_args(config=config, cli_args=cli_args)

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

    # _run_backup_pipeline(app_ctx)
    _run_backup_pipeline(combined_args, ["backup_commit_message"])


@app.command("tag")
def tag_message(
    ctx: typer.Context,
    tag_message_file: TagMessageFileOption = None,
    tag_message_backup_dir: TagMessageBackupDirOption = None,
):
    """
    Backup tag message template

    💾 [bold cyan]Backup tag message template[/bold cyan]

    Create a backup copy of the configured tag message template.

    Useful before modifying release notes templates or release message formats.

    ────────────────────────────────────────

    📦 [bold]Source:[/bold]

    Tag message template file

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy backup tag[/yellow]
        Backup the configured tag template.

      [yellow]custy backup tag --tag-msg-file templates/custy/tag-message.txt[/yellow]
        Backup a specific template file.

      [yellow]custy backup tag --backup-tag-dir backups/tag[/yellow]
        Store backups in a custom directory.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run backup tag[/yellow]
        Report the planned tag-template backup without creating or
        pruning files.

      [yellow]custy --debug backup tag[/yellow]
        Show detailed execution logs.

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Run this before:

      • Editing tag templates
      • Modifying release notes formats
      • Updating release workflows

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy backup all[/cyan]

      [cyan]custy cleanup backups[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        tag_message_file=tag_message_file,
        tag_message_backup_dir=tag_message_backup_dir,
    )

    args = resolve_backup_tag_args(config=config, cli_args=cli_args)

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

    # _run_backup_pipeline(app_ctx)
    _run_backup_pipeline(combined_args, ["backup_tag_message"])


@app.command("all")
def all_backup(
    ctx: typer.Context,
    commit_message_file: CommitMessageFileOption = None,
    tag_message_file: TagMessageFileOption = None,
    commit_message_backup_dir: CommitMessageBackupDirOption = None,
    tag_message_backup_dir: TagMessageBackupDirOption = None,
):
    """
    Backup all template files

    💾 [bold cyan]Backup all template files[/bold cyan]

    Create backups for both commit and tag message templates.

    Recommended before major workflow changes, project migrations, or release preparation.

    ────────────────────────────────────────

    📦 [bold]What gets backed up:[/bold]

      • Commit message template

      • Tag message template

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy backup all[/yellow]
        Backup all configured templates.

      [yellow]custy backup all --backup-commit-dir backups/commit[/yellow]
        Use a custom commit backup directory.

      [yellow]custy backup all --backup-tag-dir backups/tag[/yellow]
        Use a custom tag backup directory.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run backup all[/yellow]
        Report all planned template backups without creating or pruning
        files.

      [yellow]custy --debug backup all[/yellow]
        Show detailed execution logs.

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Run before:

      • Release preparation
      • Template refactoring
      • Large project changes
      • Configuration migration

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy cleanup backups[/cyan]

      [cyan]custy run release[/cyan]

      [cyan]custy init[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        commit_message_file=commit_message_file,
        tag_message_file=tag_message_file,
        commit_message_backup_dir=commit_message_backup_dir,
        tag_message_backup_dir=tag_message_backup_dir,
    )

    args = resolve_backup_all_args(config=config, cli_args=cli_args)

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

    # _run_backup_pipeline(app_ctx)
    _run_backup_pipeline(combined_args, ["backup_all"])

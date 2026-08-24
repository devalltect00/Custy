# app/cli/commands/cleanup/command.py

import typer
from types import SimpleNamespace
from dataclasses import asdict

from app.config.config_loader import get_config
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context

from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder
# from app.core.cleanup.handle_cleanup_branches import handleCleanupBranches
from app.core.cleanup.branch.handler import (
    BranchCleanupHandler,
)

from app.core.cleanup.branch.models import (
    BranchCleanupRequest,
)

from app.cli.commands.cleanup.resolver import (
    resolve_cleanup_backup_args,
    resolve_cleanup_branches_args,
    resolve_cleanup_all_args,
)
from app.cli.commands.cleanup.options import (
    TypeOption,
    KeepOption,
    CommitMessageBackupDirOption,
    TagMessageBackupDirOption,
    IncludePrefixesOption,
    MergeStatusOption,
    MaxAgeOption,
    BeforeOption,
)

def _run_cleanup_backup_pipeline(args, commands: list[str]):
    """
    Shared cleanup backup pipeline runner.
    """

    register_all_steps()

    resolver = CommandResolver()

    # 🔥 Single unified step
    config = resolver.resolve(commands)

    engine = WorkflowEngineBuilder().from_cli_args(args).build()

    ctx_obj = GitContext(engine)

    pipeline = PipelineBuilder().build(config)
    pipeline.run(ctx_obj)

def _run_cleanup_branch_pipeline(args, commands: list[str]):
    """
    Shared cleanup branch pipeline runner.
    """

    register_all_steps()

    resolver = CommandResolver()

    # 🔥 Single unified step
    config = resolver.resolve(commands)

    # args.merged_only = args.merge_only

    # engine = handleCleanupBranches(args)
    # engine.gitService = None

    # ctx_obj = GitContext(engine)
    # ctx_obj.args = args

    # pipeline = PipelineBuilder().build(config)
    # pipeline.run(ctx_obj)

    request = BranchCleanupRequest(
        include_prefixes=args.include_prefixes,
        merge_status=args.merge_status,
        max_age=args.max_age,
        before=args.before,
    )

    engine = BranchCleanupHandler(
        request=request,
        dry_run=args.dry_run,
        silent=not args.debug,
    )

    engine.gitService = None

    ctx_obj = GitContext(engine)
    ctx_obj.args = args


    pipeline = PipelineBuilder().build(config)
    pipeline.run(ctx_obj)

app = typer.Typer()

@app.callback()
def callback():
    """
Cleanup project resources

🧹 [bold cyan]Cleanup project resources[/bold cyan]

Remove obsolete backups and Git branches to keep your repository clean, organized, and easier to maintain.

Cleanup operations help reduce clutter from previous workflows, backups, and temporary development branches.

Cleanup operations support configurable retention policies and
branch filtering, making them suitable for routine repository
maintenance.

────────────────────────────────────────

📦 [bold]Available Commands:[/bold]

    [green]backups[/green]
  Remove old template backup files.

    [green]branches[/green]
  Cleanup Git branches using configurable filters.

    [green]all[/green]
  Run backup and branch cleanup together.

────────────────────────────────────────

🧩 [bold]Cleanup Targets:[/bold]

  • Commit template backups

  • Tag template backups

  • Merged branches

  • Unmerged branches

  • Branches older than a specified duration

  • Branches before a specific date

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy cleanup backups[/yellow]
    Remove old backup files.

  [yellow]custy cleanup branches[/yellow]
    Cleanup branches using configured defaults.

  [yellow]custy cleanup branches --merge-status merged[/yellow]
    Cleanup merged branches.

  [yellow]custy cleanup all[/yellow]
    Run all cleanup operations.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run cleanup all[/yellow]
    Scan backup files and Git branches, report matching candidates,
    and simulate all local and remote deletions.

  [yellow]custy --debug cleanup branches[/yellow]
    Show detailed execution logs.

────────────────────────────────────────

⚠️ [bold yellow]Warning:[/bold yellow]

Cleanup operations may permanently remove files or branches.

Always review the affected resources before running cleanup operations.

Review your filters carefully and consider using
[bold]--dry-run[/bold] before performing destructive operations.

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy backup[/cyan]
    Create template backups.

  [cyan]custy run[/cyan]
    Execute workflow pipelines.
"""

@app.command("backups")
def backups(
    ctx: typer.Context,
    type: TypeOption = None,
    keep: KeepOption = None,
    commit_message_backup_dir: CommitMessageBackupDirOption = None,
    tag_message_backup_dir: TagMessageBackupDirOption = None,
):
    """
Cleanup template backups

🧹 [bold cyan]Cleanup template backups[/bold cyan]

Remove old commit and tag template backups according to a retention policy.

Useful when backup directories grow over time.

────────────────────────────────────────

📦 [bold]Supported Backup Types:[/bold]

  • commit

  • tag

  • all

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy cleanup backups[/yellow]
    Cleanup backups using configured defaults.

  [yellow]custy cleanup backups --keep 10[/yellow]
    Keep the 10 most recent backups.

  [yellow]custy cleanup backups --type commit[/yellow]
    Cleanup commit template backups only.

  [yellow]custy cleanup backups --type tag[/yellow]
    Cleanup tag template backups only.

  [yellow]custy cleanup backups --type all[/yellow]
    Cleanup all backup types.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run cleanup backups[/yellow]
    List backup files outside the retention limit without deleting
    them.

  [yellow]custy --debug cleanup backups[/yellow]
    Show detailed execution logs.

────────────────────────────────────────

💡 [bold]Recommended Usage:[/bold]

Run periodically if:

  • Frequent backups are created
  • Templates are edited regularly
  • Storage cleanup is required

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy backup[/cyan]

  [cyan]custy cleanup all[/cyan]
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        type=type,
        keep=keep,
        commit_message_backup_dir=commit_message_backup_dir,
        tag_message_backup_dir=tag_message_backup_dir,
    )

    args = resolve_cleanup_backup_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # =========================================
    # Merge args
    # =========================================
    combined_args = SimpleNamespace(
        # **vars(args),  # ValidateArgs
        **asdict(args),
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
    )

    _run_cleanup_backup_pipeline(combined_args, ["cleanup_backups"])

@app.command("branches")
def branches(
    ctx: typer.Context,
    include_prefixes: IncludePrefixesOption = None,
    merge_status: MergeStatusOption = None,
    max_age: MaxAgeOption = None,
    before: BeforeOption = None,
):
    """
Cleanup Git branches

🌿 [bold cyan]Cleanup Git branches[/bold cyan]

Remove Git branches using configurable filtering rules.

Branches can be filtered by prefix, merge status, relative age,
or an absolute cutoff date before deletion.

────────────────────────────────────────

🧩 [bold]Available Filters:[/bold]

  [cyan]--prefix[/cyan]

    Only cleanup branches beginning with one or more prefixes.

    Examples:

      feature/
      fix/
      hotfix/
      release/

    This option may be specified multiple times.

  [cyan]--merge-status[/cyan]

    Filter branches by merge state.

    Supported values:

      merged
      unmerged
      all

  [cyan]--max-age[/cyan]

    Cleanup branches whose latest commit is older than
    the supplied duration.

    Examples:

      7d
      30d
      2w
      6mo
      1y

  [cyan]--before[/cyan]

    Cleanup branches whose latest commit occurred before
    a specific date.

    Format:

      YYYY-MM-DD

    Example:

      2026-07-01

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy cleanup branches[/yellow]
    Cleanup branches using configured defaults.

  [yellow]custy cleanup branches --merge-status merged[/yellow]
    Cleanup merged branches.

  [yellow]custy cleanup branches --merge-status unmerged[/yellow]
    Cleanup unmerged branches.

  [yellow]custy cleanup branches --prefix feature/ --prefix release/[/yellow]
    Cleanup feature and release branches.

  [yellow]custy cleanup branches --max-age 30d[/yellow]
    Cleanup branches older than 30 days.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run cleanup branches[/yellow]
    Inspect local and remote branch state and list matching branches
    without deleting them.

  [yellow]custy --debug cleanup branches[/yellow]
    Show detailed execution logs.

────────────────────────────────────────

⚠️ [bold yellow]Warning:[/bold yellow]

Branch deletion is permanent.

Protected branches are skipped automatically.

Deleted branches may be difficult to recover.

Review branch filters carefully before execution.

Use [bold]--dry-run[/bold] to review affected branches before
executing the cleanup.

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy workflow[/cyan]

  [cyan]custy cleanup backups[/cyan]

  [cyan]custy cleanup all[/cyan]
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        include_prefixes=include_prefixes,
        merge_status=merge_status,
        max_age=max_age,
        before=before,
    )

    args = resolve_cleanup_branches_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # =========================================
    # Merge args
    # =========================================
    combined_args = SimpleNamespace(
        # **vars(args),  # ValidateArgs
        **asdict(args),
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
    )

    # _run_cleanup_backup_pipeline(combined_args, ["cleanup_branches"])
    _run_cleanup_branch_pipeline(combined_args, ["cleanup_branches"])

@app.command("all")
def all(
    ctx: typer.Context,
    type: TypeOption = None,
    keep: KeepOption = None,
    include_prefixes: IncludePrefixesOption = None,
    merge_status: MergeStatusOption = None,
    max_age: MaxAgeOption = None,
    before: BeforeOption = None,
    commit_message_backup_dir: CommitMessageBackupDirOption = None,
    tag_message_backup_dir: TagMessageBackupDirOption = None,
):
    """
Run full cleanup

🧹 [bold cyan]Run full cleanup[/bold cyan]

Execute all available cleanup operations.

This includes backup retention cleanup and Git branch cleanup.

Recommended as periodic repository maintenance.

────────────────────────────────────────

📦 [bold]Operations Included:[/bold]

  • Cleanup commit template backups

  • Cleanup tag template backups

  • Cleanup Git branches

────────────────────────────────────────

🧩 [bold]Supported Branch Filters:[/bold]

  • Multiple branch prefixes

  • Merge status

  • Maximum branch age

  • Absolute cutoff date

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

  [yellow]custy cleanup all[/yellow]
    Run every cleanup operation.

  [yellow]custy cleanup all --keep 10[/yellow]
    Keep the 10 newest backups.

  [yellow]custy cleanup all --merge-status merged[/yellow]
    Cleanup merged branches.

  [yellow]custy cleanup all --prefix feature/ --prefix release/[/yellow]
    Cleanup feature and release branches.

  [yellow]custy cleanup all --max-age 90d[/yellow]
    Cleanup branches older than 90 days.

  [yellow]custy cleanup all --before 2026-01-01[/yellow]
    Cleanup branches last updated before January 1st, 2026.

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

  [yellow]custy --dry-run cleanup all[/yellow]
    Inspect every cleanup target and report planned deletions without
    changing backup files or branches.

  [yellow]custy --debug cleanup all[/yellow]
    Show detailed execution logs.

────────────────────────────────────────

⚠️ [bold yellow]Warning:[/bold yellow]

This command may permanently remove both backup files and
Git branches.

Multiple resources may be removed during execution.

Review your filters carefully and retention settings carefully. Consider using
[bold]--dry-run[/bold] before running a full cleanup.

────────────────────────────────────────

💡 [bold]Recommended Usage:[/bold]

Useful before:

  • Major releases
  • Repository maintenance
  • Storage cleanup
  • Archiving long-running feature branches

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy backup[/cyan]

  [cyan]custy cleanup branches[/cyan]

  [cyan]custy cleanup backups[/cyan]
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        type=type,
        keep=keep,
        include_prefixes=include_prefixes,
        merge_status=merge_status,
        max_age=max_age,
        before=before,
        commit_message_backup_dir=commit_message_backup_dir,
        tag_message_backup_dir=tag_message_backup_dir,
    )

    args = resolve_cleanup_all_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # =========================================
    # Merge args
    # =========================================
    combined_args = SimpleNamespace(
        # **vars(args),  # ValidateArgs
        **asdict(args),
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
    )

    # pipeline.run(ctx_obj)
    _run_cleanup_backup_pipeline(combined_args, ["cleanup_backups"])
    _run_cleanup_branch_pipeline(combined_args, ["cleanup_branches"])

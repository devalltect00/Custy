# app/cli/commands/run/command.py

import typer
from types import SimpleNamespace

from app.config.config_loader import get_config
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context, AppContext

from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder

from app.cli.commands.run.options import (
    StepsArgument,
    CheckCzOption,
    AutoStageOption,
    StageModeOption,
    CommitMessageFileOption,
    ForceCommitOption,
    CommitMessageBackupDirOption,
    TagMessageFileOption,
    VersionFileOption,
    StrategyOption,
    BumpOption,
    TagOption,
    TagMessageOption,
    PreReleaseOption,
    PostReleaseOption,
    DevReleaseOption,
    MetaOption,
    EpochOption,
    ForceTagOption,
    SkipChecksOption,
    TagMessageBackupDirOption,
    AllRemoteOption,
    RemoteOption,
    SkipTagOption,
    SyncBackupOption,
)
from app.cli.commands.run.resolver import resolve_run_args

def run(
    ctx: typer.Context,
    # steps: list[str] = typer.Argument(..., help="Pipeline steps or preset"),
    steps: StepsArgument = None,

    # shared options (pipeline-safe)
    # Commit
    ## Commit • Validation
    check_cz: CheckCzOption = None,
    ## Commit • Staging
    auto_stage: AutoStageOption = None,
    stage_mode: StageModeOption = None,
    ## Commit • Files
    commit_message_file: CommitMessageFileOption = None,
    ## Commit • Behavior
    force_commit: ForceCommitOption = None,
    ## Commit • Backup
    commit_message_backup_dir: CommitMessageBackupDirOption = None,

    # Tag
    ## Tag • Files
    tag_message_file: TagMessageFileOption = None,
    version_file: VersionFileOption = None,
    ## Tag • Versioning
    strategy: StrategyOption = None,
    bump: BumpOption = None,
    tag: TagOption = None,
    tag_message: TagMessageOption = None,
    pre_release: PreReleaseOption = None,
    post_release: PostReleaseOption = None,
    dev_release: DevReleaseOption = None,
    meta: MetaOption = None,
    epoch: EpochOption = None,
    ## Tag • Behavior
    force_tag: ForceTagOption = None,
    skip_check: SkipChecksOption = None,
    ## Tag • Backup
    tag_message_backup_dir: TagMessageBackupDirOption = None,

    # Push
    ## Push • Execution
    all_remote: AllRemoteOption = None,
    remote: RemoteOption = None,
    ## Push • Behavior
    skip_tag: SkipTagOption = None,
    sync_backup: SyncBackupOption = None,

):
    """
Execute workflow pipelines

🚀 [bold cyan]Execute workflow pipelines[/bold cyan]

Run one or more Custy workflow steps in sequence.

This command is the primary entry point for automation and combines validation, versioning, changelog generation, Git operations, backups, cleanup tasks, and workflow transitions into reusable pipelines.

[dim]Most users should use pipeline profiles instead of running individual commands manually.[/dim]

────────────────────────────────────────

📦 [bold]Workflow Profiles:[/bold]

  [green]dev[/green]

    Daily development workflow.

    commit → push

  [green]release[/green]

    Standard release workflow.

    commit → tag → push

  [green]full[/green]

    Complete release lifecycle.

    release + changelog + backups + cleanup + workflow actions

────────────────────────────────────────

🧩 [bold]Available Steps:[/bold]

Core

  • [green]validate[/green]           Check repository state and required files
  • [green]commit[/green]             Create a commit using message template
  • [green]tag[/green]                Create or bump version tag
  • [green]push[/green]               Push commits and tags to remote
  • [green]changelog[/green]          Generate or update changelog

Backup

  • [yellow]backup-commit[/yellow]      Backup commit message file
  • [yellow]backup-tag[/yellow]         Backup tag message file

Cleanup

  • [magenta]cleanup-backups[/magenta]    Remove old backup files
  • [magenta]cleanup-branches[/magenta]   Clean up merged or stale branches

Workflow

  • [color(208)]workflow[/color(208)]           Finalize workflow (post-release actions)

────────────────────────────────────────

🧪 [bold]Examples:[/bold]

Run a profile:

  [yellow]custy run dev[/yellow]

  [yellow]custy run release[/yellow]

  [yellow]custy run full[/yellow]

Run custom steps:

  [yellow]custy run commit tag[/yellow]

  [yellow]custy run commit tag push[/yellow]

  [yellow]custy run validate commit tag push changelog[/yellow]

────────────────────────────────────────

🌐 [bold]Global Options:[/bold]

Global options are specified before the command.

  [yellow]custy --dry-run run release[/yellow]
    Preview the resolved profile and its planned operations. Read-only
    discovery runs, while file, Git, workflow, and remote mutations are
    simulated.

  [yellow]custy --debug run full[/yellow]

  [yellow]custy --log-level debug run release[/yellow]

────────────────────────────────────────

💡 [bold]Recommended Usage:[/bold]

Daily development:

  [yellow]custy run dev[/yellow]

Production release:

  [yellow]custy run release[/yellow]

Complete maintenance workflow:

  [yellow]custy run full[/yellow]

────────────────────────────────────────

🔗 [bold]Related Commands:[/bold]

  [cyan]custy commit[/cyan]

  [cyan]custy tag[/cyan]

  [cyan]custy push[/cyan]

  [cyan]custy workflow[/cyan]
"""
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        steps=steps,

        # Commit
        check_cz=check_cz,
        auto_stage=auto_stage,
        stage_mode=stage_mode,
        commit_message_file=commit_message_file,
        force_commit=force_commit,
        commit_message_backup_dir=commit_message_backup_dir,

        # Tag
        tag_message_file=tag_message_file,
        version_file=version_file,
        strategy=strategy,
        bump=bump,
        tag=tag,
        tag_message=tag_message,
        pre_release=pre_release,
        post_release=post_release,
        dev_release=dev_release,
        meta=meta,
        epoch=epoch,
        force_tag=force_tag,
        skip_check=skip_check,
        tag_message_backup_dir=tag_message_backup_dir,

        # Push
        all_remote=all_remote,
        remote=remote,
        skip_tag=skip_tag,
        sync_backup=sync_backup,
    )

    args = resolve_run_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)

    # # inject into context
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
    # config = resolver.resolve(steps)
    config = resolver.resolve(args.steps)

    # ✅ 3. Create engine (inject CLI args here later)
    engine = (
        WorkflowEngineBuilder()
        # .from_cli_args(app_ctx)
        .from_cli_args(combined_args)
        .build())

    # ✅ 4. Create context
    ctx_obj = GitContext(engine)

    # ✅ 5. Build pipeline
    pipeline = PipelineBuilder().build(config)

    # ✅ 6. Execute pipeline
    pipeline.run(ctx_obj)

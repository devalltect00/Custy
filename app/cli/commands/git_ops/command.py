# app/cli/commands/git_ops/command.py

from types import SimpleNamespace

import typer

from app.cli.commands.git_ops.options import (
    AllRemoteOption,
    AutoStageOption,
    BumpOption,
    CheckCzAdditionalOption,
    CommitMessageBackupDirOption,
    CommitMessageFileOption,
    DevReleaseOption,
    EpochOption,
    ForceCommitOption,
    ForceTagOption,
    MetaOption,
    PostReleaseOption,
    PreReleaseOption,
    RemoteOption,
    SkipChecksOption,
    SkipTagOption,
    StageModeOption,
    StrategyOption,
    SyncBackupOption,
    TagMessageBackupDirOption,
    TagMessageFileOption,
    TagMessageOption,
    TagOption,
    VersionFileAdditionalOption,
    VersionFileOption,
)

# from app.services import git_ops_service
from app.cli.commands.git_ops.resolver import (
    resolve_commit_args,
    resolve_push_args,
    resolve_tag_args,
)
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder

app = typer.Typer()


@app.callback()
def callback():
    """
    Git operations

    🔧 [bold cyan]Git operations[/bold cyan]

    Perform the core Git workflow operations used by Custy.

    These commands can be executed individually or combined through workflow pipelines.

    ────────────────────────────────────────

    📦 [bold]Available Commands:[/bold]

      [green]commit[/green]
        Create a structured commit.

      [green]tag[/green]
        Create a version tag.

      [green]push[/green]
        Push commits and tags to remote repositories.

    ────────────────────────────────────────

    🔁 [bold]Workflow Relationship:[/bold]

    Individual commands:

      custy commit
      custy tag
      custy push

    Pipeline workflows:

      custy run commit
      custy run release
      custy run full

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Most users should prefer workflow pipelines:

      custy run release

    Individual commands remain useful for troubleshooting,
    manual releases, and advanced workflows.

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy validate[/cyan]

      [cyan]custy run[/cyan]

      [cyan]custy workflow[/cyan]
    """


# def _run_pipeline(app_ctx, commands: list[str]):
def _run_pipeline(args, commands: list[str]):
    """
    Shared helper to execute pipeline from CLI commands.
    """
    # print("args",args)

    register_all_steps()

    resolver = CommandResolver()
    config = resolver.resolve(commands)

    # engine = WorkflowEngineBuilder().from_cli_args(app_ctx).build()
    engine = WorkflowEngineBuilder().from_cli_args(args).build()

    ctx_obj = GitContext(engine)

    isVisible = False
    pipeline = PipelineBuilder(isVisible=isVisible).build(config)
    pipeline.run(ctx_obj)


def commit(
    ctx: typer.Context,
    commit_message_file: CommitMessageFileOption = None,
    auto_stage: AutoStageOption = None,
    stage_mode: StageModeOption = None,
    force_commit: ForceCommitOption = None,
    # Additional args for Generating release artifacts
    strategy: StrategyOption = None,
    # Backup Dir Path
    commit_message_backup_dir: CommitMessageBackupDirOption = None,
    # Additional args for validation
    version_file: VersionFileAdditionalOption = None,
    check_cz: CheckCzAdditionalOption = None,
):
    """
    Create a commit

    📝 [bold cyan]Create a structured commit[/bold cyan]

    Create a Git commit using Custy's commit workflow and configured commit message template.

    Supports automatic staging, Commitizen validation, backup integration, and project-aware versioning workflows.

    ────────────────────────────────────────

    🧩 [bold]What this command does:[/bold]

      • Load commit template

      • Optionally stage files

      • Validate commit content

      • Create Git commit

      • Integrate with Custy workflows

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy commit[/yellow]
        Create a commit using the configured template.

      [yellow]custy commit --auto-stage[/yellow]
        Stage files automatically before committing.

      [yellow]custy commit --stage-mode update[/yellow]
        Stage modified files only.

      [yellow]custy commit --allow-empty-commit[/yellow]
        Create an empty commit when necessary.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run commit[/yellow]
        Inspect prerequisites and preview generated files, staging, and
        commit creation without modifying the project or Git repository.

      [yellow]custy --debug commit[/yellow]

      [yellow]custy --log-level debug commit[/yellow]

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Use this command when:

      • Creating individual commits
      • Testing commit templates
      • Building custom workflows

    For complete workflows:

      custy run release

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy tag[/cyan]

      [cyan]custy run commit[/cyan]

      [cyan]custy run release[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        commit_message_file=commit_message_file,
        force_commit=force_commit,
        auto_stage=auto_stage,
        stage_mode=stage_mode,
        # Additional args for Generating release artifacts
        strategy=strategy,
        # Additional args for validation
        version_file=version_file,
        check_cz=check_cz,
        # Backup Dir Path
        commit_message_backup_dir=commit_message_backup_dir,
    )
    args = resolve_commit_args(config=config, cli_args=cli_args)

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
        editor_settings=config.get_section("editor"),
        commit_validation_settings=config.get_section("commit", "validation"),
        git_hook_settings=config.get_section("git", "hooks"),
    )

    # _run_pipeline(app_ctx, ["commit"])
    _run_pipeline(combined_args, ["commit"])


def tag(
    ctx: typer.Context,
    tag_message_file: TagMessageFileOption = None,
    version_file: VersionFileOption = None,
    strategy: StrategyOption = None,
    bump: BumpOption = None,
    tag: TagOption = None,
    tag_message: TagMessageOption = None,
    pre_release: PreReleaseOption = None,
    post_release: PostReleaseOption = None,
    dev_release: DevReleaseOption = None,
    meta: MetaOption = None,
    epoch: EpochOption = None,
    skip_check: SkipChecksOption = None,
    force_tag: ForceTagOption = None,
    # Backup Dir Path
    tag_message_backup_dir: TagMessageBackupDirOption = None,
):
    """
    Create a version tag

    🏷️ [bold cyan]Create a version tag[/bold cyan]

    Generate and create version tags using Custy's versioning engine.

    Supports automatic strategy detection, SemVer, PEP 440, Commitizen, date-based versions, Git-count versions, and release modifiers.

    ────────────────────────────────────────

    🧩 [bold]Supported Strategies:[/bold]

      • semver

      • pep440

      • commitizen

      • date

      • gitcount

    [dim]Project strategy is automatically detected when possible.[/dim]

    ────────────────────────────────────────

    🧩 [bold]What this command does:[/bold]

      • Determine next version

      • Update version files

      • Generate tag messages

      • Create Git tags

      • Integrate with release workflows

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy tag[/yellow]
        Generate the next version automatically.

      [yellow]custy tag --bump patch[/yellow]
        Create the next patch release.

      [yellow]custy tag --bump minor[/yellow]
        Create the next minor release.

      [yellow]custy tag --tag v1.2.3[/yellow]
        Use a specific version.

      [yellow]custy tag --pre beta[/yellow]
        Create a beta release.

      [yellow]custy tag --strategy pep440[/yellow]
        Use PEP 440 versioning.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run tag[/yellow]
        Resolve the intended version and preview related file updates and
        tag creation without applying them.

      [yellow]custy --debug tag[/yellow]

      [yellow]custy --log-level debug tag[/yellow]

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Most projects should rely on automatic strategy detection.

    Override strategy only when required.

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy version update[/cyan]

      [cyan]custy changelog generate[/cyan]

      [cyan]custy run release[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
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
        skip_check=skip_check,
        force_tag=force_tag,
        # Backup Dir Path
        tag_message_backup_dir=tag_message_backup_dir,
    )
    args = resolve_tag_args(config=config, cli_args=cli_args)

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
        editor_settings=config.get_section("editor"),
    )

    # _run_pipeline(app_ctx, ["tag"])
    _run_pipeline(combined_args, ["tag"])


def push(
    ctx: typer.Context,
    all_remote: AllRemoteOption = None,
    remote: RemoteOption = None,
    tag: TagOption = None,
    skip_tag: SkipTagOption = None,
    sync_backup: SyncBackupOption = None,
):
    """
    Push changes to remote repositories

    🚀 [bold cyan]Push commits and tags[/bold cyan]

    Push commits, tags, and release artifacts to one or more Git remotes.

    Supports multi-remote workflows, backup remotes, and release synchronization.

    ────────────────────────────────────────

    🧩 [bold]What this command does:[/bold]

      • Push commits

      • Push tags

      • Push to selected remotes

      • Synchronize backup remotes

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

      [yellow]custy push[/yellow]
        Push to the default remote.

      [yellow]custy push --remote origin[/yellow]
        Push to a specific remote.

      [yellow]custy push --all-remote[/yellow]
        Push to all configured remotes.

      [yellow]custy push --sync-backup[/yellow]
        Synchronize backup remotes.

      [yellow]custy push --skip-tag[/yellow]
        Skip tag-related push operations.

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

      [yellow]custy --dry-run push[/yellow]
        Inspect the current branch and configured remotes, then simulate
        commit and tag pushes.

      [yellow]custy --debug push[/yellow]

      [yellow]custy --log-level debug push[/yellow]

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Push is normally executed automatically by:

      custy run release
      custy run full

    Manual execution is useful for advanced workflows.

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

      [cyan]custy tag[/cyan]

      [cyan]custy run release[/cyan]

      [cyan]custy run full[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        all_remote=all_remote,
        remote=remote,
        tag=tag,
        skip_tag=skip_tag,
        sync_backup=sync_backup,
    )
    args = resolve_push_args(config=config, cli_args=cli_args)

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

    # _run_pipeline(app_ctx, ["push"])
    _run_pipeline(combined_args, ["push"])

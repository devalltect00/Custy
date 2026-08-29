# app/cli/commands/validate/command.py

from types import SimpleNamespace

import typer

from app.cli.commands.validate.options import (
    AutoStageOption,
    CheckCzOption,
    CommitMessageFileOption,
    StageModeOption,
    TagMessageFileOption,
    VersionFileOption,
)
from app.cli.commands.validate.resolver import resolve_validate_args
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.command_resolver import CommandResolver
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder


def validate(
    ctx: typer.Context,
    commit_message_file: CommitMessageFileOption = None,
    tag_message_file: TagMessageFileOption = None,
    version_file: VersionFileOption = None,
    auto_stage: AutoStageOption = None,
    stage_mode: StageModeOption = None,
    check_cz: CheckCzOption = None,
):
    """
    Validate project readiness

    🔍 [bold cyan]Validate project readiness[/bold cyan]

    Run validation checks before executing commit, tag, push, or release workflows.

    This command helps detect missing files, invalid configuration,
    repository issues, and workflow prerequisites before a pipeline starts.

    [dim]Validation is automatically included in most workflow pipelines, but can also be executed manually for troubleshooting and pre-flight checks.[/dim]

    ────────────────────────────────────────

    🧩 [bold]What gets validated:[/bold]

    • [green]Git repository[/green]
    Verify the current directory is a valid Git repository.

    • [green]Project files[/green]
    Verify required files exist and can be accessed.

    ```
      • Commit message file
      • Tag message file
      • Version file
    ```

    • [green]Git configuration[/green]
    Verify repository configuration required by Custy.

    • [green]Remote configuration[/green]
    Verify required remotes are available.

    • [green]Workflow prerequisites[/green]
    Verify the project is ready for Custy workflows.

    ────────────────────────────────────────

    ⚙️ [bold]Optional Validation Checks:[/bold]

    [cyan]--check-cz[/cyan]

    ```
      Validate Commitizen integration and configuration.
    ```

    [cyan]--auto-stage[/cyan]

    ```
      Automatically stage files before validation workflows
      when required.
    ```

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

    [yellow]custy validate[/yellow]

    ```
      Run standard validation checks.
    ```

    [yellow]custy validate --check-cz[/yellow]

    ```
      Include Commitizen validation.
    ```

    [yellow]custy validate --auto-stage[/yellow]

    ```
      Stage files before validation when applicable.
    ```

    [yellow]custy validate --version-file app/**version**.py[/yellow]

    ```
      Validate using a custom version file.
    ```

    [yellow]custy validate --commit-msg-file templates/custy/commit-message.txt[/yellow]

    ```
      Validate using a custom commit message template.
    ```

    ────────────────────────────────────────

    🌐 [bold]Global Options:[/bold]

    Global options are specified before the command.

    [yellow]custy --dry-run validate[/yellow]

    ```
      Run read-only validation and simulate mutation-capable actions,
      such as automatic staging.
    ```

    [yellow]custy --debug validate[/yellow]

    ```
      Show detailed validation logs.
    ```

    [yellow]custy --log-level debug validate[/yellow]

    ```
      Enable verbose logging output.
    ```

    ────────────────────────────────────────

    🔁 [bold]Pipeline Integration:[/bold]

    Validation is automatically included in common workflow pipelines:

    ```
    [yellow]custy run commit[/yellow]
    [yellow]custy run tag[/yellow]
    [yellow]custy run push[/yellow]
    [yellow]custy run release[/yellow]
    [yellow]custy run full[/yellow]
    ```

    [dim]Running validation manually is useful when diagnosing issues before executing larger workflows.[/dim]

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Run validation after:

    • Initial project setup
    • Configuration changes
    • Template updates
    • Before releases
    • Before CI/CD execution

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

    [cyan]custy init[/cyan]
    Initialize project files and templates.

    [cyan]custy run[/cyan]
    Execute workflow pipelines.

    [cyan]custy version[/cyan]
    Manage project versions.

    [cyan]custy changelog[/cyan]
    Generate release notes and changelogs.
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        commit_message_file=commit_message_file,
        tag_message_file=tag_message_file,
        version_file=version_file,
        auto_stage=auto_stage,
        stage_mode=stage_mode,
        check_cz=check_cz,
    )

    args = resolve_validate_args(config=config, cli_args=cli_args)

    # app_ctx = get_context(ctx)
    # app_ctx.update_from_args(args=args, debug_flag=debug)

    # app_ctx = ctx.obj
    app_ctx = get_context(ctx)

    # print("app_ctx",app_ctx)

    # =========================================
    # Merge args
    # =========================================
    combined_args = SimpleNamespace(
        **vars(args),  # ValidateArgs
        dry_run=app_ctx.dry_run,
        debug=app_ctx.debug,
        log_level=app_ctx.log_level,
        commit_validation_settings=config.get_section("commit", "validation"),
        git_hook_settings=config.get_section("git", "hooks"),
    )

    # ✅ 1. Register steps (VERY IMPORTANT)
    register_all_steps()

    # ✅ 2. Resolve commands → pipeline config
    resolver = CommandResolver()
    config = resolver.resolve(["validate"])

    # ✅ 3. Create engine (inject CLI args here later)
    engine = (
        WorkflowEngineBuilder()
        # .from_cli_args(app_ctx)
        .from_cli_args(combined_args).build()
    )

    # ✅ 4. Create context
    ctx_obj = GitContext(engine)

    # ✅ 5. Build pipeline
    isVisible = True
    pipeline = PipelineBuilder(isVisible=isVisible).build(config)

    # ✅ 6. Execute pipeline
    pipeline.run(ctx_obj)

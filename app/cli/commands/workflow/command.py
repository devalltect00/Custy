# app/cli/commands/workflow/command.py

import typer

from app.cli.commands.workflow.options import (
    CheckTransitionOption,
    DebugOption,
    DryRunOption,
    EnforceOption,
    FromBranchOption,
    FromTagOption,
    LogLevelOption,
    SyncBackupOption,
    ToBranchOption,
    ToTagOption,
)
from app.cli.commands.workflow.resolver import resolve_workflow_args
from app.cli.constants.args import CliArgs
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.pipeline.builder import PipelineBuilder
from app.core.pipeline.context import GitContext
from app.core.pipeline.step_registry import register_all_steps
from app.core.workflow.workflow_builder import WorkflowEngineBuilder

app = typer.Typer()


@app.callback(
    rich_help_panel="(Still in development)",
)
def callback():
    """
    Git workflow transitions

    ⚠️  [bold yellow]Experimental / Beta Feature[/bold yellow]

    This command is currently under active development.

    Workflow rules, branch transitions, validation behavior, and automation logic may change between releases.

    [bold]Review results carefully before using this command in production workflows.[/bold]

    ────────────────────────────────────────

    🌿 [bold cyan]Git workflow transitions[/bold cyan]

    Manage and validate branch and version transitions across your Git workflow.

    This command helps enforce workflow policies and validate release transitions before promotion between branches.

    ────────────────────────────────────────

    🧩 [bold]Current Capabilities:[/bold]

    • Branch transition validation

    • Tag transition validation

    • Workflow policy enforcement

    • Release workflow verification

    ────────────────────────────────────────

    📦 [bold]Available Commands:[/bold]

    [green]branch[/green]

    ```
      Validate and finalize workflow transitions.
    ```

    ────────────────────────────────────────

    💡 [bold]When to Use:[/bold]

    • Before promoting releases

    • Before merging release branches

    • During workflow audits

    • When enforcing repository policies

    ────────────────────────────────────────

    ⚠️  [bold yellow]Important:[/bold yellow]

    This feature is still evolving.

    Future Custy releases may introduce new workflow rules,
    validation requirements, and transition behavior.

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

    [cyan]custy validate[/cyan]

    [cyan]custy run release[/cyan]

    [cyan]custy run full[/cyan]
    """


@app.command("branch")
def branch(
    ctx: typer.Context,
    enforce: EnforceOption = None,
    check_transition: CheckTransitionOption = None,
    from_branch: FromBranchOption = None,
    to_branch: ToBranchOption = None,
    from_tag: FromTagOption = None,
    to_tag: ToTagOption = None,
    sync_backup: SyncBackupOption = None,
    dry_run: DryRunOption = None,
    debug: DebugOption = None,
    log_level: LogLevelOption = None,
):
    """
    Finalize workflow transitions

    ⚠️  [bold yellow]Experimental / Beta Feature[/bold yellow]

    Workflow transition behavior may change between releases.

    Review results before relying on automated workflow enforcement.

    ────────────────────────────────────────

    🌿 [bold cyan]Finalize workflow transitions[/bold cyan]

    Validate and enforce branch and version transitions according to configured workflow policies.

    This command is intended for advanced release workflows and repository governance.

    ────────────────────────────────────────

    🧩 [bold]What this command does:[/bold]

    • Validate branch transitions

    • Validate version transitions

    • Enforce workflow policies

    • Verify release readiness

    • Execute workflow finalization logic

    ────────────────────────────────────────

    🧪 [bold]Examples:[/bold]

    [yellow]custy workflow branch[/yellow]

    ```
      Execute workflow validation using configured settings.
    ```

    [yellow]custy workflow branch --enforce[/yellow]

    ```
      Enforce workflow policies.
    ```

    [yellow]custy workflow branch --check-transition[/yellow]

    ```
      Validate transitions without enforcement.
    ```

    [yellow]custy workflow branch --from-branch develop --to-branch main[/yellow]

    ```
      Validate a specific branch transition.
    ```

    [yellow]custy workflow branch --from-tag v1.2.0 --to-tag v1.3.0[/yellow]

    ```
      Validate a version transition.
    ```

    ────────────────────────────────────────

    🌐 [bold]Execution Options:[/bold]

    This command currently supports local execution options.

    [yellow]custy workflow branch --dry-run[/yellow]

    ```
      Inspect and validate the transition while simulating checkout,
      merge, push, and branch-cleanup mutations.
    ```

    [yellow]custy workflow branch --debug[/yellow]

    ```
      Show detailed workflow diagnostics.
    ```

    [yellow]custy workflow branch --log-level debug[/yellow]

    ```
      Enable verbose logging output.
    ```

    ────────────────────────────────────────

    ⚠️  [bold yellow]Warning:[/bold yellow]

    Workflow enforcement may affect release decisions and branch policies.

    Verify transition rules before enabling enforcement.

    ────────────────────────────────────────

    💡 [bold]Recommended Usage:[/bold]

    Start with:

    ```
    custy workflow branch --check-transition
    ```

    before enabling:

    ```
    custy workflow branch --enforce
    ```

    ────────────────────────────────────────

    🔗 [bold]Related Commands:[/bold]

    [cyan]custy validate[/cyan]

    [cyan]custy run release[/cyan]

    [cyan]custy tag[/cyan]
    """
    config = get_config()

    # REQUIRED defaults
    cli_args = CliArgs(
        enforce=enforce,
        check_transition=check_transition,
        from_branch=from_branch,
        to_branch=to_branch,
        from_tag=from_tag,
        to_tag=to_tag,
        sync_backup=sync_backup,
        dry_run=dry_run,
        debug=debug,
        log_level=log_level,
    )

    args = resolve_workflow_args(config=config, cli_args=cli_args)

    app_ctx = get_context(ctx)
    app_ctx.update_from_args(args=args, debug_flag=debug)

    # ✅ 1. Register steps (VERY IMPORTANT)
    register_all_steps()

    # ✅ 2. Resolve commands → pipeline config
    config = [{"name": "finalize"}]

    # ✅ 3. Create engine (inject CLI args here later)
    engine = WorkflowEngineBuilder().from_cli_args(app_ctx).build()

    # ✅ 4. Create context
    ctx_obj = GitContext(engine)

    # ✅ 5. Build pipeline
    pipeline = PipelineBuilder().build(config)

    # ✅ 6. Execute pipeline
    pipeline.run(ctx_obj)

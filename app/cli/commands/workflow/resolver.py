# app/cli/commands/workflow/resolver.py

from app.cli.commands.workflow.models import BranchWorkflowArgs

from app.cli.constants import LogLevelChoices

def resolve_workflow_args(config, cli_args) -> BranchWorkflowArgs:
    no_debug = cli_args.debug
    if cli_args.debug is not None:
        no_debug = not cli_args.debug

    return BranchWorkflowArgs(
    enforce=config.resolve(
        cli_args.enforce,
        ["cli", "workflow", "enforce"],
        False,
    ),
    check_transition=config.resolve(
        cli_args.check_transition,
        ["cli", "workflow", "check_transition"],
        False,
    ),
    from_branch=cli_args.from_branch or None,
    to_branch=cli_args.to_branch or None,
    from_tag=cli_args.from_tag or None,
    to_tag=cli_args.to_tag or None,
    sync_backup=config.resolve(
        cli_args.sync_backup,
        ["cli", "workflow", "sync_backup"],
        False,
    ),
    dry_run=config.resolve(
        cli_args.dry_run,
        ["cli", "execution", "dry_run"],
        False,
    ),
    no_debug=config.resolve(
        no_debug,
        ["cli", "execution", "no_debug"],
        False,
    ),
    log_level=config.resolve(
        cli_args.log_level,
        ["logging", "level"],
        LogLevelChoices.INFO
    ),
  )

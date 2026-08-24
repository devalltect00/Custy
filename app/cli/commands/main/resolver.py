# app/cli/commands/main/resolver.py

from app.cli.commands.main.models import MainArgs

from app.cli.constants import LogLevelChoices

def resolve_main_args(config, cli_args) -> MainArgs:
  no_debug = cli_args.debug
  if cli_args.debug is not None:
    no_debug = not cli_args.debug

  # print("no_debug",no_debug)

  return MainArgs(
    no_banner=cli_args.no_banner or False,
    help=cli_args.help or False,
    version=cli_args.version or None,
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
        LogLevelChoices.INFO,
    ),
  )

# app/cli/commands/init/resolver.py

from app.cli.commands.init.models import InitArgs

from app.cli.constants import (
  LogLevelChoices,
  InitMode,
)

def resolve_init_args(config, cli_args) -> InitArgs:
  return InitArgs(
    mode=cli_args.mode or InitMode.ALL,
    force_init=config.resolve(
        cli_args.force_init,
        ["initialization", "force"],
        False,
    ),
    ask=config.resolve(
        cli_args.ask,
        ["initialization", "ask"],
        False,
    ),
  )

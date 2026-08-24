# app/cli/commands/validate/resolver.py

from app.constants.path import CUSTY_COMMIT_MESSAGE_TEMPLATE, CUSTY_TAG_MESSAGE_TEMPLATE
from app.cli.commands.validate.models import ValidateArgs
from app.cli.constants import (
  LogLevelChoices,
  StageModeChoices,
)

def resolve_validate_args(config, cli_args) -> ValidateArgs:
  return ValidateArgs(
    commit_message_file=config.resolve(
        cli_args.commit_message_file,
        ["cli", "templates", "file", "commit_message"],
        CUSTY_COMMIT_MESSAGE_TEMPLATE,
    ),
    tag_message_file=config.resolve(
        cli_args.tag_message_file,
        ["cli", "templates", "file", "tag_message"],
        CUSTY_TAG_MESSAGE_TEMPLATE,
    ),
    version_file=config.resolve(
        cli_args.version_file,
        ["cli", "paths", "version_file"],
        "app/__version__.py",
    ),
    auto_stage=config.resolve(
        cli_args.auto_stage,
        ["cli", "execution", "auto_stage"],
        False,
    ),
    stage_mode=config.resolve(
        cli_args.stage_mode,
        ["cli", "execution", "stage_mode"],
        StageModeChoices.ALL
    ),
    check_cz=config.resolve(
        cli_args.check_cz,
        ["cli", "execution", "check_cz"],
        False,
    ),
  )

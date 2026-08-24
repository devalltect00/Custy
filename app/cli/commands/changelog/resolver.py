# app/cli/commands/changelog/resolver.py

from app.cli.commands.changelog.models import ChangelogArgs

from app.constants.path import CUSTY_COMMIT_MESSAGE_TEMPLATE
from app.cli.constants import LogLevelChoices

def resolve_changelog_args(config, cli_args) -> ChangelogArgs:
  return ChangelogArgs(
    commit_message_file=config.resolve(
        cli_args.commit_message_file,
        ["cli", "templates", "file", "commit_message"],
        CUSTY_COMMIT_MESSAGE_TEMPLATE,
    ),
    force_changelog=config.resolve(
        cli_args.force_changelog,
        ["cli", "changelog", "force_generation"],
        False,
    )
  )

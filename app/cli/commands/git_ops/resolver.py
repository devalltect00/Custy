# app/cli/commands/git_ops/resolver.py

from app.constants.path import (
  CUSTY_COMMIT_MESSAGE_TEMPLATE,
  CUSTY_TAG_MESSAGE_TEMPLATE,
  CUSTY_BACKUP_COMMIT_DIR,
  CUSTY_BACKUP_TAG_DIR,
)
from app.core.git_ops.helper import detect_project_strategy
from app.cli.commands.git_ops.models import (
  CommitArgs,
  TagArgs,
  PushArgs,
)
from app.cli.constants import (
  StrategyChoices,
  StageModeChoices,
  LogLevelChoices,
)

def resolve_commit_args(config, cli_args) -> CommitArgs:
#   print("=========cli_args.version_file",cli_args.version_file)
  return CommitArgs(
    commit_message_file=config.resolve(
        cli_args.commit_message_file,
        ["cli", "templates", "file", "commit_message"],
        CUSTY_COMMIT_MESSAGE_TEMPLATE,
    ),

    force_commit=config.resolve(
        cli_args.force_commit,
        ["cli", "execution", "force_commit"],
        False,
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

    # Additional args for Generating release artifacts
    strategy=config.resolve(
        cli_args.strategy,
        ["cli", "versioning", "strategy"],
        detect_project_strategy(no_debug=True) or StrategyChoices.SEMVER,
    ),

    # Additional args for validation
    version_file=config.resolve(
        cli_args.version_file,
        ["cli", "paths", "version_file"],
        "app/__version__.py",
    ),
    check_cz=config.resolve(
        cli_args.check_cz,
        ["cli", "execution", "check_cz"],
        False,
    ),

    # Backup Dir Path
    commit_message_backup_dir=config.resolve(
        cli_args.commit_message_backup_dir,
        ["cli", "templates", "directory", "backups_commit"],
        CUSTY_BACKUP_COMMIT_DIR,
    ),
  )

def resolve_tag_args(config, cli_args) -> TagArgs:
  return TagArgs(
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
    strategy=config.resolve(
        cli_args.strategy,
        ["cli", "versioning", "strategy"],
        detect_project_strategy(no_debug=True) or StrategyChoices.SEMVER,
    ),
    bump=config.resolve(
        cli_args.bump,
        ["cli", "versioning", "bump"],
        None,
    ),
    tag=cli_args.tag or None,
    tag_message=cli_args.tag_message or None,
    pre_release=cli_args.pre_release or None,
    post_release=cli_args.post_release or False,
    dev_release=cli_args.dev_release or False,
    meta=cli_args.meta or None,
    epoch=cli_args.epoch or None,
    skip_check=config.resolve(
        cli_args.skip_check,
        ["cli", "execution", "skip_check"],
        False,
    ),
    force_tag=config.resolve(
        cli_args.force_tag,
        ["cli", "execution", "force_tag"],
        False,
    ),

    # Backup Dir Path
    tag_message_backup_dir=config.resolve(
        cli_args.tag_message_backup_dir,
        ["cli", "templates", "directory", "backups_tag"],
        CUSTY_BACKUP_TAG_DIR,
    ),
  )

def resolve_push_args(config, cli_args) -> PushArgs:
  return PushArgs(
    all_remote=config.resolve(
        cli_args.all_remote,
        ["cli", "push", "all_remote"],
        True,
    ),
    remote=cli_args.remote or "origin",
    tag=cli_args.tag,
    skip_tag=config.resolve(
        cli_args.skip_tag,
        ["cli", "push", "skip_tag"],
        False,
    ),
    sync_backup=config.resolve(
        cli_args.sync_backup,
        ["cli", "push", "sync_backup"],
        False,
    ),
  )

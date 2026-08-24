# app/cli/commands/backup/resolver.py

from app.constants.path import (
  CUSTY_COMMIT_MESSAGE_TEMPLATE,
  CUSTY_TAG_MESSAGE_TEMPLATE,
  CUSTY_BACKUP_COMMIT_DIR,
  CUSTY_BACKUP_TAG_DIR,
)

from app.cli.commands.backup.models import (
  BackupCommitArgs,
  BackupTagArgs,
  BackupAllArgs,
)

def resolve_backup_commit_args(config, cli_args) -> BackupCommitArgs:
  return BackupCommitArgs(
    commit_message_file=config.resolve(
        cli_args.commit_message_file,
        ["cli", "templates", "file", "commit_message"],
        CUSTY_COMMIT_MESSAGE_TEMPLATE,
    ),
    commit_message_backup_dir=config.resolve(
        cli_args.commit_message_backup_dir,
        ["cli", "templates", "directory", "backups_commit"],
        CUSTY_BACKUP_COMMIT_DIR,
    ),
  )

def resolve_backup_tag_args(config, cli_args) -> BackupTagArgs:
  return BackupTagArgs(
    tag_message_file=config.resolve(
        cli_args.tag_message_file,
        ["cli", "templates", "file", "tag_message"],
        CUSTY_TAG_MESSAGE_TEMPLATE,
    ),
    tag_message_backup_dir=config.resolve(
        cli_args.tag_message_backup_dir,
        ["cli", "templates", "directory", "backups_tag"],
        CUSTY_BACKUP_TAG_DIR,
    ),
  )

def resolve_backup_all_args(config, cli_args) -> BackupAllArgs:
  return BackupAllArgs(
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
    commit_message_backup_dir=config.resolve(
        cli_args.commit_message_backup_dir,
        ["cli", "templates", "directory", "backups_commit"],
        CUSTY_BACKUP_COMMIT_DIR,
    ),
    tag_message_backup_dir=config.resolve(
        cli_args.tag_message_backup_dir,
        ["cli", "templates", "directory", "backups_tag"],
        CUSTY_BACKUP_TAG_DIR,
    ),
  )

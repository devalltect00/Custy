# app/cli/commands/cleanup/resolver.py

"""
Cleanup argument resolvers.

This module resolves cleanup-related command-line arguments by
combining CLI values, configuration defaults, and built-in defaults.

Resolvers also perform validation and convert human-readable CLI
values into strongly typed objects before they are passed into the
cleanup workflow.
"""

from datetime import datetime, timedelta

from app.utils.parsing import (
    parse_date,
    parse_duration,
)

from app.constants.path import (
  CUSTY_BACKUP_COMMIT_DIR,
  CUSTY_BACKUP_TAG_DIR,
)

from app.cli.commands.cleanup.models import (
  CleanupBackupArgs,
  CleanupBranchesArgs,
  CleanupAllArgs,
)

from app.cli.constants import (
  CleanupTypeChoices,
  MergeStatusChoices,
)

def _resolve_branch_cleanup_filters(
    config,
    cli_args,
) -> tuple[timedelta | None, datetime | None]:
    """
    Resolve and validate branch cleanup filters.

    This helper resolves branch-related filter options by combining
    command-line arguments, configuration values, and built-in
    defaults. It also converts human-readable values into strongly
    typed objects.

    Supported filters
    -----------------
    - max_age
    - before

    Validation
    ----------
    The ``--max-age`` and ``--before`` options are mutually exclusive
    and cannot be used together.

    Parameters
    ----------
    config:
        Custy configuration loader.

    cli_args:
        Parsed CLI arguments.

    Returns
    -------
    tuple[timedelta | None, datetime | None]
        A tuple containing:

        - Parsed maximum branch age.
        - Parsed cutoff date.

    Raises
    ------
    ValueError
        If mutually exclusive options are supplied.
    """

    max_age_value = config.resolve(
        cli_args.max_age,
        ["cli", "cleanup", "branch", "max_age"],
        None,
    )

    max_age = (
        parse_duration(max_age_value)
        if max_age_value
        else None
    )

    before_value = config.resolve(
        cli_args.before,
        ["cli", "cleanup", "branch", "before"],
        None,
    )

    before = (
        parse_date(before_value)
        if before_value
        else None
    )

    if max_age is not None and before is not None:
        raise ValueError(
            (
                "Cleanup options '--max-age' and '--before' "
                "cannot be used together."
            )
        )

    return max_age, before

def resolve_cleanup_backup_args(config, cli_args) -> CleanupBackupArgs:
  return CleanupBackupArgs(
    type=config.resolve(
        cli_args.type,
        ["cli", "cleanup", "backup", "type"],
        CleanupTypeChoices.ALL,
    ),
    keep=config.resolve(
        cli_args.keep,
        ["cli", "cleanup", "backup", "keep"],
        10,
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

def resolve_cleanup_branches_args(
    config,
    cli_args,
) -> CleanupBranchesArgs:
    """
    Resolve branch cleanup arguments.

    CLI values have the highest priority, followed by configuration
    values and finally built-in defaults.

    All string values are converted into strongly typed objects before
    returning.
    """
    max_age, before = _resolve_branch_cleanup_filters(
        config,
        cli_args,
    )

    return CleanupBranchesArgs(
        include_prefixes = config.resolve(
            cli_args.include_prefixes,
            ["cli", "cleanup", "branch", "include_prefixes"],
            [],
        ),
        merge_status = config.resolve(
            cli_args.merge_status,
            ["cli", "cleanup", "branch", "merge_status"],
            MergeStatusChoices.MERGED,
        ),
        max_age=max_age,
        before=before,
    )

def resolve_cleanup_all_args(config, cli_args) -> CleanupAllArgs:
    max_age, before = _resolve_branch_cleanup_filters(
        config,
        cli_args,
    )

    return CleanupAllArgs(
        type=config.resolve(
            cli_args.type,
            ["cli", "cleanup", "backup", "type"],
            CleanupTypeChoices.ALL,
        ),
        keep=config.resolve(
            cli_args.keep,
            ["cli", "cleanup", "backup", "keep"],
            10,
        ),
        include_prefixes = config.resolve(
            cli_args.include_prefixes,
            ["cli", "cleanup", "branch", "include_prefixes"],
            [],
        ),
        merge_status = config.resolve(
            cli_args.merge_status,
            ["cli", "cleanup", "branch", "merge_status"],
            MergeStatusChoices.MERGED,
        ),
        max_age=max_age,
        before=before,
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

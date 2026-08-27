# app/cli/commands/run/resolver.py


from app.cli.commands.run.models import RunArgs
from app.cli.constants import (
    StageModeChoices,
    StrategyChoices,
)
from app.constants.path import (
    CUSTY_BACKUP_COMMIT_DIR,
    CUSTY_BACKUP_TAG_DIR,
    CUSTY_COMMIT_MESSAGE_TEMPLATE,
    CUSTY_TAG_MESSAGE_TEMPLATE,
)
from app.constants.resolver import resolve_version_file
from app.core.git_ops.helper import detect_project_strategy


def resolve_run_args(config, cli_args) -> RunArgs:
    return RunArgs(
        steps=cli_args.steps,
        # Commit
        ## Commit • Validation
        check_cz=config.resolve(
            cli_args.check_cz,
            ["cli", "execution", "check_cz"],
            False,
        ),
        ## Commit • Staging
        auto_stage=config.resolve(
            cli_args.auto_stage,
            ["cli", "execution", "auto_stage"],
            False,
        ),
        stage_mode=config.resolve(
            cli_args.stage_mode,
            ["cli", "execution", "stage_mode"],
            StageModeChoices.ALL,
        ),
        ## Commit • Files
        commit_message_file=config.resolve(
            cli_args.commit_message_file,
            ["cli", "templates", "file", "commit_message"],
            CUSTY_COMMIT_MESSAGE_TEMPLATE,
        ),
        ## Commit • Behavior
        force_commit=config.resolve(
            cli_args.force_commit,
            ["cli", "execution", "force_commit"],
            False,
        ),
        ## Commit • Backup
        commit_message_backup_dir=config.resolve(
            cli_args.commit_message_backup_dir,
            ["cli", "templates", "directory", "backups_commit"],
            CUSTY_BACKUP_COMMIT_DIR,
        ),
        # Tag
        ## Tag • Files
        tag_message_file=config.resolve(
            cli_args.tag_message_file,
            ["cli", "templates", "file", "tag_message"],
            CUSTY_TAG_MESSAGE_TEMPLATE,
        ),
        version_file=resolve_version_file(
            config=config,
            value=cli_args.version_file,
        ),
        ## Tag • Versioning
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
        ## Tag • Behavior
        force_tag=config.resolve(
            cli_args.force_tag,
            ["cli", "execution", "force_tag"],
            False,
        ),
        skip_check=config.resolve(
            cli_args.skip_check,
            ["cli", "execution", "skip_check"],
            False,
        ),
        ## Tag • Backup
        tag_message_backup_dir=config.resolve(
            cli_args.tag_message_backup_dir,
            ["cli", "templates", "directory", "backups_tag"],
            CUSTY_BACKUP_TAG_DIR,
        ),
        # Push
        ## Push • Execution
        all_remote=config.resolve(
            cli_args.all_remote,
            ["cli", "push", "all_remote"],
            True,
        ),
        remote=cli_args.remote or "origin",
        ## Push • Behavior
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

# app/builders/git_tool_builder.deprecated.py

from app.core.git_ops.engine import GitWorkflowEngine

# =======================
# 🏗️ Factory method
# =======================


def build_git_tool(
    args,
    *,
    with_tagging: bool = True,
    with_tag: bool = False,
    with_commit_message_file: bool = True,
    with_tag_message_file: bool = True,
    with_version_file: bool = False,
    auto_stage: bool = False,
) -> GitWorkflowEngine:
    return GitWorkflowEngine(
        args=args,
        # -----------------------
        # Commit
        # -----------------------
        message_file=args.commit_message_file if with_commit_message_file else None,

        # -----------------------
        # Tagging
        # -----------------------
        tag=args.tag if with_tagging or with_tag else None,
        tag_msg=args.tag_message if with_tagging else None,
        tag_msg_file=args.tag_message_file if with_tag_message_file else None,

        strategy=args.strategy if with_tagging else None,
        bump=args.bump if with_tagging else None,

        pre_release=args.pre_release if with_tagging else None,
        post_release=args.post_release if with_tagging else None,
        dev_release=args.dev_release if with_tagging else None,

        meta=args.meta if with_tagging else None,
        epoch=args.epoch if with_tagging else None,

        # -----------------------
        # Execution
        # -----------------------
        dry_run=args.dry_run,
        skip_checks=getattr(args, "skip_checks", False),
        no_debug=getattr(args, "no_debug", False),

        # -----------------------
        # Version file
        # -----------------------
        version_file=args.version_file if with_version_file else None,

        # -----------------------
        # Staging
        # -----------------------
        auto_stage=auto_stage,
        stage_mode=args.stage_mode if auto_stage else None,

        # -----------------------
        # Advanced Flags
        # -----------------------
        force_tag=args.force_tag if with_tagging else False,
        force_changelog=getattr(args, "force_changelog", False),
        force_commit=getattr(args, "force_commit", False),

        # -----------------------
        # Sync Backups
        # -----------------------
        sync_backup=getattr(args, "sync_backup", False),
    )

def minimal_build_git_tool(
    args,
    *,
    with_commit_message_file: bool = True,
    with_tag_message_file: bool = True,
    with_version_file: bool = False,
    auto_stage: bool = False,
) -> GitWorkflowEngine:
    return GitWorkflowEngine(
        args=args,
        # -----------------------
        # Commit
        # -----------------------
        message_file=None,

        # -----------------------
        # Tagging
        # -----------------------
        tag=None,
        tag_msg=None,
        tag_msg_file=None,

        strategy=None,
        bump=None,

        pre_release=None,
        post_release=None,
        dev_release=None,

        meta=None,
        epoch=None,

        # -----------------------
        # Execution
        # -----------------------
        dry_run=args.dry_run,
        skip_checks=getattr(args, "skip_checks", False),
        no_debug=getattr(args, "no_debug", False),

        # -----------------------
        # Version file
        # -----------------------
        version_file=args.version_file if with_version_file else None,

        # -----------------------
        # Staging
        # -----------------------
        auto_stage=auto_stage,
        stage_mode=args.stage_mode if auto_stage else None,

        # -----------------------
        # Advanced Flags
        # -----------------------
        force_tag=False,
        force_changelog=getattr(args, "force_changelog", False),
        force_commit=getattr(args, "force_commit", False),

        # -----------------------
        # Sync Backups
        # -----------------------
        sync_backup=getattr(args, "sync_backup", False),
    )

# from app.core.git_commit_tagger import GitCommitTagger


# def build_git_tool(
#     message_file=None,
#     tag=None,
#     tag_msg=None,
#     tag_msg_file=None,
#     strategy=None,
#     bump=None,
#     pre_release=None,
#     post_release=False,
#     dev_release=False,
#     meta=None,
#     epoch=None,
#     force_tag=False,
#     dry_run=False,
#     version_file=None,
#     auto_stage=False,
#     stage_mode=None,
#     force_changelog=False,
#     force_commit=False,
#     sync_backup=False,
#     skip_checks=False,
#     no_debug=False,
# ):
#     return GitCommitTagger(
#         message_file=message_file,
#         tag=tag,
#         tag_msg=tag_msg,
#         tag_msg_file=tag_msg_file,
#         strategy=strategy,
#         bump=bump,
#         pre_release=pre_release,
#         post_release=post_release,
#         dev_release=dev_release,
#         meta=meta,
#         epoch=epoch,
#         force_tag=force_tag,
#         dry_run=dry_run,
#         version_file=version_file,
#         auto_stage=auto_stage,
#         stage_mode=stage_mode,
#         force_changelog=force_changelog,
#         force_commit=force_commit,
#         sync_backup=sync_backup,
#         skip_checks=skip_checks,
#         no_debug=no_debug,
#     )

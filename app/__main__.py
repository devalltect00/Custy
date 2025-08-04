# app/__main__.py

r"""Commit and Tag Automation Script.

This script automates the process of:
- Verifies Git is initialized
- Open commit message file for editing (VS Code or Notepad)
- Committing using a message file
- Creating a Git tag (manually or auto-bumped)
- Pushing both the commit and tag to origin
- Support version bumping

Usage:
    python .\\bin\\commit_and_tag.py commit-msg.txt --tag v1.2.3 --tag-msg "Release v1.2.3"
    python .\\bin\\commit_and_tag.py commit-msg.txt --tag v1.2.3
    python .\\bin\\commit_and_tag.py commit-msg.txt --bump patch
    python .\\tools\\git-commit\\commit_and_tag.py .\\tools\\git-commit\\commit-msg.txt --strategy semver --bump patch --version-file .\\app\\__version__.py
    python .\\tools\\git-commit\\commit_and_tag.py .\\tools\\git-commit\\commit-msg.txt \
        --strategy semver \
        --bump patch \
        --pre-release rc \
        --version-file .\\app\\__version__.py
    python .\\tools\\git-commit\\commit_and_tag.py --help # To show this help message and exit
"""

import argparse
import pathlib
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pyfiglet import Figlet

from .git_commit_tagger import GitCommitTagger
from .utils import detect_project_strategy, maybe_assert_is_final

# =======================
# 🏗️ Factory method
# =======================


def build_git_tool(
    args,
    *,
    with_tagging: bool = True,
    with_version_file: bool = True,
    auto_stage: bool = False,
) -> GitCommitTagger:
    return GitCommitTagger(
        message_file=args.message_file,
        tag=args.tag if with_tagging else None,
        tag_msg=args.tag_msg if with_tagging else None,
        tag_msg_file=args.tag_msg_file if with_tagging else None,
        strategy=args.strategy if with_tagging else None,
        bump=args.bump if with_tagging else None,
        pre_release=args.pre_release if with_tagging else None,
        post_release=args.post_release if with_tagging else None,
        dev_release=args.dev_release if with_tagging else None,
        meta=args.meta if with_tagging else None,
        epoch=args.epoch if with_tagging else None,
        force_tag=args.force_tag if with_tagging else False,
        dry_run=args.dry_run,
        version_file=args.version_file if with_version_file else None,
        auto_stage=auto_stage,
        stage_mode=args.stage_mode if auto_stage else None,
        force_changelog=getattr(args, "force_changelog", False),
        force_commit=getattr(args, "force_commit", False),
        sync_backup=getattr(args, "sync_backup", False),
        skip_checks=getattr(args, "skip_checks", False),
        no_debug=getattr(args, "no_debug", False),
    )


# =======================
# 🚀 Command Handlers
# =======================


def handle_commit_tag_bump(args):
    build_git_tool(args).execute_commit_tag_bump()


def handle_push(args):
    tool = build_git_tool(args, with_tagging=False, with_version_file=False)
    tool.push_changes()


def handle_changelog(args):
    from .utils import ChangelogGenerator, GitHelper

    latest_tag = GitHelper().get_latest_tag()

    # Enforce final version before generating changelog
    # maybe_assert_is_final(latest_tag, context="changelog", force=args.force_changelog)

    tool = build_git_tool(args, with_tagging=False)
    tool.tag = latest_tag
    # gen = ChangelogGenerator()
    # rendered = gen.generate()
    # gen.write_to_files(rendered)

    tool._generate_changelog()
    tool.force_changelog = True


def handle_validate(args):
    tool = build_git_tool(args, with_tagging=False, with_version_file=False)
    tool.validate()
    tool.git.check_remote_origin()
    tool.cz.check_commit()


def handle_backup(args):
    build_git_tool(
        args,
        with_tagging=False,
        with_version_file=False,
    )._backup_commit_message()


def handle_all(args):
    tool = build_git_tool(args, auto_stage=True)
    tool.execute_all()


def handle_cleaned_backups(args):
    from .utils import BackupManager

    manager = BackupManager(keep=args.keep)

    def clean(type_dir: str, stem: str):
        backup_dir = Path(f"backups/{type_dir}")
        print(f"🧹 CLeaning {backup_dir} (keeping {args.keep})")
        manager._prune_old_backups(backup_dir=backup_dir, stem=stem)

    if args.type in ("commit", "all"):
        clean("commit", "commit-msg")
    if args.type in ("tag", "all"):
        clean("tag", "tag-msg")


def handle_cleanup_branches(args):
    from .utils import BranchCleaner

    cleaner = BranchCleaner(
        prefix=args.prefix,
        merged_only=args.merged_only,
        older_than=args.older_than,
    )
    cleaner.clean()


def handle_workflow(args):
    from .utils import WorkflowManager

    manager = WorkflowManager()

    if args.enforce:
        manager.enforce_consistency()

    if args.check_.transition:
        manager.check_transition(
            from_branch=args.from_branch,
            from_tag=args.from_tag,
            to_branch=args.to_branch,
            to_tag=args.to_tag,
        )


def get_version(pkg_name="custy") -> str:
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        # Try read from local __version__.py if available
        try:
            here = pathlib.Path(__file__).resolve()

            version_path = here.parent / "__version__.py"

            if version_path.exists():
                with open(version_path) as f:
                    for line in f:
                        if "__version__" in line:
                            return line.split("=")[-1].strip().strip('"')
        except FileNotFoundError:
            pass
        return "0.0.0"


def show_banner():
    app_name = "custy"
    app_version = get_version(pkg_name="name")

    font = "cosmic"
    fig = Figlet(font=font)
    custy_banner = fig.renderText(app_name)
    version_banner = f"v{app_version}"

    # ANSI Colors
    BOLD_CYAN = "\033[1;96m"
    BOLD_WHITE = "\033[1;97m"
    RESET = "\033[0m"

    # print(f"\033[95m{custy_banner}\033[0m")
    # print(f"\033[96m{version_banner.center(50)}\033[0m")

    print(f"\n{BOLD_CYAN}{custy_banner}{RESET}")
    print(f"{BOLD_WHITE}{version_banner.center(50)}{RESET}\n")


# =======================
# 🏁 CLI Entry
# =======================


def main() -> None:
    show_banner()

    detect_project_strategy(no_debug=False)

    parser = argparse.ArgumentParser(
        description="Git commit, tag, and version automation tool",
    )
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
    )

    def add_common_arguments(p):
        p.add_argument(
            "message_file",
            nargs="?",
            default="./templates/commit-msg.txt",
            help="Path to commit message file (default: ./templates/commit-msg.txt) (open in editor before commit)",
        )
        p.add_argument(
            "--version-file",
            metavar="FILE",
            default="app/__version__.py",
            help="Path to __version__.py to auto-update (default: app/__version__.py)",
        )
        p.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate commands without executing. Dry run mode.",
        )
        p.add_argument(
            "--force-commit",
            action="store_true",
            help="Allow committing even when no staged changes are detected. Creates an empty commit.",
        )

    def add_tagging_arguments(p):
        p.add_argument(
            "--strategy",
            choices=["semver", "pep440", "date", "gitcount", "commitizen"],
            default=detect_project_strategy(no_debug=True),  # <-- auto logic
            help=(
                "Strategy to generate tag (Auto generate tag using a strategy). ",
                "Tagging strategy (e.g. pep440, semver, date, gitcount, or commitizen). ",
                "CLI overrides config or auto-detect.",
            ),
        )
        p.add_argument(
            "--bump",
            choices=["patch", "minor", "major", "auto"],
            help="Auto bump from latest tag. Version bump level (Semver bump level when using --strategy=semver. use 'auto' only with --strategy=commitizen)",
        )
        p.add_argument(
            "--tag",
            metavar="vX.Y.Z",
            help="Manually specify tag (e.g. v1.2.3)",
        )
        p.add_argument(
            "--tag-msg",
            help="Message for the Git tag (default: same as tag name)",
        )
        p.add_argument(
            "--tag-msg-file",
            default="./templates/tag-msg.txt",
            help="Path to file containing tag message (default: ./templates/tag-msg.txt).",
        )
        p.add_argument(
            "--pre-release",
            help="Optional Pre-release label (e.g. alpha, beta, rc, dev, next, preview, etc)",
        )
        p.add_argument(
            "--post-release",
            action="store_true",
            help="Mark this version as post-release",
        )
        p.add_argument(
            "--dev-release",
            action="store_true",
            help="Mark this version as development release",
        )
        p.add_argument(
            "--meta",
            help="Meta version label (e.g. sha.abc123)",
        )
        p.add_argument(
            "--epoch",
            type=int,
            help="Set version epoch (e.g. 1!1.2.3)",
        )
        p.add_argument(
            "--force-tag",
            action="store_true",
            help="Force version bump and tagging even if commit type is not allowed.",
        )

    def add_sync_argument(p):
        p.add_argument(
            "--sync-backup",
            action="store_true",
            help="Also push commit and tag `backup` remote (e.g., Github).",
        )

    def add_force_changelog_argument(p):
        p.add_argument(
            "--force-changelog",
            action="store_true",
            help="Force changelog generation even for pre-release versions.",
        )

    def add_control_debug_argument(p):
        p.add_argument(
            "--no-debug",
            action="store_true",
            help="Hide debug message",
        )

    def add_cleanup_backup_argument(p):
        p.add_argument(
            "--type",
            choices=["commit", "tag", "all"],
            default="all",
            help="Which backup type to clean (default: all)",
        )
        p.add_argument(
            "--keep",
            type=int,
            default=10,
            help="How many last backup to keep (default: 10)",
        )

    def add_cleanup_branch_argument(p):
        p.add_argument(
            "--prefix",
            required=True,
            help="Branch prefix to match (e.g. feature/, release/)",
        )
        p.add_argument(
            "--merged-only", action="store_true", help="Only cleanup merged branches."
        )
        p.add_argument(
            "--older-than", help="Only delete branches older than N days (e.g. 30d)"
        )

    def add_workflow_argument(p):
        p.add_argument(
            "--enforce", action="store_true", help="Enforce branch-tag strategy"
        )
        p.add_argument(
            "--check_transition",
            action="store_true",
            help="Validate a version/branch transition",
        )
        p.add_argument(
            "--from-branch", help="Override from-branch (e.g. main, develop)"
        )
        p.add_argument("--from-tag", help="Override from-tag (e.g. v1.2.3, v1.2.3a1)")
        p.add_argument("--to-branch", help="Override to-branch (e.g. main, develop)")
        p.add_argument("--to-tag", help="Override to-tag (e.g. main, develop)")

    def add_check_skip(p):
        p.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip branching→tag transition validation (for advanced users)",
    )

    # -----------------------------
    # Subcommand: commit-tag-bump
    # -----------------------------
    commit_parser = subparser.add_parser(
        "commit-tag-bump",
        help="Commit, tag, and version bump",
    )
    add_common_arguments(commit_parser)
    add_tagging_arguments(commit_parser)
    add_control_debug_argument(commit_parser)

    commit_parser.add_argument(
        "message_file",
        nargs="?",
        default="tools/git_commit/commit-msg.txt",
        help="Path to commit message file (default: tools/git_commit/commit-msg.txt) (open in editor before commit)",
    )

    # -----------------------------
    # Subcommand: changelog
    # -----------------------------
    changelog_parser = subparser.add_parser(
        "changelog",
        help="Generate and push changelog",
    )
    add_common_arguments(changelog_parser)
    add_sync_argument(changelog_parser)
    add_force_changelog_argument(changelog_parser)
    add_control_debug_argument(changelog_parser)

    # -----------------------------
    # Subcommand: push
    # -----------------------------
    push_parser = subparser.add_parser(
        "push",
        help="Push commit and tags",
    )
    add_common_arguments(push_parser)

    # -----------------------------
    # Subcommand: validate
    # -----------------------------
    validate_parser = subparser.add_parser(
        "validate",
        help="Validate commit message, etc",
    )
    # Message file
    validate_parser.add_argument(
        "message_file",
        nargs="?",
        default="tools/git_commit/commit-msg.txt",
        help="Path to commit message file (default: tools/git_commit/commit-msg.txt) (open in editor before commit)",
    )
    add_common_arguments(validate_parser)

    # -----------------------------
    # Subcommand: backup
    # -----------------------------
    backup_parser = subparser.add_parser(
        "backup",
        help="Backup files",
    )
    add_common_arguments(backup_parser)

    # -----------------------------
    # Subcommand: all
    # -----------------------------
    all_parser = subparser.add_parser(
        "all",
        help="Run full workflow. Full commit + tag + push flow, etc",
    )
    add_common_arguments(all_parser)
    add_tagging_arguments(all_parser)
    add_sync_argument(all_parser)
    add_force_changelog_argument(all_parser)
    add_control_debug_argument(all_parser)
    add_check_skip(all_parser)

    cleanup_backup_parser = subparser.add_parser(
        "cleaned-backups",
        help="Cleaned old backup files for commit/tag messages",
    )
    add_cleanup_backup_argument(cleanup_backup_parser)

    cleanup_branch_parser = subparser.add_parser(
        "clean-branches", help="Cleanup local + remote branches."
    )
    add_cleanup_branch_argument(cleanup_branch_parser)
    add_control_debug_argument(cleanup_branch_parser)

    # Miscellaneous
    commit_misc_group = all_parser.add_argument_group("Other options")

    commit_misc_group.add_argument(
        "--stage-mode",
        choices=["all", "update"],
        default="all",
        help=(
            "Choose how files are auto-staged\n"
            " all     = git add . (default, stage all changes including new files)\n"
            " update  = git add --update (stage only modified/deleted tracked files)"
        ),
    )

    workflow_parser = subparser.add_parser("workflow", help="Workflow and enforcement")

    add_workflow_argument(workflow_parser)

    # -----------------------------
    # Parse and Dispatch
    # -----------------------------
    args = parser.parse_args()

    DISPATCH = {
        "commit-tag-bump": handle_commit_tag_bump,
        "changelog": handle_changelog,
        "push": handle_push,
        "validate": handle_validate,
        "backup": handle_backup,
        "cleaned-backups": handle_cleaned_backups,
        "all": handle_all,
        "cleanup_branches": handle_cleanup_branches,
    }

    if args.command in DISPATCH:
        DISPATCH[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

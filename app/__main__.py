# tools/git-commit/__main__.py

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
import sys

from .git_commit_tagger import GitCommitTagger
from .utils import ChangelogGenerator

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
        strategy=args.strategy if with_tagging else None,
        bump=args.bump if with_tagging else None,
        pre_release=args.pre_release if with_tagging else None,
        dry_run=args.dry_run,
        version_file=args.version_file if with_version_file else None,
        auto_stage=auto_stage,
        stage_mode=args.stage_mode if auto_stage else None,
    )


# =======================
# 🚀 Command Handlers
# =======================


def handle_commit_tag_bump(args):
    build_git_tool(args).execute_commit_tag_bump()


def handle_push(args):
    tool = build_git_tool(args, with_tagging=False, with_version_file=False)
    tool.push()


def handle_changelog(args):
    # build_git_tool(args, with_tagging=False)
    gen = ChangelogGenerator()
    rendered = gen.generate()
    gen.write_to_files(rendered)


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


# =======================
# 🏁 CLI Entry
# =======================


def main() -> None:
    print("✅ CLI launched!")

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
            default="./tools/git_commit/commit-msg.txt",
            help="Path to commit message file (default: ./tools/git_commit/commit-msg.txt) (open in editor before commit)",
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

    def add_tagging_arguments(p):
        p.add_argument(
            "--strategy",
            choices=["semver", "date", "gitcount", "commitizen"],
            default="semver",
            help="Strategy to generate tag (Auto generate tag using a strategy). Tagging strategy (e.g. semver, date, gitcount, or commitizen)",
        )
        p.add_argument(
            "--bump",
            choices=["patch", "minor", "major", "auto"],
            required=True,
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
            "--pre-release",
            help="Optional Pre-release label (e.g. alpha, beta, rc, dev, next, preview, etc)",
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
        "all": handle_all,
    }

    if args.command in DISPATCH:
        DISPATCH[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

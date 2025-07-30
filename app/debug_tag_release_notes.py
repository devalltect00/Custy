# app\git_commit_tagger.py
""" """
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from termcolor import colored

from .utils import (BackupManager, ChangelogGenerator, CommitizenHelper,
                    CommitizenStrategy, DateStrategy, GitCountStrategy,
                    GitHelper, PEP404Strategy, ReleaseInfo, ReleaseNoteBuilder,
                    SemverStrategy, VersionType, contains_allowed_commit_type,
                    detect_project_strategy, get_last_tag_before,
                    get_sorted_tags, maybe_assert_is_final)

# =======================
# 🚀 Main Class
# =======================


class GitCommitTagger:
    """Automates Git commit + tagging flow, with support for bumping, strategy, dry-run, and version file updates."""

    def __init__(
        self,
        message_file: str,
        tag: str | None,
        tag_msg: str | None,
        tag_msg_file: str | None,
        strategy: str | None,
        bump: str | None,
        pre_release: str | None = None,
        post_release: bool | None = False,
        dev_release: bool | None = False,
        meta: str | None = None,
        epoch: int | None = None,
        force_tag: bool | None = False,
        dry_run: bool = False,
        version_file: str | None = None,
        auto_stage: bool | None = False,
        stage_mode: str | None = "all",
        force_changelog: bool | None = False,
    ) -> None:
        self.message_path: Path = Path(message_file)
        self.tag_input: str | None = tag
        self.tag_msg_input: str | None = tag_msg
        self.tag_msg_file: str | None = tag_msg_file
        self.strategy_input: str | None = strategy
        self.bump_level: str | None = bump
        self.pre_release: str | None = pre_release
        self.post_release: bool | None = post_release
        self.dev_release: bool | None = dev_release
        self.meta: str | None = meta
        self.epoch: int | None = epoch
        self.force_tag: bool | None = force_tag
        self.dry_run: bool = dry_run
        self.version_file: str | None = Path(version_file) if version_file else None
        self.auto_stage: bool | None = auto_stage
        self.stage_mode: str | None = stage_mode
        self.force_changelog: bool | None = force_changelog

        self.tag: str = ""
        self.tag_msg: str = ""
        self.backup_commit_message_path: Path = None

        self.git = GitHelper(dry_run=dry_run)
        self.cz = CommitizenHelper(dry_run=dry_run)
        self.changelog_generator = ChangelogGenerator(dry_run=dry_run)
        self.backup_manager = BackupManager(keep=10)

    def _resolve_tag(self) -> None:
        # if self.bump_level:
        #     current_tag = self.get_latest_tag()
        #     self.tag = self.bump_version(current_tag, self.bump_level)
        # elif self.tag_input:
        #     self.tag = self.tag_input
        if self.tag_input:
            self.tag = self.tag_input
        elif self.strategy_input == "semver" and self.bump_level:
            self.tag = SemverStrategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                build_meta=self.meta,
            ).get_next_tag()
        elif self.strategy_input == "pep440" and self.bump_level:
            self.tag = PEP404Strategy(
                bump=self.bump_level,
                pre_release=self.pre_release,
                post_release=self.post_release,
                dev_release=self.dev_release,
                local=self.meta,
                epoch=self.epoch,
            ).get_next_tag()
        elif self.strategy_input == "commitizen" and self.bump_level == "auto":
            self.tag = CommitizenStrategy(self.pre_release).get_next_tag()
        elif self.strategy_input == "date":
            self.tag = DateStrategy().get_next_tag()
        elif self.strategy_input == "gitcount":
            self.tag = GitCountStrategy().get_next_tag()
        else:
            print("❌ ERROR: Provide either --tag or use  --strategy with --bump.")
            sys.exit(1)

        # self.tag_msg = self.tag_msg_input or self.tag
        self._resolve_tag_message()

    def _resolve_tag_message(self) -> None:
        """
        Resolve tag message: use CLI --tag-msg, or fallback to tag-msg.txt or tag name.
        1. CLI argument --tag-msg (self.tag_msg_input)
        2. CLI argument --tag-msg-file (self.tag_msg_file) (Open editor if file doesn't exist)
        3. Fallback to default: 'Release vX.Y.Z'
        """

        if self.tag_msg_input:
            self.tag_msg = self.tag_msg_input
            print("✅ Using tag message from --tag-msg CLI input.")
            return

        tag_msg_path = Path(self.tag_msg_file or "templates/tag-msg.txt")

        if not tag_msg_path.exists():
            # Create file with default content
            default_content = (
                f"Release {self.tag}\n\n# Write additional tag notes below\n"
            )
            tag_msg_path.parent.mkdir(parents=True, exist_ok=True)
            tag_msg_path.write_text(default_content, encoding="utf-8")
            print(f"📝 Created default tag message file: {tag_msg_path}")

        # self._open_editor(tag_msg_path)

    def _open_editor(self, path: Path) -> None:
        print(f"📝 Opening {path} for editing...")
        editors = [["code", "--wait"], ["notepad"]]
        for editor_cmd in editors:
            try:
                if not self.dry_run:
                    self.git.runner.run(
                        command=editor_cmd + [str(path)],
                        shell=True,
                        check=True,
                    )
                return
            except Exception:
                continue
        print("❌ ERROR: Could not open editor. Please edit the message file manually.")
        sys.exit(1)

    def _prepare_release_message_from_prereleases(self, version: str) -> str:
        """ """
        version_prefix = version.removeprefix("v")  # handle both v1.3.4 abd 1.3.4
        all_tags = (
            self.git.get_all_tags()
        )  # expects list[str], e.g. ['1.3.4a1', '1.3.4b2', '1.3.3', ...]
        sorted_tags = get_sorted_tags(all_tags)

        # Find matching pre-release tags for this version, e.g., 1.3.4a1, b1, rc1...
        prerelease_tags = [
            t
            for t in sorted_tags
            if t.startswith(version_prefix) and re.search(r"(a|b|rc|dev)\d*", t)
        ]
        prerelease_tags = list(reversed(prerelease_tags))  # Newest tag first

        if not prerelease_tags:
            return f"Release v{version}\n\n---\n\n_No pre-release tags found for {version}_"

        sections = []

        for i, tag in enumerate(prerelease_tags):
            # Find previous tag to compute commit range
            if i + 1 < len(prerelease_tags):
                prev_tag = prerelease_tags[i + 1]
            else:
                prev_tag = get_last_tag_before(tag, sorted_tags)

            commits = self.git.get_commits_between_tags(prev_tag, tag)

            if not commits:
                continue

            section_lines = [f"### 🔹 from tag: {tag}\n"]

            for c in commits:
                sha = c["sha"][:7]
                author = c["author"]
                date = datetime.strptime(c["date"], "%a %b %d %H:%M:%S %Y %z")
                header = c["header"]
                body = self._clean_commit_body(c["body"])

                commit_block = dedent(f"""
                    -  **{header}**
                    _SHA: {sha}_
                    _Author: {author}_
                    _Date: {date}_

                    {body.strip()}
                """).strip()

                section_lines.append(commit_block)

            sections.append("\n\n".join(section_lines))

        final_output = f"Release v{version}\n\n---\n\n" + "\n\n---\n\n".join(sections)
        return final_output

    def _clean_commit_body(self, body: str) -> str:
        """
        Remove 'Changelog: handled separately' from footer/body
        """
        lines = body.strip().splitlines()
        cleaned = [
            line for line in lines if "Changelog: handled separately" not in line
        ]
        return "\n".join(cleaned).strip()

    def _write_template_to_message_file(self, content: str):
        """
        Write prefilled message content to both commit-msg.txt and tag-msg.txt
        """
        if self.message_path:
            self.message_path.write_text(content.strip(), encoding="utf-8")
        if self.tag_msg_file:
            Path(self.tag_msg_file).write_text(content.strip(), encoding="utf-8")

    def _is_pre_release(self, version: str) -> bool:
        return bool(re.search(r"(a|b|rc|dev)\d*", version))

    def _prepare_and_edit_release_message_if_final(self):
        """
        If this is a final release (not pre-release), aggregate commits
        and prefill both commit and tag message files before opening editor.
        """
        if not self._is_pre_release(self.tag) and self.pre_release is None:
            notes = self._prepare_release_message_from_prereleases(self.tag)
            self._write_template_to_message_file(notes)
        self._open_editor()

    def _generate_release_notes(self):
        """
        Generate commit-msg.txt and tag-msg.txt using ReleaseNoteBuilder.
        Handles pre-release history, changelog logic, and commit metadata.
        """
        version = self.tag
        version_type = VersionType.detect(version)
        all_tags = self.git.get_all_tags()
        sorted_tags = get_sorted_tags(all_tags)
        version_prefix = version.removeprefix("v")

        # Find pre-release tags this version (e.g. v1.4.0a1, rc1, etc.)
        prereleases = [
            t for t in sorted_tags
            if t.startswith(version_prefix) and re.search(r"(a|b|rc|dev)", t)
        ]
        prereleases = list(reversed(prereleases))
        latest_pre = prereleases[0] if prereleases else None

        # Determine if there are any changes since last RC/prerelease
        has_changes = True
        if version_type == VersionType.FINAL and latest_pre:
            changes = self.git.get_commits_between_tags(latest_pre, version)
            has_changes = bool(changes)

        # Build structured release info
        info = ReleaseInfo(
            version=version,
            version_type=version_type,
            app_name="Custy",
            prerelease_tags=prereleases,
            latest_prerelease=latest_pre,
            has_changes_since_rc=has_changes
        )

        builder = ReleaseNoteBuilder(info)

        # Write commit-msg.txt
        if self.message_path:
            self.message_path.write_text(builder.build_commit_msg(), encoding="utf-8")

        # Write tag-msg.txt
        if self.tag_msg_file:
            Path(self.tag_msg_file).write_text(builder.build_tag_msg(), encoding="utf-8")

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
        stage_mode=None,
        force_changelog=args.force_changelog
        if hasattr(args, "force_changelog")
        else False,
    )

def handle_all(args):
    tool = build_git_tool(args, auto_stage=True)
    # tool._prepare_and_edit_release_message_if_final()
    tool._resolve_tag()
    tool._generate_release_notes()
    tool._open_editor(args.message_file)
    # tool._resolve_tag()
    print(f"Next tag version: {tool.tag}")

if __name__ == "__main__":
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

    def add_tagging_arguments(p):
        p.add_argument(
            "--strategy",
            choices=["semver", "pep440", "date", "gitcount", "commitizen"],
            default=detect_project_strategy(),  # <-- auto logic
            help=(
                "Strategy to generate tag (Auto generate tag using a strategy). ",
                "Tagging strategy (e.g. pep440, semver, date, gitcount, or commitizen). ",
                "CLI overrides config or auto-detect.",
            ),
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

    all_parser = subparser.add_parser(
        "all",
        help="Run full workflow. Full commit + tag + push flow, etc",
    )
    add_common_arguments(all_parser)
    add_tagging_arguments(all_parser)

    args = parser.parse_args()

    DISPATCH = {
        "all": handle_all,
    }

    if args.command in DISPATCH:
        DISPATCH[args.command](args)



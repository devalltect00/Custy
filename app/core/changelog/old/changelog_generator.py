# app/core/changelog/old/changelog_generator.py
"""
Changelog Generator

Generates a semantic changelog grouped by Git tags and categorized by commit type,
based on conventional commits. Output is rendered using a Jinja2 template.

Support dry-run mode, and can be configured via [tool.mycz] in pyproject.toml.

=====

Generates structured changelog from Git history.

Architecture:
    CLI
      → ChangelogGenerator
        → GitService
        → MessageAggregator
        → CommitPipeline
        → Template rendering

Responsibilities:
- Fetch tags and commits from GitService
- Normalize and sort tags
- Process commit messages through pipeline
- Group commits by type/scope
- Render changelog using Jinja2

Supports:
- Dry-run mode
- Config-driven behavior
- Template injection
"""

import sys
import tomllib
from datetime import datetime
from packaging.version import Version, InvalidVersion
from jinja2 import Template
from rich.console import Console
from rich.progress import track
from typing import List, Optional

from app.constants.path import CUSTY_SETTINGS, CUSTY_CHANGELOG_J2

from app.core.dry_run import DryRunSupport
# from app.core.git_ops.helper import GitHelper
from app.core.git_ops.git.factory import create_git_service

from .changelog_cleaner import ChangelogCleaner
from app.config.config_loader import ConfigLoader

from .pipeline import (
    CommitPipeline,
    SkipMergeStage,
    CleanStage,
    BreakingChangeStage,
    ReleaseTransformStage,
    NormalTransformStage,
)

from .message_providers import (
    GitMessageProvider,
    TemplateMessageProvider,
)

from .message_aggregator import MessageAggregator



class ChangelogGenerator(DryRunSupport):
    """
    Generates a categorized changelog based on Git commit message,
    with optional dry-run mode and configuration from pyproject.toml

    Args:
        config_path (str): Path to config file
        dry_run (bool): Simulate execution
        template_path (str | None): Custom template path

    Returns:
        None

    Raises:
        RuntimeError: If template loading fails

    Examples:
        >>> generator = ChangelogGenerator()
        >>> content = generator.generate()
    """

    def __init__(
        self,
        # config_path: str = "pyproject.toml",
        config_path: str = CUSTY_SETTINGS,
        dry_run: bool = False,
        template_path: Optional[str] = None,
        # template_path: str | None = CUSTY_CHANGELOG_J2,
    ) -> None:
        """
        Initializes the generator.

        Args:
            config_path (str): Path to the pyproject.toml or .custy.toml file.
            dry_run (bool): If True, simulate actions (e.g., file writes).
            template_path: Optional[str]: Path to the custom Jinja2 template.

        """
        super().__init__(dry_run=dry_run)
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.config_loader = ConfigLoader().get("cli", "templates", "file", "changelog")
        self.template_path = (
            template_path
            or self.config_loader
            or self.config.get(
                "template_path",
                # "templates/changelog/changelog.j2",
                CUSTY_CHANGELOG_J2,
            )
        )

        self.git = create_git_service(dry_run=dry_run)

        ##### Adding
        # self.config_changelog_loader = ConfigLoader(".custy.toml")
        self.config_changelog_loader = ConfigLoader()
        self.config_changelog = self.config_changelog_loader.config
        #####/

    def _load_config(self, path: str) -> dict:
        """
        # Loads config from [tool.mycz] section of pyproject.toml
        Load configuration from TOML file.

        Args:
            path (str): Path to the pyproject.toml file.

        Returns:
            dict: Parsed config dictionary

        """
        try:
            with open(path, "rb") as f:
                data = tomllib.load(f)
                return data.get("tool", {}).get("mycz", {})
        except FileNotFoundError:
            return {}

    def _load_commit_template(self) -> str:
        """
        Load commit-msg template file if exists

        Returns:
            str: Template content or empty string
        """
        # template_path = self.config_changelog_loader.get(
        #     "changelog", "template", "commit_template"
        # )
        template_path = self.config_changelog_loader.get(
            "cli", "templates", "file", "commit_message",
        )

        if not template_path:
            return ""

        try:
            with open(template_path, encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""

    def get_commits(self) -> list[str]:
        """
        Extracts all Git commit messages.

        Returns:
            list[str]: List of commit messages (latest first).

        """

        def on_error():
            print("❌ ERROR: Failed to extract commit logs.")
            print("💡 Make sure this is a valid Git repository.")
            sys.exit(1)

        result = self.runner.run(
            command=["git", "log", "--pretty=format:%B"],
            capture_output=True,
            text=True,
            check=True,
            on_error=on_error,
        )
        if result is None:
            return []

        raw = result.stdout.strip()
        return [msg.strip() for msg in raw.split("\n\n") if msg.strip()]

    # --------------------------------------------------------
    # NEW: TAG NORMALIZATION + SORTING
    # --------------------------------------------------------

    def _normalize_tag(self, tag: str) -> str:
        """
        Remove leading 'v'.
        """
        return tag.lstrip("v")

    def _is_valid_tag(self, tag: str) -> bool:
        """
        Filter unwanted tags.
        """
        ignore_keywords = ["test", "temp", "ci"]
        return not any(k in tag.lower() for k in ignore_keywords)

    def _sort_tags(self, tags: list[str]) -> list[str]:
        """
        Sort tags using semantic version ordering.

        Returns:
            list[str]: Sorted tags (latest first)
        """
        valid_tags = []

        for tag in tags:
            if not tag:
                continue

            if not self._is_valid_tag(tag):
                continue

            normalized = self._normalize_tag(tag)

            try:
                Version(normalized)
                valid_tags.append((tag, normalized))
            except InvalidVersion:
                continue

        # Sort DESCENDING (latest first)
        valid_tags.sort(key=lambda x: Version(x[1]), reverse=True)

        # Return original tag format (keep v if exists)
        return [t[0] for t in valid_tags]

    # --------------------------------------------------------

    def generate(self, commits: list[str] | None = None) -> str:
        """
        Generate Rendered changelog content from tag and commits.

        Args:
            commits: (list[str]): List of commit messages.

        Returns:
            str: Formatted changelog string. Rendered changelog.

        """
        from collections import defaultdict

        original_silent = self.runner.get_silent()
        self.git.executor.set_silent(True)

        is_dry_run_backup = self.git.executor.get_is_dry_run()
        self.git.executor.set_is_dry_run(False)
        raw_tags = self.git.get_tags()
        self.git.executor.set_is_dry_run(is_dry_run_backup)

        # tags.insert(0, "")  # Include commits before first tag

        # 🔥 FIXED: normalize + sort
        sorted_tags = self._sort_tags(raw_tags)

        # Add unreleased at top
        tags = [""] + sorted_tags  # "" = Unreleased

        releases = []

        # =========================
        # CONFIG LOAD
        # =========================
        ##### Adding2 + 4
        # cleaning_config = self.config_changelog_loader.get("changelog", "cleaning", default={})
        # # print("cleaning_config", cleaning_config)
        # cleaner = ChangelogCleaner(config=cleaning_config)

        # tag_behavior = self.config_changelog_loader.get("changelog", "tag_behavior", default={})
        # scope_map = self.config_changelog_loader.get("changelog", "scope_map", default={})

        # breaking_config = self.config_changelog_loader.get("changelog", "breaking", default={})
        # breaking_enabled = breaking_config.get("enable", False)
        # breaking_keywords = breaking_config.get("keywords", [])

        # repo_url = self.config_changelog_loader.get("changelog", "links", "repository")
        # enable_compare = self.config_changelog_loader.get("changelog", "links", "enable_compare", default=False)

         # =========================
        # CONFIG
        # =========================
        cleaning_config = self.config_changelog_loader.get("changelog", "cleaning", default={})
        cleaner = ChangelogCleaner(config=cleaning_config)

        breaking_cfg = self.config_changelog_loader.get("changelog", "breaking", default={})
        scope_map = self.config_changelog_loader.get("changelog", "scope_map", default={})
        tag_behavior = self.config_changelog_loader.get("changelog", "tag_behavior", default={})

        repo_url = self.config_changelog_loader.get("changelog", "links", "repository")
        enable_compare = self.config_changelog_loader.get("changelog", "links", "enable_compare", default=False)

        template_cfg = self.config_changelog_loader.get("changelog", "template", default={})
        template_enabled = template_cfg.get("enabled", False)
        template_mode = template_cfg.get("mode", "append_top")
        # template_only_latest = template_cfg.get("only_latest", True)

        # release_config = self.config_changelog_loader.get("changelog", "release", default={})
        # render_config = self.config_changelog_loader.get("changelog", "render", default={})
        #####/2 + 4

        # =========================
        # PIPELINE
        # =========================
        pipeline = CommitPipeline([
            SkipMergeStage(
                ignore=self.config_changelog_loader.get("changelog", "ignore_merge_commits", True)
            ),
            CleanStage(cleaner),
            BreakingChangeStage(
                breaking_cfg.get("enable", False),
                breaking_cfg.get("keywords", []),
            ),
            ReleaseTransformStage(),
            NormalTransformStage(),
        ])

        yes=True

        console = Console()
        for i in track(
            range(len(tags) - 1),
            description="[bold cyan]Generating changelog...",
        ):
            prev = tags[i + 1]
            current = tags[i]

            # =========================
            # MESSAGE PROVIDERS
            # =========================
            providers = [GitMessageProvider(self.git)]

            if template_enabled:
                providers.append(
                    TemplateMessageProvider(
                        loader=self._load_commit_template,
                        only_unreleased=True,  # 🔥 important
                    )
                )

            aggregator = MessageAggregator(
                providers=providers,
                mode=template_mode,
            )

            messages = aggregator.get_messages(prev, current, is_latest=(i == 0))

            if not messages:
                continue

            # =========================
            # PIPELINE PROCESSING
            # =========================
            parsed = pipeline.run(messages, self.git)

            # =========================
            # GROUPING
            # =========================
            grouped = {}

            for c in parsed:
                t = c["type"]
                scope = scope_map.get(c["scope"], c["scope"]).lower().strip()

                grouped.setdefault(t, defaultdict(list))
                grouped[t][scope].append(c)

            # =========================
            # DEDUP
            # =========================
            def dedup(items):
                seen = set()
                result = []
                for c in items:
                    key = (c["type"], c["scope"], c["subject"])
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append(c)
                return result

            for t in grouped:
                for s in grouped[t]:
                    grouped[t][s] = dedup(grouped[t][s])

            # =========================
            # COMPARE LINK
            # =========================
            compare_url = None
            if enable_compare and repo_url and prev:
                compare_url = f"{repo_url}/compare/{prev}...{current}"

            # =========================
            # TAG BEHAVIOR
            # =========================
            behavior = tag_behavior.get(current, {})

            if behavior.get("mode") == "hidden":
                continue

            release_entry = {
                "version": current or "Unreleased",
                "date": self.git.get_tag_date(current)
                if current else datetime.now().strftime("%Y-%m-%d"),
                "changes": grouped,
                "compare_url": compare_url,
            }

            if behavior.get("mode") == "title_only":
                release_entry["changes"] = {}

            if behavior.get("mode") == "custom":
                release_entry["changes"] = {}
                release_entry["custom_message"] = behavior.get("message")

            releases.append(release_entry)
            #####/ + 3

        self.runner.set_silent(original_silent)  # Restore print setting

        # Render
        try:
            with open(self.template_path, encoding="utf-8") as f:
                template_str = f.read()
            template = Template(template_str)
            return template.render(releases=releases).strip()
            # rendered = template.render(releases=releases).strip()
            # rendered = template.render
            # print(print("self.config", self.config))(releases=releases).strip()

            # 🔥 Apply template integration if enabled
            # rendered = self.apply_template_integration(rendered)

            return rendered
        except FileNotFoundError:
            print(f"❌ Template file not found: {self.template_path}")
            sys.exit(1)

    def apply_template_integration(self, generated: str) -> str:
        """
        print(print("self.config", self.config))
        Apply commit-msg template integration into changelog
        """

        template_enabled = self.config_changelog_loader.get(
            "changelog", "template", "enabled", default=False
        )

        if not template_enabled:
            return generated

        mode = self.config_changelog_loader.get(
            "changelog", "template", "mode", default="append_top"
        )

        template_content = self._load_commit_template()

        if not template_content:
            return generated

        # Clean template (optional minimal cleanup)
        template_content = template_content.strip()

        if mode == "override":
            return template_content

        if mode == "append_top":
            return f"{template_content}\n\n---\n\n{generated}"

        if mode == "append_bottom":
            return f"{generated}\n\n---\n\n{template_content}"

        if mode == "merge":
            # simple merge: inject into top release
            parts = generated.split("\n", 1)
            if len(parts) == 2:
                header, rest = parts
                return f"{header}\n\n{template_content}\n\n{rest}"
            return generated

        return generated



    def write_to_files(self, content: str, path: str = "CHANGELOG.md") -> None:
        """
        Saves the changelog content to a file (or simulates if dry-run).

        Args:
            content (str): The changelog content to write.
            path (str): Path to the output file.

        """
        if self.runner.is_dry_run:
            print(f"(dry-run) Would write changelog to: {path}")
            print("\n--- Begin Preview ---\n")
            print(content)
            print("\n--- End Preview ---\n")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ CHANGELOG written to {path}")

    # --------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------
    # --------------------------------------------------------

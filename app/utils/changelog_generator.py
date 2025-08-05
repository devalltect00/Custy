# app\utils\changelog_generator.py
"""
Changelog Generator

Generates a semantic changelog grouped by Git tags and categorized by commit type,
based on conventional commits. Output is rendered using a Jinja2 template.

Support dry-run mode, and can be configured via [tool.mycz] in pyproject.toml.
"""

import sys
from datetime import datetime

import tomllib
from jinja2 import Template
from rich.console import Console
from rich.progress import track

from .dry_run_support import DryRunSupport
from .git import GitHelper


class ChangelogGenerator(DryRunSupport):
    """
    Generates a categorized changelog based on Git commit message,
    with optional dry-run mode and configuration from pyproject.toml
    """

    def __init__(
        self,
        config_path: str = "pyproject.toml",
        dry_run: bool = False,
        template_path: str | None = None,
    ) -> None:
        """
        Initializes the generator.

        Args:
            config_path (str): Path to the pyproject.toml file.
            dry_run (bool): If True, simulate actions (e.g., file writes).
            template_path: Optional[str]: Path to the custom Jinja2 template.

        """
        super().__init__(dry_run=dry_run)
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.template_path = template_path or self.config.get(
            "template_path",
            "templates/changelog/changelog.j2",
        )

        self.git = GitHelper(dry_run=dry_run)

    def _load_config(self, path: str) -> dict:
        """
        Loads config from [tool.mycz] section of pyproject.toml

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

    def generate(self, commits: list[str] | None = None) -> str:
        """
        Generate Rendered changelog content from tag and commits.

        Args:
            commits: (list[str]): List of commit messages.

        Returns:
            str: Formatted changelog string. Rendered changelog.

        """
        original_silent = self.runner.get_silent()
        self.git.runner.set_silent(True)

        tags = self.git.get_tags()
        tags.insert(0, "")  # Include commits before first tag
        releases = []

        console = Console()
        for i in track(
            range(len(tags) - 1),
            description="[bold cyan]Generating changelog...",
        ):
            prev = tags[i + 1]
            current = tags[i]
            messages = self.git.get_commits_between(prev, current)
            if not messages:
                continue

            parsed = [self.git.parse_commit(msg) for msg in messages]

            grouped: dict[str, list[dict]] = {}
            for commit in parsed:
                grouped.setdefault(commit["type"], []).append(commit)

            releases.append(
                {
                    "version": current or "Unreleased",  # Optionally pull latest tag
                    "date": self.git.get_tag_date(current)
                    if current
                    else datetime.now().strftime("%Y-%m-%d"),
                    "changes": grouped,
                },
            )

        self.runner.set_silent(original_silent)  # Restore print setting

        # Render
        try:
            with open(self.template_path, encoding="utf-8") as f:
                template_str = f.read()
            template = Template(template_str)
            return template.render(releases=releases).strip()
        except FileNotFoundError:
            print(f"❌ Template file not found: {self.template_path}")
            sys.exit(1)

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
            print(f"✅ CHANGELOG.md written to {path}")

    # --------------------------------------------------------
    # Internal helpers
    # --------------------------------------------------------
    # --------------------------------------------------------

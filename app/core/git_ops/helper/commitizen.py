# app/core/git_ops/helper/commitizen.py

import re
import subprocess
import sys
import logging
from pathlib import Path

from app.core.dry_run import DryRunSupport

"""
Utilities class (Commitizen)
"""

logger = logging.getLogger(__name__)

# =======================
# 🔧 Utilities CLass
# =======================


class CommitizenHelper(DryRunSupport):
    """
    Helper class for Commitizen-related operations.
    """

    def commit(self) -> None:
        """Running `cz commit` top open the COmmitizen commit prompt."""
        print("📝 Running `cz commit`...")
        try:
            command = ["cz", "commit"]
            self.runner.run(command, check=True)
        except subprocess.CalledProcessError:
            print("❌ ERROR: Commit failed.")
            sys.exit(1)

    # def check_commit(self) -> None:
    #     """cz check"""
    #     print("🧪 Validating commit message with cz check...")
    #     try:
    #         command = ["cz", "check"]
    #         self.runner.run(command, check=True)
    #     except subprocess.CalledProcessError:
    #         print("❌ Commit message does not follow conventional format.")
    #         sys.exit(1)

    def generate_changelog_with_commitizen(self) -> None:
        """Cz changelog"""
        print("📦 Generating changelog using Commitizen...")
        try:
            self.runner.run(["cz", "changelog"], check=False)
            print("✅ CHANGELOG.md generated")
        except subprocess.CalledProcessError as e:
            print("❌ ERROR: Failed to generate changelog with Commitizen.")
            print(f"🔍 Detail: {e}")
            sys.exit(1)

    def check_commit(self, path: Path) -> None:
        """
        Args:
            path (Path): the path of commit message (commit-message.txt)

        """
        print("🧪 Validating commit message message With Commitizen...")
        try:
            # cz check --commit-msg-file {message_path}
            self.runner.run(
                ["cz", "check", "--commit-msg-file", str(path)],
                check=True,
                read_only=True,
            )
            print("✅ Commit message passed Commitizen check.")
        except subprocess.CalledProcessError:
            print("❌ Commit message does not follow Conventional Commits.")
            print("💡 Example: feat(api): add authentication middleware")
            sys.exit(1)

    def update_cz_toml_version(self, new_version: str) -> None:
        """
        Updates the `version` field in .cz.toml to match the new version tag.

        Args:
            new_version (str): The new semantic version (e.g., "v1.2.3")

        Notes:
            - Strips leading 'v' before writing, if present.
            - Only modifes the `version = "..."` line.
            - Safe against missing file or malformed format.

        Raises:
            SystemExit: If .cz.toml does not exist or is not writable.

        """
        cz_path = Path(".cz.toml")
        if not cz_path.exists():
            logger.warning("⚠️ [yellow]Skipping[/yellow] [dim].cz.toml[/dim] update: file not found.")
            return

        cleaned_version = new_version.lstrip("v")

        if self.runner.get_is_dry_run():
            logger.info(
                "[dry_run](dry-run)[/dry_run] Would update "
                f"[dim].cz.toml[/dim] version to {cleaned_version}."
            )
            return

        try:
            content = cz_path.read_text()

            # Clean "v" prefix if it exists
            # Use regex to replace: version = "1.0.0"
            new_content, count = re.subn(
                r'version\s*=\s*".*?"',
                f'version = "{cleaned_version}"',
                content,
            )

            if count == 0:
                logger.warning("⚠️ Could not find 'version =' field in [dim].cz.toml[/dim].")
                return

            cz_path.write_text(new_content)
            # logger.info(f"✅ [green]Updated[/green] [dim].cz.toml[/dim] version to {cleaned_version}")
            logger.info(f"✅ [dim].cz.toml[/dim] [green]Updated[/green]. Version updated to {cleaned_version}")
        except Exception as e:
            logger.error("❌ [red]ERROR:[red] Failed to update [dim].cz.toml[dim] version.")
            print(f"🔍 Detail: {e}")
            sys.exit(1)

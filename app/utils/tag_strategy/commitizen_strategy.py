# tools\utils\tag_strategy\commitizen_strategy.py
"""
CommitizenStrategy class
"""

import re
import subprocess
import sys

from .semver_strategy import SemverStrategy

# =======================
# 🔧 Concrete Strategies
# =======================


class CommitizenStrategy:
    """Strategy that auto-detects bump level using commitizen
    and delegates to SemverStrategy to build the next tag.
    """

    def __init__(self, pre: str | None) -> None:
        self.pre = pre

    def get_next_tag(self) -> str:
        """Parse `cz bump --dry-run` output to detect bump level."""
        try:
            command = ["cz", "bump", "--dry-run", "--changelog"]
            output = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            print("❌ Failed to run `CZ bump`:")
            print(e.output)
            sys.exit(1)

        # Extract version bump from line like:
        # bump: version 1.0.0 → 1.1.0
        match = re.search(r"bump: version (\d+\.\d+\.\d+) → (\d+\.\d+\.\d+)", output)

        if not match:
            print("❌ No eligible commits found to bump.")
            print("💡 Make sure your commits use conventional commit messages like:")
            print("   - feat: add feature")
            print("   - fix: resolve bug")
            sys.exit(1)

        current_version = match.group(1)
        next_version = match.group(2)

        print(f"🔢 Current version (from Git tag): {current_version}")
        print(f"🔮 Next version (from cz bump): {next_version}")

        bump_level = self._get_bump_type(current_version, next_version)

        return SemverStrategy(bump=bump_level, pre=self.pre).get_next_tag()

    def _get_bump_type(self, current: str, next_: str) -> str:
        cur = list(map(int, current.split(".")))
        nxt = list(map(int, next_.split(".")))

        if nxt[0] > cur[0]:
            return "major"
        if nxt[1] > cur[1]:
            return "minor"
        return "patch"

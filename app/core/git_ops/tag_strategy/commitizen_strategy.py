# app/core/git_ops/tag_strategy/commitizen_strategy.py
"""
Strategy that uses Commitizen to determine bump level.
"""

import re
import subprocess
# import sys
import logging
from typing import Optional

from .semver_strategy import SemverStrategy

logger = logging.getLogger(__name__)

# =======================
# 🔧 Concrete Strategies
# =======================


class CommitizenStrategy:
    """
    Strategy that auto-detects bump level using commitizen
    and delegates to SemverStrategy to build the next tag.

    Detect bump level using Commitizen and generate next SemVer tag.

    Args:
        pre (Optional[str])
        dry_run (bool)
        no_debug (bool)
    """

    def __init__(
        self,
        pre: Optional[str] = None,
        dry_run: bool = False,
        no_debug: bool = False,
    ) -> None:
        self.pre = pre
        self.dry_run = dry_run
        self.no_debug = no_debug

    def get_next_tag(self) -> str:
        """
        Parse `cz bump --dry-run` output to detect bump level.

        Determine bump using `cz bump --dry-run`.

        Returns:
            str: next version
        """
        try:
            command = ["cz", "bump", "--dry-run", "--changelog"]

            logger.debug(f"Running: {' '.join(command)}")

            output = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            logger.error("❌ Commitizen failed. Failed to run `CZ bump`:")
            logger.error(e.output)
            # sys.exit(1)
            raise RuntimeError("Failed to run commitizen") from e

        # Extract version bump from line like:
        # bump: version 1.0.0 → 1.1.0
        # match = re.search(r"bump: version (\d+\.\d+\.\d+) → (\d+\.\d+\.\d+)", output)
        match = re.search(
            r"bump: version (\d+\.\d+\.\d+) → (\d+\.\d+\.\d+)",
            output,
        )

        if not match:
            logger.error("❌ No eligible commits found to bump.")
            logger.info("💡 Make sure your commits use conventional commit messages like:")
            logger.info("   - feat: add feature")
            logger.info("   - fix: resolve bug")
            # sys.exit(1)
            # raise RuntimeError("No eligible commits found to bump.") from e
            raise RuntimeError("No eligible commits found to bump.")

        current_version = match.group(1)
        next_version = match.group(2)

        logger.info(f"🔢 Current version (from Git tag): {current_version}")
        logger.info(f"🔮 Next version (from cz bump): {next_version}")

        bump_level = self._get_bump_type(current_version, next_version)

        next_version = SemverStrategy(
            bump=bump_level,
            pre=self.pre,
            dry_run=self.dry_run,
            no_debug=self.no_debug,
        ).get_next_tag()

        logger.info(f"Next Commitizen + SemVer version: {next_version}")
        return next_version

    def _get_bump_type(self, current: str, next_: str) -> str:
        """
        Infer bump level from version diff.
        """
        cur = list(map(int, current.split(".")))
        nxt = list(map(int, next_.split(".")))

        if nxt[0] > cur[0]:
            return "major"
        if nxt[1] > cur[1]:
            return "minor"
        return "patch"

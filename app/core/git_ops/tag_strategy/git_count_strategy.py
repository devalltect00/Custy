# app/core/git_ops/tag_strategy/git_count_strategy.py
"""
Strategy based on total commit count.
"""

# import subprocess
# import sys
import logging

from app.core.git_ops.git.factory import create_git_service

logger = logging.getLogger(__name__)

# =======================
# 🔧 Concrete Strategies
# =======================


class GitCountStrategy:
    """
    Generate version using commit count.

    Example:
        v123

    Args:
        dry_run (bool)
        no_debug (bool)
    """

    def __init__(
        self,
        dry_run: bool = False,
        no_debug: bool = False,
    ) -> None:
        self.git = create_git_service(dry_run=dry_run, no_debug=no_debug)

    def get_next_tag(self) -> str:
        """
        Count commits and generate tag.

        Returns:
            str
        """
        try:
            count = self.git.get_commit_count()

            next_version = f"v{count}"
            logger.info(f"Next Git Count version: {next_version}")

            return next_version
        except Exception as e:
            logger.exception(f"❌ Failed to count Git commits. Error: {e}")
            # sys.exit(1)
            raise

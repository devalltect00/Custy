# app/core/git_ops/tag_strategy/pep440_strategy.py
"""
PEP440 tag generation strategy.
"""

import logging
from typing import Optional

# from ..git_helper import GitHelper
from app.core.git_ops.git.factory import create_git_service
from app.core.git_ops.helper.pep440_helper import PEP440VersionHelper

logger = logging.getLogger(__name__)

# =======================
# 🔧 Concrete Strategies
# =======================


class PEP440Strategy:
    """
    Strategy for generating PEP440-compliant version tags.

    Args:
        bump (Optional[str]): major/minor/patch/None
        epoch (Optional[int])
        pre_release (Optional[str])
        post_release (Optional[bool])
        dev_release (Optional[bool])
        local (Optional[str])
        dry_run (bool)
        no_debug (bool)
    """

    def __init__(
        self,
        bump: Optional[str],
        epoch: Optional[int],
        pre_release: Optional[str] = None,
        post_release: Optional[bool] = None,
        dev_release: Optional[bool] = None,
        local: Optional[str] = None,
        dry_run: bool = False,
        no_debug: bool = False,
    ) -> None:
        self.bump = bump
        self.pre_release = pre_release
        self.post_release = post_release
        self.dev_release = dev_release
        self.local = local
        self.epoch = epoch

        self.git = create_git_service(dry_run=dry_run, no_debug=no_debug)

    def get_next_tag(self) -> str:
        """
        Generate next PEP440 version.

        Returns:
            str: new version
        """
        latest_tag = self.git.get_latest_tag()
        logger.debug(f"Latest tag: {latest_tag}")

        helper = PEP440VersionHelper(latest_tag)

        level = None if self.bump == "auto" else self.bump

        next_version = helper.get_bump_version(
            # level=self.bump,
            level=level,
            target_pre=self.pre_release,
            post=self.post_release,
            dev=self.dev_release,
            local=self.local,
            epoch=self.epoch,
        )

        logger.info(f"Next PEP440 version: {next_version}")
        return next_version

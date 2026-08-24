# app/core/git_ops/tag_strategy/semver_strategy.py
"""
SemVer tag generation strategy.
"""

import logging
from typing import Optional

# from ..git_helper import GitHelper
from app.core.git_ops.git.factory import create_git_service
from app.core.git_ops.helper.semver_helper import SemverVersionHelper

logger = logging.getLogger(__name__)

# =======================
# 🔧 Concrete Strategies
# =======================


class SemverStrategy:
    """
    Strategy for generating SemVer-compliant version tags.

    Args:
        bump (Optional[str]): major/minor/patch
        pre_release (Optional[str]): alpha/beta/rc
        build_meta (Optional[str])
        dev (bool)
        post (bool)
        dry_run (bool)
        no_debug (bool)
    """

    def __init__(
        self,
        bump: Optional[str],
        pre_release: Optional[str] = None,
        build_meta: Optional[str] = None,
        dev: bool = False,
        post: bool = False,
        dry_run: bool = False,
        no_debug: bool = False,
    ) -> None:
        self.bump = bump
        self.pre_release = pre_release
        self.build_meta = build_meta
        self.dev = dev
        self.post = post
        
        self.git = create_git_service(dry_run=dry_run, no_debug=no_debug)

    def get_next_tag(self) -> str:
        latest_tag = self.git.get_latest_tag()
        logger.debug(f"Latest tag: {latest_tag}")

        helper = SemverVersionHelper(latest_tag)

        next_version = helper.get_bump_version(
            level=self.bump,
            target_pre=self.pre_release,
            build=self.build_meta,
            prefix_v=True,
            dev=self.dev,
            post=self.post,
        )

        logger.info(f"Next SemVer version: {next_version}")
        return next_version

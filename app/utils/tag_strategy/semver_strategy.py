# app\utils\tag_strategy\semver_strategy.py
"""
SemverStrategy class
"""

from ..git import GitHelper
from ..semver_helper import SemverVersionHelper

# =======================
# 🔧 Concrete Strategies
# =======================


class SemverStrategy:
    def __init__(
        self,
        bump: str | None,
        pre_release: str | None = None,
        build_meta: str | None = None,
    ) -> None:
        self.bump: str = bump
        self.pre_release: str | None = pre_release
        self.build_meta: str | None = build_meta
        self.git = GitHelper(dry_run=False)

    def get_next_tag(self) -> str:
        latest_tag = self.git.get_latest_tag()
        helper = SemverVersionHelper(latest_tag)
        return helper.get_bump_version(
            level=self.bump,
            target_pre=self.pre_release,
            build=self.build_meta,
            prefix_v=True
        )

# app\utils\tag_strategy\semver_strategy.py
"""
SemverStrategy class
"""

from ..git import GitHelper
from ..pep440_helper import PEP440VersionHelper

# =======================
# 🔧 Concrete Strategies
# =======================


class PEP440Strategy:
    def __init__(
        self,
        bump: str | None,
        epoch: int | None,
        pre_release: str | None = None,
        post_release: bool | None = None,
        dev_release: bool | None = None,
        local: str | None = None,
    ) -> None:
        self.bump: str = bump
        self.pre_release: str | None = pre_release
        self.post_release: bool | None = post_release
        self.dev_release: bool | None = dev_release
        self.local: str | None = local
        self.epoch: int | None = epoch
        self.git = GitHelper(dry_run=False)

    def get_next_tag(self) -> str:
        latest_tag = self.git.get_latest_tag()
        helper = PEP440VersionHelper(latest_tag)
        return helper.get_bump_version(
            level=self.bump,
            target_pre=self.pre_release,
            post=self.post_release,
            dev=self.dev_release,
            local=self.local,
            epoch=self.epoch,
        )

# tools\utils\tag_strategy\semver_strategy.py
"""
SemverStrategy class
"""

from ..git import GitHelper

# =======================
# 🔧 Concrete Strategies
# =======================


class SemverStrategy:
    def __init__(
            self,
            bump: str,
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
        print("from semver_strategy:", self.epoch)
        return self.git.bump_version(
            current=latest_tag,
            level=self.bump,
            pre=self.pre_release,
            post=self.post_release,
            dev=self.dev_release,
            local=self.local,
            epoch=self.epoch,
        )

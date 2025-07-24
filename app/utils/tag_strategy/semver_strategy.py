# tools\utils\tag_strategy\semver_strategy.py
"""
SemverStrategy class
"""

from ..git import GitHelper

# =======================
# 🔧 Concrete Strategies
# =======================


class SemverStrategy:
    def __init__(self, bump: str, pre: str | None = None) -> None:
        self.bump = bump
        self.pre = pre
        self.git = GitHelper(dry_run=False)

    def get_next_tag(self) -> str:
        latest_tag = self.git.get_latest_tag()
        return self.git.bump_version(latest_tag, self.bump, self.pre)

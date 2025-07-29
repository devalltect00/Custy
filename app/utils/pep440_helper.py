# app\utils\pep440_helper.py
"""
"""

import re
import sys


class PEP440VersionHelper:
    """
    A helper class to bump semantic version numbers considering tier order and PEP 440 compatibility.

    Tier Precedence:
        dev < alpha < beta < rc < final < post

    Usage:
        helper = PEP440VersionHelper("v1.2.3rc1")
        new_version = helper.get_bumped_version(
            level="patch",
            target_pre="beta",
            post=False,
            dev=False,
            local="abc123",
            epoch=None,
        )
    """

    TIER_ORDER = {"dev": 0, "a": 1, "b": 2, "rc": 3, None: 4, "post": 5}
    PRE_TIER_MAP = {"alpha": "a", "beta": "b", "rc": "rc", "a": "a", "b": "b"}

    def __init__(self, current: str):
        self.original = current
        self.epoch, self.major, self.minor, self.patch = self._parse_base_version(current)
        self.current_pre, self.current_pre_num = self._parse_pre(current)
        self.post_tag = self._search_tag("post")
        self.dev_tag = self._search_tag("dev")
        self.local_tag = self._search_tag(r"\+(.*)", group=1)

        self.going_down = False # will be set in determine_dump()

    def _parse_base_version(self, version: str):
        # Remove leading 'v', extract epoch,, major, minor, patch
        match = re.match(r"(?:(\d+)!)?v?(\d+)\.(\d+)\.(\d+)", version)
        if not match:
            raise ValueError(f"❌ Invalid PEP440 format: '{version}' (expected) [N!]X.Y.Z or vX.Y.Z")
        epoch, major, minor, patch = match.groups()
        return int(epoch) if epoch else None, int (major), int(minor), int(patch)

    def _parse_pre(self, version: str):
        match = re.search(r"(a|b|rc)(\d+)", version)
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def _search_tag(self, tag: str, group=1):
        pattern = tag if tag == "post" else tag + r"(\d+)"
        match = re.search(pattern, self.original)
        return match.group(group) if match else None

    def _tier_value(self, short: str | None) -> int:
        return self.TIER_ORDER.get(short, 4)

    def determine_bump(self, target_pre: str | None) -> bool:
        """
        Determines if base version (major.minor.patch) must be bumped
        when transitioning from current pre-release to target pre-release.
        Also sets `self.going_down` if tier is downgraded.
        """
        # Determine current and target pre tiers
        short_target = self.PRE_TIER_MAP.get(target_pre, target_pre)
        if short_target not in self.TIER_ORDER and short_target is not None:
            raise ValueError(f"Invalid pre-release tier: {target_pre}")

        # Case: same pre-release tier rc1 → rc2
        # Current is pre-release
        if self.current_pre:
            if short_target == self.current_pre:
                return False    # same tier → keep version
            if self._tier_value(short_target) > self._tier_value(self.current_pre):
                return False    # upgrade tier → keep version
            self.going_down = True
            return True # downgrade → bump base

        # Current is final
        if short_target:
            return True # final → pre → bump base

        # final → final
        return True

    def get_bump_version(
        self,
        level: str,
        target_pre: str | None = None,
        post: bool = False,
        dev: bool = False,
        local: str | None = None,
        epoch: int | None = None,
    ) -> str:
        """
        Returns the next version string based on bump level and pre/post/dev transitions.

        Args:
            level: 'patch', 'minor', or 'major'
            target_pre: e.g. 'alpha', 'beta', 'rc', or None
            post: bool, append .postN if True
            dev: bool, append .devN if True
            local: optional +metadata
            epoch: optional epoch override

        Returns:
            str: new version (e.g., '1.2.4rc1')
        """
        bump = self.determine_bump(target_pre)

        # Apply level bump if needed
        if bump:
            if level == "patch":
                self.patch += 1
            elif level == "minor":
                self.minor += 1
                self.patch = 0
            elif level == "major":
                self.major += 1
                self.minor = 0
                self.patch = 0
            else:
                raise ValueError(f"❌ Unknown bump level: {level}. Use: Patch, minor, or major.")

        # Compose version
        version = f"{self.major}.{self.minor}.{self.patch}"

        short = self.PRE_TIER_MAP.get(target_pre, target_pre)
        # Add new pre-release
        if short:
            pre_num = 1
            if short == self.current_pre and not bump:
                pre_num = self.current_pre_num + 1
            version += f"{short}{pre_num}"

        # Post-release
        if post:
            version += f".post{int(self.post_tag) + 1 if self.post_tag else 1}"

        # Development-release
        if dev:
            version += f".dev{int(self.dev_tag) + 1 if self.dev_tag else 1}"

        # Local version metadata
        if local:
            version += f"+{local}"

        # Add epoch
        if epoch or self.epoch:
            version = f"{epoch or self.epoch}!{version}"

        return version

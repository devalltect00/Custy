# app\utils\pep440_helper.py
""" """

import re
import sys


class PEP440VersionHelper:
    """
    A helper class to bump PEP 440-compliant version strings.

    Tier Precedence:
        dev < alpha < beta < rc < final < post

    Supports:
        - Semantic base bumping (major, minor, patch)
        - pre-release tier transitions (dev, a, b, rc)
        - Final releases
        - Post-release (.postN)
        - Dev releases (.devN)
        - Optional local tags  (+meta)
        - Optional epochs (!N)
        - Strict tier regression validation

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
        """
        Initialize with an existing version strings.
        Parses all tags and segments
        """
        self.original = current
        self.epoch, self.major, self.minor, self.patch = self._parse_base_version(current)
        self.current_pre, self.current_pre_num = self._parse_pre(current)
        self.post_tag = self._search_tag("post")
        self.dev_tag = self._search_tag("dev")
        self.local_tag = self._search_tag(r"\+(.*)", group=1)

        self.going_down = False  # will be set in determine_dump()

    def _parse_base_version(self, version: str):
        """
        Extract epoch, major, minor, patch.
        """
        print("version", version)
        match = re.match(r"(?:(\d+)!)?v?(\d+)\.(\d+)\.(\d+)", version)
        if not match:
            raise ValueError(
                f"❌ Invalid PEP440 format: '{version}' (expected) [N!]X.Y.Z or vX.Y.Z"
            )
        epoch, major, minor, patch = match.groups()
        return int(epoch) if epoch else None, int(major), int(minor), int(patch)

    def _parse_pre(self, version: str):
        """
        Extract pre-release type and number (e.g., a2 → ('a', 2)).
        """
        match = re.search(r"(a|b|rc)(\d+)", version)
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def _search_tag(self, tag: str, group=1):
        """
        Extract numeric or custom tag or post/dev/local.
        """
        pattern = {
            "post": r"post(\d+)",
            "dev": r"dev(\d+)",
        }.get(tag, tag)
        match = re.search(pattern, self.original)
        return match.group(group) if match else None

    def _tier_value(self, short: str | None) -> int:
        """
        Get integer value representing tier precedence.
        """
        return self.TIER_ORDER.get(short, 4)

    def _current_tier(self) -> str | None:
        """
        Determine current version's tier.
        """
        if self.dev_tag is not None:
            return "dev"
        if self.current_pre is not None:
            return self.current_pre
        if self.post_tag is not None:
            return "post"
        return None  # final

    def _needs_base_bump(self, target_tier: str | None) -> bool:
        """
        Determine if base version must be bumped when moving to target tier.
        """
        current = self._current_tier()
        curr_val = self._tier_value(current)
        target_value = self._tier_value(target_tier)

        if current == target_tier:
            return False
        if curr_val <  target_value:
            return False
        return True

    def get_bump_version(
        self,
        level: str | None = None,
        target_pre: str | None = None,
        post: bool = False,
        dev: bool = False,
        local: str | None = None,
        epoch: int | None = None,
    ) -> str:
        """
        Returns the next version string based on bump level and pre/post/dev transitions.

        Args:
            level (str | None): 'patch', 'minor', 'major', or None
            target_pre (str | None): e.g. 'alpha', 'beta', 'rc', or None
            post (bool): whether to add a post-release
            dev: (bool) whether to add a dev release
            local: local tag (e.g., sha.abc123), metadata
            epoch: explicit epoch override

        Returns:
            str: new version string (e.g., '1.2.4rc1')

        Raises:
            ValueError: for invalid format or illegal transitions
        """
        short = self.PRE_TIER_MAP.get(target_pre, target_pre)
        target_tier = "dev" if dev else short if short else "post" if post else None
        current_tier = self._current_tier()

        # ❌ Disallow dev/post addition on pre-release
        if current_tier in {"a", "b", "rc"} and post:
            raise ValueError(f"❌ Cannot add post-release to pre-release version: {self.original}")
        if current_tier in {"a", "b", "rc"} and dev:
            raise ValueError(f"❌ Cannot add dev-release to pre-release version: {self.original}")
        if current_tier == "dev" and post:
            raise ValueError(f"❌ Cannot add post-release to dev-release version: {self.original}")

        # ❌ Disallow tier regression only if base not bumped
        if self._tier_value(target_tier) < self._tier_value(current_tier):
            if not self._needs_base_bump(target_tier):
                raise ValueError(f"❌ Invalid tier regression: {self.original} → {target_tier}")

        # ❌ Disallow pre → lower-pre even if base will bump
        if current_tier in {"a", "b", "rc"} and target_tier in {"a", "b", "rc"}:
            if self._tier_value(target_tier) < self._tier_value(current_tier):
                raise ValueError(f"❌ Cannot downgrade pre-release tier: {self.original} → {target_tier}")

        # ❌ Disallow post → post without bump intent
        if current_tier == "post" and target_tier is None and not level:
            raise ValueError(f"❌ No version bump or tier specified for post-release: {self.original}")

        # Determine base bump
        if target_tier or post or dev:
            needs_bump = self._needs_base_bump(target_tier)
        elif current_tier in {"a", "b", "rc", "dev"}:
            needs_bump = False
        else:
            # 🩹 Patch: Avoid bump if only epoch or local specified
            if local or epoch:
                needs_bump = False
            else:
                needs_bump = True

        # Apply level bump if needed
        if needs_bump:
            level = level or "patch"
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
                raise ValueError(
                    f"❌ Unknown bump level: {level}. Use: Patch, minor, or major."
                )

        version = f"{self.major}.{self.minor}.{self.patch}"

        # Pre-release
        if short:
            pre_num = 1
            if short == self.current_pre and not needs_bump:
                pre_num = self.current_pre_num + 1
            version += f"{short}{pre_num}"

        # Post-release
        if post:
            post_num = int(self.post_tag) + 1 if self.post_tag else 1
            version += f".post{post_num}"

        # Development-release
        if dev:
            dev_num = int(self.dev_tag) + 1 if self.dev_tag else 1
            version += f".dev{dev_num}"

        # Local version metadata
        if local:
            version += f"+{local}"

        # Add epoch
        if epoch or self.epoch:
            version = f"{epoch or self.epoch}!{version}"

        return version

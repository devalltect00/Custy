# app/core/git_ops/helper/pep440_helper.py
"""
PEP440VersionHelper

Implements versioning rules according to PEP 440 for Python projects.

Supports:
- Epochs (!N)
- Dev releases (.devN)
- Pre-releases (aN, bN, rcN)
- Post-releases (.postN)
- Local versions (+meta)

Example:
    helper = PEP440VersionHelper("v1.2.3rc1")
    new_version = helper.get_bump_version(target_pre="beta")
    # Returns: '1.2.3b1' or '1.2.4b1' depending on context

Implements VersionHelperBase to provide strategy-specific logic for:
- Tier classification
- Tier precedence
- Suggested version tagging
- Valid branch-to-tag transitions

"""

import re
from typing import Optional

from .version_helper_base import VersionHelperBase


class PEP440VersionHelper(VersionHelperBase):
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

    TIER_ORDER = {"dev": 0, "a": 1, "b": 2, "rc": 3, None: 4, "release": 4, "post": 5}
    PRE_TIER_MAP = {"alpha": "a", "beta": "b", "rc": "rc", "a": "a", "b": "b"}

    def __init__(self, current: str):
        """
        Initialize with an existing version strings.
        Parses all tags and segments
        """
        self.original = current
        self.epoch, self.major, self.minor, self.patch = self._parse_base_version()
        self.current_pre, self.current_pre_num = self._parse_pre()
        self.post_tag = self._search_tag("post")
        self.dev_tag = self._search_tag("dev")
        self.local_tag = self._search_tag(r"\+(.*)", group=1)

        self.going_down = False  # will be set in determine_dump()

    def set_version(self, new_version: str):
        """
        Update the helper’s version state to a new version.
        Re-parses all internal state based on new version string.

        Args:
            new_version (str): The new version string (e.g., '1.3.0rc1')

        """
        self.__init__(new_version)

    # =========================================================
    # ===================== PROPERTIES =========================
    # =========================================================

    @property
    def tier(self) -> str:
        """
        Current lifecycle tier.

        Returns:
            One of:

                dev
                a
                b
                rc
                release
                post
        """
        return self._current_tier() or "release"

    @property
    def is_prerelease(self) -> bool:
        """
        Whether this version is a pre-release.
        """
        return self.current_pre is not None

    @property
    def is_dev(self) -> bool:
        """
        Whether this version is a development release.
        """
        return self.dev_tag is not None

    @property
    def is_post(self) -> bool:
        """
        Whether this version is a post release.
        """
        return self.post_tag is not None

    @property
    def sort_key(self) -> tuple:
        return (
            self.epoch or 0,
            self.major,
            self.minor,
            self.patch,
            self._tier_value(self._current_tier()),
            (
                int(self.dev_tag)
                if self.dev_tag is not None
                else (
                    self.current_pre_num
                    if self.current_pre_num is not None
                    else int(self.post_tag) if self.post_tag is not None else 0
                )
            ),
        )

    def normalize(self) -> str:
        """
        Return a normalized version string.

        Removes only the optional ``v`` prefix while preserving
        epoch, pre-release, post-release, dev-release and local
        metadata.

        Examples
        --------

        v1.2.3rc1
            -> 1.2.3rc1

        2!v1.2.3rc1
            -> 2!1.2.3rc1
        """

        version = self.original

        if "!" in version:
            epoch, value = version.split("!", 1)
            return f"{epoch}!{value.lstrip('v')}"

        return version.lstrip("v")

    # =========================================================
    # ===================== PARSING ============================
    # =========================================================

    def _parse_base_version(self):
        """
        Extract epoch, major, minor, patch.
        """
        match = re.match(r"(?:(\d+)!)?v?(\d+)\.(\d+)\.(\d+)", self.original)
        if not match:
            raise ValueError(
                f"❌ Invalid PEP440 format: '{self.original}' (expected) [N!]X.Y.Z or vX.Y.Z",
            )
        epoch, major, minor, patch = match.groups()
        return int(epoch) if epoch else None, int(major), int(minor), int(patch)

    def _parse_pre(self):
        """
        Extract pre-release type and number (e.g., a2 → ('a', 2)).
        """
        match = re.search(r"(a|b|rc)(\d+)", self.original)
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

    def _tier_value(self, tag: Optional[str]) -> int:
        """
        Get integer value representing tier precedence.
        """
        return self.TIER_ORDER.get(tag, 4)

    def _current_tier(self) -> Optional[str]:
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

    def _needs_base_bump(self, target_tier: Optional[str]) -> bool:
        """
        Determine if base version must be bumped when moving to target tier.
        """
        current = self._current_tier()
        curr_val = self._tier_value(current)
        target_value = self._tier_value(target_tier)

        if current == target_tier:
            return False
        if curr_val < target_value:
            return False
        return True

    def get_bump_version(
        self,
        level: Optional[str] = None,
        target_pre: Optional[str] = None,
        post: bool = False,
        dev: bool = False,
        local: Optional[str] = None,
        epoch: Optional[int] = None,
    ) -> str:
        """
        Returns the next version string based on bump level and pre/post/dev transitions.

        Args:
            level (Optional[str]): 'patch', 'minor', 'major', or None
            target_pre (Optional[str]): e.g. 'alpha', 'beta', 'rc', or None
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
            raise ValueError(
                f"❌ Cannot add post-release to pre-release version: {self.original}",
            )
        if current_tier in {"a", "b", "rc"} and dev:
            raise ValueError(
                f"❌ Cannot add dev-release to pre-release version: {self.original}",
            )
        if current_tier == "dev" and post:
            raise ValueError(
                f"❌ Cannot add post-release to dev-release version: {self.original}",
            )

        # ❌ Disallow tier regression only if base not bumped
        if self._tier_value(target_tier) < self._tier_value(current_tier):
            if not self._needs_base_bump(target_tier):
                raise ValueError(
                    f"❌ Invalid tier regression: {self.original} → {target_tier}",
                )

        # ❌ Disallow pre → lower-pre even if base will bump
        if current_tier in {"a", "b", "rc"} and target_tier in {"a", "b", "rc"}:
            if self._tier_value(target_tier) < self._tier_value(current_tier):
                raise ValueError(
                    f"❌ Cannot downgrade pre-release tier: {self.original} → {target_tier}",
                )

        # ❌ Disallow post → post without bump intent
        if current_tier == "post" and target_tier is None and not level:
            raise ValueError(
                f"❌ No version bump or tier specified for post-release: {self.original}",
            )

        # Determine base bump
        if target_tier or post or dev:
            needs_bump = self._needs_base_bump(target_tier)
        elif current_tier in {"a", "b", "rc", "dev"} or local or epoch:
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
                    f"❌ Unknown bump level: {level}. Use: Patch, minor, or major.",
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

    def classify(self, tag: str) -> str:
        """
        Classifies a version string into one of: dev, a, b, rc, post, release.

        Args:
            tag (str): The version string, stripped of prefix (e.g., '1.2.3a1')

        Returns:
            str: Version tier keyword

        """
        # PEP 440: dev a, b, rc, release, post
        if ".post" in tag:
            return "post"
        if "rc" in tag:
            return "rc"
        if "b" in tag:
            return "b"
        if "a" in tag:
            return "a"
        if "dev" in tag:
            return "dev"
        return "release"

    def tier_order(self) -> dict[str, int]:
        return self.TIER_ORDER

    def suggest_tag(self, branch: str) -> str:
        # Optional: Generate suggested tag
        if branch == "develop":
            return self.get_bump_version(target_pre="dev")
        if branch.startswith("release/"):
            return self.get_bump_version(target_pre="rc")
        if branch == "main":
            return self.get_bump_version()  # final
        if branch.startswith("hotfix/"):
            return self.get_bump_version(post=True)
        return self.original  # No change

    def get_transaction_cases(self) -> dict:
        """
        Returns valid transition mappings from (from_branch, from_tier, to_branch, to_tier)
        to a CASE identifier used by WorkflowManager.

        These transitions help determine which Git commands to run
        during initial/final workflow steps.
        """
        # Major transition cases
        # Case transition map
        return {
            ("develop", "release", "develop", "dev"): "CASE 1",
            ("develop", "release", "develop", "a"): "CASE 1",
            ("develop", "release", "develop", "b"): "CASE 1",
            ("develop", "dev", "develop", "rc"): "CASE 2",
            ("develop", "a", "develop", "rc"): "CASE 2",
            ("develop", "b", "develop", "rc"): "CASE 2",
            ("release", "rc", "release", "release"): "CASE 3",
            ("main", "release", "main", "dev"): "CASE 4",
            ("main", "release", "main", "a"): "CASE 4",
            ("main", "release", "main", "b"): "CASE 4",
            ("main", "release", "main", "post"): "CASE 5",
            ("hotfix", "post", "hotfix", "release"): "CASE 6",
            # === EXTENDED CASES ===
            ("feature", "release", "feature", "dev"): "CASE 7",
            ("feature", "dev", "feature", "dev"): "CASE 7",
            ("archive", "release", "archive", "release"): "CASE 8",
            ("archive", "dev", "archive", "release"): "CASE 8",
            ("ci", "release", "ci", "dev"): "CASE 9",
            ("ci", "dev", "ci", "dev"): "CASE 9",
        }

    def get_reference_transaction_cases(self) -> dict:
        return {
            ("main", "release", "develop", "dev"): "CASE 1",
            ("main", "release", "develop", "a"): "CASE 1",
            ("main", "release", "develop", "b"): "CASE 1",
            ("develop", "dev", "release", "rc"): "CASE 2",
            ("develop", "a", "release", "rc"): "CASE 2",
            ("develop", "b", "release", "rc"): "CASE 2",
            ("release", "rc", "main", "release"): "CASE 3",
            ("develop", "release", "develop", "dev"): "CASE 4",
            ("develop", "release", "develop", "a"): "CASE 4",
            ("develop", "release", "develop", "b"): "CASE 4",
            ("main", "release", "hotfix", "post"): "CASE 5",
            ("hotfix", "post", "main", "release"): "CASE 6",
            # === EXTENDED CASES ===
            ("feature", "dev", "develop", "dev"): "CASE 7",
            ("archive", "release", "main", "release"): "CASE 8",
            ("ci", "dev", "main", "dev"): "CASE 9",
        }

    def compare(
        self,
        other: PEP440VersionHelper | str,
    ) -> int:

        if isinstance(other, str):
            other = PEP440VersionHelper(other)

        if self.sort_key < other.sort_key:
            return -1

        if self.sort_key > other.sort_key:
            return 1

        return 0

    @classmethod
    def supports(cls, version: str) -> bool:

        if not version:
            return False

        try:
            cls(version)
            return True
        except Exception:
            return False

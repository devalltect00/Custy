# app/core/git_ops/helper/semver_helper.py

"""
semver_helper.py

Enhanced Semantic Version helper.

Extends standard SemVer with lifecycle support compatible with PEP440 logic.

Supported:
- major.minor.patch
- pre-release: alpha, beta, rc
- dev: -dev.N
- post: -post.N
- build metadata: +meta

Tier precedence:
    dev < alpha < beta < rc < release < post
"""

import re
from .version_helper_base import VersionHelperBase

from typing import Dict, Optional


class SemverVersionHelper(VersionHelperBase):
    """
    Extended SemVer helper with lifecycle support.

    Maintains SemVer compliance while supporting:
    - dev releases
    - post releases
    - workflow compatibility with PEP440
    """

    TIER_ORDER = {
        "dev": 0,
        "alpha": 1,
        "beta": 2,
        "rc": 3,
        None: 4,
        "release": 4,
        "post": 5,
    }

    def __init__(self, current: str):
        super().__init__(current)

        self.prefix_v = current.startswith("v")
        self.version = current.lstrip("v")

        self.major, self.minor, self.patch = self._parse_base_version()
        self.current_pre, self.current_pre_num = self._parse_pre()
        self.dev_tag = self._parse_dev()
        self.post_tag = self._parse_post()
        self.build_meta = self._parse_build()

    # =========================================================
    # ===================== STATE ==============================
    # =========================================================

    def set_version(self, new_version: str) -> None:
        """
        Reinitialize helper with new version.

        Args:
            new_version (str)
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
                - dev
                - alpha
                - beta
                - rc
                - release
                - post
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
        """
        Tuple suitable for sorting Semantic Versions.

        Ordering:

            dev
                <
            alpha
                <
            beta
                <
            rc
                <
            release
                <
            post

        Build metadata is ignored.

        Returns:
            Comparable tuple.
        """

        tier = self._tier_value(self._current_tier())

        tier_number = 0

        if self.dev_tag is not None:
            tier_number = self.dev_tag

        elif self.current_pre_num is not None:
            tier_number = self.current_pre_num

        elif self.post_tag is not None:
            tier_number = self.post_tag

        return (
            self.major,
            self.minor,
            self.patch,
            tier,
            tier_number,
        )

    def normalize(self) -> str:
        """
        Return a normalized version string.

    Normalization removes only the optional ``v`` prefix
    while preserving lifecycle identifiers and build
    metadata.

        Examples
        --------
        v1.2.3
            -> 1.2.3

        v1.2.3+linux
            -> 1.2.3+linux

        Returns:
            Normalized version.
        """
        return self.version.strip()

    # =========================================================
    # ===================== PARSING ============================
    # =========================================================

    def _parse_base_version(self):
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", self.version)
        if not match:
            raise ValueError(f"Invalid SemVer: {self.original}")
        return tuple(map(int, match.groups()))

    def _parse_pre(self):
        match = re.search(r"-(alpha|beta|rc)\.(\d+)", self.version)
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def _parse_dev(self):
        match = re.search(r"-dev\.(\d+)", self.version)
        return int(match.group(1)) if match else None

    def _parse_post(self):
        match = re.search(r"-post\.(\d+)", self.version)
        return int(match.group(1)) if match else None

    def _parse_build(self):
        match = re.search(r"\+(.*)", self.version)
        return match.group(1) if match else None

    # =========================================================
    # ===================== TIER ===============================
    # =========================================================

    def _tier_value(self, tier: Optional[str]) -> int:
        return self.TIER_ORDER.get(tier, 4)

    def _current_tier(self):
        if self.dev_tag is not None:
            return "dev"
        if self.current_pre:
            return self.current_pre
        if self.post_tag is not None:
            return "post"
        return None

    # =========================================================
    # ===================== BUMP ===============================
    # =========================================================

    def get_bump_version(
        self,
        level: Optional[str] = None,
        target_pre: Optional[str] = None,
        build: Optional[str] = None,
        prefix_v: bool = True,
        dev: bool = False,
        post: bool = False,
    ) -> str:
        """
        Generate next SemVer version.

        Args:
            level (str): 'major', 'minor', 'patch'
            target_pre (str): 'alpha', 'beta', 'rc'
            build (str): metadata
            prefix_v (bool): include 'v'
            dev (bool): dev release
            post (bool): post release

        Returns:
            str: new version

        Raises:
            ValueError: invalid transitions
        """

        current_tier = self._current_tier()
        target_tier = (
            "dev" if dev else target_pre if target_pre else "post" if post else None
        )

        # Prevent invalid regression
        if self._tier_value(target_tier) < self._tier_value(current_tier):
            raise ValueError(
                f"Invalid tier regression: {current_tier} → {target_tier}"
            )

        # Determine bump necessity
        needs_bump = current_tier is None

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
                raise ValueError(f"Unknown level: {level}")

        version = f"{self.major}.{self.minor}.{self.patch}"

        # dev
        if dev:
            num = (self.dev_tag or 0) + 1
            version += f"-dev.{num}"

        # pre
        elif target_pre:
            num = (
                self.current_pre_num + 1
                if target_pre == self.current_pre
                else 1
            )
            version += f"-{target_pre}.{num}"

        # post
        elif post:
            num = (self.post_tag or 0) + 1
            version += f"-post.{num}"

        if build:
            version += f"+{build}"

        if prefix_v:
            version = f"v{version}"

        return version

    # =========================================================
    # ===================== CLASSIFY ===========================
    # =========================================================

    def classify(self, tag: str) -> str:
        """
        Classifies a SemVer tag into one of: alpha, beta, rc, or release.

        Args:
            tag (str): The version string stripped of the 'v' prefix

        Returns:
            str: Tier keyword for classification

        """

        if "-post." in tag:
            return "post"
        if "-rc." in tag:
            return "rc"
        if "-beta." in tag:
            return "beta"
        if "-alpha." in tag:
            return "alpha"
        if "-dev." in tag:
            return "dev"
        return "release"

    def tier_order(self) -> Dict[str, int]:
        return self.TIER_ORDER

    # =========================================================
    # ===================== SUGGESTION =========================
    # =========================================================

    def suggest_tag(self, branch: str) -> str:
        """
        Suggest next tag based on branch.

        Returns:
            str
        """
        if branch == "develop":
            return self.get_bump_version(dev=True)
        if branch.startswith("release/"):
            return self.get_bump_version(target_pre="rc")
        if branch == "main":
            return self.get_bump_version()
        if branch.startswith("hotfix/"):
            return self.get_bump_version(post=True)
        return self.original

    # =========================================================
    # ===================== Transaction Cases ==================
    # =========================================================

    def get_transaction_cases(self) -> dict:
        """
        Minimal transition mapping for SemVer workflow.

        Returns valid transition mappings from (from_branch, from_tier, to_branch, to_tier)
        to a CASE identifier used by WorkflowManager.

        These transitions help determine which Git commands to run
        during initial/final workflow steps.

        Returns:
            dict
        """
        # Major transition cases
        # Case transition map
        return {
            ("develop", "release", "develop", "alpha"): "CASE 1",
            ("develop", "release", "develop", "beta"): "CASE 1",
            ("develop", "alpha", "develop", "rc"): "CASE 2",
            ("develop", "beta", "develop", "rc"): "CASE 2",
            ("release", "rc", "release", "release"): "CASE 3",
            ("main", "release", "main", "alpha"): "CASE 4",
            ("main", "release", "main", "beta"): "CASE 4",
        }

    def get_reference_transaction_cases(self) -> dict:
        return {
            ("main", "release", "develop", "alpha"): "CASE 1",
            ("main", "release", "develop", "beta"): "CASE 1",
            ("develop", "alpha", "release", "rc"): "CASE 2",
            ("develop", "beta", "release", "rc"): "CASE 2",
            ("release", "rc", "main", "release"): "CASE 3",
            ("develop", "release", "develop", "alpha"): "CASE 4",
            ("develop", "release", "develop", "beta"): "CASE 4",
        }

    def compare(
        self,
        other: "SemverVersionHelper | str",
    ) -> int:
        """
        Compare this version against another version.

        Returns
        -------
        -1
            self < other

        0
            self == other

        1
            self > other
        """

        if isinstance(other, str):
            other = SemverVersionHelper(other)

        if self.sort_key < other.sort_key:
            return -1

        if self.sort_key > other.sort_key:
            return 1

        return 0

    @classmethod
    def supports(
        cls,
        version: str,
    ) -> bool:
        """
        Check whether the supplied version is a supported
        Semantic Version.

        Args:
            version:
                Version string.

        Returns:
            True if parsing succeeds.
        """
        if not version:
            return False

        try:
            cls(version)
            return True
        except ValueError:
            return False

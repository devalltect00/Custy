# app\utils\semver_helper.py
"""
SemverVersionHelper

Implements versioning logic following the Semantic Versioning 2.0.0 specification.

Supports:
- Major.Minor.Patch
- Pre-release: -alpha.N, -beta.N, -rc.N
- Build metadata: +meta
- v-prefixed versions

Example:
    helper = SemverVersionHelper("1.2.3-beta.2")
    new_version = helper.get_bump_version(target_pre="rc")
    # Returns: '1.2.3-rc.1' or '1.2.4-rc.1' depending on rules

This class does NOT support:
- Epochs
- Post-releases
- Dev releases

Implements VersionHelperBase to support unified version management.
"""

import re

from .version_helper_base import VersionHelperBase


class SemverVersionHelper(VersionHelperBase):
    """
    A helper class for generating valid SemVer-compliant version strings.

    This class supports semantic versioning according to the SemVer 2.0.0 specification:
    https://semver.org/

    Features:
        - Semantic version bumping (major, minor, patch)
        - Pre-release identifiers (alpha, beta, rc)
        - Tier progression rules and downgrade protection
        - Build metadata (e.g., +sha.abc123)
        - Optional 'v' prefix handling

    Does NOT support:
        - Epochs
        - Post/Dev releases


    Tier Precedence (increasing):
        alpha < beta < rc < final (no suffix)

    Rules:
        - Final → Pre-release is allowed (with base bump).
        - Same-tier pre-release will increment the numeric suffix (e.g., beta.2 → beta.3).
        - Tier upgrades are allowed (e.g., alpha → beta), same base version.
        - Tier regressions (e.g., beta → alpha) are disallowed, even with base bump.
        - Adding build metadata will also bump version by default (patch-level).

    Example:
        >>> SemverVersionHelper("1.2.3-alpha.2").get_bump_version(target_pre="beta")
        '1.2.3-beta.1'
    """

    TIER_ORDER = {"alpha": 0, "beta": 1, "rc": 2, None: 3, "release": 3}

    def __init__(self, current: str):
        """
        Initialize from current version string.

        Args:
            current (str): Version string (e.g. "1.2.3", "v1.2.3-beta.2+sha.abc123")
        """
        self.original = current
        self.prefix_v = current.startswith("v")
        self.version = current.lstrip("v")

        self.major, self.minor, self.patch = self._parse_base_version()
        self.current_pre, self.current_pre_num = self._parse_pre()
        self.build_meta = self._parse_build()

    def _parse_base_version(self):
        """
        Extract major, minor, and patch from version.
        """
        # Remove leading 'v', extract epoch,, major, minor, patch
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", self.original)
        if not match:
            raise ValueError(
                f"❌ Invalid SemVer format: '{self.original}' (expected) X.Y.Z or vX.Y.Z"
            )
        return tuple(map(int, match.groups()))

    def _parse_pre(self):
        """
        Extract pre-release identifier and numeric suffix (e.g., rc.2).
        """
        match = re.search(r"-(alpha|beta|rc)\.(\d+)", self.original)
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def _parse_build(self):
        """
        Extract build metadata (e.g., +sha.abc123).
        """
        match = re.search(r"\+(.*)$", self.original)
        return match.group(1) if match else None

    def _tier_value(self, tag: str | None) -> int:
        """
        Return integer value representing tier precedence.
        """
        return self.TIER_ORDER.get(tag, 3)

    def _needs_based_bump(self, target_pre: str | None) -> bool:
        """
        Decide if a base version bump is needed when moving to the target pre-release tier.

        Returns:
            bool: True if bump required, False otherwise.
        """
        current_val = self._tier_value(self.current_pre)
        target_val = self._tier_value(target_pre)

        if self.current_pre == target_pre:
            return False
        if current_val < target_val:
            return False
        return True

    def get_bump_version(
        self,
        level: str | None = None,
        target_pre: str | None = None,
        build: str | None = None,
        prefix_v: bool = False,
    ) -> str:
        """
        Generate the next bumped SemVer version string.

        Args:
            level (str, optional): One of "patch", "minor", or "major". If omitted, defaults to "patch".
            target_pre (str, optional): One of "alpha", "beta", or "rc". Indicates next pre-release type.
            build (str, optional): Build metadata to append after "+" (e.g., "sha.abc123").
            prefix_v (bool, optional): Whether to prefix the final version with "v" (e.g., "v1.2.3").

        Returns:
            str: Next version string according to SemVer rules.

        Raises:
            ValueError: If an invalid bump level is provided, or if a tier regression is attempted.

        Example:
            >>> SemverVersionHelper("1.2.3").get_bump_version(target_pre="alpha")
            '1.2.4-alpha.1'
        """
        current_tier = self.current_pre
        target_tier = target_pre

        # ❌ Disallow downgrade of pre-release tier even bump
        if (
            current_tier in {"alpha", "beta", "rc"}
            and target_tier in {"alpha", "beta", "rc"}
            and self._tier_value(target_tier) < self._tier_value(current_tier)
        ):
            raise ValueError(f"❌ Cannot downgrade pre-release tier: {current_tier} → {target_tier}")

        # Determine if based dump is needed
        if target_tier:
            needs_bump = self._needs_based_bump(target_tier)
        elif current_tier:
            needs_bump = False
        else:
            needs_bump = True  # Includes pure build case

        # Perform version bump
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

        # Add pre-release
        if target_tier:
            pre_num = 1
            if target_tier == self.current_pre and not needs_bump:
                pre_num = self.current_pre_num + 1
            version += f"-{target_tier}.{pre_num}"

        # Add build metadata
        if build:
            version += f"+{build}"

        # Add optional v prefix
        if prefix_v:
            version = f"v{version}"

        return version

    def classify(self, tag: str) -> str:
        """
        Classifies a SemVer tag into one of: alpha, beta, rc, or release.

        Args:
            tag (str): The version string stripped of the 'v' prefix

        Returns:
            str: Tier keyword for classification
        """
        # Semver: alpha, beta, rc, release
        if "rc." in tag:
            return "rc"
        elif "beta." in tag:
            return "beta"
        elif "alpha." in tag:
            return "alpha"
        return "release"

    def tier_order(self) -> dict:
        return self.TIER_ORDER

    def suggest_tag(self, branch: str) -> str:
        # Optional: Generate suggested tag
        if self.branch == "develop":
            return self.get_bump_version(target_pre="dev")
        elif self.branch.startswith("release/"):
            return self.get_bump_version(target_pre="rc")
        elif self.branch == "main":
            return self.get_bump_version()  # final
        elif self.branch.startswith("hotfix/"):
            return self.get_bump_version(post=True)
        return self.original  # No change

    def get_transaction_cases(self) -> dict:
        # Major transition cases
        # Case transition map
        return {
            ("main", "release", "develop", "alpha"): "CASE 1",
            ("main", "release", "develop", "beta"): "CASE 1",

            ("develop", "alpha", "release", "rc"): "CASE 2",
            ("develop", "beta", "release", "rc"): "CASE 2",

            ("release", "rc", "main", "release"): "CASE 3",

            ("main", "release", "develop", "alpha"): "CASE 4",
            ("main", "release", "develop", "beta"): "CASE 4",
        }

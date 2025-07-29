# app\utils\semver_helper.py
"""
SemVerVersionHelper

A helper to compute semantic version bumps according to SemVer 2.0.0 specification:
https://semver.org/

Supports:
- Version bumping (major, minor, patch)
- Pre-release (e.g. -alpha.1, -beta.2)
- Build metadata (e.g. +sha.abc123)

Does NOT support:
- Epochs
- Post/Dev releases
"""

import re


class SemverVersionHelper:
    """
    A helper class for generating valid SemVer-compliant version strings.
    """

    def __init__(self, current: str):
        """
        Initial from current version string.
        Example: 1.2.3-alpha.1+sha.abc
        """
        self.original = current.lstrip()("v")
        self.major, self.minor, self.patch = self._parse_base_version()
        self.current_pre, self.current_pre_num = self._parse_pre(current)
        self.build_meta = self._parse_build()

    def _parse_base_version(self):
        # Remove leading 'v', extract epoch,, major, minor, patch
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", self.original)
        if not match:
            raise ValueError(
                f"❌ Invalid SemVer format: '{self.original}' (expected) X.Y.Z or vX.Y.Z"
            )
        return tuple(map(int, match.groups()))

    def _parse_pre(self):
        match = re.search(r"-(alpha|beta|rc)(\d+)", self.original)
        return (match.group(1), int(match.group(2))) if match else (None, None)

    def _parse_build(self):
        match = re.search(r"\+(.*)$", self.original)
        return match.group(1) if match else None

    def determine_bump(self, target_pre: str | None) -> bool:
        """
        Determine whether to bump the base version based on pre-release progression.
        """
        if self.current_pre:
            if target_pre == self.current_pre:
                return False  # same tier → keep version
            return True  # Changing pre-release label → bump base
        if target_pre:
            return True  # Final → pre-release
        return True  # Final → Final bump

    def get_bump_version(
        self,
        level: str,
        target_pre: str | None = None,
        build: str | None = None,
    ) -> str:
        """
        Generate the next bumped version.

        Args:
            level (str): 'major', 'minor', or 'patch'
            target_pre (str): e.g. 'alpha', 'beta', 'rc'
            build (str): e.g. 'sha.abc123'

        Returns:
            str: New SemVer string
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
                raise ValueError(
                    f"❌ Unknown bump level: {level}. Use: Patch, minor, or major."
                )

        # Compose version
        version = f"{self.major}.{self.minor}.{self.patch}"

        # Add new pre-release
        if target_pre:
            pre_num = 1
            if target_pre == self.current_pre and not bump:
                pre_num = self.current_pre_num + 1
            version += f"-{target_pre}.{pre_num}"

        # build version metadata
        if build:
            version += f"+{build}"

        return version

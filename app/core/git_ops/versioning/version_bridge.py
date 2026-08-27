# app/core/git_ops/versioning/version_bridge.py

"""
version_bridge.py

Provides conversion utilities between:
- PEP 440 version format
- Semantic Versioning (SemVer)

Purpose:
- Enable interoperability between Python (PEP440) and other ecosystems (SemVer)
- Normalize version handling across strategies
"""

import re


class VersionBridge:
    """
    Utility class for converting between versioning formats.

    Supports:
        - PEP440 → SemVer
        - SemVer → PEP440 (basic)
    """

    # =========================================================
    # ===================== PEP440 → SEMVER ====================
    # =========================================================

    @staticmethod
    def pep440_to_semver(tag: str) -> str | None:
        """
        Convert PEP 440 version into SemVer-compatible format.

        Examples:
            1.2.3rc1      → v1.2.3-rc.1
            1.2.3a2       → v1.2.3-alpha.2
            1.2.3.dev1    → v1.2.3-dev.1
            1.2.3.post1   → v1.2.3-post.1
            1.2.3+meta    → v1.2.3+meta

        Args:
            tag (str): PEP440 version string

        Returns:
            str | None: SemVer string or None if invalid
        """
        tag = tag.lstrip("v")

        # Extract build metadata
        if "+" in tag:
            tag, meta = tag.split("+", 1)
        else:
            meta = None

        # Base version
        match = re.match(r"(\d+\.\d+\.\d+)", tag)
        if not match:
            return None

        base = match.group(1)
        rest = tag[len(base) :]

        result = f"v{base}"

        # Pre-release
        pre = re.search(r"(a|b|rc)(\d+)", rest)
        if pre:
            typ, num = pre.groups()
            mapping = {"a": "alpha", "b": "beta", "rc": "rc"}
            result += f"-{mapping[typ]}.{num}"

        # Dev
        dev = re.search(r"\.dev(\d+)", rest)
        if dev:
            result += f"-dev.{dev.group(1)}"

        # Post
        post = re.search(r"\.post(\d+)", rest)
        if post:
            result += f"-post.{post.group(1)}"

        # Metadata
        if meta:
            result += f"+{meta}"

        return result

    # =========================================================
    # ===================== SEMVER → PEP440 ====================
    # =========================================================

    @staticmethod
    def semver_to_pep440(tag: str) -> str | None:
        """
        Convert SemVer version into PEP 440 format.

        Examples:
            v1.2.3-alpha.1 → 1.2.3a1
            v1.2.3-beta.2  → 1.2.3b2
            v1.2.3-rc.1    → 1.2.3rc1
            v1.2.3-dev.1   → 1.2.3.dev1
            v1.2.3-post.1  → 1.2.3.post1

        Args:
            tag (str): SemVer version string

        Returns:
            str | None
        """
        tag = tag.lstrip("v")

        # Split metadata
        if "+" in tag:
            tag, meta = tag.split("+", 1)
        else:
            meta = None

        # Split pre
        if "-" in tag:
            base, suffix = tag.split("-", 1)
        else:
            base, suffix = tag, None

        result = base

        if suffix:
            match = re.match(r"(alpha|beta|rc|dev|post)\.(\d+)", suffix)
            if match:
                typ, num = match.groups()
                mapping = {
                    "alpha": f"a{num}",
                    "beta": f"b{num}",
                    "rc": f"rc{num}",
                    "dev": f".dev{num}",
                    "post": f".post{num}",
                }
                result += mapping[typ]

        if meta:
            result += f"+{meta}"

        return result

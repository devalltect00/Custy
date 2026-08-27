# app/core/git_ops/versioning/models/version_type.py

import re
from enum import Enum


# -----------------------------
# 🚦 Version Type Enum (PEP 440 & SenVer aware)
# -----------------------------
class VersionType(str, Enum):
    FINAL = "final"
    POST = "post"
    RC = "rc"
    BETA = "beta"
    ALPHA = "alpha"
    DEV = "dev"

    @classmethod
    def detect(cls, version: str) -> VersionType:
        """
        Detects the release stage of a version string based on PEP 440 and SemVer conventions.
        Supports:
        - PEP 440: 1.2.3a1, 1.2.3b1, 1.2.3rc1, 1.2.3.post1, 1.2.3.dev1
        - SemVer: 1.2.3-alpha.1, 1.2.3-beta.1, 1.2.3-rc.1, etc.

        Args:
            version (str): Version string

        Returns:
            VersionType: Enum corresponding to detected stage.

        """
        version = version.lower()

        # SemVer patterns
        if "-alpha" in version or ".alpha" in version:
            return cls.ALPHA
        if "-beta" in version or ".beta" in version:
            return cls.BETA
        if "-rc" in version or ".rc" in version or "rc" in version:
            return cls.RC

        # PEP 440 patterns
        if re.search(r"[\d]a\d+", version):
            return cls.ALPHA
        if re.search(r"[\d]b\d+", version):
            return cls.BETA
        if re.search(r"[\d]rc\d+", version):
            return cls.RC
        if ".post" in version:
            return cls.POST
        if ".dev" in version or "dev" in version:
            return cls.DEV

        return cls.FINAL

    def is_dev(self) -> bool:
        return self == VersionType.DEV

    def is_alpha(self) -> bool:
        return self == VersionType.ALPHA

    def is_beta(self) -> bool:
        return self == VersionType.BETA

    def is_rc(self) -> bool:
        return self == VersionType.RC

    def is_pre_release(self) -> bool:
        return self in {
            VersionType.DEV,
            VersionType.ALPHA,
            VersionType.BETA,
            VersionType.RC,
        }

    def is_final_release(self) -> bool:
        return self == VersionType.FINAL

    def is_post_release(self) -> bool:
        return self == VersionType.POST

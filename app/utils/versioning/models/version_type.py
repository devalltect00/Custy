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
    def detect(cls, version: str) -> "VersionType":
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
        elif "-beta" in version or ".beta" in version:
            return cls.BETA
        elif "-rc" in version or ".rc" in version or "rc" in version:
            return cls.RC

        # PEP 440 patterns
        if re.search(r"[\d]a\d+", version):
            return cls.ALPHA
        elif re.search(r"[\d]b\d+", version):
            return cls.BETA
        elif re.search(r"[\d]rc\d+", version):
            return cls.RC
        elif ".post" in version:
            return cls.POST
        elif ".dev" in version or "dev" in version:
            return cls.DEV

        return cls.FINAL

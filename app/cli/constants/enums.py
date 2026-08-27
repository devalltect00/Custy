# app/cli/constants/enums.py

from enum import Enum


class StrategyChoices(str, Enum):
    SEMVER = "semver"
    PEP440 = "pep440"
    DATE = "date"
    GIT_COUNT = "gitcount"
    COMMITIZEN = "commitizen"
    NONE = None


class BumpChoices(str, Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"
    AUTO = "auto"
    NONE = None


class StageModeChoices(str, Enum):
    ALL = "all"  # git add .
    UPDATE = "update"  # git add --update
    NONE = "none"  # do not stage anything
    MANUAL = "manual"  # require user to stage manually


class LogLevelChoices(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value = value.upper()
            for member in cls:
                if member.value == value:
                    return member


class CleanupTypeChoices(str, Enum):
    ALL = "all"
    COMMIT = "commit"
    TAG = "tag"
    BRANCH = "branch"


class InitMode(str, Enum):
    ALL = "all"
    ALL_NO_EXAMPLES = "all_no_examples"
    CONFIG = "config"
    TEMPLATES = "templates"
    EXAMPLES = "examples"


class StepChoices(str, Enum):
    COMMIT = "commit"
    TAG = "tag"
    PUSH = "push"
    DEV = "dev"
    RELEASE = "release"
    FULL = "full"


class MergeStatusChoices(str, Enum):
    """
    Branch merge status filter.

    This enumeration controls which Git branches should be considered
    during cleanup operations.

    Members
    -------
    ALL
        Consider every branch regardless of merge status.

    MERGED
        Consider only branches that have already been merged into the
        current target branch.

    UNMERGED
        Consider only branches that have not yet been merged.
    """

    ALL = "all"

    MERGED = "merged"

    UNMERGED = "unmerged"

    @classmethod
    def _missing_(cls, value):
        """
        Perform case-insensitive enum lookup.

        Parameters
        ----------
        value:
            Incoming CLI value.

        Returns
        -------
        MergeStatusChoices | None
            Matching enum member when found.
        """
        if isinstance(value, str):
            value = value.lower()

            for member in cls:
                if member.value == value:
                    return member

        return None

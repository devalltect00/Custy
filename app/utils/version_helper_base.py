# app\utils\version_helper_base.py
"""
version_helper_base.py

Abstract base class for implementing versioning strategy helpers such as PEP 440 and SemVer.

Defines the interface required for:
    - Classifying version tiers (e.g., dev, rc, post)
    - Suggesting the next version tag based on branch context
    - Validating tier progression rules and transitions
"""

from abc import ABC, abstractmethod


class VersionHelperBase(ABC):
    """
    Abstract base class for all version helpers (PEP 440, SemVer, etc.).

    Implementations must support:
        - Version classification by tier (e.g., dev, rc, release)
        - Tier precedence ordering
        - Suggested version for the current branch
        - Valid transition case mapping
    """

    def __init__(self, tag: str):
        """
        Args:
            tag (str): The current Git tag string (e.g., 'v1.2.3', '1.2.3rc1')
        """
        self.original = tag

    @abstractmethod
    def _parse_base_version(self):
        """
        """
        ...

    @abstractmethod
    def _parse_pre(self):
        """
        """
        ...

    @abstractmethod
    def _tier_value(self, short: str | None) -> int:
        """
        """
        ...

    @abstractmethod
    def classify(self, tag: str) -> str:
        """
        Classifies the version tier from a tag.

        Args:
            tag (str): A version string (without 'v' prefix)

        Returns:
            str: One of {'dev', 'a', 'b', 'rc', 'release', 'post'} or {'alpha', 'beta', 'rc', 'release'}
        """
        ...

    @abstractmethod
    def tier_order(self) -> dict:
        """
        Returns a mapping of tier names to precedence values.

        Returns:
            dict: Mapping from tier name to an integer for sorting.
        """
        ...

    @abstractmethod
    def suggest_tag(self, branch: str) -> str:
        """
        Suggests the next tag based on the current branch name.

        Args:
            branch (str): Git branch name (e.g. 'develop', 'release/1.2')

        Returns:
            str: Suggested tag version (e.g., '1.2.3rc1')
        """
        ...

    @abstractmethod
    def get_transaction_cases(self) -> dict:
        """
        Returns a dictionary of valid CASE transitions.

        Returns:
            dict: Mapping of (from_branch, from_tier, to_branch, to_tier) to case name (e.g. 'CASE 2')
        """
        ...


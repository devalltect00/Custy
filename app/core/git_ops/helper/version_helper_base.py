# app/core/git_ops/helper/version_helper_base.py
"""
version_helper_base.py

Abstract base class for implementing versioning strategy helpers such as PEP 440 and SemVer.

Defines the interface required for:
    - Classifying version tiers (e.g., dev, rc, post)
    - Suggesting the next version tag based on branch context
    - Validating tier progression rules and transitions

This defines a unified interface for different versioning strategies,
such as:
- PEP 440 (Python ecosystem)
- Semantic Versioning (SemVer)

Design Goals:
- Provide a consistent API for version manipulation
- Allow interchangeable strategy usage
- Support workflow logic (branch transitions, tier classification)

Used by:
- BranchWorkflowManager
- Tag strategies
- Version bump automation
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class VersionHelperBase(ABC):
    """
    Abstract base class for all version helpers (PEP 440, SemVer, etc.).

    Implementations must provide:
    - Version parsing
    - Tier classification
    - Tier ordering
    - Version bump logic
    - Transition rules
    """

    def __init__(self, tag: str):
        """
        Initialize helper with current version.

        Args:
            tag (str): The current Git tag string (e.g., 'v1.2.3', '1.2.3rc1')

        """
        self.original = tag

    @abstractmethod
    def set_version(self, new_version: str):
        """
        Update the internal version to a new version string.
        Re-parse all internal components.

        Args:
            new_version (str): New version string

        Returns:
            None
        """
        ...

    # =========================================================
    # ===================== PARSING ============================
    # =========================================================
    
    @abstractmethod
    def _parse_base_version(self):
        """
        Extract base version components.

        Returns:
            tuple: (major, minor, patch)
        """
        ...

    @abstractmethod
    def _parse_pre(self):
        """
        Extract pre-release information.

        Returns:
            tuple: (type, number) or (None, None)
        """
        ...

    @abstractmethod
    def _tier_value(self, short: Optional[str]) -> int:
        """
        Convert tier name into comparable numeric value.

        Args:
            tier (Optional[str])

        Returns:
            int: ordering value
        """
        ...

    # =========================================================
    # ===================== CLASSIFICATION =====================
    # =========================================================
    
    @abstractmethod
    def classify(self, tag: str) -> str:
        """
        Classifies the version tier from a tag.

        Examples:
            PEP440 → dev, a, b, rc, release, post
            SemVer → dev, alpha, beta, rc, release, post

        Args:
            tag (str): A version string (without 'v' prefix)

        Returns:
            str: tier name. One of {'dev', 'a', 'b', 'rc', 'release', 'post'} or {'alpha', 'beta', 'rc', 'release'}

        """
        ...

    @abstractmethod
    def tier_order(self) -> Dict[str, int]:
        """
        Returns a mapping of tier names to precedence values.

        Returns:
            dict {tier, order}: Mapping from tier name to an integer for sorting.

        """
        ...

    # =========================================================
    # ===================== VERSION LOGIC ======================
    # =========================================================
    
    @abstractmethod
    def get_bump_version(self, **kwargs) -> str:
        """
        Generate next version.

        Strategy-specific parameters allowed.

        Returns:
            str: new version string
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

    # =========================================================
    # ===================== WORKFLOW ===========================
    # =========================================================

    @abstractmethod
    def get_transaction_cases(self) -> dict:
        """
        Define valid workflow transitions.

        Returns:
            dict:
                {
                    (from_branch, from_tier, to_branch, to_tier): "CASE X"
                }
        """
        ...

    # OPTIONAL (not required by SemVer)
    def get_reference_transaction_cases(self) -> dict:
        """
        Optional detailed reference transitions.

        Returns:
            dict
        """
        return {}

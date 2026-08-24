# app/core/git_ops/tag_strategy/base.py

"""
TagStrategy protocol/interface

Defines the interface for all tag generation strategies.

Used by:
- CLI
- WorkflowManager
"""

# =======================
# 🔧 Tag Strategy Pattern
# =======================

from typing import Protocol


class TagStrategy(Protocol):
    """
    Strategy interface for generating next version tag.
    """

    def get_next_tag(self) -> str:
        """
        Compute next version tag.

        Returns:
            str: next version
        """
        ...

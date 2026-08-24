# app/core/git_ops/tag_sorter/base.py

"""
Tag Sorter Protocol

Defines the interface implemented by all tag sorting
strategies.

A sorter is responsible only for ordering version tags.

Examples
--------
- Semantic Versioning
- PEP 440
- Date-based versions
- Git count versions

A sorter never generates versions.
Generation belongs to ``tag_strategy``.
"""

from __future__ import annotations

from typing import Protocol


class TagSorter(Protocol):
    """
    Protocol implemented by all tag sorters.
    """

    def sort(
        self,
        tags: list[str],
        *,
        reverse: bool = True,
    ) -> list[str]:
        """
        Sort version tags.

        Args:
            tags:
                Tags to sort.

            reverse:
                True for newest-first,
                False for oldest-first.

        Returns:
            Sorted version tags.
        """
        ...

    def latest(
        self,
        tags: list[str],
    ) -> str | None:
        """
        Return the newest tag.

        Args:
            tags:
                Available tags.

        Returns:
            The newest tag, or ``None`` if no tags exist.
        """
        ...

    def oldest(
        self,
        tags: list[str],
    ) -> str | None:
        """
        Return the oldest tag.

        Args:
            tags:
                Available tags.

        Returns:
            The oldest tag, or ``None`` if no tags exist.
        """
        ...

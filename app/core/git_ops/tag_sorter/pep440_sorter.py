# app/core/git_ops/tag_sorter/pep440_sorter.py

"""
PEP 440 Tag Sorter.

Sorts Python version tags according to PEP 440.

This sorter is responsible only for ordering existing tags.
It never generates or modifies version numbers.

Examples
--------
>>> sorter = PEP440Sorter()
>>> sorter.sort(["1.0.2", "1.0.10", "1.0.1"])
['1.0.10', '1.0.2', '1.0.1']
"""

from __future__ import annotations

from app.core.git_ops.helper.pep440_helper import PEP440VersionHelper

from .base import TagSorter


class PEP440Sorter(TagSorter):
    """
    Sort PEP 440 version tags.
    """

    def _sort_key(
        self,
        tag: str,
    ) -> tuple:
        """
        Return the sortable key for a PEP 440 version.

        Args:
            tag:
                PEP 440 Version tag.

        Returns:
            Comparable tuple produced by
            ``PEP440VersionHelper.sort_key``.
        """
        return PEP440VersionHelper(tag).sort_key

    def sort(
        self,
        tags: list[str],
        *,
        reverse: bool = True,
    ) -> list[str]:
        """
        Sort PEP 440 tags.

        Args:
            tags:
                Tags to sort.

            reverse:
                True for newest-first.
                False for oldest-first.

        Returns:
            Sorted tags.
        """
        return sorted(
            tags,
            key=self._sort_key,
            reverse=reverse,
        )

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
            Newest tag or ``None`` if the list is empty.
        """
        ordered = self.sort(tags)

        if not ordered:
            return None

        return ordered[0]

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
            Oldest tag or ``None`` if the list is empty.
        """
        ordered = self.sort(
            tags,
            reverse=False,
        )

        if not ordered:
            return None

        return ordered[0]

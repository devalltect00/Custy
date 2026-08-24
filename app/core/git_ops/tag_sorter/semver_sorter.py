# app/core/git_ops/tag_sorter/semver_sorter.py

"""
Semantic Version Tag Sorter.

Sorts Semantic Version tags using ``SemverVersionHelper``.

This sorter is responsible only for ordering existing tags.
It never generates or modifies version numbers.

Examples
--------
>>> sorter = SemverSorter()
>>> sorter.sort(["1.0.2", "1.0.10", "1.0.1"])
['1.0.10', '1.0.2', '1.0.1']
"""

from __future__ import annotations

from app.core.git_ops.helper.semver_helper import SemverVersionHelper

from .base import TagSorter


class SemverSorter(TagSorter):
    """
    Sort Semantic Version tags.
    """

    def _sort_key(
        self,
        tag: str,
    ) -> tuple:
        """
        Return the sortable key for a Semantic Version tag.

        Args:
            tag:
                Semantic Version tag.

        Returns:
            Comparable tuple produced by
            ``SemverVersionHelper.sort_key``.
        """
        return SemverVersionHelper(tag).sort_key

    def sort(
        self,
        tags: list[str],
        *,
        reverse: bool = True,
    ) -> list[str]:
        """
        Sort Semantic Version tags.

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
        Return the newest Semantic Version tag.

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
        Return the oldest Semantic Version tag.

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

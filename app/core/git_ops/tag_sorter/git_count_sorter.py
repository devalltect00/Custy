# app/core/git_ops/tag_sorter/git_count_sorter.py

"""
Git Count Tag Sorter.

Sorts tags representing integer build counts.

Examples
--------
1
2
10
25
100
"""

from __future__ import annotations

from .base import TagSorter


class GitCountSorter(TagSorter):
    """
    Sort integer build count tags.
    """

    def _sort_key(
        self,
        tag: str,
    ) -> int:
        """
        Return the sortable integer for a tag.

        Args:
            tag:
                Integer build count tag.

        Returns:
            Parsed integer.
        """
        return int(tag)

    def sort(
        self,
        tags: list[str],
        *,
        reverse: bool = True,
    ) -> list[str]:
        """
        Sort build count tags.

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
        Return the newest build count.
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
        Return the oldest build count.
        """
        ordered = self.sort(
            tags,
            reverse=False,
        )

        if not ordered:
            return None

        return ordered[0]

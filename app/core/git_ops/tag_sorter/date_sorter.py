# app/core/git_ops/tag_sorter/date_sorter.py

"""
Date-based Tag Sorter.

Sorts tags representing dates.

Examples
--------
2025.01.01
2025.08.06
2026.01.15
"""

from __future__ import annotations

from datetime import datetime

from .base import TagSorter


class DateSorter(TagSorter):
    """
    Sort date-based version tags.
    """

    def __init__(
        self,
        date_format: str = "%Y.%m.%d",
    ) -> None:
        self._date_format = date_format

    DATE_FORMAT = "%Y.%m.%d"

    def _sort_key(
        self,
        tag: str,
    ) -> datetime:
        """
        Return the sortable datetime for a tag.
        """
        return datetime.strptime(
            tag,
            self._date_format,
        )

    def sort(
        self,
        tags: list[str],
        *,
        reverse: bool = True,
    ) -> list[str]:
        """
        Sort date tags.
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
        Return the newest date tag.
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
        Return the oldest date tag.
        """
        ordered = self.sort(
            tags,
            reverse=False,
        )

        if not ordered:
            return None

        return ordered[0]

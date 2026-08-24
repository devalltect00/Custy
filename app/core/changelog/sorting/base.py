# app/core/changelog/sorting/base.py

"""
Release Sorter Protocol

Defines the contract implemented by changelog release
sorters.
"""

from __future__ import annotations

from typing import Protocol

from app.core.changelog.models.changelog import (
    Changelog,
)


class ReleaseSorter(Protocol):
    """
    Protocol implemented by release sorters.
    """

    def sort(
        self,
        changelog: Changelog,
        *,
        ascending: bool = False,
    ) -> Changelog:
        """
        Sort releases contained in a changelog.

        Args:
            changelog:
                Changelog to sort.

            ascending:
                Whether releases should be sorted from
                oldest to newest.

        Returns:
            Sorted changelog.
        """
        ...

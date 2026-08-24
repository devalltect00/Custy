# app/core/changelog/sorting/release_sorter.py

"""
Default Release Sorter

Sorts releases contained in a changelog.
"""

from __future__ import annotations

from datetime import datetime

from app.core.changelog.models.changelog import (
    Changelog,
)
from app.core.changelog.models.release import (
    Release,
)
from app.core.changelog.sorting.base import (
    ReleaseSorter,
)


class DefaultReleaseSorter(ReleaseSorter):
    """
    Default implementation of the release sorter.
    """

    DATE_FORMAT = "%Y-%m-%d"

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

        unreleased = [
            release
            for release in changelog.releases
            if release.version.casefold() == "unreleased"
        ]

        released = [
            release
            for release in changelog.releases
            if release.version.casefold() != "unreleased"
        ]

        released = sorted(
            released,
            key=self._sort_key,
            reverse=not ascending,
        )

        return Changelog(
            releases=unreleased + released,
        )

    def _sort_key(
        self,
        release: Release,
    ) -> datetime:
        """
        Compute the sorting key for a release.

        Args:
            release:
                Release to evaluate.

        Returns:
            Datetime used for sorting.
        """

        if release.release_date is None:
            return datetime.min

        try:
            return datetime.strptime(
                release.release_date,
                self.DATE_FORMAT,
            )

        except ValueError:
            return datetime.min

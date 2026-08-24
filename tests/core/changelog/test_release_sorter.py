# tests/core/changelog/test_release_sorter.py

"""
Unit tests for changelog release ordering.
"""

from app.core.changelog.models.changelog import Changelog
from app.core.changelog.models.release import Release
from app.core.changelog.sorting.release_sorter import DefaultReleaseSorter


def test_unreleased_is_first_then_releases_are_newest_first() -> None:
    """
    Unreleased always precedes date-sorted released versions.
    """

    changelog = Changelog(
        releases=[
            Release(version="1.0.0", release_date="2025-01-01"),
            Release(version="Unreleased"),
            Release(version="1.1.0", release_date="2025-02-01"),
        ]
    )

    result = DefaultReleaseSorter().sort(changelog)

    assert [release.version for release in result.releases] == [
        "Unreleased",
        "1.1.0",
        "1.0.0",
    ]

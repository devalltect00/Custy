# tests/core/git_ops/tag_sorter/test_date_sorter.py

"""
Tests for DateSorter.
"""

from __future__ import annotations

import pytest

from app.core.git_ops.tag_sorter.date_sorter import DateSorter


@pytest.fixture
def sorter() -> DateSorter:
    """
    Create a DateSorter instance.
    """
    return DateSorter()


# =========================================================
# sort()
# =========================================================


def test_sort_returns_empty_list_for_empty_input(
    sorter: DateSorter,
):
    """
    Empty input should remain empty.
    """
    assert sorter.sort([]) == []


def test_sort_single_tag(
    sorter: DateSorter,
):
    """
    A single tag should be returned unchanged.
    """
    tags = ["2025.08.06"]

    assert sorter.sort(tags) == [
        "2025.08.06",
    ]


def test_sort_date_versions(
    sorter: DateSorter,
):
    """
    Dates should be sorted chronologically.
    """
    tags = [
        "2024.12.31",
        "2026.01.01",
        "2025.08.06",
        "2025.01.01",
    ]

    assert sorter.sort(tags) == [
        "2026.01.01",
        "2025.08.06",
        "2025.01.01",
        "2024.12.31",
    ]


def test_sort_reverse_false(
    sorter: DateSorter,
):
    """
    reverse=False should return oldest first.
    """
    tags = [
        "2025.08.06",
        "2024.01.01",
        "2026.01.01",
    ]

    assert sorter.sort(
        tags,
        reverse=False,
    ) == [
        "2024.01.01",
        "2025.08.06",
        "2026.01.01",
    ]


# =========================================================
# latest()
# =========================================================


def test_latest_returns_none_for_empty_input(
    sorter: DateSorter,
):
    """
    Empty list has no latest tag.
    """
    assert sorter.latest([]) is None


def test_latest_returns_newest_date(
    sorter: DateSorter,
):
    """
    latest() should return the newest date.
    """
    tags = [
        "2025.08.06",
        "2026.01.01",
        "2024.12.31",
    ]

    assert sorter.latest(tags) == "2026.01.01"


# =========================================================
# oldest()
# =========================================================


def test_oldest_returns_none_for_empty_input(
    sorter: DateSorter,
):
    """
    Empty list has no oldest date.
    """
    assert sorter.oldest([]) is None


def test_oldest_returns_oldest_date(
    sorter: DateSorter,
):
    """
    oldest() should return the oldest date.
    """
    tags = [
        "2025.08.06",
        "2026.01.01",
        "2024.12.31",
    ]

    assert sorter.oldest(tags) == "2024.12.31"


# =========================================================
# invalid
# =========================================================


def test_invalid_date_raises(
    sorter: DateSorter,
):
    """
    Invalid dates should raise ValueError.
    """
    with pytest.raises(ValueError):
        sorter.sort(
            [
                "2025.08.06",
                "invalid",
            ]
        )


# =========================================================
# Additional
# =========================================================


def test_custom_date_format():
    """
    DateSorter should support custom date formats.
    """
    sorter = DateSorter(
        date_format="%Y%m%d",
    )

    tags = [
        "20250101",
        "20241231",
        "20260101",
    ]

    assert sorter.sort(tags) == [
        "20260101",
        "20250101",
        "20241231",
    ]

def test_duplicate_dates(
    sorter: DateSorter,
):
    """
    Duplicate dates should be preserved.
    """
    tags = [
        "2025.08.06",
        "2025.08.06",
        "2025.01.01",
    ]

    assert sorter.sort(tags) == [
        "2025.08.06",
        "2025.08.06",
        "2025.01.01",
    ]

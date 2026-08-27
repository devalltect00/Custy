# tests/core/git_ops/tag_sorter/test_git_count_sorter.py

"""
Tests for GitCountSorter.
"""

from __future__ import annotations

import pytest

from app.core.git_ops.tag_sorter.git_count_sorter import GitCountSorter


@pytest.fixture
def sorter() -> GitCountSorter:
    """
    Create a GitCountSorter instance.
    """
    return GitCountSorter()


# =========================================================
# sort()
# =========================================================


def test_sort_returns_empty_list_for_empty_input(
    sorter: GitCountSorter,
):
    """
    Empty input should remain empty.
    """
    assert sorter.sort([]) == []


def test_sort_single_tag(
    sorter: GitCountSorter,
):
    """
    A single tag should be returned unchanged.
    """
    tags = ["10"]

    assert sorter.sort(tags) == ["10"]


def test_sort_git_counts(
    sorter: GitCountSorter,
):
    """
    Git count tags should be sorted numerically.
    """
    tags = [
        "10",
        "1",
        "100",
        "25",
        "3",
    ]

    assert sorter.sort(tags) == [
        "100",
        "25",
        "10",
        "3",
        "1",
    ]


def test_sort_reverse_false(
    sorter: GitCountSorter,
):
    """
    reverse=False should return the oldest build first.
    """
    tags = [
        "10",
        "1",
        "100",
        "25",
        "3",
    ]

    assert sorter.sort(
        tags,
        reverse=False,
    ) == [
        "1",
        "3",
        "10",
        "25",
        "100",
    ]


# =========================================================
# latest()
# =========================================================


def test_latest_returns_none_for_empty_input(
    sorter: GitCountSorter,
):
    """
    Empty list has no latest tag.
    """
    assert sorter.latest([]) is None


def test_latest_returns_highest_count(
    sorter: GitCountSorter,
):
    """
    latest() should return the highest build count.
    """
    tags = [
        "10",
        "1",
        "100",
        "25",
    ]

    assert sorter.latest(tags) == "100"


# =========================================================
# oldest()
# =========================================================


def test_oldest_returns_none_for_empty_input(
    sorter: GitCountSorter,
):
    """
    Empty list has no oldest tag.
    """
    assert sorter.oldest([]) is None


def test_oldest_returns_lowest_count(
    sorter: GitCountSorter,
):
    """
    oldest() should return the lowest build count.
    """
    tags = [
        "10",
        "1",
        "100",
        "25",
    ]

    assert sorter.oldest(tags) == "1"


# =========================================================
# duplicates
# =========================================================


def test_duplicate_counts(
    sorter: GitCountSorter,
):
    """
    Duplicate build counts should be preserved.
    """
    tags = [
        "10",
        "10",
        "3",
    ]

    assert sorter.sort(tags) == [
        "10",
        "10",
        "3",
    ]


# =========================================================
# invalid
# =========================================================


def test_invalid_git_count_raises(
    sorter: GitCountSorter,
):
    """
    Invalid build counts should raise ValueError.
    """
    with pytest.raises(ValueError):
        sorter.sort(
            [
                "10",
                "abc",
            ]
        )


# =========================================================
# Additional
# =========================================================


def test_sort_handles_lexicographical_bug(
    sorter: GitCountSorter,
):
    """
    Ensure numeric ordering instead of lexicographical ordering.
    """
    tags = [
        "9",
        "10",
        "11",
        "100",
    ]

    assert sorter.sort(tags) == [
        "100",
        "11",
        "10",
        "9",
    ]

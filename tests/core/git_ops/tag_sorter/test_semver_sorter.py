# tests/core/git_ops/tag_sorter/test_semver_sorter.py

"""
Tests for SemverSorter.
"""

from __future__ import annotations

import pytest

from app.core.git_ops.tag_sorter.semver_sorter import SemverSorter


@pytest.fixture
def sorter() -> SemverSorter:
    """
    Create a SemverSorter instance.
    """
    return SemverSorter()


# =========================================================
# sort()
# =========================================================


def test_sort_returns_empty_list_for_empty_input(
    sorter: SemverSorter,
):
    """
    Empty input should remain empty.
    """
    assert sorter.sort([]) == []


def test_sort_single_tag(
    sorter: SemverSorter,
):
    """
    A single tag should be returned unchanged.
    """
    tags = ["1.0.0"]

    assert sorter.sort(tags) == ["1.0.0"]


def test_sort_patch_versions(
    sorter: SemverSorter,
):
    """
    Patch versions should be sorted numerically.
    """
    tags = [
        "1.10.2",
        "1.10.14",
        "1.10.9",
        "1.10.1",
    ]

    assert sorter.sort(tags) == [
        "1.10.14",
        "1.10.9",
        "1.10.2",
        "1.10.1",
    ]


def test_sort_minor_versions(
    sorter: SemverSorter,
):
    """
    Minor version has higher priority than patch.
    """
    tags = [
        "1.9.99",
        "1.10.0",
        "1.8.20",
    ]

    assert sorter.sort(tags) == [
        "1.10.0",
        "1.9.99",
        "1.8.20",
    ]


def test_sort_major_versions(
    sorter: SemverSorter,
):
    """
    Major version has highest precedence.
    """
    tags = [
        "2.0.0",
        "10.0.0",
        "1.999.999",
    ]

    assert sorter.sort(tags) == [
        "10.0.0",
        "2.0.0",
        "1.999.999",
    ]


def test_sort_reverse_false(
    sorter: SemverSorter,
):
    """
    reverse=False should return oldest first.
    """
    tags = [
        "2.0.0",
        "1.0.0",
        "3.0.0",
    ]

    assert sorter.sort(
        tags,
        reverse=False,
    ) == [
        "1.0.0",
        "2.0.0",
        "3.0.0",
    ]


# =========================================================
# latest()
# =========================================================


def test_latest_returns_none_for_empty_input(
    sorter: SemverSorter,
):
    """
    Empty list has no latest tag.
    """
    assert sorter.latest([]) is None


def test_latest_returns_highest_version(
    sorter: SemverSorter,
):
    """
    latest() should return newest version.
    """
    tags = [
        "1.2.0",
        "2.0.0",
        "1.9.9",
    ]

    assert sorter.latest(tags) == "2.0.0"


# =========================================================
# oldest()
# =========================================================


def test_oldest_returns_none_for_empty_input(
    sorter: SemverSorter,
):
    """
    Empty list has no oldest tag.
    """
    assert sorter.oldest([]) is None


def test_oldest_returns_lowest_version(
    sorter: SemverSorter,
):
    """
    oldest() should return oldest version.
    """
    tags = [
        "1.2.0",
        "2.0.0",
        "1.0.0",
    ]

    assert sorter.oldest(tags) == "1.0.0"


# =========================================================
# invalid
# =========================================================


def test_invalid_version_raises(
    sorter: SemverSorter,
):
    """
    Invalid versions should raise ValueError.
    """
    with pytest.raises(ValueError):
        sorter.sort(
            [
                "1.0.0",
                "invalid",
            ]
        )


# =========================================================
# Additional
# =========================================================


def test_sort_handles_lexicographical_bug(
    sorter: SemverSorter,
):
    """
    Ensure semantic ordering instead of lexicographical ordering.
    """
    tags = [
        "1.10.8",
        "1.10.9",
        "1.10.10",
        "1.10.11",
        "1.10.14",
    ]

    assert sorter.sort(tags) == [
        "1.10.14",
        "1.10.11",
        "1.10.10",
        "1.10.9",
        "1.10.8",
    ]


# =========================================================
# Semver-specific tests
# =========================================================


def test_sort_prerelease_order(
    sorter: SemverSorter,
):
    """
    Development, pre-release, release and post-release
    should follow Semantic Version precedence.
    """
    tags = [
        "1.2.3",
        "1.2.3-post.1",
        "1.2.3-rc.1",
        "1.2.3-beta.1",
        "1.2.3-alpha.1",
        "1.2.3-dev.1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-post.1",
        "1.2.3",
        "1.2.3-rc.1",
        "1.2.3-beta.1",
        "1.2.3-alpha.1",
        "1.2.3-dev.1",
    ]

def test_sort_dev_versions(
    sorter: SemverSorter,
):
    """
    Development releases should be ordered by their
    development number.
    """
    tags = [
        "1.2.3-dev.2",
        "1.2.3-dev.10",
        "1.2.3-dev.1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-dev.10",
        "1.2.3-dev.2",
        "1.2.3-dev.1",
    ]

def test_sort_alpha_versions(
    sorter: SemverSorter,
):
    """
    Alpha releases should be ordered numerically.
    """
    tags = [
        "1.2.3-alpha.2",
        "1.2.3-alpha.10",
        "1.2.3-alpha.1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-alpha.10",
        "1.2.3-alpha.2",
        "1.2.3-alpha.1",
    ]

def test_sort_beta_versions(
    sorter: SemverSorter,
):
    tags = [
        "1.2.3-beta.1",
        "1.2.3-beta.4",
        "1.2.3-beta.2",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-beta.4",
        "1.2.3-beta.2",
        "1.2.3-beta.1",
    ]

def test_sort_rc_versions(
    sorter: SemverSorter,
):
    tags = [
        "1.2.3-rc.3",
        "1.2.3-rc.1",
        "1.2.3-rc.2",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-rc.3",
        "1.2.3-rc.2",
        "1.2.3-rc.1",
    ]

def test_sort_post_versions(
    sorter: SemverSorter,
):
    tags = [
        "1.2.3-post.1",
        "1.2.3-post.5",
        "1.2.3-post.2",
    ]

    assert sorter.sort(tags) == [
        "1.2.3-post.5",
        "1.2.3-post.2",
        "1.2.3-post.1",
    ]

def test_sort_build_metadata(
    sorter: SemverSorter,
):
    """
    Build metadata should not affect precedence.
    """
    tags = [
        "1.2.3+linux",
        "1.2.3+windows",
        "1.2.3",
    ]

    result = sorter.sort(tags)

    assert set(result) == {
        "1.2.3",
        "1.2.3+linux",
        "1.2.3+windows",
    }

def test_sort_mixed_semver_versions(
    sorter: SemverSorter,
):
    """
    Mixed Semantic Versions should be sorted according
    to SemVer precedence.
    """
    tags = [
        "2.0.0-dev.1",
        "2.0.0-alpha.1",
        "2.0.0-beta.2",
        "2.0.0-rc.1",
        "2.0.0",
        "2.0.0-post.1",
        "1.9.9",
    ]

    assert sorter.sort(tags) == [
        "2.0.0-post.1",
        "2.0.0",
        "2.0.0-rc.1",
        "2.0.0-beta.2",
        "2.0.0-alpha.1",
        "2.0.0-dev.1",
        "1.9.9",
    ]

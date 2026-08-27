# tests/core/git_ops/tag_sorter/test_pep440_sorter.py

"""
Tests for PEP440Sorter.
"""

from __future__ import annotations

import pytest

from app.core.git_ops.tag_sorter.pep440_sorter import PEP440Sorter


@pytest.fixture
def sorter() -> PEP440Sorter:
    """
    Create a PEP440Sorter instance.
    """
    return PEP440Sorter()


# =========================================================
# sort()
# =========================================================


def test_sort_returns_empty_list_for_empty_input(
    sorter: PEP440Sorter,
):
    """
    Empty input should remain empty.
    """
    assert sorter.sort([]) == []


def test_sort_single_tag(
    sorter: PEP440Sorter,
):
    """
    A single tag should be returned unchanged.
    """
    tags = ["1.0.0"]

    assert sorter.sort(tags) == ["1.0.0"]


def test_sort_patch_versions(
    sorter: PEP440Sorter,
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
    sorter: PEP440Sorter,
):
    """
    Minor versions take precedence over patch versions.
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
    sorter: PEP440Sorter,
):
    """
    Major versions take precedence.
    """
    tags = [
        "10.0.0",
        "2.0.0",
        "1.999.999",
    ]

    assert sorter.sort(tags) == [
        "10.0.0",
        "2.0.0",
        "1.999.999",
    ]


def test_sort_reverse_false(
    sorter: PEP440Sorter,
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
    sorter: PEP440Sorter,
):
    assert sorter.latest([]) is None


def test_latest_returns_highest_version(
    sorter: PEP440Sorter,
):
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
    sorter: PEP440Sorter,
):
    assert sorter.oldest([]) is None


def test_oldest_returns_lowest_version(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.0",
        "2.0.0",
        "1.0.0",
    ]

    assert sorter.oldest(tags) == "1.0.0"


# =========================================================
# PEP 440-specific tests
# =========================================================


def test_sort_dev_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.3.dev2",
        "1.2.3.dev10",
        "1.2.3.dev1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3.dev10",
        "1.2.3.dev2",
        "1.2.3.dev1",
    ]


def test_sort_alpha_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.3a2",
        "1.2.3a10",
        "1.2.3a1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3a10",
        "1.2.3a2",
        "1.2.3a1",
    ]


def test_sort_beta_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.3b2",
        "1.2.3b10",
        "1.2.3b1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3b10",
        "1.2.3b2",
        "1.2.3b1",
    ]


def test_sort_rc_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.3rc2",
        "1.2.3rc10",
        "1.2.3rc1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3rc10",
        "1.2.3rc2",
        "1.2.3rc1",
    ]


def test_sort_post_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1.2.3.post2",
        "1.2.3.post10",
        "1.2.3.post1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3.post10",
        "1.2.3.post2",
        "1.2.3.post1",
    ]


def test_sort_pep440_precedence(
    sorter: PEP440Sorter,
):
    """
    Development, pre-release, final and post-release
    should follow PEP 440 precedence.
    """
    tags = [
        "1.2.3.post1",
        "1.2.3",
        "1.2.3rc1",
        "1.2.3b1",
        "1.2.3a1",
        "1.2.3.dev1",
    ]

    assert sorter.sort(tags) == [
        "1.2.3.post1",
        "1.2.3",
        "1.2.3rc1",
        "1.2.3b1",
        "1.2.3a1",
        "1.2.3.dev1",
    ]


def test_sort_epoch_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "1!1.0.0",
        "2!1.0.0",
        "3!1.0.0",
    ]

    assert sorter.sort(tags) == [
        "3!1.0.0",
        "2!1.0.0",
        "1!1.0.0",
    ]


def test_sort_local_versions(
    sorter: PEP440Sorter,
):
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


def test_sort_mixed_pep440_versions(
    sorter: PEP440Sorter,
):
    tags = [
        "2!1.0.0",
        "1!2.0.0.post2",
        "1!2.0.0",
        "1!2.0.0rc2",
        "1!2.0.0b1",
        "1!2.0.0a1",
        "1!2.0.0.dev3",
    ]

    assert sorter.sort(tags) == [
        "2!1.0.0",
        "1!2.0.0.post2",
        "1!2.0.0",
        "1!2.0.0rc2",
        "1!2.0.0b1",
        "1!2.0.0a1",
        "1!2.0.0.dev3",
    ]


def test_invalid_version_raises(
    sorter: PEP440Sorter,
):
    with pytest.raises(ValueError):
        sorter.sort(
            [
                "1.0.0",
                "invalid",
            ]
        )

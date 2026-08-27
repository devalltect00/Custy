# tests/core/git_ops/tag_sorter/test_factory.py

"""
Tests for TagSorterFactory.
"""

from __future__ import annotations

import pytest

# from app.constants.strategy import StrategyChoices
from app.cli.constants.enums import StrategyChoices
from app.core.git_ops.tag_sorter.date_sorter import DateSorter
from app.core.git_ops.tag_sorter.factory import TagSorterFactory
from app.core.git_ops.tag_sorter.git_count_sorter import GitCountSorter
from app.core.git_ops.tag_sorter.pep440_sorter import PEP440Sorter
from app.core.git_ops.tag_sorter.semver_sorter import SemverSorter


def test_create_semver_sorter():
    """
    Should create SemverSorter.
    """
    sorter = TagSorterFactory.create(
        StrategyChoices.SEMVER,
    )

    assert isinstance(
        sorter,
        SemverSorter,
    )


def test_create_pep440_sorter():
    """
    Should create PEP440Sorter.
    """
    sorter = TagSorterFactory.create(
        StrategyChoices.PEP440,
    )

    assert isinstance(
        sorter,
        PEP440Sorter,
    )


def test_create_date_sorter():
    """
    Should create DateSorter.
    """
    sorter = TagSorterFactory.create(
        StrategyChoices.DATE,
    )

    assert isinstance(
        sorter,
        DateSorter,
    )


def test_create_git_count_sorter():
    """
    Should create GitCountSorter.
    """
    sorter = TagSorterFactory.create(
        StrategyChoices.GIT_COUNT,
    )

    assert isinstance(
        sorter,
        GitCountSorter,
    )


def test_pass_constructor_arguments():
    """
    Constructor kwargs should be forwarded.
    """
    sorter = TagSorterFactory.create(
        StrategyChoices.DATE,
        date_format="%Y%m%d",
    )

    assert isinstance(
        sorter,
        DateSorter,
    )

    assert sorter._date_format == "%Y%m%d"


def test_unknown_strategy_raises():
    """
    Unsupported strategies should raise ValueError.
    """

    class Dummy:
        pass

    with pytest.raises(ValueError):
        TagSorterFactory.create(Dummy())


# =========================================================
# Additional
# =========================================================


def test_custom_date_format_is_used():
    sorter = TagSorterFactory.create(
        StrategyChoices.DATE,
        date_format="%Y%m%d",
    )

    assert sorter.sort(
        [
            "20250101",
            "20240101",
        ]
    ) == [
        "20250101",
        "20240101",
    ]

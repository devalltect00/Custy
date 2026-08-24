# app/core/git_ops/tag_sorter/factory.py

"""
Factory for creating tag sorters.
"""

from __future__ import annotations

# from app.constants.strategy import StrategyChoices
from app.cli.constants.enums import StrategyChoices

from .base import TagSorter
from .date_sorter import DateSorter
from .git_count_sorter import GitCountSorter
from .pep440_sorter import PEP440Sorter
from .semver_sorter import SemverSorter


class TagSorterFactory:
    """
    Factory for creating TagSorter implementations.
    """

    _SORTERS: dict[StrategyChoices, type[TagSorter]] = {
        StrategyChoices.SEMVER: SemverSorter,
        StrategyChoices.PEP440: PEP440Sorter,
        StrategyChoices.DATE: DateSorter,
        StrategyChoices.GIT_COUNT: GitCountSorter,
    }

    @classmethod
    def create(
        cls,
        strategy: StrategyChoices,
        **kwargs,
    ) -> TagSorter:
        """
        Create a TagSorter.

        Args:
            strategy:
                Versioning strategy.

            **kwargs:
                Additional sorter-specific arguments.

        Returns:
            TagSorter implementation.

        Raises:
            ValueError:
                If the strategy is unsupported.
        """
        sorter_cls = cls._SORTERS.get(strategy)

        if sorter_cls is None:
            raise ValueError(
                f"Unsupported tag sorting strategy: {strategy}"
            )

        return sorter_cls(**kwargs)

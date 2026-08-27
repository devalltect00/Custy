# tests/core/git_ops/git/test_service_tags.py

"""
Tests for strategy-aware Git tag sorting in GitService.

Coverage:
    - strategy resolution
    - sorter creation and caching
    - newest-first tag ordering
    - latest and oldest version tag helpers
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.cli.constants.enums import StrategyChoices
from app.core.git_ops.git.service import GitService


def create_service(
    *,
    strategy: StrategyChoices | str | None = StrategyChoices.SEMVER,
    stdout: str = "",
    date_format: str = "%Y.%m.%d",
) -> tuple[GitService, MagicMock, MagicMock]:
    """
    Create a GitService with mocked executor and configuration.
    """

    executor = MagicMock()
    executor.get_tags.return_value = SimpleNamespace(
        stdout=stdout,
    )
    executor.get_silent.return_value = True

    config = MagicMock()
    config.get.return_value = date_format

    service = GitService(
        executor=executor,
        config=config,
        strategy=strategy,
    )

    return service, executor, config


class TestResolveTagSortingStrategy:
    """
    Tests for GitService._resolve_tag_sorting_strategy().
    """

    def test_uses_explicit_enum_strategy(self):
        service, _, _ = create_service(
            strategy=StrategyChoices.SEMVER,
        )

        with patch(
            "app.core.git_ops.git.service.detect_tag_sorting_strategy"
        ) as detector:
            result = service._resolve_tag_sorting_strategy()

        assert result == StrategyChoices.SEMVER
        detector.assert_not_called()

    def test_accepts_raw_string_strategy(self):
        service, _, _ = create_service(
            strategy="pep440",
        )

        result = service._resolve_tag_sorting_strategy()

        assert result == StrategyChoices.PEP440

    @pytest.mark.parametrize(
        "strategy",
        [
            None,
            StrategyChoices.NONE,
            StrategyChoices.COMMITIZEN,
        ],
    )
    def test_detects_sorting_strategy_when_required(
        self,
        strategy,
    ):
        service, executor, _ = create_service(
            strategy=strategy,
        )

        with patch(
            "app.core.git_ops.git.service.detect_tag_sorting_strategy",
            return_value="pep440",
        ) as detector:
            result = service._resolve_tag_sorting_strategy()

        assert result == StrategyChoices.PEP440
        detector.assert_called_once_with(
            no_debug=True,
        )
        executor.get_silent.assert_called_once_with()

    def test_rejects_unknown_raw_strategy(self):
        service, _, _ = create_service(
            strategy="unknown",
        )

        with pytest.raises(ValueError):
            service._resolve_tag_sorting_strategy()


class TestGetTagSorter:
    """
    Tests for GitService._get_tag_sorter().
    """

    @patch("app.core.git_ops.git.service.TagSorterFactory.create")
    def test_creates_sorter_for_explicit_strategy(
        self,
        create_sorter,
    ):
        sorter = MagicMock()
        create_sorter.return_value = sorter

        service, _, _ = create_service(
            strategy=StrategyChoices.SEMVER,
        )

        result = service._get_tag_sorter()

        assert result is sorter
        create_sorter.assert_called_once_with(
            strategy=StrategyChoices.SEMVER,
        )

    @patch("app.core.git_ops.git.service.TagSorterFactory.create")
    def test_forwards_date_format(
        self,
        create_sorter,
    ):
        sorter = MagicMock()
        create_sorter.return_value = sorter

        service, _, config = create_service(
            strategy=StrategyChoices.DATE,
            date_format="%Y-%m-%d",
        )

        result = service._get_tag_sorter()

        assert result is sorter

        config.get.assert_called_once_with(
            "cli",
            "versioning",
            "date_format",
            default="%Y.%m.%d",
        )
        create_sorter.assert_called_once_with(
            strategy=StrategyChoices.DATE,
            date_format="%Y-%m-%d",
        )

    @patch("app.core.git_ops.git.service.TagSorterFactory.create")
    def test_caches_sorter_instance(
        self,
        create_sorter,
    ):
        sorter = MagicMock()
        create_sorter.return_value = sorter

        service, _, _ = create_service()

        first = service._get_tag_sorter()
        second = service._get_tag_sorter()

        assert first is sorter
        assert second is sorter
        create_sorter.assert_called_once_with(
            strategy=StrategyChoices.SEMVER,
        )


class TestGetTags:
    """
    Tests for GitService.get_tags().
    """

    @patch("app.core.git_ops.git.service.TagSorterFactory.create")
    def test_returns_empty_list_without_creating_sorter(
        self,
        create_sorter,
    ):
        service, executor, _ = create_service(
            stdout="",
        )

        result = service.get_tags()

        assert result == []
        executor.get_tags.assert_called_once_with()
        create_sorter.assert_not_called()

    def test_passes_reverse_true_to_sorter(self):
        service, _, _ = create_service(
            stdout="1.0.0\n2.0.0\n",
        )

        sorter = MagicMock()
        sorter.sort.return_value = [
            "2.0.0",
            "1.0.0",
        ]
        service._tag_sorter = sorter

        result = service.get_tags()

        assert result == [
            "2.0.0",
            "1.0.0",
        ]
        sorter.sort.assert_called_once_with(
            [
                "1.0.0",
                "2.0.0",
            ],
            reverse=True,
        )

    @pytest.mark.parametrize(
        (
            "strategy",
            "tags",
            "expected",
        ),
        [
            (
                StrategyChoices.SEMVER,
                [
                    "v1.9.0",
                    "v1.10.0",
                    "v1.2.0",
                ],
                [
                    "v1.10.0",
                    "v1.9.0",
                    "v1.2.0",
                ],
            ),
            (
                StrategyChoices.PEP440,
                [
                    "1.9.0",
                    "1.10.0rc1",
                    "1.10.0",
                    "1.10.0b1",
                ],
                [
                    "1.10.0",
                    "1.10.0rc1",
                    "1.10.0b1",
                    "1.9.0",
                ],
            ),
            (
                StrategyChoices.DATE,
                [
                    "2026.01.02",
                    "2025.12.31",
                    "2026.07.18",
                ],
                [
                    "2026.07.18",
                    "2026.01.02",
                    "2025.12.31",
                ],
            ),
            (
                StrategyChoices.GIT_COUNT,
                [
                    "9",
                    "100",
                    "20",
                    "2",
                ],
                [
                    "100",
                    "20",
                    "9",
                    "2",
                ],
            ),
        ],
    )
    def test_sorts_tags_newest_first(
        self,
        strategy,
        tags,
        expected,
    ):
        service, _, _ = create_service(
            strategy=strategy,
            stdout="\n".join(tags),
        )

        result = service.get_tags()

        assert result == expected


class TestVersionTagBoundaries:
    """
    Tests for latest and oldest version-tag helpers.
    """

    def test_get_latest_version_tag(self):
        service, _, _ = create_service(
            strategy=StrategyChoices.SEMVER,
            stdout="\n".join(
                [
                    "v1.2.0",
                    "v2.0.0",
                    "v1.10.0",
                ]
            ),
        )

        result = service.get_latest_version_tag()

        assert result == "v2.0.0"

    def test_get_latest_version_tag_returns_none_when_empty(
        self,
    ):
        service, _, _ = create_service(
            stdout="",
        )

        result = service.get_latest_version_tag()

        assert result is None

    def test_get_oldest_version_tag(self):
        service, _, _ = create_service(
            strategy=StrategyChoices.SEMVER,
            stdout="\n".join(
                [
                    "v1.2.0",
                    "v2.0.0",
                    "v1.10.0",
                ]
            ),
        )

        result = service.get_oldest_version_tag()

        assert result == "v1.2.0"

    def test_get_oldest_version_tag_returns_none_when_empty(
        self,
    ):
        service, _, _ = create_service(
            stdout="",
        )

        result = service.get_oldest_version_tag()

        assert result is None

# tests/core/changelog/test_generator.py

"""
Unit tests for changelog release-family planning.

The tests exercise pure generator helpers without invoking Git,
writing files, or rendering the repository changelog.
"""

from unittest.mock import MagicMock

import pytest

from app.core.changelog.generator import ChangelogGenerator
from app.core.changelog.models.commit import Commit


@pytest.fixture
def generator() -> ChangelogGenerator:
    """
    Create an uninitialized generator for pure helper tests.

    Returns:
        Generator instance whose tested methods require no
        runtime collaborators.
    """

    return object.__new__(ChangelogGenerator)


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("1.10.6", "stable"),
        ("1.10.6b1", "beta"),
        ("1.10.6rc4", "rc"),
        ("v1.10.6-rc.4", "rc"),
        ("v1.10.6-beta.1", "beta"),
        ("1.10.6.dev1", "dev"),
    ],
)
def test_recognizes_pep440_and_semver_release_stages(
    generator: ChangelogGenerator,
    version: str,
    expected: str,
) -> None:
    """
    Supported PEP 440 and SemVer prereleases are classified.
    """

    assert generator._release_stage(version) == expected


def test_stable_release_uses_previous_stable_boundary(
    generator: ChangelogGenerator,
) -> None:
    """
    A final release aggregates its complete prerelease family.
    """

    tags = [
        "1.10.6",
        "1.10.6rc4",
        "1.10.6rc3",
        "1.10.6b1",
        "1.10.5",
    ]

    assert generator._previous_boundary(tags, 0) == ("1.10.5", 4)
    assert generator._promoted_tags(
        tags=tags,
        current_index=0,
        previous_index=4,
    ) == ["1.10.6rc4", "1.10.6rc3", "1.10.6b1"]


def test_prerelease_uses_adjacent_boundary(
    generator: ChangelogGenerator,
) -> None:
    """
    A release candidate compares with the adjacent prerelease.
    """

    tags = ["1.10.6", "1.10.6rc2", "1.10.6rc1", "1.10.6b1"]

    assert generator._previous_boundary(tags, 1) == ("1.10.6rc1", 2)


def test_selects_commit_matching_current_version(
    generator: ChangelogGenerator,
) -> None:
    """
    Release summary extraction selects the exact release family commit.
    """

    commits = [
        Commit(
            subject="ordinary fix",
            body="Details",
            commit_type="fix",
            scope="core",
            breaking=False,
            commit_date="",
            hash="",
        ),
        Commit(
            subject="1.10.6 — final release",
            body="Final release of Custy 1.10.6.",
            commit_type="release",
            scope="release",
            breaking=False,
            commit_date="",
            hash="",
        ),
    ]

    selected = generator._select_release_commit(commits, "1.10.6")

    assert selected is commits[1]


def test_does_not_select_unrelated_release_commit(
    generator: ChangelogGenerator,
) -> None:
    """
    A release commit for another version cannot supply metadata.
    """

    commits = [
        Commit(
            subject="1.10.11",
            body="Final release of Custy 1.10.11.",
            commit_type="release",
            scope="main",
            breaking=False,
            commit_date="",
            hash="",
        )
    ]

    assert generator._select_release_commit(commits, "1.10.13") is None


def test_promotions_exclude_current_and_stable_versions(
    generator: ChangelogGenerator,
) -> None:
    """
    Only prereleases in the current stable family are promoted.
    """

    assert generator._valid_promotions(
        versions=[
            "1.10.6rc2",
            "1.10.6",
            "1.10.5",
            "1.10.6b1",
        ],
        current="1.10.6",
    ) == ["1.10.6rc2", "1.10.6b1"]


def test_collect_releases_reports_each_release_candidate(
    generator: ChangelogGenerator,
    monkeypatch,
) -> None:
    """Unreleased content and every Git tag advance progress once."""

    tags = ["v2.0.0", "v2.0.0-rc.1"]
    generator.git_service = MagicMock()
    generator.git_service.get_tags.return_value = tags
    generator.config = MagicMock()
    generator._collect_messages = MagicMock(return_value=[])

    progress = MagicMock()
    progress_context = MagicMock()
    progress_context.__enter__.return_value = progress
    progress_context.__exit__.return_value = False
    progress_factory = MagicMock(return_value=progress_context)

    monkeypatch.setattr(
        "app.core.changelog.generator.MessageProviderFactory.create",
        MagicMock(return_value=[]),
    )
    monkeypatch.setattr(
        "app.core.changelog.generator.progress_task",
        progress_factory,
    )

    changelog = generator._collect_releases()

    progress_factory.assert_called_once_with(
        "Generating changelog",
        total=3,
    )
    assert progress.update.call_args_list == [
        (("Processing Unreleased changes",), {}),
        (("Processing release v2.0.0",), {}),
        (("Processing release v2.0.0-rc.1",), {}),
    ]
    assert progress.advance.call_count == 3
    assert changelog.releases == []


def test_write_to_file_preserves_destination_during_dry_run(
    generator: ChangelogGenerator,
    tmp_path,
    capsys,
) -> None:
    """Dry-run prints rendered content without changing the destination."""

    target = tmp_path / "CHANGELOG.md"
    target.write_text("existing", encoding="utf-8")
    generator.runner = MagicMock()
    generator.runner.is_dry_run = True

    generator.write_to_file("# Preview", target)

    assert target.read_text(encoding="utf-8") == "existing"
    output = capsys.readouterr().out
    assert "Would write changelog" in output
    assert "# Preview" in output


def test_write_to_file_persists_rendered_content(
    generator: ChangelogGenerator,
    tmp_path,
) -> None:
    """Normal execution writes the rendered changelog."""

    target = tmp_path / "CHANGELOG.md"
    generator.runner = MagicMock()
    generator.runner.is_dry_run = False

    generator.write_to_file("# Generated", target)

    assert target.read_text(encoding="utf-8") == "# Generated"

"""Tests for Docker and distribution build-version resolution."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock

from app.core.build.version import (
    resolve_repository_version,
    version_from_git_description,
)


class TestVersionFromGitDescription:
    """Tests conversion of supported Git tag forms to package versions."""

    def test_exact_semver_release(self) -> None:
        """An exact prefixed SemVer tag becomes its public package version."""

        assert version_from_git_description("v2.1.0-0-gabc1234") == "2.1.0"

    def test_semver_release_after_additional_commits(self) -> None:
        """Commit distance is represented as a post release."""

        assert version_from_git_description("1.10.14-51-g90876ce") == "1.10.14.post51"

    def test_semver_prerelease_is_normalized_for_python(self) -> None:
        """SemVer RC spelling converts to a valid PEP 440 package version."""

        assert version_from_git_description("v2.0.0-rc.1-0-gabc1234") == "2.0.0rc1"

    def test_pep440_post_release_distance_remains_valid(self) -> None:
        """Commits after an existing post release use the next development post."""

        assert (
            version_from_git_description("1.0.0.post1-3-gabc1234") == "1.0.0.post2.dev3"
        )

    def test_untagged_description_uses_fallback(self) -> None:
        """A revision-only description cannot invent a release version."""

        assert version_from_git_description("90876ce", fallback="0.0.0") == "0.0.0"


class TestResolveRepositoryVersion:
    """Tests the read-only Git command boundary."""

    def test_runs_git_without_a_shell(self, tmp_path: Path) -> None:
        """Repository discovery uses an argument list and shell=False."""

        runner = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=["git", "describe"],
                returncode=0,
                stdout="v2.1.0-4-gabc1234\n",
                stderr="",
            )
        )

        version = resolve_repository_version(tmp_path, runner=runner)

        assert version == "2.1.0.post4"
        runner.assert_called_once_with(
            ["git", "describe", "--tags", "--long", "--always"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
            shell=False,
        )

    def test_git_failure_uses_fallback(self, tmp_path: Path) -> None:
        """Unavailable repository metadata returns the explicit fallback."""

        runner = MagicMock(side_effect=FileNotFoundError("git missing"))

        version = resolve_repository_version(
            tmp_path,
            fallback="0.0.0",
            runner=runner,
        )

        assert version == "0.0.0"

# tests/core/git_ops/git/test_service_remote.py

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    svc = GitService(executor=executor, config=config)

    return svc


class TestResolveRemotes:
    """
    Tests GitService.resolve_remotes().
    """

    def test_explicit_remotes_have_priority(self, service):
        remotes = ["origin", "backup"]

        result = service.resolve_remotes(remotes=remotes)

        assert result == remotes

        service.config.resolve.assert_not_called()

    def test_push_main(self, service):
        service.config.resolve.return_value = "main"

        service.config.get.side_effect = [
            ["origin"],
            ["backup"],
        ]

        result = service.resolve_remotes()

        assert result == ["origin"]

    def test_push_backup(self, service):
        service.config.resolve.return_value = "backup"

        service.config.get.side_effect = [
            ["origin"],
            ["backup"],
        ]

        result = service.resolve_remotes()

        assert result == ["backup"]

    def test_push_all(self, service):
        service.config.resolve.return_value = "all"

        service.config.get.side_effect = [
            ["origin"],
            ["backup", "origin"],
        ]

        result = service.resolve_remotes()

        assert result == ["origin", "backup"]

    def test_unknown_strategy_falls_back_main(self, service):
        service.config.resolve.return_value = "unknown"

        service.config.get.side_effect = [
            ["origin"],
            ["backup"],
        ]

        result = service.resolve_remotes()

        assert result == ["origin"]

    def test_cli_push_to_is_forwarded(self, service):
        service.config.resolve.return_value = "backup"

        service.config.get.side_effect = [
            ["origin"],
            ["mirror"],
        ]

        result = service.resolve_remotes(push_to="backup")

        service.config.resolve.assert_called_once_with(
            cli_value="backup",
            config_keys=["git", "push_to"],
            default="main",
        )

        assert result == ["mirror"]


class TestResolveDefaultRemote:
    """
    Tests GitService.resolve_default_remote().
    """

    def test_explicit_remote(self, service):
        service.config.resolve.return_value = "backup"

        result = service.resolve_default_remote("backup")

        assert result == "backup"

        service.config.resolve.assert_called_once_with(
            cli_value="backup",
            config_keys=["git", "default_remote"],
            default="origin",
        )

    def test_default_remote(self, service):
        service.config.resolve.return_value = "origin"

        assert service.resolve_default_remote() == "origin"


class TestGetRemoteUrl:
    """
    Tests GitService.get_remote_url().
    """

    def test_success(self, service):
        service.executor.remote_get_url.return_value = CommandResult(
            returncode=0,
            stdout="https://github.com/user/repo.git\n",
        )

        assert (
            service.get_remote_url("origin")
            == "https://github.com/user/repo.git"
        )

    def test_failure_returns_none(self, service):
        service.executor.remote_get_url.return_value = CommandResult(
            returncode=1,
            stderr="missing",
        )

        assert service.get_remote_url("origin") is None


class TestCheckRemote:
    """
    Tests GitService.check_remote().
    """

    def test_exists(self, service):
        service.executor.remote_get_url.return_value = CommandResult(
            returncode=0,
            stdout="git@github.com:user/repo.git",
        )

        assert service.check_remote("origin") is True

    def test_missing(self, service):
        service.executor.remote_get_url.return_value = CommandResult(
            returncode=1,
            stderr="fatal",
        )

        assert service.check_remote("origin") is False

# tests/core/git_ops/git/test_service_diff.py

from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()
    return GitService(executor=executor, config=config)


class TestGetModifiedFiles:
    """
    Tests GitService.get_modified_files().
    """

    def test_returns_files(self, service):
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=0,
            stdout="a.py\nb.py\nREADME.md\n",
        )

        result = service.get_modified_files()

        assert result == [
            "a.py",
            "b.py",
            "README.md",
        ]

        service.executor.diff_name_only.assert_called_once()

    def test_empty(self, service):
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=0,
            stdout="",
        )

        assert service.get_modified_files() == []

    def test_failure_returns_empty(self, service):
        service.executor.diff_name_only.return_value = CommandResult(
            returncode=1,
            stderr="fatal",
        )

        assert service.get_modified_files() == []

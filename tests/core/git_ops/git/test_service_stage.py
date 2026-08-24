# tests/core/git_ops/git/test_service_stage.py

"""
Tests for staging-related GitService methods.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.core.git_ops.git.service import GitService


@pytest.fixture
def service():
    executor = MagicMock()
    config = MagicMock()

    return GitService(
        executor=executor,
        config=config,
    )


class TestHasStagedFiles:
    """
    Tests has_staged_files().
    """

    def test_has_changes(self, service):
        result = MagicMock()
        result.skipped = False
        result.has_changes = True

        service.executor.diff_cached_quiet.return_value = result

        assert service.has_staged_files() is True

    def test_no_changes(self, service):
        result = MagicMock()
        result.skipped = False
        result.has_changes = False

        service.executor.diff_cached_quiet.return_value = result

        assert service.has_staged_files() is False

    def test_skipped_inspection_falls_back_to_false(self, service):
        """An unavailable staged-state result remains non-blocking."""

        result = MagicMock()
        result.skipped = True
        # result.has_changes =
        result.has_changes = True  # value doesn't matter

        service.executor.diff_cached_quiet.return_value = result

        assert service.has_staged_files() is False


class TestAutoStageAll:
    """
    Tests auto_stage_all().
    """

    def test_success(self, service):
        result = MagicMock()
        result.success = True

        service.executor.add_all.return_value = result

        service.auto_stage_all()

        service.executor.add_all.assert_called_once_with()

    def test_failure(self, service):
        result = MagicMock()
        result.success = False

        service.executor.add_all.return_value = result

        with pytest.raises(RuntimeError):
            service.auto_stage_all()


class TestAutoStageUpdate:
    """
    Tests auto_stage_update().
    """

    def test_success(self, service):
        result = MagicMock()
        result.success = True

        service.executor.add_update.return_value = result

        service.auto_stage_update()

        service.executor.add_update.assert_called_once_with()

    def test_failure(self, service):
        result = MagicMock()
        result.success = False

        service.executor.add_update.return_value = result

        with pytest.raises(RuntimeError):
            service.auto_stage_update()


class TestStageFiles:
    """
    Tests stage_files().
    """

    def test_empty_file_list(self, service):
        service.stage_files([])

        service.executor.add_files.assert_not_called()

    def test_all_missing_files(self, service, tmp_path):
        missing = tmp_path / "missing.txt"

        service.stage_files([missing])

        service.executor.add_files.assert_not_called()

    def test_success(self, service, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"

        f1.write_text("a")
        f2.write_text("b")

        result = MagicMock()
        result.success = True

        service.executor.add_files.return_value = result

        service.stage_files([f1, f2])

        service.executor.add_files.assert_called_once_with(
            [
                str(f1),
                str(f2),
            ]
        )

    def test_failure(self, service, tmp_path):
        f = tmp_path / "a.txt"
        f.write_text("hello")

        result = MagicMock()
        result.success = False

        service.executor.add_files.return_value = result

        with pytest.raises(RuntimeError):
            service.stage_files([f])


class TestListStagedFiles:
    """
    Tests list_staged_files().
    """

    def test_returns_files(self, service):
        result = MagicMock()
        result.stdout = "a.py\nb.py\n"

        service.executor.list_staged_files.return_value = result

        assert service.list_staged_files() == [
            "a.py",
            "b.py",
        ]

    def test_empty(self, service):
        result = MagicMock()
        result.stdout = ""

        service.executor.list_staged_files.return_value = result

        assert service.list_staged_files() == []

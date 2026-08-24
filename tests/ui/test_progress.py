# tests/ui/test_progress.py

"""
tests/ui/test_progress.py

Unit tests for reusable progress helpers.

These tests verify that the progress helper functions construct Rich
Progress instances with the expected configuration and correctly manage
spinner lifecycle events.
"""

from unittest.mock import MagicMock

import pytest
from rich.progress import Progress

from app.ui import progress


class DummyProgress:
    """Simple Progress replacement used for testing."""

    def __init__(self, *args, **kwargs):
        """Store constructor arguments."""

        self.args = args
        self.kwargs = kwargs

        self.add_task = MagicMock(return_value=123)
        self.update = MagicMock()

    def __enter__(self):
        """Enter the context manager."""

        return self

    def __exit__(self, exc_type, exc, tb):
        """Exit the context manager."""

        return False


class TestProgress:
    """Tests for progress helper functions."""

    # ==========================================================
    # create_progress()
    # ==========================================================

    def test_create_progress_returns_progress_instance(self):
        """Creates a configured Rich Progress instance."""

        result = progress.create_progress()

        assert isinstance(result, Progress)

    def test_create_progress_uses_shared_console(
        self,
        monkeypatch,
    ):
        """Uses the shared application console."""

        captured = {}

        def fake_progress(*args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs

            return DummyProgress(*args, **kwargs)

        monkeypatch.setattr(
            progress,
            "Progress",
            fake_progress,
        )

        progress.create_progress()

        assert captured["kwargs"]["console"] is progress.console

        # Spinner
        assert captured["args"][0].__class__.__name__ == "SpinnerColumn"

        # Description
        assert captured["args"][1].__class__.__name__ == "TextColumn"

        # Progress bar
        assert captured["args"][2].__class__.__name__ == "BarColumn"

        # Counter
        assert captured["args"][3].__class__.__name__ == "TextColumn"

        # Timer
        assert captured["args"][4].__class__.__name__ == "TimeElapsedColumn"

    # ==========================================================
    # progress_spinner()
    # ==========================================================

    def test_progress_spinner_creates_spinner(
        self,
        monkeypatch,
    ):
        """Creates a temporary spinner."""

        dummy = DummyProgress()

        monkeypatch.setattr(
            progress,
            "Progress",
            lambda *args, **kwargs: dummy,
        )

        with progress.progress_spinner(
            "Loading",
        ):
            pass

        dummy.add_task.assert_called_once_with(
            description="Loading",
            total=None,
        )

        dummy.update.assert_called_once_with(
            123,
            description="Loading ✔",
        )

    def test_progress_spinner_uses_transient_mode(
        self,
        monkeypatch,
    ):
        """Creates a transient spinner."""

        captured = {}

        def fake_progress(*args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs

            return DummyProgress(*args, **kwargs)

        monkeypatch.setattr(
            progress,
            "Progress",
            fake_progress,
        )

        with progress.progress_spinner(
            "Building",
        ):
            pass

        assert captured["kwargs"]["transient"] is True
        assert captured["kwargs"]["console"] is progress.console

    def test_progress_spinner_allows_code_execution(
        self,
        monkeypatch,
    ):
        """Executes code inside the spinner context."""

        dummy = DummyProgress()

        monkeypatch.setattr(
            progress,
            "Progress",
            lambda *args, **kwargs: dummy,
        )

        executed = False

        with progress.progress_spinner(
            "Running",
        ):
            executed = True

        assert executed is True

    def test_progress_spinner_updates_after_context_exit(
        self,
        monkeypatch,
    ):
        """Updates the spinner description after completion."""

        dummy = DummyProgress()

        monkeypatch.setattr(
            progress,
            "Progress",
            lambda *args, **kwargs: dummy,
        )

        with progress.progress_spinner(
            "Finished",
        ):
            pass

        dummy.update.assert_called_once()

        _, kwargs = dummy.update.call_args

        assert kwargs["description"] == "Finished ✔"

    # ==========================================================
    # progress_task()
    # ==========================================================

    def test_progress_task_tracks_determinate_work(
        self,
        monkeypatch,
    ):
        """Creates a determinate task and exposes update controls."""

        dummy = DummyProgress()
        dummy.advance = MagicMock()

        monkeypatch.setattr(
            progress,
            "create_progress",
            MagicMock(return_value=dummy),
        )

        with progress.progress_task(
            "Generating changelog",
            total=3,
        ) as task:
            task.update("Processing v2.0.0")
            task.advance()

        dummy.add_task.assert_called_once_with(
            description="Generating changelog",
            total=3,
        )
        dummy.advance.assert_called_once_with(123, 1)
        assert dummy.update.call_args_list[0].kwargs == {
            "description": "Processing v2.0.0",
        }
        assert dummy.update.call_args_list[-1].kwargs == {
            "completed": 3,
            "description": "Generating changelog ✔",
        }

    def test_progress_task_preserves_exceptions(
        self,
        monkeypatch,
    ):
        """Closes the progress display without hiding task failures."""

        dummy = DummyProgress()

        monkeypatch.setattr(
            progress,
            "create_progress",
            MagicMock(return_value=dummy),
        )

        with pytest.raises(RuntimeError, match="generation failed"):
            with progress.progress_task(
                "Generating changelog",
                total=1,
            ):
                raise RuntimeError("generation failed")

        dummy.update.assert_not_called()

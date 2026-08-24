# tests/core/workflow/test_workflow_push_resolve.py

"""
Unit tests for WorkflowEngine remote resolution helpers.

This module verifies:

- _resolve_main_remotes()
- _resolve_backup_remotes()
"""


import pytest

from app.core.workflow.workflow_engine import WorkflowEngine
from app.core.exceptions.validation_error import ValidationError


class TestResolveMainRemotes:
    """
    Tests _resolve_main_remotes().
    """

    def test_returns_configured_remotes(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.main_remotes = [
            "origin",
            "mirror",
        ]

        assert workflow_engine._resolve_main_remotes() == [
            "origin",
            "mirror",
        ]

    def test_uses_origin_when_confirmed(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ):
        workflow_engine.main_remotes = []

        workflow_engine.gitService.check_remote.return_value = True

        monkeypatch.setattr(
            "builtins.input",
            lambda _: "y",
        )

        assert workflow_engine._resolve_main_remotes() == [
            "origin",
        ]

    def test_raises_when_no_remote_available(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.main_remotes = []

        workflow_engine.gitService.check_remote.return_value = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine._resolve_main_remotes()

        assert exc.value.code == "MAIN_REMOTE_MISSING"


class TestResolveBackupRemotes:
    """
    Tests _resolve_backup_remotes().
    """

    def test_returns_configured_backup(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.backup_remotes = [
            "backup",
        ]

        assert workflow_engine._resolve_backup_remotes() == [
            "backup",
        ]

    def test_returns_default_backup(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ):
        workflow_engine.backup_remotes = []

        workflow_engine.gitService.check_remote.return_value = True

        monkeypatch.setattr(
            "builtins.input",
            lambda _: "yes",
        )

        assert workflow_engine._resolve_backup_remotes() == [
            "backup",
        ]

    def test_returns_empty_when_backup_missing(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.backup_remotes = []

        workflow_engine.gitService.check_remote.return_value = False

        assert workflow_engine._resolve_backup_remotes() == []

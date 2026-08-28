# tests/core/workflow/test_workflow_push_resolve.py

"""
Unit tests for WorkflowEngine remote resolution helpers.

This module verifies:

- _resolve_main_remotes()
- _resolve_backup_remotes()
"""

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.workflow.workflow_engine import WorkflowEngine


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

    def test_uses_configured_default_remote(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.main_remotes = []
        workflow_engine.default_remote = "upstream"

        assert workflow_engine._resolve_main_remotes() == [
            "upstream",
        ]

    def test_raises_when_no_remote_available(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.main_remotes = []
        workflow_engine.default_remote = ""

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

    def test_returns_empty_when_backup_missing(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.backup_remotes = []

        assert workflow_engine._resolve_backup_remotes() == []


class TestResolvePushRemoteGroups:
    """Tests complete push destination selection and precedence."""

    def test_explicit_remote_overrides_all_other_selection(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.remote = "upstream"
        workflow_engine.all_remote = True
        workflow_engine.push_to = "all"
        workflow_engine.main_remotes = ["origin"]
        workflow_engine.backup_remotes = ["backup"]

        assert workflow_engine._resolve_push_remote_groups("main") == (
            ["upstream"],
            [],
        )

    def test_main_strategy_selects_main_group(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.all_remote = False
        workflow_engine.push_to = "main"
        workflow_engine.main_remotes = ["origin", "github"]
        workflow_engine.backup_remotes = ["backup"]

        assert workflow_engine._resolve_push_remote_groups("main") == (
            ["origin", "github"],
            [],
        )

    def test_backup_strategy_selects_backup_group(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.all_remote = False
        workflow_engine.push_to = "backup"
        workflow_engine.main_remotes = ["origin"]
        workflow_engine.backup_remotes = ["backup"]

        assert workflow_engine._resolve_push_remote_groups("main") == (
            [],
            ["backup"],
        )

    def test_all_remote_selects_deduplicated_groups(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.all_remote = True
        workflow_engine.push_to = "main"
        workflow_engine.main_remotes = ["origin", "mirror"]
        workflow_engine.backup_remotes = ["mirror", "backup"]

        assert workflow_engine._resolve_push_remote_groups("main") == (
            ["origin", "mirror"],
            ["backup"],
        )

    def test_sync_backup_adds_backup_to_main_strategy(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.push_to = "main"
        workflow_engine.sync_backup = True
        workflow_engine.main_remotes = ["origin"]
        workflow_engine.backup_remotes = ["backup"]

        assert workflow_engine._resolve_push_remote_groups("main") == (
            ["origin"],
            ["backup"],
        )

    def test_non_critical_branch_skips_backup_group(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.all_remote = True
        workflow_engine.main_remotes = ["origin"]
        workflow_engine.backup_remotes = ["backup"]

        assert workflow_engine._resolve_push_remote_groups("feature/docs") == (
            ["origin"],
            [],
        )

    def test_missing_selected_backup_raises(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.push_to = "backup"
        workflow_engine.backup_remotes = []

        with pytest.raises(ValidationError) as exc:
            workflow_engine._resolve_push_remote_groups("main")

        assert exc.value.code == "BACKUP_REMOTE_MISSING"

    def test_invalid_push_target_raises(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.push_to = "custom"

        with pytest.raises(ValidationError) as exc:
            workflow_engine._resolve_push_remote_groups("main")

        assert exc.value.code == "INVALID_PUSH_TARGET"

    def test_invalid_remote_group_type_raises(
        self,
        workflow_engine: WorkflowEngine,
    ):
        workflow_engine.main_remotes = "origin"

        with pytest.raises(ValidationError) as exc:
            workflow_engine._resolve_push_remote_groups("main")

        assert exc.value.code == "INVALID_REMOTE_CONFIG"

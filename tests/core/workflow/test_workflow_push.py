# tests/core/workflow/test_workflow_push.py

"""
Unit tests for WorkflowEngine.push_changes().

This module verifies orchestration of pushing commits and tags to
configured Git remotes.

Covered behaviors include:

- Main remote resolution
- Backup remote resolution
- Non-critical branch handling
- Backup synchronization
"""

import logging
from unittest.mock import MagicMock

import pytest

from app.core.workflow.workflow_engine import WorkflowEngine

# ==========================================================
# Push Orchestration
# ==========================================================


class TestPushChanges:
    """
    Tests WorkflowEngine.push_changes().
    """

    def test_pushes_main_remote_only(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Pushes only the configured main remotes when backup
        synchronization is disabled.
        """

        workflow_engine.sync_backup = False

        workflow_engine.gitService.get_current_branch.return_value = "main"

        resolve_groups = MagicMock(return_value=(["origin"], []))
        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_push_remote_groups",
            resolve_groups,
        )

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        resolve_groups.assert_called_once_with(current_branch="main")

        push.assert_called_once_with(
            ["origin"],
            label="main",
            include_tag=True,
        )

    def test_commit_only_push_propagates_tag_exclusion(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """Commit-only orchestration must exclude tags for every remote group."""

        workflow_engine.gitService.get_current_branch.return_value = "main"
        monkeypatch.setattr(
            workflow_engine,
            "_resolve_push_remote_groups",
            MagicMock(return_value=(["origin"], ["backup"])),
        )
        push = MagicMock()
        monkeypatch.setattr(workflow_engine, "_push_to_remotes", push)

        workflow_engine.push_changes(include_tag=False)

        assert push.call_args_list == [
            ((["origin"],), {"label": "main", "include_tag": False}),
            ((["backup"],), {"label": "backup", "include_tag": False}),
        ]

    def test_pushes_main_and_backup(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """
        Pushes both main and backup remotes.
        """

        workflow_engine.sync_backup = True

        workflow_engine.gitService.get_current_branch.return_value = "main"

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_push_remote_groups",
            MagicMock(return_value=(["origin"], ["backup"])),
        )

        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        assert push.call_count == 2

    def test_container_push_explains_credential_boundary(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
        caplog,
    ) -> None:
        """Container execution explains that host credentials are isolated."""

        monkeypatch.setenv("CUSTY_CONTAINER", "1")
        workflow_engine.gitService.get_current_branch.return_value = "main"
        monkeypatch.setattr(
            workflow_engine,
            "_resolve_push_remote_groups",
            MagicMock(return_value=(["origin"], [])),
        )
        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            MagicMock(),
        )
        caplog.set_level(logging.INFO)

        workflow_engine.push_changes()

        assert "Host credential-manager sessions are not inherited" in caplog.text

    def test_dry_run_resolves_all_groups_without_pushing(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """Dry-run reports all targets without mutating any remote."""

        workflow_engine.dry_run = True
        workflow_engine.all_remote = True
        workflow_engine.main_remotes = ["origin"]
        workflow_engine.backup_remotes = ["backup"]
        workflow_engine.tag = "v2.1.0"
        workflow_engine.gitService.get_current_branch.return_value = "main"

        workflow_engine.push_changes()

        workflow_engine.gitService.push.assert_not_called()
        workflow_engine.gitService.push_tag.assert_not_called()

    @pytest.mark.parametrize(
        "branch",
        [
            "feature/login",
            "feature/api",
            "ci/build",
            "sandbox/demo",
        ],
    )
    def test_skips_backup_for_non_critical_branches(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
        branch,
    ) -> None:
        """
        Backup remotes are skipped on non-critical branches.
        """

        workflow_engine.sync_backup = True

        workflow_engine.gitService.get_current_branch.return_value = branch

        resolve_groups = MagicMock(return_value=(["origin"], []))
        monkeypatch.setattr(
            workflow_engine,
            "_resolve_push_remote_groups",
            resolve_groups,
        )

        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        resolve_groups.assert_called_once_with(current_branch=branch)
        push.assert_called_once()

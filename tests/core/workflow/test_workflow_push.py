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

        resolve_main = MagicMock(return_value=["origin"])
        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_main_remotes",
            resolve_main,
        )

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        resolve_main.assert_called_once()

        push.assert_called_once_with(
            ["origin"],
            label="main",
        )

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
            "_resolve_main_remotes",
            MagicMock(return_value=["origin"]),
        )

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_backup_remotes",
            MagicMock(return_value=["backup"]),
        )

        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        assert push.call_count == 2

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

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_main_remotes",
            MagicMock(return_value=["origin"]),
        )

        backup = MagicMock(return_value=["backup"])

        monkeypatch.setattr(
            workflow_engine,
            "_resolve_backup_remotes",
            backup,
        )

        push = MagicMock()

        monkeypatch.setattr(
            workflow_engine,
            "_push_to_remotes",
            push,
        )

        workflow_engine.push_changes()

        backup.assert_not_called()

        push.assert_called_once()

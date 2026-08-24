# tests/core/workflow/test_workflow_cleanup.py

"""
Unit tests for backup cleanup handling in WorkflowEngine.

This module verifies that WorkflowEngine delegates cleanup work to
HandleCleanupBackups with the configured target and retention count.
"""

from unittest.mock import MagicMock

from app.core.workflow.workflow_engine import WorkflowEngine


class TestCleanupBackups:
    """Tests for WorkflowEngine.cleanup_backups()."""

    def test_instantiates_cleanup_handler_and_runs_cleanup(
        self,
        workflow_engine: WorkflowEngine,
        monkeypatch,
    ) -> None:
        """Creates the cleanup handler and calls cleanup()."""

        cleanup = MagicMock()

        handler = MagicMock(return_value=MagicMock(cleanup=cleanup))

        monkeypatch.setattr(
            "app.core.workflow.workflow_engine.HandleCleanupBackups",
            handler,
        )

        workflow_engine.cleanup_backups()

        handler.assert_called_once_with(
            target=workflow_engine.cleanup_backup_type,
            keep=workflow_engine.backup_retention_count,
            dry_run=workflow_engine.dry_run,
        )
        cleanup.assert_called_once()

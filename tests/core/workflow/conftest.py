# tests/core/workflow/conftest.py

"""
Shared pytest fixtures for workflow tests.
"""

from unittest.mock import MagicMock

import pytest

from app.core.workflow.workflow_config import WorkflowConfig
from app.core.workflow.workflow_engine import WorkflowEngine


@pytest.fixture
def workflow_engine():
    """
    Create a WorkflowEngine with mocked collaborators.

    Every external dependency is replaced so each test focuses only
    on WorkflowEngine behaviour.
    """

    engine = WorkflowEngine(WorkflowConfig())

    engine.gitService = MagicMock()
    engine.commitizenHelper = MagicMock()
    engine.changelogGenerator = MagicMock()
    engine.backupManager = MagicMock()
    engine.branchWorkflowManager = MagicMock()

    return engine

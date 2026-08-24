# app/core/pipeline/context.py

"""
Pipeline Context

Shared state across all pipeline steps.

This context is passed between steps and provides access to:
- WorkflowEngine (main logic)
- GitService (git operations)
- Commitizen helper
- runtime state (tag, workflow_case, etc.)

- Thin wrapper around WorkflowEngine
- No duplication of config data
- Holds only runtime (mutable) state
- Exposes services for steps (git, cz)

This replaces the heavy reliance on self inside GitWorkflowEngine.
"""

from typing import List, Optional


class GitContext:
    """
    Shared context passed across pipeline steps.

    Holds:
    - references to tools
    - runtime state (tag, workflow case, etc.)
    - staging data

    Args:
        tool: GitWorkflowEngine instance

    Attributes:
        engine (WorkflowEngine):
            Core workflow engine (source of truth)

        git (GitService):
            Git operations service

        cz (CommitizenHelper | None):
            Commitizen helper (optional)

        # ===== Runtime State =====
        tag (Optional[str]):
            Resolved version tag

        workflow_case (Optional[str]):
            Branch workflow transition case

        files_to_stage (List[str]):
            Files to be staged before commit

    Examples:
        >>> ctx = GitContext(tool)
        >>> ctx.tag = "v1.2.3"
    """

    def __init__(self, engine):
        # =========================================================
        # 🔧 Core references
        # =========================================================
        self.engine = engine

        # New system
        self.git = engine.gitService

        # TEMP fallback (for old steps still using GitHelper)
        # self.git_legacy = engine.git

        # self.cz = engine.cz
        self.cz = getattr(engine, "cz", None)

        self.args = None

        # =========================================================
        # 📦 Runtime state
        # =========================================================
        self.tag: Optional[str] = None
        self.workflow_case: Optional[str] = None
        self.files_to_stage: List[str] = []

    # =========================================================
    # 🧰 Helpers (optional but useful)
    # =========================================================

    def set_tag(self, tag: str):
        """
        Set resolved tag.

        Usually called by:
        - prepare_version step
        """
        self.tag = tag

    def add_files(self, files: List[str]):
        """
        Add files to staging list.
        """
        self.files_to_stage.extend(files)

    def clear_files(self):
        """
        Reset staging list.
        """
        self.files_to_stage = []

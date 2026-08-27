# app/core/git_ops/git/result.py

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CommandResult:
    """
    Low-level command execution result.

    Used by GitCommandExecutor to wrap subprocess results safely.
    """

    returncode: int
    stdout: str = ""
    stderr: str = ""
    skipped: bool = False  # True when a mutation is simulated in dry-run mode

    @property
    def success(self) -> bool:
        """Return True if the command succeeded or was safely simulated."""
        return self.returncode == 0

    @property
    def has_changes(self) -> bool:
        """
        Used for commands like:
            git diff --quiet

        Returns:
            bool:
                True  → changes exist (returncode != 0)
                False → no changes
        """
        return self.returncode != 0

    @classmethod
    def from_completed(cls, result) -> CommandResult:
        """Create from subprocess.CompletedProcess."""
        return cls(
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
        )

    @classmethod
    def dry_run(cls) -> CommandResult:
        """Return a result representing a simulated mutation."""
        return cls(returncode=0, skipped=True)


# ================================
# High-level workflow result
# ================================


@dataclass
class OperationResult:
    """
    High-level result for workflow operations.

    Used by WorkflowManager and services.
    """

    success: bool
    message: str = ""
    data: Optional[Any] = None

    @classmethod
    def ok(cls, message: str = "", data: Any = None) -> OperationResult:
        return cls(True, message, data)

    @classmethod
    def fail(cls, message: str = "", data: Any = None) -> OperationResult:
        return cls(False, message, data)

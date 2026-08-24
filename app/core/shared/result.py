# app/core/shared/result.py

"""
Shared command execution result models.

This module contains result objects used by low-level executors.

The goal is to provide a consistent return type for:
- GitExecutor
- GitHubExecutor
- DockerExecutor

Instead of exposing subprocess.CompletedProcess directly,
executors return CommandResult objects.

This makes services easier to test and keeps implementation
details hidden from higher layers.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CommandResult:
    """
    Result of a command execution.

    This class wraps the result returned by subprocess commands
    and provides helper properties for common checks.

    Attributes:
        returncode (int):
            Command exit code.

        stdout (str):
            Standard output from the command.

        stderr (str):
            Standard error output from the command.

        skipped (bool):
            True when command execution was skipped
            (for example during dry-run mode).
    """

    returncode: int
    stdout: str = ""
    stderr: str = ""
    skipped: bool = False

    @property
    def success(self) -> bool:
        """
        Check whether the command completed successfully.

        Returns:
            bool:
                True if return code is 0.
        """
        return self.returncode == 0

    @property
    def failed(self) -> bool:
        """
        Check whether the command failed.

        Returns:
            bool:
                True if return code is not 0.
        """
        return not self.success

    @classmethod
    def from_completed_process(cls, result) -> "CommandResult":
        """
        Create a CommandResult from a subprocess result.

        Args:
            result:
                subprocess.CompletedProcess instance.

        Returns:
            CommandResult:
                Normalized command result.
        """
        return cls(
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
        )

    @classmethod
    def dry_run(cls) -> "CommandResult":
        """
        Create a dry-run result.

        Returns:
            CommandResult:
                Successful skipped result.
        """
        return cls(
            returncode=0,
            stdout="",
            stderr="",
            skipped=True,
        )

# tests/core/workflow/test_workflow_commit_errors.py

"""
Unit tests for commit creation error handling in WorkflowEngine.

This module verifies validation, error handling, and special execution
paths during commit creation.

Covered behaviors include:

- Missing commit message validation
- Missing staged changes
- Force commit
- Dry-run execution
- Git service failures
- Inline commit message precedence
"""

from pathlib import Path

import pytest

from app.core.exceptions.validation_error import ValidationError
from app.core.git_ops.git.result import CommandResult
from app.core.git_ops.hooks import GitHookPlan, HookExecution
from app.core.shared import GitOperationError
from app.core.workflow.workflow_engine import WorkflowEngine

# ==========================================================
# Commit Message Validation
# ==========================================================


class TestCreateCommitValidation:
    """
    Tests validation performed before creating a commit.
    """

    def test_raises_when_no_commit_message_source(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Raises ValidationError when neither an inline commit message
        nor a commit message file is provided.
        """

        workflow_engine.commit_message_input = None
        workflow_engine.commit_message_file = None

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_commit()

        assert exc.value.code == "COMMIT_MESSAGE_MISSING"

        workflow_engine.gitService.commit.assert_not_called()


# ==========================================================
# Staging Validation
# ==========================================================


class TestCreateCommitStaging:
    """
    Tests staged-file validation before creating commits.
    """

    def test_raises_when_no_staged_files(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """
        Raises ValidationError when no staged files exist and
        force_commit is disabled.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat: test")

        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = False
        workflow_engine.force_commit = False

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_commit()

        assert exc.value.code == "NO_STAGED_CHANGES"

        workflow_engine.gitService.commit.assert_not_called()


# ==========================================================
# Force Commit
# ==========================================================


class TestForceCommit:
    """
    Tests the force-commit workflow.
    """

    def test_force_commit_allows_empty_commit(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """
        Allows commit creation without staged files when
        force_commit is enabled.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat: test")

        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = False
        workflow_engine.force_commit = True

        workflow_engine.create_commit()

        workflow_engine.gitService.commit.assert_called_once()


# ==========================================================
# Dry Run
# ==========================================================


class TestDryRunCommit:
    """
    Tests dry-run behavior during commit creation.
    """

    def test_dry_run_does_not_execute_git_commit(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """
        Does not invoke GitService.commit() during a dry run.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat: test")

        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.dry_run = True

        workflow_engine.create_commit()

        workflow_engine.gitService.commit.assert_not_called()


# ==========================================================
# Commit Failure Handling
# ==========================================================


class TestCommitFailure:
    """
    Tests exception handling during commit creation.
    """

    def test_wraps_git_exception(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """
        Converts unexpected GitService errors into ValidationError.
        """

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("feat: test")

        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = True

        workflow_engine.gitService.commit.side_effect = RuntimeError("boom")

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_commit()

        assert exc.value.code == "COMMIT_FAILED"

    def test_surfaces_repository_hook_diagnostics(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """Classifies a mounted cross-platform hook failure without hiding it."""

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("fix: test\n", encoding="utf-8")
        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.gitService.commit.side_effect = GitOperationError(
            "Git commit failed",
            operation="commit",
            returncode=2,
            stderr=".git/hooks/pre-commit: Syntax error: '(' unexpected",
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_commit()

        assert exc.value.code == "GIT_HOOK_FAILED"
        assert "Syntax error" in exc.value.context["detail"]


class TestManagedPreCommitHooks:
    """Verify safe direct hook execution before the final Git commit."""

    def test_success_uses_no_verify_only_after_direct_hooks_pass(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """A verified pre-commit plan bypasses only its broken wrapper."""

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("fix: portable hook\n")
        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.commit_hook_plan = GitHookPlan(
            execution=HookExecution.PRE_COMMIT,
            stages=("pre-commit",),
        )
        workflow_engine.gitHookService.run.return_value = CommandResult(returncode=0)

        workflow_engine.create_commit()

        workflow_engine.gitHookService.run.assert_called_once_with(
            workflow_engine.commit_hook_plan,
            message_file=commit_file,
        )
        workflow_engine.gitService.commit.assert_called_once_with(
            message=None,
            message_file=str(commit_file),
            no_verify=True,
        )

    def test_failed_direct_hook_prevents_git_commit(
        self,
        workflow_engine: WorkflowEngine,
        tmp_path: Path,
    ) -> None:
        """A failing pre-commit check never reaches ``git commit``."""

        commit_file = tmp_path / "commit.txt"
        commit_file.write_text("fix: rejected\n")
        workflow_engine.commit_message_file = commit_file
        workflow_engine.gitService.has_staged_files.return_value = True
        workflow_engine.commit_hook_plan = GitHookPlan(
            execution=HookExecution.PRE_COMMIT,
            stages=("pre-commit",),
        )
        workflow_engine.gitHookService.run.return_value = CommandResult(
            returncode=1,
            stdout="end-of-file-fixer failed",
        )

        with pytest.raises(ValidationError) as exc:
            workflow_engine.create_commit()

        assert exc.value.code == "PRE_COMMIT_HOOK_FAILED"
        workflow_engine.gitService.commit.assert_not_called()


# ==========================================================
# Commit Message Resolution
# ==========================================================


class TestCommitMessageResolution:
    """
    Tests commit message selection priority.
    """

    def test_prefers_inline_message(
        self,
        workflow_engine: WorkflowEngine,
    ) -> None:
        """
        Prefers an inline commit message over a commit message file.
        """

        workflow_engine.commit_message_input = "feat: inline"
        workflow_engine.commit_message_file = Path("ignored.txt")

        workflow_engine.gitService.has_staged_files.return_value = True

        workflow_engine.create_commit()

        workflow_engine.gitService.commit.assert_called_once_with(
            message="feat: inline",
            message_file=None,
            no_verify=False,
        )

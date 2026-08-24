# tests/core/branch_workflow/test_branch_workflow_manager.py

"""
Tests for BranchWorkflowManager.

This module covers:

- initialization
- helper selection
- helper delegation
- internal version validation helpers

Target:
    app/core/branch_workflow/branch_workflow_manager.py
"""

from unittest.mock import MagicMock, patch

import pytest

from app.core.branch_workflow.branch_workflow_manager import (
    BranchWorkflowManager,
)


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def git_mock():
    git = MagicMock()
    git.get_current_branch.return_value = "develop"
    git.get_latest_tag.return_value = "v1.2.3.dev1"
    return git


@pytest.fixture
def pep_helper():
    helper = MagicMock()
    helper.suggest_tag.return_value = "v1.2.3.dev2"
    return helper


@pytest.fixture
def semver_helper():
    helper = MagicMock()
    helper.suggest_tag.return_value = "v1.2.4"
    return helper


# ============================================================
# Initialization
# ============================================================


class TestInitialization:
    """
    Tests constructor behaviour.
    """

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_uses_pep440_helper(
        self,
        create_git,
        pep_cls,
        detect_strategy,
        git_mock,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        BranchWorkflowManager(
            dry_run=True,
            no_debug=True,
            sync_backup=True,
        )

        pep_cls.assert_called_once_with("v1.2.3.dev1")

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.SemverVersionHelper"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_uses_semver_helper(
        self,
        create_git,
        semver_cls,
        detect_strategy,
        git_mock,
    ):
        detect_strategy.return_value = "semver"
        create_git.return_value = git_mock

        BranchWorkflowManager()

        semver_cls.assert_called_once_with("v1.2.3.dev1")

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_git_service_created(
        self,
        create_git,
        detect_strategy,
        git_mock,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        BranchWorkflowManager(
            dry_run=True,
            no_debug=False,
        )

        create_git.assert_called_once_with(
            dry_run=True,
            no_debug=False,
        )

    # @patch(
    #     "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    # )
    # @patch(
    #     "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    # )
    # def test_runner_silent_called(
    #     self,
    #     create_git,
    #     detect_strategy,
    #     git_mock,
    # ):
    #     detect_strategy.return_value = "pep440"
    #     create_git.return_value = git_mock

    #     mgr = BranchWorkflowManager(no_debug=True)

    #     mgr.runner.set_silent.assert_called_once_with(True)


    # @patch(
    #     "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    # )
    # @patch(
    #     "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    # )
    # @patch(
    #     "app.core.dry_run.dry_run.DryRun.runner",
    #     new_callable=MagicMock,
    # )
    # def test_runner_silent_called(
    #     self,
    #     runner,
    #     create_git,
    #     detect_strategy,
    #     git_mock,
    # ):
    #     detect_strategy.return_value = "pep440"
    #     create_git.return_value = git_mock

    #     BranchWorkflowManager(no_debug=True)

    #     runner.set_silent.assert_called_once_with(True)


# ============================================================
# suggest_tag_for_current_branch
# ============================================================


class TestSuggestTag:
    """
    Tests tag suggestion delegation.
    """

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_calls_helper(
        self,
        create_git,
        helper_cls,
        detect_strategy,
        git_mock,
        pep_helper,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock
        helper_cls.return_value = pep_helper

        mgr = BranchWorkflowManager()

        result = mgr.suggest_tag_for_current_branch()

        assert result == "v1.2.3.dev2"

        pep_helper.suggest_tag.assert_called_once_with(
            "develop"
        )


# ============================================================
# _check_pep440_pre
# ============================================================


class TestCheckPep440Pre:
    """
    Tests pre-release detection.
    """

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_valid_pre_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v1.2.3.dev1"

        mgr._check_pep440_pre(
            "dev",
            "alpha",
            "beta",
        )

        out = capsys.readouterr().out

        assert "matches allowed pre-release tiers" in out

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_invalid_pre_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v1.2.3"

        mgr._check_pep440_pre("rc")

        out = capsys.readouterr().out

        assert "does NOT match expected pre-release tier" in out


# ============================================================
# _check_final_release
# ============================================================


class TestCheckFinalRelease:
    """
    Tests stable release detection.
    """

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_valid_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v2.0.0"

        mgr._check_final_release()

        out = capsys.readouterr().out

        assert "valid stable release" in out

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_invalid_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v2.0.0rc1"

        mgr._check_final_release()

        out = capsys.readouterr().out

        assert "must not include pre/post/dev suffix" in out


# ============================================================
# _check_post_release
# ============================================================


class TestCheckPostRelease:
    """
    Tests post-release validation.
    """

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_valid_post_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v2.0.0.post1"

        mgr._check_post_release()

        out = capsys.readouterr().out

        assert "includes '.post'" in out

    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_invalid_post_release(
        self,
        create_git,
        detect_strategy,
        git_mock,
        capsys,
    ):
        detect_strategy.return_value = "pep440"
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        mgr.tag = "v2.0.0"

        mgr._check_post_release()

        out = capsys.readouterr().out

        assert "Post-release tag expected" in out


##### Part 2

# ============================================================
# enforce_consistency
# ============================================================


class TestEnforceConsistency:
    """
    Tests branch routing performed by enforce_consistency().
    """

    @pytest.mark.parametrize(
        ("branch", "expected_method"),
        [
            ("develop", "_check_pep440_pre"),
            ("release/1.2", "_check_pep440_pre"),
            ("main", "_check_final_release"),
            ("hotfix/1.2.1", "_check_post_release"),
        ],
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_dispatches_to_validation_methods(
        self,
        create_git,
        detect_strategy,
        git_mock,
        branch,
        expected_method,
    ):
        detect_strategy.return_value = "pep440"

        git_mock.get_current_branch.return_value = branch
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        with (
            patch.object(mgr, "_check_pep440_pre") as pre,
            patch.object(mgr, "_check_final_release") as final,
            patch.object(mgr, "_check_post_release") as post,
        ):
            mgr.enforce_consistency()

            if expected_method == "_check_pep440_pre":
                pre.assert_called_once()
                final.assert_not_called()
                post.assert_not_called()

            elif expected_method == "_check_final_release":
                final.assert_called_once()
                pre.assert_not_called()
                post.assert_not_called()

            else:
                post.assert_called_once()
                pre.assert_not_called()
                final.assert_not_called()


    @pytest.mark.parametrize(
        "branch",
        [
            "feature/my-feature",
            "ci/github-actions",
            "archive/old-release",
            "unknown",
        ],
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
    )
    @patch(
        "app.core.branch_workflow.branch_workflow_manager.create_git_service"
    )
    def test_non_validating_branches(
        self,
        create_git,
        detect_strategy,
        git_mock,
        branch,
    ):
        """
        Branches that should not invoke validation helpers.
        """

        detect_strategy.return_value = "pep440"

        git_mock.get_current_branch.return_value = branch
        create_git.return_value = git_mock

        mgr = BranchWorkflowManager()

        with (
            patch.object(mgr, "_check_pep440_pre") as pre,
            patch.object(mgr, "_check_final_release") as final,
            patch.object(mgr, "_check_post_release") as post,
        ):
            mgr.enforce_consistency()

            pre.assert_not_called()
            final.assert_not_called()
            post.assert_not_called()

##### Part 3

# ============================================================
# check_transition
# ============================================================

@pytest.fixture
def manager():
    with (
        patch(
            "app.core.branch_workflow.branch_workflow_manager.create_git_service"
        ) as create_git,
        patch(
            "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
        ) as detect,
        patch(
            "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
        ) as helper_cls,
    ):
        git = MagicMock()
        git.get_current_branch.return_value = "develop"
        git.get_latest_tag.return_value = "v1.0.0.dev1"

        helper = MagicMock()

        helper.classify.side_effect = lambda tag: {
            "1.0.0.dev1": "dev",
            "1.0.0a1": "alpha",
            "1.0.0rc1": "rc",
            "1.0.0": "release",
        }[tag]

        helper.tier_order.return_value = {
            "dev": 0,
            "alpha": 1,
            "beta": 2,
            "rc": 3,
            "release": 4,
        }

        helper.get_transaction_cases.return_value = {
            ("develop", "dev", "release", "rc"): "CASE 2",
        }

        helper_cls.return_value = helper

        detect.return_value = "pep440"
        create_git.return_value = git

        yield BranchWorkflowManager()


class TestCheckTransition:

    def test_returns_matching_case(
        self,
        manager,
    ):
        """
        CASE lookup
        """
        result = manager.check_transition(
            from_branch="develop",
            from_tag="v1.0.0.dev1",
            to_branch="release/1.0",
            to_tag="v1.0.0rc1",
        )

        assert result == "CASE 2"

    def test_same_branch_same_tier_returns_empty(
        self,
        manager,
    ):
        """
        Stable iteration
        """
        result = manager.check_transition(
            from_branch="develop",
            from_tag="v1.0.0.dev1",
            to_branch="develop",
            to_tag="v1.0.0.dev1",
        )

        assert result == ""

    def test_same_branch_tier_promotion(
        self,
        manager,
    ):
        """
        Tier promotion
        """
        result = manager.check_transition(
            from_branch="develop",
            from_tag="v1.0.0.dev1",
            to_branch="develop",
            to_tag="v1.0.0a1",
        )

        assert result == ""

    def test_invalid_transition_returns_empty(
        self,
        manager,
    ):
        """
        Invalid transition
        """
        result = manager.check_transition(
            from_branch="main",
            from_tag="v1.0.0",
            to_branch="feature/test",
            to_tag="v1.0.0.dev1",
        )

        assert result == ""

    def test_auto_detects_current_branch_and_tag(
        self,
        manager,
    ):
        """
        Auto detection
        """
        manager.check_transition()

        manager.git.get_current_branch.assert_called()
        manager.git.get_latest_tag.assert_called()


# ============================================================
# run_initial_workflow
# ============================================================


class TestRunInitialWorkflow:
    """
    Tests initial workflow execution for each CASE.
    """

    @pytest.fixture
    def manager(self):
        with (
            patch(
                "app.core.branch_workflow.branch_workflow_manager.create_git_service"
            ) as create_git,
            patch(
                "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
            ) as detect,
            patch(
                "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
            ) as helper_cls,
        ):
            git = MagicMock()
            git.get_current_branch.return_value = "develop"
            git.get_latest_tag.return_value = "v1.2.0.dev1"

            helper = MagicMock()
            helper.major = 1
            helper.minor = 2
            helper.patch = 3

            helper_cls.return_value = helper
            detect.return_value = "pep440"
            create_git.return_value = git

            mgr = BranchWorkflowManager()

            mgr.runner.run = MagicMock()
            mgr._ensure_no_staged_changes = MagicMock()

            yield mgr


    def test_case1(self, manager):
        manager.run_initial_workflow("CASE 1", "v1.2.0")

        manager.runner.run.assert_any_call(
            ["git", "checkout", "develop"],
            check=True,
        )

        manager.runner.run.assert_any_call(
            ["git", "pull", "origin", "develop"],
            check=True,
        )


    def test_case2(self, manager):
        manager.run_initial_workflow("CASE 2", "v1.2.0rc1")

        manager.runner.run.assert_called_once_with(
            ["git", "checkout", "-b", "release/1.2"],
            check=True,
        )


    def test_case3(self, manager):
        manager.run_initial_workflow("CASE 3", "v1.2.0")

        manager._ensure_no_staged_changes.assert_called_once()

        manager.runner.run.assert_any_call(
            ["git", "checkout", "main"],
            check=True,
        )

        manager.runner.run.assert_any_call(
            ["git", "merge", "release/1.2"],
            check=True,
        )


    def test_case4(self, manager):
        manager.run_initial_workflow("CASE 4", "v1.2.0")

        manager.runner.run.assert_any_call(
            ["git", "checkout", "develop"],
            check=True,
        )


    def test_case5(self, manager):
        manager.run_initial_workflow("CASE 5", "v1.2.1.post1")

        manager.runner.run.assert_any_call(
            ["git", "checkout", "-b", "hotfix/1.2.3"],
            check=True,
        )


    def test_case6(self, manager):
        manager.runner.run.reset_mock()

        manager.run_initial_workflow("CASE 6", "v1.2.1")

        manager.runner.run.assert_not_called()


    def test_case7(self, manager):
        manager.branch = "feature/login"

        manager.run_initial_workflow("CASE 7", "v1.2.0")

        manager.runner.run.assert_any_call(
            ["git", "merge", "feature/login"],
            check=True,
        )


    def test_case8(self, manager):
        manager.runner.run.reset_mock()

        manager.run_initial_workflow("CASE 8", "v1.2.0")

        manager.runner.run.assert_not_called()


    def test_case9(self, manager):
        manager.branch = "ci/actions"

        manager.run_initial_workflow("CASE 9", "v1.2.0")

        manager.runner.run.assert_any_call(
            ["git", "merge", "ci/actions"],
            check=True,
        )


# ============================================================
# run_final_workflow
# ============================================================


class TestRunFinalWorkflow:
    """
    Tests post-release workflow execution.
    """

    @pytest.fixture
    def manager(self):
        with (
            patch(
                "app.core.branch_workflow.branch_workflow_manager.create_git_service"
            ) as create_git,
            patch(
                "app.core.branch_workflow.branch_workflow_manager.detect_project_strategy"
            ) as detect,
            patch(
                "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
            ) as helper_cls,
        ):
            git = MagicMock()
            git.get_current_branch.return_value = "develop"
            git.get_latest_tag.return_value = "v1.2.0"

            helper = MagicMock()
            helper.major = 1
            helper.minor = 2
            helper.patch = 3

            helper_cls.return_value = helper
            detect.return_value = "pep440"
            create_git.return_value = git

            mgr = BranchWorkflowManager(sync_backup=True)

            mgr.runner.run = MagicMock()
            mgr.cleanup_release_branch = MagicMock()
            mgr.cleanup_hotfix_branch = MagicMock()
            mgr._ensure_no_staged_changes = MagicMock()

            yield mgr


    @pytest.mark.parametrize(
        "case",
        [
            "CASE 1",
            "CASE 2",
            "CASE 4",
            "CASE 5",
            "CASE 7",
            "CASE 8",
        ],
    )
    def test_informational_cases(
        self,
        manager,
        case,
    ):
        assert manager.run_final_workflow(case, "v1.2.0") is False


    def test_case3(self, manager):
        manager.git.branch_exists.return_value = True

        assert manager.run_final_workflow("CASE 3", "v1.2.0") is True

        manager.cleanup_release_branch.assert_called_once()


    def test_case6(self, manager):
        assert manager.run_final_workflow("CASE 6", "v1.2.1") is True

        manager._ensure_no_staged_changes.assert_called_once()


    def test_case9(self, manager):
        manager.branch = "ci/actions"

        assert manager.run_final_workflow("CASE 9", "v1.2.0") is True

        manager.runner.run.assert_any_call(
            ["git", "merge", "ci/actions"],
            check=True,
        )


class TestStagedChangeGuard:
    """Tests staged-change safety behavior for branch mutations."""

    @pytest.fixture
    def manager(self):
        with (
            patch(
                "app.core.branch_workflow.branch_workflow_manager.create_git_service"
            ) as create_git,
            patch(
                "app.core.branch_workflow.branch_workflow_manager."
                "detect_project_strategy"
            ) as detect,
            patch(
                "app.core.branch_workflow.branch_workflow_manager.PEP440VersionHelper"
            ),
        ):
            git = MagicMock()
            git.get_current_branch.return_value = "develop"
            git.get_latest_tag.return_value = "v1.2.0.dev1"
            git.has_staged_files.return_value = True

            create_git.return_value = git
            detect.return_value = "pep440"

            yield BranchWorkflowManager(dry_run=True)

    def test_dry_run_reports_guard_without_terminating(self, manager, capsys):
        manager._ensure_no_staged_changes(context="merge")

        manager.git.has_staged_files.assert_called_once_with()
        assert "real execution would stop here" in capsys.readouterr().out

    def test_real_execution_terminates_when_changes_are_staged(self, manager):
        """A real branch mutation retains the clean-index safety guard."""

        manager.runner.set_is_dry_run(False)

        with pytest.raises(SystemExit) as error:
            manager._ensure_no_staged_changes(context="merge")

        assert error.value.code == 1

    def test_clean_index_returns_without_warning(self, manager, capsys):
        """A clean index allows the workflow to continue normally."""

        manager.git.has_staged_files.return_value = False

        manager._ensure_no_staged_changes(context="merge")

        assert capsys.readouterr().out == ""

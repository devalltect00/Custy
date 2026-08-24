# tests/regression/test_command_resolver_regressions.py

"""
tests/regression/test_command_resolver_regressions.py

Regression tests for CommandResolver.

These tests protect recursive profile resolution,
deduplication, and ordering.
"""

import pytest

from app.core.pipeline.command_resolver import CommandResolver


class TestCommandResolverRegressions:
    """
    Regression tests for CommandResolver.
    """

    def test_validate_profile_contains_expected_steps(self):
        """
        Regression:
        The validate profile should always resolve to the
        expected validation steps.
        """
        resolver = CommandResolver()

        steps = resolver.resolve(["validate"])

        names = [step["name"] for step in steps]

        assert "ensure_git_repo_step" in names
        assert "ensure_remote_exists_step" in names
        assert "ensure_version_file_step" in names
        assert "ensure_staged_changes_step" in names
        assert "ensure_commitizen_convention_step" in names
        assert "ensure_commit_message_file_step" in names
        assert "ensure_commit_message_file_exists_step" in names
        assert "ensure_tag_message_file_step" in names
        assert "ensure_tag_message_file_exists_step" in names

    def test_release_profile_expands_sub_profiles(self):
        """
        Regression:
        Nested profiles must always expand correctly.
        """
        resolver = CommandResolver()

        steps = resolver.resolve(["release"])

        names = [step["name"] for step in steps]

        assert "ensure_git_repo_step" in names
        assert "prepare_version_step" in names
        assert "workflow_init_step" in names
        assert "commit_step" in names
        assert "tag_step" in names
        assert "push_step" in names

    def test_duplicate_steps_are_removed(self):
        """
        Regression:
        Duplicate steps should never appear after profile expansion.
        """
        resolver = CommandResolver()

        steps = resolver.resolve(
            [
                "validate",
                "release",
            ]
        )

        names = [step["name"] for step in steps]

        assert len(names) == len(set(names))

    def test_step_order_is_stable(self):
        """
        Regression:
        Step ordering must remain deterministic.
        """
        resolver = CommandResolver()

        steps = resolver.resolve(["release"])

        names = [step["name"] for step in steps]

        assert names.index("ensure_git_repo_step") < names.index(
            "prepare_version_step"
        )

        assert names.index("prepare_version_step") < names.index(
            "workflow_init_step"
        )

        assert names.index("workflow_init_step") < names.index(
            "commit_step"
        )

        assert names.index("commit_step") < names.index(
            "tag_step"
        )

        assert names.index("tag_step") < names.index(
            "push_step"
        )

    def test_unknown_profile_raises_error(self):
        """
        Regression:
        Unknown commands should raise ValueError.
        """
        resolver = CommandResolver()

        with pytest.raises(
            ValueError,
            match="Unknown command: does_not_exist",
        ):
            resolver.resolve(["does_not_exist"])

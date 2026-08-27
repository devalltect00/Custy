# tests/core/pipeline/test_command_resolver.py

"""
tests/workflow/test_command_resolver.py

Unit tests for CommandResolver.
"""

import pytest

from app.core.pipeline.command_resolver import CommandResolver


class TestCommandResolver:
    def test_no_command_raises(self):
        resolver = CommandResolver()

        with pytest.raises(ValueError):
            resolver.resolve([])

    def test_unknown_command_raises(self):
        resolver = CommandResolver()

        with pytest.raises(ValueError):
            resolver.resolve(["unknown"])

    def test_single_profile(self):
        resolver = CommandResolver()

        steps = resolver.resolve(["commit"])

        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_release_profile(self):
        resolver = CommandResolver()

        steps = resolver.resolve(["release"])

        names = [s["name"] for s in steps]

        assert "commit_step" in names
        assert "tag_step" in names
        assert "push_step" in names

    def test_merge_profiles(self):
        resolver = CommandResolver()

        steps = resolver.resolve(["commit", "push"])

        names = [s["name"] for s in steps]

        assert "commit_step" in names
        assert "push_step" in names

    def test_deduplicate(self):
        resolver = CommandResolver()

        data = [
            {"name": "a"},
            {"name": "b"},
            {"name": "a"},
            {"name": "c"},
            {"name": "b"},
        ]

        result = resolver._deduplicate(data)

        assert result == [
            {"name": "a"},
            {"name": "b"},
            {"name": "c"},
        ]

    def test_order_and_deduplicate(self):
        resolver = CommandResolver()

        data = [
            {"name": "commit_step"},
            {"name": "ensure_git_repo_step"},
            {"name": "commit_step"},
            {"name": "push_step"},
        ]

        result = resolver._order_and_deduplicate(data)

        names = [x["name"] for x in result]

        assert names == [
            "ensure_git_repo_step",
            "commit_step",
            "push_step",
        ]

    def test_expand_profile(self):
        resolver = CommandResolver()

        expanded = resolver._expand_profile(resolver.profiles["validate"])

        assert len(expanded) > 0

    def test_expand_nested_profile(self):
        resolver = CommandResolver()

        expanded = resolver._expand_profile(resolver.profiles["release"])

        names = [s["name"] for s in expanded]

        assert "ensure_git_repo_step" in names
        assert "prepare_version_step" in names
        assert "commit_step" in names
        assert "tag_step" in names
        assert "push_step" in names

    def test_circular_profile_detection(self):
        resolver = CommandResolver()

        resolver.profiles["loop_a"] = [
            {"name": "loop_b"},
        ]

        resolver.profiles["loop_b"] = [
            {"name": "loop_a"},
        ]

        with pytest.raises(ValueError):
            resolver.resolve(["loop_a"])

        resolver.profiles.pop("loop_a")
        resolver.profiles.pop("loop_b")

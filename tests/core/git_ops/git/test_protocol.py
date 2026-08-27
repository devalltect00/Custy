# tests/core/git_ops/git/test_protocol.py

"""
Tests for app.core.git_ops.git.protocol.

Coverage target:
    100%
"""

from typing import Protocol

from app.core.git_ops.git.protocol import IGitCommandExecutor


class TestIGitCommandExecutor:
    """
    Tests for IGitCommandExecutor protocol.
    """

    def test_protocol_is_protocol(self):
        """
        Ensure the interface is a typing.Protocol.
        """

        assert issubclass(IGitCommandExecutor, Protocol)

    def test_core_methods_exist(self):
        """
        Core Git methods are defined.
        """

        methods = [
            "diff_cached_quiet",
            "add_all",
            "add_update",
            "add_files",
            "list_staged_files",
            "rev_parse_inside_work_tree",
            "rev_parse_head",
            "current_branch",
            "symbolic_head",
            "branch_exists",
        ]

        for method in methods:
            assert hasattr(IGitCommandExecutor, method)

    def test_remote_methods_exist(self):
        """
        Remote operations are defined.
        """

        assert hasattr(IGitCommandExecutor, "remote_get_url")
        assert hasattr(IGitCommandExecutor, "push")
        assert hasattr(IGitCommandExecutor, "push_tag")

    def test_commit_methods_exist(self):
        """
        Commit/tag operations are defined.
        """

        assert hasattr(IGitCommandExecutor, "commit")
        assert hasattr(IGitCommandExecutor, "tag")

    def test_log_methods_exist(self):
        """
        Log inspection methods are defined.
        """

        methods = [
            "log_between",
            "show_commit",
            "get_commits_between_tags",
            "get_commit_count",
            "get_tag_date",
            "get_all_tags",
            "get_tags",
            "describe_latest_tag",
            "diff_name_only",
        ]

        for method in methods:
            assert hasattr(IGitCommandExecutor, method)

    def test_property_methods_exist(self):
        """
        Runtime configuration methods are defined.
        """

        assert hasattr(IGitCommandExecutor, "get_silent")
        assert hasattr(IGitCommandExecutor, "set_silent")
        assert hasattr(IGitCommandExecutor, "get_is_dry_run")
        assert hasattr(IGitCommandExecutor, "set_is_dry_run")

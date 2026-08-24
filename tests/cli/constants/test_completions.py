# tests/cli/constants/test_completions.py

"""
tests/cli/constants/test_completions.py

Constant-level tests for completion helper exports.
"""

from app.cli.constants import completions


EXPECTED = {
    "completion_initialization_mode",
    "completion_commit_message_file",
    "completion_tag_message_file",
    "completion_version_file",
    "completion_commit_message_backup_dir",
    "completion_tag_message_backup_dir",
    "completion_tag",
    "completion_tag_message",
    "completion_meta",
    "completion_remote_name",
    "completion_steps",
}


class TestCompletionExports:

    def test_expected_functions_exist(self):
        for name in EXPECTED:
            assert hasattr(completions, name)

    def test_all_completion_functions_return_lists(self):
        for name in EXPECTED:
            fn = getattr(completions, name)
            result = fn()
            assert isinstance(result, list)

    def test_completion_lists_are_not_empty(self):
        for name in EXPECTED:
            fn = getattr(completions, name)
            assert len(fn()) > 0

    def test_step_completion_contains_common_steps(self):
        values = completions.completion_steps()
        assert "commit" in values
        assert "tag" in values
        assert "push" in values

    def test_remote_completion_contains_origin(self):
        assert "origin" in completions.completion_remote_name()

# tests/cli/utils/test_completion.py

"""
tests/cli/utils/test_completion.py

Unit tests for CLI completion helpers.
"""

from app.cli.constants import completions


class TestCompletions:
    def test_initialization_modes(self):
        values = completions.completion_initialization_mode()
        assert "all" in values
        assert "config" in values

    def test_commit_message_completion(self):
        values = completions.completion_commit_message_file()
        assert values == ["templates/custy/commit-message.txt"]

    def test_tag_message_file_completion(self):
        values = completions.completion_tag_message_file()
        assert values == ["templates/custy/tag-message.txt"]

    def test_version_file_completion(self):
        values = completions.completion_version_file()
        assert "app/__version__.py" in values
        assert "src/__version__.py" in values

    def test_backup_dirs(self):
        assert completions.completion_commit_message_backup_dir()
        assert completions.completion_tag_message_backup_dir()

    def test_tag_completion(self):
        values = completions.completion_tag()
        assert "v1.0.0" in values
        assert "1.0.0" in values

    def test_tag_message_completion(self):
        values = completions.completion_tag_message()
        assert any("Release" in v for v in values)

    def test_meta_completion(self):
        assert completions.completion_meta() == ["sha.abc123"]

    def test_remote_completion(self):
        values = completions.completion_remote_name()
        assert "origin" in values
        assert "backup" in values

    def test_steps_completion(self):
        values = completions.completion_steps()
        assert {"commit", "tag", "push"}.issubset(set(values))

# tests/constants/test_path.py

"""
tests/constants/test_path.py

Unit tests for path constants.
"""

from pathlib import Path

from app.constants import path


class TestPathConstants:

    def test_project_source(self):
        assert path.THIS_PROJECT_SOURCE == "app"

    def test_settings_path(self):
        assert path.CUSTY_SETTINGS == Path(".config/custy/config.toml")

    def test_template_paths(self):
        assert path.CUSTY_COMMIT_MESSAGE_TEMPLATE.name == "commit-message.txt"
        assert path.CUSTY_TAG_MESSAGE_TEMPLATE.name == "tag-message.txt"
        assert path.CUSTY_CHANGELOG_J2.name == "changelog.j2"

    def test_backup_directories(self):
        assert path.CUSTY_BACKUP_COMMIT_DIR.name == "commit"
        assert path.CUSTY_BACKUP_TAG_DIR.name == "tag"

    def test_changelog_path(self):
        assert path.CHANGELOG_PATH == Path("CHANGELOG.md")

    def test_logging_constants(self):
        assert path.LOG_DIRECTORY == "logs"
        assert path.LOG_FILENAME == "custy.log"

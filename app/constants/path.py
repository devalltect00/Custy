# app/constants/path.py

from pathlib import Path

# PROJECT SOURCE
THIS_PROJECT_SOURCE = "app"

### FILES PATH
CUSTY_SETTINGS = Path(".config/custy/config.toml")
CUSTY_CHANGELOG_J2 = Path(".config/custy/templates/changelog/changelog.j2")
CUSTY_COMMIT_MESSAGE_TEMPLATE = Path(".config/custy/templates/commit-message.txt")
CUSTY_TAG_MESSAGE_TEMPLATE = Path(".config/custy/templates/tag-message.txt")
CHANGELOG_PATH = Path("CHANGELOG.md")

### DIR PATH
CUSTY_BACKUP_COMMIT_DIR = Path(".config/custy/templates/backups/commit")
CUSTY_BACKUP_TAG_DIR = Path(".config/custy/templates/backups/tag")

# LOG
LOG_DIRECTORY = "logs"
LOG_FILENAME = "custy.log"

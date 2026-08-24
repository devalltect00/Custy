# app/core/initialize/registry.py

from app.constants.path import (
    CUSTY_SETTINGS,
    CUSTY_CHANGELOG_J2,
    CUSTY_COMMIT_MESSAGE_TEMPLATE,
    CUSTY_TAG_MESSAGE_TEMPLATE,
)
from app.constants.resolver import (
    TARGET_PROJECT_SOURCE,
)
from app.core.initialize.loader import load_template
from app.core.initialize.models.template_file import TemplateFile
from app.core.initialize.models.template_dir import TemplateDir


def detect_version_file():
    import os

    if os.path.exists(TARGET_PROJECT_SOURCE):
        return f"{TARGET_PROJECT_SOURCE}/__version__.py"
    return "src/__version__.py"


class DirRegistry:
    @staticmethod
    def get_config_directories() -> list[str]:
        return [".config/custy"]

    @staticmethod
    def get_templates_directories() -> list[str]:
        return [
            ".config/custy/templates",
            ".config/custy/templates/backups",
            ".config/custy/templates/backups/commit",
            ".config/custy/templates/backups/tag",
            ".config/custy/templates/changelog",
        ]

    @staticmethod
    def get_examples_directories() -> list[str]:
        return [
            ".config/custy/templates/examples",
            ".config/custy/templates/examples/commit_message",
            ".config/custy/templates/examples/tag_message",
        ]

    def get_all_directories(self) -> list[str]:
        return [
            *self.get_config_directories(),
            *self.get_templates_directories(),
            *self.get_examples_directories(),
        ]


class FileRegistry:
    def __init__(self):
        # =========================
        # CONFIG
        # =========================
        self.config = TemplateFile(
            target_path=CUSTY_SETTINGS,
            content=lambda: load_template("config.toml"),
        )

        # =========================
        # VERSION FILE
        # =========================
        self.version = TemplateFile(
            target_path=detect_version_file(),
            content=lambda: load_template("__version__.py"),
        )

        # =========================
        # CHANGELOG TEMPLATE
        # =========================
        self.changelog = TemplateFile(
            target_path=CUSTY_CHANGELOG_J2,
            content=lambda: load_template("changelog/changelog.j2"),
        )

        # =========================
        # EMPTY FILES
        # =========================
        self.commit_message = TemplateFile(
            target_path=CUSTY_COMMIT_MESSAGE_TEMPLATE,
            content=lambda: "",
        )
        self.tag_message = TemplateFile(
            target_path=CUSTY_TAG_MESSAGE_TEMPLATE,
            content=lambda: "",
        )

    @staticmethod
    def get_config() -> list[TemplateFile]:
        # =========================
        # CONFIG
        # =========================
        return [
            TemplateFile(
                target_path=CUSTY_SETTINGS,
                content=lambda: load_template("config.toml"),
            )
        ]

    @staticmethod
    def get_templates() -> list[TemplateFile]:
        return [
            # =========================
            # CHANGELOG TEMPLATE
            # =========================
            TemplateFile(
                target_path=CUSTY_CHANGELOG_J2,
                content=lambda: load_template("changelog/changelog.j2"),
            ),

            # =========================
            # EMPTY FILES
            # =========================
            TemplateFile(
                target_path=CUSTY_COMMIT_MESSAGE_TEMPLATE,
                content=lambda: "",
            ),
            TemplateFile(
                target_path=CUSTY_TAG_MESSAGE_TEMPLATE,
                content=lambda: "",
            ),
        ]

    @staticmethod
    def get_version() -> list[TemplateFile]:
        # =========================
        # VERSION FILE
        # =========================
        return [
            TemplateFile(
                target_path=detect_version_file(),
                content=lambda: load_template("__version__.py"),
            )
        ]

    @staticmethod
    def get_examples() -> list[TemplateDir]:
        return [
            TemplateDir(
                target=".config/custy/templates/examples",
                source="examples",
            )
        ]

    def get_all_files(self) -> list[TemplateFile]:
        return [
            *self.get_config(),
            *self.get_templates(),
            *self.get_version(),
            *self.get_examples(),
        ]

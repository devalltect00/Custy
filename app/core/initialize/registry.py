# app/core/initialize/registry.py

from pathlib import Path

from app.config.config_loader import ConfigLoader
from app.constants.path import (
    CUSTY_CHANGELOG_J2,
    CUSTY_COMMIT_MESSAGE_TEMPLATE,
    CUSTY_SETTINGS,
    CUSTY_TAG_MESSAGE_TEMPLATE,
)
from app.constants.resolver import resolve_project_layout
from app.core.initialize.loader import load_template
from app.core.initialize.models.template_dir import TemplateDir
from app.core.initialize.models.template_file import TemplateFile


def detect_version_file(
    *,
    root: str | Path | None = None,
    config: ConfigLoader | None = None,
) -> str | None:
    """Select a new Python version module only when one is needed.

    Existing Python or Node.js version metadata is preserved. Node.js and
    generic projects do not receive a Python ``__version__.py`` file.

    Args:
        root: Target-project root. Defaults to the current working directory.
        config: Optional Custy configuration loader.

    Returns:
        Relative Python version-module path, or ``None`` when no file should
        be created.
    """

    layout = resolve_project_layout(config=config, root=root)

    if not layout.is_python or layout.version_target is not None:
        return None

    target = layout.source_dir / "__version__.py"
    try:
        return target.relative_to(layout.root).as_posix()
    except ValueError:
        return str(target)


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
        version_file = detect_version_file()
        self.version = (
            TemplateFile(
                target_path=version_file,
                content=lambda: load_template("__version__.py"),
            )
            if version_file
            else None
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
        version_file = detect_version_file()
        if not version_file:
            return []

        return [
            TemplateFile(
                target_path=version_file,
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

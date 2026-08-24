# app/core/initialize/builder/init_builder.py

from typing import Optional

from app.cli.constants.enums import InitMode
from app.core.initialize.models.init_config import InitConfig
from app.core.initialize.models.init_spec import InitSpec
from app.core.initialize.registry import DirRegistry, FileRegistry


class InitBuilder:
    """
    Builder for InitSpec.

    Responsibilities:
    - Transform InitConfig → InitSpec
    - Handle mode-based logic
    - Allow overrides (advanced usage)

    Design:
    - Config = input
    - Builder = decision logic
    - Plan = execution data
    """

    def __init__(self, config: Optional[InitConfig] = None):
        self.config = config or InitConfig()

        # Optional overrides (advanced usage)
        self._name: Optional[str] = None
        self._templates: Optional[list] = None
        self._dirs: Optional[list] = None
        self._template_dirs: Optional[list] = None
        self._messages: Optional[list[str]] = None

    # =========================================================
    # 🔧 Fluent API (Optional)
    # =========================================================

    def with_name(self, name: str):
        self._name = name
        return self

    def with_templates(self, templates: list):
        self._templates = templates
        return self

    def with_dirs(self, dirs: list):
        self._dirs = dirs
        return self

    def with_template_dirs(self, template_dirs: list):
        self._template_dirs = template_dirs
        return self

    def with_messages(self, messages: list[str]):
        self._messages = messages
        return self

    # =========================================================
    # 🧠 Build from Mode
    # =========================================================

    def _build_from_mode(self, mode: InitMode) -> InitSpec:
        if mode == InitMode.CONFIG:
            return InitSpec(
                name="configuration",
                templates=FileRegistry.get_config(),
                dirs=DirRegistry.get_config_directories(),
                messages=["✔ Configuration files created"],
            )

        elif mode == InitMode.TEMPLATES:
            return InitSpec(
                name="templates",
                templates=FileRegistry.get_templates(),
                dirs=DirRegistry.get_templates_directories(),
                messages=["✔ Templates generated"],
            )

        elif mode == InitMode.EXAMPLES:
            return InitSpec(
                name="examples",
                templates=None,
                dirs=DirRegistry.get_examples_directories(),
                template_dirs=FileRegistry.get_examples(),
                messages=["✔ Example resources added"],
            )

        elif mode == InitMode.ALL_NO_EXAMPLES:
            return InitSpec(
                name="all (no examples)",
                templates=(
                    FileRegistry.get_config()
                    + FileRegistry.get_templates()
                    + FileRegistry.get_version()
                ),
                dirs=(
                    DirRegistry.get_config_directories()
                    + DirRegistry.get_templates_directories()
                ),
                messages=[
                    "✔ Configuration files created",
                    "✔ Version file added",
                    "✔ Templates generated",
                ],
            )

        elif mode == InitMode.ALL:
            return InitSpec(
                name="all",
                templates=(
                    FileRegistry.get_config()
                    + FileRegistry.get_templates()
                    + FileRegistry.get_version()
                ),
                dirs=(
                    DirRegistry.get_config_directories()
                    + DirRegistry.get_templates_directories()
                    + DirRegistry.get_examples_directories()
                ),
                template_dirs=FileRegistry.get_examples(),
                messages=[
                    "✔ Configuration files created",
                    "✔ Version file added",
                    "✔ Templates generated",
                    "✔ Example resources added",
                ],
            )

        else:
            raise ValueError(f"Unsupported init mode: {mode}")

    # =========================================================
    # ✅ Validation
    # =========================================================

    def _validate(self):
        if not self.config.mode and not self._templates:
            raise ValueError("Either mode or templates must be provided")

    # =========================================================
    # 🚀 Build
    # =========================================================

    def build(self) -> InitSpec:
        self._validate()

        # 1. Base plan
        if self.config.mode:
            plan = self._build_from_mode(self.config.mode)
        else:
            plan = InitSpec(
                name=self._name or "custom",
                templates=self._templates or [],
                dirs=self._dirs or [],
                template_dirs=self._template_dirs,
                messages=self._messages,
            )

        # 2. Overrides
        if self._name:
            plan.name = self._name

        if self._templates:
            plan.templates = self._templates

        if self._dirs:
            plan.dirs = self._dirs

        if self._template_dirs:
            plan.template_dirs = self._template_dirs

        if self._messages:
            plan.messages = self._messages

        return plan

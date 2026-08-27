# app/core/git_ops/helper/project_detector.py

"""Resolve version strategies from configuration and project markers."""

from __future__ import annotations

import logging

from app.config.config_loader import get_config
from app.core.project import ProjectEcosystem, detect_project_layout

logger = logging.getLogger(__name__)


def detect_project_strategy(
    cli_value: str | None = None,
    no_debug: bool | None = False,
) -> str:
    """Detect the version-generation strategy for the target project.

    Resolution order:
        1. Explicit CLI value.
        2. tool.custy.cli.versioning.strategy.
        3. Python marker -> PEP 440.
        4. Node.js, PHP, mixed, or generic marker -> SemVer.
    """

    if cli_value:
        return cli_value

    config_value = get_config().get("cli", "versioning", "strategy")
    if config_value:
        if not no_debug:
            logger.info("Detected configured version strategy: %s", config_value)
        return str(config_value)

    layout = detect_project_layout()
    if ProjectEcosystem.PYTHON in layout.ecosystems:
        strategy = "pep440"
    else:
        strategy = "semver"

    if not no_debug:
        logger.info("Detected project version strategy: %s", strategy)

    return strategy


def detect_tag_sorting_strategy(
    no_debug: bool | None = False,
) -> str:
    """Detect a supported Git-tag sorting grammar from project markers."""

    layout = detect_project_layout()
    if ProjectEcosystem.PYTHON in layout.ecosystems:
        strategy = "pep440"
    else:
        strategy = "semver"

    if not no_debug:
        logger.info("Detected tag sorting strategy: %s", strategy)

    return strategy

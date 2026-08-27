# app/core/changelog/rendering/template_loader.py

"""Load changelog templates from project or packaged resources."""

from __future__ import annotations

import logging
from importlib.resources import files
from pathlib import Path

from app.constants.path import CUSTY_CHANGELOG_J2, THIS_PROJECT_SOURCE
from app.core.shared.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

PACKAGED_CHANGELOG_TEMPLATE = "changelog/changelog.j2"


def load_changelog_template(
    template_path: str | Path | None = None,
) -> str:
    """Load a project override or the packaged changelog template.

    The generated template under ``.config/custy`` is user-owned and may not
    exist before ``custy init`` runs. When the default generated path is
    absent, Custy uses its packaged template so importing commands and
    constructing workflows remain safe in an uninitialized project.

    Args:
        template_path: Optional project template path. ``None`` selects the
            standard generated path under ``.config/custy``.

    Returns:
        UTF-8 changelog template content.

    Raises:
        ConfigurationError: A custom template path does not exist or the
            packaged fallback cannot be loaded.
    """

    selected_path = Path(template_path) if template_path else CUSTY_CHANGELOG_J2

    if selected_path.is_file():
        logger.debug("Loading project changelog template: %s", selected_path)
        return selected_path.read_text(encoding="utf-8")

    if selected_path != CUSTY_CHANGELOG_J2:
        raise ConfigurationError(
            "Configured changelog template does not exist: "
            f"{selected_path}. Run 'custy init' or correct the template path."
        )

    logger.debug(
        "Project changelog template is unavailable; using packaged default: %s",
        selected_path,
    )

    try:
        return (
            files(f"{THIS_PROJECT_SOURCE}.templates")
            .joinpath(PACKAGED_CHANGELOG_TEMPLATE)
            .read_text(encoding="utf-8")
        )
    except (FileNotFoundError, ModuleNotFoundError) as exc:
        raise ConfigurationError(
            "Custy's packaged changelog template is unavailable. "
            "Reinstall Custy and try again."
        ) from exc

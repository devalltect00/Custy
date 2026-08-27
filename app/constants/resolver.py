# app/constants/resolver.py

"""Runtime configuration and target-project path resolvers.

This module intentionally performs no filesystem validation at import time.
Commands call these helpers after the current working directory and Custy
configuration are known.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.config.config_loader import ConfigLoader, get_config
from app.core.project import AUTO_VALUE, ProjectLayout, detect_project_layout
from app.core.shared import ConfigurationError


def resolve_directory(
    value: str | Path,
    *,
    name: str,
    must_exist: bool = True,
    root: str | Path | None = None,
) -> Path:
    """Resolve a directory path relative to a target-project root.

    Args:
        value: Relative or absolute directory path.
        name: Human-readable name used in error messages.
        must_exist: Validate existence and directory type when true.
        root: Resolution root. Defaults to the current working directory.

    Returns:
        Absolute normalized directory path.

    Raises:
        ConfigurationError: If required directory validation fails.
    """

    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path(root or Path.cwd()) / path
    path = path.resolve()

    if must_exist and not path.exists():
        raise ConfigurationError(f"{name} directory does not exist: {path}")
    if must_exist and not path.is_dir():
        raise ConfigurationError(f"{name} is not a directory: {path}")

    return path


def resolve_project_layout(
    *,
    config: ConfigLoader | None = None,
    project_source: str | Path | None = None,
    version_file: str | Path | None = None,
    root: str | Path | None = None,
) -> ProjectLayout:
    """Resolve configured values and detect the target-project layout."""

    loader = config or get_config()
    source_value: Any = loader.resolve(
        project_source,
        ["project", "project_source"],
        AUTO_VALUE,
    )
    version_value: Any = loader.resolve(
        version_file,
        ["cli", "paths", "version_file"],
        AUTO_VALUE,
    )

    return detect_project_layout(
        root=root,
        project_source=source_value,
        version_file=version_value,
    )


def resolve_project_source(
    *,
    config: ConfigLoader | None = None,
    value: str | Path | None = None,
    root: str | Path | None = None,
) -> Path:
    """Resolve an explicit or automatically detected project source."""

    return resolve_project_layout(
        config=config,
        project_source=value,
        root=root,
    ).source_dir


def resolve_version_file(
    *,
    config: ConfigLoader | None = None,
    value: str | Path | None = None,
    root: str | Path | None = None,
) -> Path | None:
    """Resolve an explicit or automatically detected version target."""

    return resolve_project_layout(
        config=config,
        version_file=value,
        root=root,
    ).version_target

# app/constants/resolver.py

"""
Configuration value resolvers.

Responsibilities
----------------

- Resolve configuration values from ConfigLoader
- Normalize filesystem paths
- Validate required directories
- Provide application-wide resolved constants

This module centralizes configuration resolution logic
so the rest of the application can consume validated
values without worrying about configuration details.

Examples
--------

Config:

    [tool.custy.project]
    project_source = "app"

Result:

    TARGET_PROJECT_SOURCE
    -> Path("/my-project/app")

Relative paths are resolved from the current working
directory. Absolute paths are preserved.
"""

from pathlib import Path

from app.config.config_loader import (
    get_config,
)

from app.core.shared import ConfigurationError

config = get_config()


def resolve_directory(
    value: str,
    *,
    name: str,
    must_exist: bool = True,
) -> Path:
    """
    Resolve a directory path.

    Parameters
    ----------
    value:
        Directory path from configuration.

        May be:

        - Relative path
        - Absolute path

    name:
        Human-readable configuration name used
        in validation error messages.

    must_exist:
        If True, validate that the directory exists.

    Returns
    -------
    Path
        Fully resolved directory path.

    Raises
    ------
    ConfigurationError
        If the directory does not exist.

    ConfigurationError
        If the path exists but is not a directory.
    """

    path = Path(value)

    if not path.is_absolute():
        path = Path.cwd() / path

    path = path.resolve()

    if must_exist and not path.exists():
        raise ConfigurationError(
            f"{name} directory does not exist: {path}"
        )

    if must_exist and not path.is_dir():
        raise ConfigurationError(
            f"{name} is not a directory: {path}"
        )

    return path


def resolve_project_source() -> Path:
    """
    Resolve the project source directory.

    Configuration
    -------------

        [tool.custy.project]
        project_source = "app"

    Returns
    -------
    Path
        Validated source directory path.

    Examples
    --------

    Config:

        project_source = "app"

    Result:

        Path("/project/app")

    Config:

        project_source = "src"

    Result:

        Path("/project/src")
    """

    value = config.resolve(
        cli_value=None,
        config_keys=[
            "project",
            "project_source",
        ],
        default="app",
    )

    return resolve_directory(
        value=value,
        name="Project source",
        must_exist=True,
    )


# =========================================================
# Resolved Constants
# =========================================================

TARGET_PROJECT_SOURCE = resolve_project_source()
"""
Validated project source directory.

Examples
--------

app/
src/
backend/

This value is guaranteed to:

- Exist
- Be a directory
- Be an absolute Path
"""

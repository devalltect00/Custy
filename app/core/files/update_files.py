# app/core/files/update_files.py

"""Cross-project version metadata update helpers.

Responsibilities:
- Update static Python project versions in pyproject.toml.
- Update Python __version__.py modules without discarding unrelated content.
- Update Node.js package metadata and supported npm lock metadata.
- Dispatch explicit and automatically detected version targets.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from tomlkit import dumps, parse

from app.core.shared import ConfigurationError

logger = logging.getLogger(__name__)


def normalize_metadata_version(new_version: str) -> str:
    """Remove a conventional Git ``v`` prefix before writing metadata."""

    return new_version.strip().removeprefix("v")


def update_toml_project_version(
    new_version: str,
    pyproject_path: str | Path = "pyproject.toml",
) -> bool:
    """Update a static ``project.version`` field in pyproject.toml.

    Returns:
        ``True`` when the field was updated, otherwise ``False`` for projects
        that intentionally use dynamic version metadata.

    Raises:
        FileNotFoundError: If the requested pyproject.toml does not exist.
        ConfigurationError: If the TOML content cannot be parsed.
    """

    path = Path(pyproject_path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    try:
        document = parse(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ConfigurationError(
            f"Unable to parse Python project metadata: {path}. {exc}"
        ) from exc

    project = document.get("project")
    if project is None or "version" not in project:
        logger.info("%s has no static project.version; leaving it unchanged.", path)
        return False

    normalized = normalize_metadata_version(new_version)
    old_version = project["version"]
    project["version"] = normalized
    path.write_text(dumps(document), encoding="utf-8")
    logger.info("%s version updated: %s -> %s", path, old_version, normalized)
    return True


def _load_json_object(file_path: Path) -> dict[str, Any]:
    """Load a JSON object with an actionable configuration error."""

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(
            f"Unable to parse JSON version metadata: {file_path}. {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ConfigurationError(
            f"JSON version metadata must contain an object: {file_path}."
        )
    return data


def update_json_version(file_path: Path, new_version: str) -> bool:
    """Update top-level JSON version metadata and npm root lock metadata."""

    if not file_path.exists():
        return False

    data = _load_json_object(file_path)
    normalized = normalize_metadata_version(new_version)
    updated = False
    old_version = data.get("version")

    if isinstance(old_version, str):
        data["version"] = normalized
        updated = True

    packages = data.get("packages")
    if isinstance(packages, dict):
        root_package = packages.get("")
        if isinstance(root_package, dict) and isinstance(
            root_package.get("version"),
            str,
        ):
            root_package["version"] = normalized
            updated = True

    if not updated:
        logger.info(
            "%s has no supported version field; leaving it unchanged.", file_path
        )
        return False

    file_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    logger.info("%s version updated: %s -> %s", file_path, old_version, normalized)
    return True


def update_python_version_module(file_path: Path, new_version: str) -> bool:
    """Update or add ``__version__`` in an existing Python module."""

    if not file_path.exists():
        return False

    normalized = normalize_metadata_version(new_version)
    content = file_path.read_text(encoding="utf-8")
    replacement = f'__version__ = "{normalized}"'
    pattern = re.compile(
        r'^__version__\s*=\s*(["\']).*?\1\s*$',
        flags=re.MULTILINE,
    )
    updated_content, count = pattern.subn(replacement, content, count=1)

    if count == 0:
        separator = "" if not content or content.endswith("\n") else "\n"
        updated_content = f"{content}{separator}{replacement}\n"

    file_path.write_text(updated_content, encoding="utf-8")
    logger.info("%s version updated to %s", file_path, normalized)
    return True


def update_node_project_version(root: str | Path, new_version: str) -> bool:
    """Update supported Node.js package and npm lock metadata."""

    root_path = Path(root)
    updated = False

    for filename in ("package.json", "package-lock.json", "npm-shrinkwrap.json"):
        updated |= update_json_version(root_path / filename, new_version)

    if (root_path / "yarn.lock").exists():
        logger.debug("yarn.lock detected; no manual version rewrite is required.")

    return updated


def update_version_target(file_path: Path, new_version: str) -> bool:
    """Update a configured version target using its supported file format.

    Raises:
        ConfigurationError: If the configured target format is unsupported.
    """

    path = Path(file_path)
    if path.name == "pyproject.toml":
        return update_toml_project_version(new_version, path)
    if path.suffix.lower() == ".json":
        return update_json_version(path, new_version)
    if path.suffix.lower() == ".py":
        return update_python_version_module(path, new_version)

    raise ConfigurationError(
        f"Unsupported version target: {path}. Supported targets are Python "
        "__version__.py modules, pyproject.toml, and JSON package metadata."
    )


def update_version_universal(
    root: str | Path | None,
    new_version: str,
    project_type: str | None = None,
) -> bool:
    """Update supported project metadata under a repository root.

    Args:
        root: Project root. Defaults to the current working directory.
        new_version: Version or ``v``-prefixed Git tag to apply.
        project_type: Optional ``python`` or ``node`` restriction.

    Returns:
        Whether any supported metadata field was updated.

    Raises:
        ValueError: If project_type is not supported.
    """

    if project_type not in {None, "python", "node"}:
        raise ValueError(f"Unsupported project type: {project_type}")

    root_path = Path(root or ".")
    updated = False

    if project_type in (None, "python"):
        pyproject = root_path / "pyproject.toml"
        if pyproject.exists():
            updated |= update_toml_project_version(new_version, pyproject)

    if project_type in (None, "node"):
        if (root_path / "package.json").exists():
            updated |= update_node_project_version(root_path, new_version)

    if not updated:
        logger.debug("No supported project version metadata was updated.")

    return updated


if __name__ == "__main__":
    raise SystemExit("Use Custy commands instead of executing this module directly.")

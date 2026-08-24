# app/core/files/update_files.py

import logging
import json

from pathlib import Path
from tomlkit import parse, dumps
from typing import Optional

logger = logging.getLogger(__name__)

def update_toml_project_version(new_version: str, pyproject_path: str = "pyproject.toml") -> bool:
    path = Path(pyproject_path)

    if not path.exists():
        raise FileNotFoundError(f"{pyproject_path} not found")

    content = path.read_text(encoding="utf-8")
    doc = parse(content)

    if "project" not in doc:
        logger.info(f"⏩ No [project] section on [dim]{pyproject_path}[/dim] → ignored")
        return False

    project = doc["project"]

    if "version" not in project:
        logger.info(f"⏩ No version field on [dim]{pyproject_path}[/dim] → ignored")
        return False

    old_version = project["version"]
    project["version"] = new_version

    path.write_text(dumps(doc), encoding="utf-8")

    logger.info(f"✅ [dim]{pyproject_path}[/dim] [green]Updated[/green]. Version updated: {old_version} [yellow]→[/yellow] {new_version}")
    return True

def update_json_version(file_path: Path, new_version: str) -> bool:
    if not file_path.exists():
        return False

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        logger.error(f"Skipping invalid JSON: {file_path}")
        return False

    if "version" not in data:
        logger.warning(f"{file_path.name}: no version field → ignored")
        return False

    old_version = data["version"]
    data["version"] = new_version

    file_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    logger.info(f"{file_path.name}: {old_version} → {new_version}")
    return True


def update_node_project_version(root: str, new_version: str):
    root_path = Path(root)

    updated = False

    # 1. package.json (required)
    updated |= update_json_version(root_path / "package.json", new_version)

    # 2. package-lock.json (npm)
    updated |= update_json_version(root_path / "package-lock.json", new_version)

    # 3. npm-shrinkwrap.json (optional)
    updated |= update_json_version(root_path / "npm-shrinkwrap.json", new_version)

    # 4. yarn.lock (DO NOT EDIT)
    yarn_lock = root_path / "yarn.lock"
    if yarn_lock.exists():
        logger.info("yarn.lock detected → run `yarn install` to sync version")

    if not updated:
        logger.info("No files updated")

    return updated

def update_version_universal(
    root: Optional[str],
    new_version: str,
    project_type: Optional[str] = None,
    ) -> bool:
    """
    Update version across project files.

    Args:
        root (str): project root
        new_version (str): version to apply
        project_type (str | None):
            - 'python' → update only Python files
            - 'node' → update only Node files
            - None → auto-detect (default behavior)

    Returns:
        bool: whether any file was updated
    """

    # Normalize root
    # root_path = Path(root or ".").resolve()
    root_path = Path(root or ".")

    updated = False

    # =========================================================
    # Python project
    # =========================================================
    if project_type in (None, "python"):
        pyproject = root_path / "pyproject.toml"

        if (pyproject).exists():
            logger.debug("Detected Python project")
            logger.debug("Updating Python project (pyproject.toml)")
            updated |= update_toml_project_version(
                pyproject_path=pyproject,
                new_version=new_version,
            )

            # If explicitly python → stop here
            if project_type == "python":
                return updated

    # =========================================================
    # Node project
    # =========================================================
    if project_type in (None, "node"):
        package_json = root_path / "package.json"

        if (package_json).exists():
            logger.debug("Detected Node project")
            logger.debug("Updating Node project (package.json)")
            updated |= update_node_project_version(
                root=root_path,
                new_version=new_version
            )

            if project_type == "node":
                return updated

    if not updated:
        # logger.debug("⏩ No supported project files found or nothing updated")
        logger.debug("⏩ No supported project files found or nothing updated on (pyproject.toml or package.json or node project files)")

    return updated

if __name__ == "__main__":
    update_toml_project_version("pyproject.toml", "1.2.3")
    update_node_project_version(".", "1.2.3")

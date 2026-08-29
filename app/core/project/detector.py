# app/core/project/detector.py

"""Detect target-project layout without assuming a framework or language.

Responsibilities:
- Identify Python, Node.js, mixed, and generic repositories.
- Resolve an optional source directory at command runtime.
- Locate supported version metadata without requiring it.
- Validate explicit user-configured paths with actionable errors.
"""

from __future__ import annotations

import json
import tomllib
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from app.core.shared import ConfigurationError

AUTO_VALUE = "auto"


class ProjectEcosystem(StrEnum):
    """Supported high-level target-project ecosystems."""

    PYTHON = "python"
    NODE = "node"
    PHP = "php"
    GENERIC = "generic"


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved target-project layout.

    Attributes:
        root: Absolute repository or working-directory root.
        source_dir: Existing source directory selected for project operations.
        ecosystems: Detected project ecosystems. Generic is used only when no
            supported ecosystem marker exists.
        version_target: Existing supported version metadata target, if any.
        source_is_explicit: Whether source_dir came from user configuration.
        version_is_explicit: Whether version_target came from user configuration.
    """

    root: Path
    source_dir: Path
    ecosystems: frozenset[ProjectEcosystem]
    version_target: Path | None
    source_is_explicit: bool = False
    version_is_explicit: bool = False

    @property
    def is_python(self) -> bool:
        """Return whether Python project markers were detected."""

        return ProjectEcosystem.PYTHON in self.ecosystems

    @property
    def is_node(self) -> bool:
        """Return whether Node.js project markers were detected."""

        return ProjectEcosystem.NODE in self.ecosystems

    @property
    def is_generic(self) -> bool:
        """Return whether no supported ecosystem marker was detected."""

        return self.ecosystems == frozenset({ProjectEcosystem.GENERIC})


def _resolve_path(value: str | Path, root: Path) -> Path:
    """Resolve a configured path relative to the target-project root."""

    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _is_auto(value: str | Path | None) -> bool:
    """Return whether a configured value requests automatic detection."""

    return value is None or str(value).strip().lower() in {"", AUTO_VALUE}


def _detect_ecosystems(root: Path) -> frozenset[ProjectEcosystem]:
    """Detect project ecosystems from conventional root-level marker files."""

    detected: set[ProjectEcosystem] = set()

    if any(
        (root / marker).exists()
        for marker in ("pyproject.toml", "setup.py", "requirements.txt")
    ):
        detected.add(ProjectEcosystem.PYTHON)

    if (root / "package.json").exists():
        detected.add(ProjectEcosystem.NODE)

    if (root / "composer.json").exists():
        detected.add(ProjectEcosystem.PHP)

    if not detected:
        detected.add(ProjectEcosystem.GENERIC)

    return frozenset(detected)


def _first_existing_directory(candidates: Iterable[Path], root: Path) -> Path:
    """Return the first existing directory or the project root."""

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    return root


def _detect_source_directory(
    root: Path,
    ecosystems: frozenset[ProjectEcosystem],
) -> Path:
    """Detect a useful source directory while always allowing the root."""

    if ProjectEcosystem.PYTHON in ecosystems:
        candidates = (root / "app", root / "src")
    elif ProjectEcosystem.NODE in ecosystems:
        candidates = (root / "src", root / "app")
    else:
        candidates = (root / "src", root / "app")

    return _first_existing_directory(candidates, root)


def _has_pyproject_version(path: Path) -> bool:
    """Return whether pyproject.toml contains a static project version."""

    if not path.is_file():
        return False

    try:
        with path.open("rb") as stream:
            data = tomllib.load(stream)
    except OSError, tomllib.TOMLDecodeError:
        return False

    project = data.get("project")
    return isinstance(project, dict) and isinstance(project.get("version"), str)


def _has_json_version(path: Path) -> bool:
    """Return whether a JSON metadata file contains a string version."""

    if not path.is_file():
        return False

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError, json.JSONDecodeError:
        return False

    return isinstance(data, dict) and isinstance(data.get("version"), str)


def detect_project_name(*, root: str | Path | None = None) -> str:
    """Resolve a human-readable project name from common metadata.

    Args:
        root: Target-project root. Defaults to the current working directory.

    Returns:
        ``project.name`` from ``pyproject.toml``, ``name`` from
        ``package.json``, or the project-directory name when neither metadata
        source provides a non-empty string.

    Notes:
        Invalid or unreadable optional metadata is ignored so generic projects
        remain valid Custy targets.
    """

    project_root = Path(root or Path.cwd()).expanduser().resolve()
    pyproject_path = project_root / "pyproject.toml"
    if pyproject_path.is_file():
        try:
            with pyproject_path.open("rb") as stream:
                project = tomllib.load(stream).get("project")
            if isinstance(project, dict):
                name = project.get("name")
                if isinstance(name, str) and name.strip():
                    return name.strip()
        except OSError, tomllib.TOMLDecodeError:
            pass

    package_path = project_root / "package.json"
    if package_path.is_file():
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
            if isinstance(package, dict):
                name = package.get("name")
                if isinstance(name, str) and name.strip():
                    return name.strip()
        except OSError, json.JSONDecodeError, UnicodeError:
            pass

    return project_root.name or "Project"


def _python_version_candidates(root: Path, source_dir: Path) -> tuple[Path, ...]:
    """Return deterministic Python version-module candidates."""

    candidates: list[Path] = [
        source_dir / "__version__.py",
        root / "__version__.py",
    ]

    if source_dir != root and source_dir.is_dir():
        candidates.extend(sorted(source_dir.glob("*/__version__.py")))

    return tuple(dict.fromkeys(candidate.resolve() for candidate in candidates))


def _detect_version_target(
    root: Path,
    source_dir: Path,
    ecosystems: frozenset[ProjectEcosystem],
) -> Path | None:
    """Locate an existing supported version target."""

    if ProjectEcosystem.PYTHON in ecosystems:
        for candidate in _python_version_candidates(root, source_dir):
            if candidate.is_file():
                return candidate

        pyproject = root / "pyproject.toml"
        if _has_pyproject_version(pyproject):
            return pyproject.resolve()

    if ProjectEcosystem.NODE in ecosystems:
        package_json = root / "package.json"
        if _has_json_version(package_json):
            return package_json.resolve()

    return None


def detect_project_layout(
    *,
    root: str | Path | None = None,
    project_source: str | Path | None = AUTO_VALUE,
    version_file: str | Path | None = AUTO_VALUE,
) -> ProjectLayout:
    """Detect and validate the target-project layout.

    Args:
        root: Target-project root. Defaults to the current working directory.
        project_source: Explicit source directory or "auto".
        version_file: Explicit version target or "auto".

    Returns:
        Resolved project layout. Generic projects and projects without version
        metadata are valid and therefore may return no version target.

    Raises:
        ConfigurationError: If an explicitly configured path does not exist or
            has the wrong filesystem type.
    """

    project_root = Path(root or Path.cwd()).expanduser().resolve()
    if not project_root.is_dir():
        raise ConfigurationError(
            f"Project root directory does not exist: {project_root}. "
            "Run Custy from an existing project directory."
        )

    ecosystems = _detect_ecosystems(project_root)

    source_is_explicit = not _is_auto(project_source)
    if source_is_explicit:
        source_dir = _resolve_path(project_source, project_root)
        if not source_dir.exists():
            raise ConfigurationError(
                f"Configured project source does not exist: {source_dir}. "
                "Set tool.custy.project.project_source to 'auto' or an "
                "existing directory."
            )
        if not source_dir.is_dir():
            raise ConfigurationError(
                f"Configured project source is not a directory: {source_dir}. "
                "Set tool.custy.project.project_source to an existing "
                "directory."
            )
    else:
        source_dir = _detect_source_directory(project_root, ecosystems)

    version_is_explicit = not _is_auto(version_file)
    if version_is_explicit:
        version_target = _resolve_path(version_file, project_root)
        if not version_target.exists():
            raise ConfigurationError(
                f"Configured version target does not exist: {version_target}. "
                "Set tool.custy.cli.paths.version_file to 'auto', create the "
                "file, or configure an existing version target."
            )
        if not version_target.is_file():
            raise ConfigurationError(
                f"Configured version target is not a file: {version_target}."
            )
    else:
        version_target = _detect_version_target(
            project_root,
            source_dir,
            ecosystems,
        )

    return ProjectLayout(
        root=project_root,
        source_dir=source_dir,
        ecosystems=ecosystems,
        version_target=version_target,
        source_is_explicit=source_is_explicit,
        version_is_explicit=version_is_explicit,
    )

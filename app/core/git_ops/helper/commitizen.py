# app/core/git_ops/helper/commitizen.py

"""Commitizen discovery and command integration.

Commitizen is optional. This module detects project configuration separately
from executable availability and returns structured command results so callers
can choose strict failure or a safe Custy fallback.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import tomllib
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from app.core.dry_run import DryRunSupport

logger = logging.getLogger(__name__)

_CONFIG_FILENAMES = (
    ".cz.toml",
    ".cz.yaml",
    ".cz.yml",
    ".cz.json",
)


@dataclass(frozen=True, slots=True)
class CommitizenInspection:
    """Describe Commitizen configuration and executable availability."""

    config_path: Path | None
    executable: str | None
    config_error: str | None = None

    @property
    def configured(self) -> bool:
        """Return whether a Commitizen configuration source was detected."""

        return self.config_path is not None

    @property
    def available(self) -> bool:
        """Return whether the ``cz`` executable is available."""

        return self.executable is not None

    @property
    def valid(self) -> bool:
        """Return whether the detected configuration passed basic parsing."""

        return self.config_error is None


@dataclass(frozen=True, slots=True)
class CommitizenCommandResult:
    """Normalized result returned by a Commitizen subprocess command."""

    returncode: int
    stdout: str = ""
    stderr: str = ""

    @property
    def success(self) -> bool:
        """Return whether Commitizen exited successfully."""

        return self.returncode == 0


class CommitizenHelper(DryRunSupport):
    """Discover and run optional Commitizen project integration."""

    def __init__(
        self,
        dry_run: bool = False,
        is_silent: bool = False,
        *,
        project_root: Path | None = None,
        executable_resolver: Callable[[str], str | None] = shutil.which,
    ) -> None:
        """Initialize Commitizen integration and discovery dependencies."""

        super().__init__(dry_run=dry_run, is_silent=is_silent)
        self.project_root = Path.cwd() if project_root is None else Path(project_root)
        self.executable_resolver = executable_resolver

    def inspect(self) -> CommitizenInspection:
        """Inspect project configuration and executable availability."""

        executable = self.executable_resolver("cz")

        for filename in _CONFIG_FILENAMES:
            config_path = self.project_root / filename
            if config_path.is_file():
                return CommitizenInspection(
                    config_path=config_path,
                    executable=executable,
                    config_error=self._validate_config_file(config_path),
                )

        pyproject_path = self.project_root / "pyproject.toml"
        if not pyproject_path.is_file():
            return CommitizenInspection(None, executable)

        try:
            raw = pyproject_path.read_text(encoding="utf-8")
        except OSError as error:
            return CommitizenInspection(
                pyproject_path,
                executable,
                f"Unable to read {pyproject_path}: {error}",
            )

        if "[tool.commitizen" not in raw:
            return CommitizenInspection(None, executable)

        try:
            parsed = tomllib.loads(raw)
            section = parsed.get("tool", {}).get("commitizen")
            if not isinstance(section, Mapping):
                raise ValueError("[tool.commitizen] must be a TOML table")
        except (tomllib.TOMLDecodeError, ValueError) as error:
            return CommitizenInspection(pyproject_path, executable, str(error))

        return CommitizenInspection(pyproject_path, executable)

    @staticmethod
    def _validate_config_file(path: Path) -> str | None:
        """Return a basic parsing error for a dedicated Commitizen file."""

        try:
            if path.suffix == ".toml":
                with path.open("rb") as file:
                    parsed = tomllib.load(file)
                section = parsed.get("tool", {}).get("commitizen")
                if not isinstance(section, Mapping):
                    raise ValueError("[tool.commitizen] must be a TOML table")
            elif path.suffix == ".json":
                parsed_json = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(parsed_json, Mapping):
                    raise ValueError("Commitizen JSON configuration must be an object")
        except (OSError, UnicodeError, ValueError, tomllib.TOMLDecodeError) as error:
            return str(error)

        return None

    def commit(self) -> CommitizenCommandResult:
        """Run the interactive ``cz commit`` command."""

        executable = self._require_executable()
        return self._run_command([executable, "commit"], read_only=False)

    def generate_changelog_with_commitizen(self) -> CommitizenCommandResult:
        """Run Commitizen changelog generation."""

        executable = self._require_executable()
        return self._run_command([executable, "changelog"], read_only=False)

    def check_commit(self, path: Path | None = None) -> CommitizenCommandResult:
        """Validate a message file or the most recent commit with Commitizen."""

        executable = self._require_executable()
        if path is None:
            command = [executable, "check", "--rev-range", "HEAD~1..HEAD"]
        else:
            command = [
                executable,
                "check",
                "--commit-msg-file",
                str(path),
            ]
        return self._run_command(command, read_only=True)

    def _require_executable(self) -> str:
        """Resolve ``cz`` or raise an actionable runtime error."""

        executable = self.executable_resolver("cz")
        if executable is None:
            raise RuntimeError(
                "Commitizen executable 'cz' was not found. "
                'Install Custy with `pip install "custy[commitizen]"`.'
            )
        return executable

    def _run_command(
        self,
        command: list[str],
        *,
        read_only: bool,
    ) -> CommitizenCommandResult:
        """Execute and normalize a Commitizen command without losing output."""

        try:
            result = self.runner.run(
                command,
                check=False,
                read_only=read_only,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
        except OSError as error:
            return CommitizenCommandResult(returncode=1, stderr=str(error))

        if result is None:
            if self.runner.get_is_dry_run() and not read_only:
                return CommitizenCommandResult(returncode=0)
            return CommitizenCommandResult(
                returncode=1,
                stderr="Commitizen command did not complete successfully.",
            )

        return CommitizenCommandResult(
            returncode=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
        )

    def update_cz_toml_version(self, new_version: str) -> None:
        """Update the ``version`` field in ``.cz.toml`` when available."""

        cz_path = self.project_root / ".cz.toml"
        if not cz_path.exists():
            logger.warning(
                "⚠️ [yellow]Skipping[/yellow] [dim].cz.toml[/dim] update: "
                "file not found."
            )
            return

        cleaned_version = new_version.lstrip("v")
        if self.runner.get_is_dry_run():
            logger.info(
                "[dry_run](dry-run)[/dry_run] Would update "
                f"[dim].cz.toml[/dim] version to {cleaned_version}."
            )
            return

        try:
            content = cz_path.read_text(encoding="utf-8")
            new_content, count = re.subn(
                r'version\s*=\s*".*?"',
                f'version = "{cleaned_version}"',
                content,
            )
            if count == 0:
                logger.warning(
                    "⚠️ Could not find 'version =' field in [dim].cz.toml[/dim]."
                )
                return

            cz_path.write_text(new_content, encoding="utf-8")
            logger.info(
                "✅ [dim].cz.toml[/dim] [green]Updated[/green]. "
                f"Version updated to {cleaned_version}"
            )
        except (OSError, UnicodeError) as error:
            logger.error(
                "❌ Failed to update [dim].cz.toml[/dim] version: %s",
                error,
            )

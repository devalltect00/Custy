# tests/integration/test_cross_project_startup.py

"""Regression tests for importing Custy from heterogeneous repositories."""

import os
import subprocess
import sys
from pathlib import Path


def _environment_with_project_on_pythonpath() -> dict[str, str]:
    """Return an environment that imports the current Custy source tree."""

    project_root = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = str(project_root)
    if existing:
        environment["PYTHONPATH"] += os.pathsep + existing
    return environment


class TestCrossProjectStartup:
    """Ensures CLI imports do not require an app directory or configuration."""

    def test_imports_cli_from_generic_repository(self, tmp_path):
        """Imports the complete CLI from a repository with no known markers."""

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from app.cli.main import app; print(app.info.name)",
            ],
            cwd=tmp_path,
            env=_environment_with_project_on_pythonpath(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert "Project source directory does not exist" not in result.stderr

    def test_help_runs_from_node_repository_without_custy_config(self, tmp_path):
        """Runs protected CLI help from a Node.js-style repository."""

        (tmp_path / "package.json").write_text(
            '{"name": "docs", "version": "0.1.0"}',
            encoding="utf-8",
        )
        (tmp_path / "src").mkdir()

        result = subprocess.run(
            [sys.executable, "-m", "app", "--help", "--no-banner"],
            cwd=tmp_path,
            env=_environment_with_project_on_pythonpath(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert "Traceback" not in result.stderr
        assert "Project source directory does not exist" not in result.stderr

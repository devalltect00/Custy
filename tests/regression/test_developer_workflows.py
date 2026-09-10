# tests/regression/test_developer_workflows.py

"""Regression tests for repository-local development exclusions."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    """Read a repository file as UTF-8 text."""

    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_named_virtual_environments_stay_outside_tooling_inputs() -> None:
    """Exclude dedicated environments from Git, Docker, and formatters."""

    environment_names = (
        "dev_venv",
        "prod_venv",
        "venv_dev",
        "venv_prod",
        "publish_venv",
        "venv_publish",
        "other_venv",
        "venv_other",
    )

    for ignore_file in (".gitignore", ".dockerignore", ".prettierignore"):
        text = _read(ignore_file)
        for environment_name in environment_names:
            assert f"{environment_name}/" in text

    pyproject = _read("pyproject.toml")
    for environment_name in environment_names:
        assert pyproject.count(environment_name) >= 2

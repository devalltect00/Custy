# tests/core/changelog/test_template_loader.py

"""Tests for project and packaged changelog-template loading."""

from pathlib import Path

import pytest

from app.core.changelog.rendering import template_loader
from app.core.shared.exceptions import ConfigurationError


def test_project_template_overrides_packaged_default(tmp_path: Path) -> None:
    """An existing project template remains the highest-priority source."""

    project_template = tmp_path / "changelog.j2"
    project_template.write_text("project override", encoding="utf-8")

    assert (
        template_loader.load_changelog_template(project_template) == "project override"
    )


def test_missing_generated_template_uses_packaged_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A fresh project can construct changelog services before initialization."""

    generated_template = tmp_path / ".config/custy/templates/changelog/changelog.j2"
    monkeypatch.setattr(
        template_loader,
        "CUSTY_CHANGELOG_J2",
        generated_template,
    )

    content = template_loader.load_changelog_template()

    assert "release.version" in content


def test_missing_custom_template_raises_configuration_error(tmp_path: Path) -> None:
    """A misspelled custom path is reported instead of silently ignored."""

    custom_template = tmp_path / "missing-custom.j2"

    with pytest.raises(ConfigurationError, match="template does not exist"):
        template_loader.load_changelog_template(custom_template)

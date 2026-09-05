# tests/core/git_ops/credentials/test_service.py

"""Tests for credential setup, status, and config persistence."""

from pathlib import Path

import pytest

from app.config.config_loader import ConfigLoader
from app.core.git_ops.credentials import (
    CredentialProvider,
    CredentialService,
    CredentialSource,
)
from app.core.shared import ConfigurationError


def _service(tmp_path: Path) -> tuple[CredentialService, Path]:
    project = tmp_path / "project"
    project.mkdir()
    config_path = project / "config.toml"
    config_path.write_text(
        "[tool.custy.git]\n"
        'default_remote = "origin"\n\n'
        "[tool.custy.git.credentials]\n"
        'mode = "native"\n'
        "container_only = true\n"
        'source_order = ["file", "environment"]\n'
        "interactive_fallback = true\n"
        "fail_non_interactive = true\n",
        encoding="utf-8",
    )
    return (
        CredentialService(
            ConfigLoader(config_path),
            project_root=project,
            credential_root=tmp_path / "secrets",
            environment={"CUSTY_CONTAINER": "1"},
            is_container=True,
        ),
        config_path,
    )


def test_file_setup_keeps_token_out_of_config(tmp_path):
    service, config_path = _service(tmp_path)
    stored = service.set_provider(
        CredentialProvider.GITHUB,
        source=CredentialSource.FILE,
        token="super-secret",
    )
    rendered = config_path.read_text(encoding="utf-8")
    assert stored is not None and stored.is_file()
    assert "super-secret" not in rendered
    assert 'mode = "auto"' in rendered
    assert "enabled = true" in rendered
    assert service.is_managed_fallback_active() is True


def test_environment_setup_stores_only_variable_name(tmp_path):
    service, config_path = _service(tmp_path)
    service.set_provider(
        CredentialProvider.GITLAB,
        source=CredentialSource.ENVIRONMENT,
        token_env="MY_GITLAB_TOKEN",
    )
    rendered = config_path.read_text(encoding="utf-8")
    assert "MY_GITLAB_TOKEN" in rendered
    assert "password" not in rendered.lower()


def test_remove_preserves_file_unless_explicit(tmp_path):
    service, _ = _service(tmp_path)
    path = service.set_provider(
        CredentialProvider.GITHUB,
        source=CredentialSource.FILE,
        token="super-secret",
    )
    assert path is not None
    returned_path, deleted = service.remove_provider(CredentialProvider.GITHUB)
    assert returned_path == path
    assert deleted is False
    assert path.exists()
    _, deleted = service.remove_provider(
        CredentialProvider.GITHUB,
        delete_file=True,
    )
    assert deleted is True
    assert not path.exists()


def test_dry_run_status_does_not_open_token_file(tmp_path, monkeypatch):
    service, _ = _service(tmp_path)
    path = service.store.resolve_token_path("github.token")
    path.parent.mkdir(parents=True)
    path.write_text("secret\n", encoding="utf-8")

    def fail_if_read(_):
        raise AssertionError("dry-run must not read token material")

    monkeypatch.setattr(service.store, "read_token_file", fail_if_read)
    statuses = service.statuses(dry_run=True)
    assert statuses[0].file_status == "present (not validated in dry-run)"


def test_missing_config_fails_before_token_file_is_written(tmp_path):
    missing = tmp_path / "project" / "config.toml"
    missing.parent.mkdir()
    service = CredentialService(
        ConfigLoader(missing),
        project_root=missing.parent,
        credential_root=tmp_path / "secrets",
        environment={"CUSTY_CONTAINER": "1"},
        is_container=True,
    )

    with pytest.raises(ConfigurationError, match="not initialized"):
        service.set_provider(
            CredentialProvider.GITHUB,
            source=CredentialSource.FILE,
            token="super-secret",
        )

    assert not (tmp_path / "secrets" / "github.token").exists()


def test_invalid_config_fails_before_external_file_is_deleted(tmp_path):
    service, config_path = _service(tmp_path)
    path = service.set_provider(
        CredentialProvider.GITHUB,
        source=CredentialSource.FILE,
        token="super-secret",
    )
    assert path is not None
    config_path.write_text("[invalid", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="cannot be updated safely"):
        service.remove_provider(
            CredentialProvider.GITHUB,
            delete_file=True,
        )

    assert path.exists()

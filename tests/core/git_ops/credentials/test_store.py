# tests/core/git_ops/credentials/test_store.py

"""Tests for external credential token storage."""

import pytest

from app.core.git_ops.credentials.store import CredentialStore
from app.core.shared import ConfigurationError


@pytest.fixture
def store(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    return CredentialStore(
        project_root=project,
        credential_root=tmp_path / "secrets",
        environment={},
    )


def test_write_read_replace_and_delete(store):
    path = store.write_token_file("github.token", "secret-value")
    assert path.read_text(encoding="utf-8") == "secret-value\n"
    assert store.read_token_file("github.token") == "secret-value"
    with pytest.raises(ConfigurationError, match="already exists"):
        store.write_token_file("github.token", "replacement")
    store.write_token_file("github.token", "replacement", replace=True)
    assert store.read_token_file("github.token") == "replacement"
    assert store.delete_token_file("github.token") is True
    assert store.delete_token_file("github.token") is False


def test_missing_file_falls_through(store):
    assert store.read_token_file("missing.token") is None


@pytest.mark.parametrize("token", ["", " token", "token ", "one\ntwo", "a\x00b"])
def test_malformed_token_is_rejected(store, token):
    with pytest.raises(ConfigurationError):
        store.write_token_file("github.token", token)


def test_token_path_inside_project_is_rejected(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    store = CredentialStore(project_root=project, credential_root=tmp_path / "secrets")
    with pytest.raises(ConfigurationError, match="outside the target project"):
        store.resolve_token_path(str(project / "github.token"))


def test_dry_run_does_not_create_file(store):
    path = store.write_token_file("github.token", "secret", dry_run=True)
    assert not path.exists()

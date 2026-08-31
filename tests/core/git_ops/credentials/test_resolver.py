# tests/core/git_ops/credentials/test_resolver.py

"""Tests for native-first credential resolution."""

from pathlib import Path

import pytest

from app.config.config_loader import ConfigLoader
from app.core.git_ops.credentials import CredentialProvider, CredentialSource
from app.core.git_ops.credentials.resolver import CredentialResolver
from app.core.git_ops.credentials.settings import CredentialSettingsLoader
from app.core.git_ops.credentials.store import CredentialStore
from app.core.shared import ConfigurationError


def _resolver(
    tmp_path: Path,
    *,
    mode: str = "auto",
    environment: dict[str, str] | None = None,
    is_container: bool = True,
    is_interactive: bool = True,
) -> tuple[CredentialResolver, CredentialStore]:
    project = tmp_path / "project"
    project.mkdir()
    config_path = project / "config.toml"
    config_path.write_text(
        "[tool.custy.git.credentials]\n"
        f'mode = "{mode}"\n'
        "container_only = true\n"
        'source_order = ["file", "environment"]\n'
        "interactive_fallback = true\n"
        "fail_non_interactive = true\n\n"
        "[tool.custy.git.credentials.github]\n"
        "enabled = true\n"
        'username = "x-access-token"\n'
        'token_file = "github.token"\n'
        'token_env = "CUSTY_GITHUB_TOKEN"\n',
        encoding="utf-8",
    )
    settings = CredentialSettingsLoader(ConfigLoader(config_path)).load()
    store = CredentialStore(
        project_root=project,
        credential_root=tmp_path / "secrets",
        environment=environment or {},
    )
    return (
        CredentialResolver(
            settings,
            store,
            environment=environment or {},
            is_container=is_container,
            is_interactive=is_interactive,
        ),
        store,
    )


def test_file_precedes_environment(tmp_path):
    resolver, store = _resolver(
        tmp_path,
        environment={"CUSTY_GITHUB_TOKEN": "environment-secret"},
    )
    store.write_token_file("github.token", "file-secret")
    material = resolver.resolve_material("https://github.com/org/project.git")
    assert material is not None
    assert material.provider is CredentialProvider.GITHUB
    assert material.source is CredentialSource.FILE
    assert material.token == "file-secret"

    plan = resolver.plan("https://github.com/org/project.git")
    assert plan.helper == "custy"
    assert plan.terminal_passthrough is False


def test_missing_file_falls_through_to_environment(tmp_path):
    resolver, _ = _resolver(
        tmp_path,
        environment={"CUSTY_GITHUB_TOKEN": "environment-secret"},
    )
    material = resolver.resolve_material("https://github.com/org/project.git")
    assert material is not None
    assert material.source is CredentialSource.ENVIRONMENT


@pytest.mark.parametrize(
    "remote_url",
    [
        "git@github.com:org/project.git",
        "ssh://git@github.com/org/project.git",
        "https://example.com/org/project.git",
        "https://github.com.evil.example/org/project.git",
    ],
)
def test_ssh_and_unapproved_hosts_stay_native(tmp_path, remote_url):
    resolver, store = _resolver(tmp_path)
    store.write_token_file("github.token", "file-secret")
    assert resolver.resolve_material(remote_url) is None


def test_native_mode_never_reads_external_material(tmp_path):
    resolver, store = _resolver(tmp_path, mode="native")
    store.write_token_file("github.token", "file-secret")
    assert resolver.resolve_material("https://github.com/org/project.git") is None


def test_container_only_preserves_local_credentials(tmp_path):
    resolver, store = _resolver(tmp_path, is_container=False)
    store.write_token_file("github.token", "file-secret")
    assert resolver.resolve_material("https://github.com/org/project.git") is None


def test_noninteractive_plan_disables_git_prompt(tmp_path):
    resolver, _ = _resolver(tmp_path, is_interactive=False)
    plan = resolver.plan("https://github.com/org/project.git")
    assert plan.helper is None
    assert plan.environment == {"GIT_TERMINAL_PROMPT": "0"}
    assert plan.terminal_passthrough is False


def test_interactive_plan_gives_native_git_terminal_ownership(tmp_path):
    resolver, _ = _resolver(tmp_path, is_interactive=True)

    plan = resolver.plan("https://github.com/org/project.git")

    assert plan.helper is None
    assert plan.environment == {}
    assert plan.terminal_passthrough is True
    assert plan.reason == "native Git authentication with interactive fallback"


def test_malformed_existing_file_stops_instead_of_falling_through(tmp_path):
    environment = {"CUSTY_GITHUB_TOKEN": "environment-secret"}
    resolver, store = _resolver(tmp_path, environment=environment)
    path = store.resolve_token_path("github.token")
    path.parent.mkdir(parents=True)
    path.write_text("invalid\nsecond-line\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="exactly one"):
        resolver.resolve_material("https://github.com/org/project.git")

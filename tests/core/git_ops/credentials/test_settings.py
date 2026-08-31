# tests/core/git_ops/credentials/test_settings.py

"""Tests for strict Git credential policy loading."""

from pathlib import Path

import pytest

from app.config.config_loader import ConfigLoader
from app.core.git_ops.credentials import CredentialMode, CredentialProvider
from app.core.git_ops.credentials.settings import CredentialSettingsLoader
from app.core.shared import ConfigurationError


def _loader(tmp_path: Path, body: str = "") -> CredentialSettingsLoader:
    config_path = tmp_path / "config.toml"
    config_path.write_text(f"[tool.custy.git.credentials]\n{body}\n", encoding="utf-8")
    return CredentialSettingsLoader(ConfigLoader(config_path))


def test_missing_section_uses_native_safe_defaults(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("[tool.custy]\n", encoding="utf-8")
    settings = CredentialSettingsLoader(ConfigLoader(path)).load()
    assert settings.mode is CredentialMode.NATIVE
    assert settings.container_only is True
    assert settings.providers[CredentialProvider.GITHUB].enabled is False


def test_custom_policy_and_provider_are_loaded(tmp_path):
    settings = _loader(
        tmp_path,
        'mode = "auto"\n'
        "container_only = false\n"
        'source_order = ["environment", "file"]\n'
        "interactive_fallback = false\n"
        "fail_non_interactive = true\n\n"
        "[tool.custy.git.credentials.github]\n"
        "enabled = true\n"
        'username = "automation"\n'
        'token_file = "custom.token"\n'
        'token_env = "CUSTOM_GITHUB_TOKEN"',
    ).load()
    github = settings.providers[CredentialProvider.GITHUB]
    assert settings.mode is CredentialMode.AUTO
    assert [source.value for source in settings.source_order] == [
        "environment",
        "file",
    ]
    assert github.enabled is True
    assert github.username == "automation"


@pytest.mark.parametrize(
    "body, expected",
    [
        ('mode = "unsupported"', "Unsupported"),
        ('source_order = ["vault"]', "file"),
        ('container_only = "yes"', "boolean"),
        (
            '[tool.custy.git.credentials.github]\ntoken_env = "NOT VALID"',
            "environment-variable",
        ),
    ],
)
def test_invalid_policy_is_rejected(tmp_path, body, expected):
    with pytest.raises(ConfigurationError, match=expected):
        _loader(tmp_path, body).load()

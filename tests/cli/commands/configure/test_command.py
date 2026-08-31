# tests/cli/commands/configure/test_command.py

"""Tests for the public credential configuration CLI."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from click.utils import strip_ansi
from typer.testing import CliRunner

from app.cli.commands.configure import command
from app.core.git_ops.credentials import CredentialMode, CredentialProvider
from app.core.shared import ConfigurationError

runner = CliRunner()


def test_set_environment_never_accepts_or_prompts_for_token(monkeypatch):
    service = MagicMock()
    service.settings.providers.__getitem__.return_value = SimpleNamespace(
        token_env="CUSTY_GITHUB_TOKEN"
    )
    service.set_provider.return_value = None
    monkeypatch.setattr(command, "_service", lambda: service)
    result = runner.invoke(
        command.credentials_app,
        [
            "set",
            "--provider",
            "github",
            "--source",
            "environment",
            "--token-env",
            "MY_GITHUB_TOKEN",
        ],
    )
    assert result.exit_code == 0
    service.set_provider.assert_called_once()
    assert service.set_provider.call_args.kwargs["token"] is None
    assert "MY_GITHUB_TOKEN" in result.output
    service.ensure_initialized_config.assert_called_once_with()


def test_status_does_not_render_token_values(monkeypatch):
    service = MagicMock()
    service.settings = SimpleNamespace(
        mode=CredentialMode.AUTO,
        container_only=True,
        source_order=[],
    )
    service.store.credential_root.return_value = "external-root"
    service.statuses.return_value = [
        SimpleNamespace(
            provider=CredentialProvider.GITHUB,
            enabled=True,
            username="x-access-token",
            token_path="github.token",
            file_status="valid",
            environment_name="CUSTY_GITHUB_TOKEN",
            environment_status="missing",
        )
    ]
    monkeypatch.setattr(command, "_service", lambda: service)
    result = runner.invoke(command.credentials_app, ["status"])
    assert result.exit_code == 0
    assert "Token values are never displayed" in result.output
    assert "password=" not in result.output


def test_help_has_no_visible_token_option():
    result = runner.invoke(
        command.credentials_app,
        ["set", "--help"],
        color=False,
        terminal_width=160,
    )
    help_output = strip_ansi(result.output)

    assert result.exit_code == 0
    assert "--token-file" in help_output
    assert "--token-env" in help_output
    assert "--token " not in help_output


def test_hidden_token_prompt_rejects_noninteractive_input(monkeypatch):
    monkeypatch.setattr(command.sys.stdin, "isatty", lambda: False)
    prompt = MagicMock()
    monkeypatch.setattr(command.typer, "prompt", prompt)

    with pytest.raises(ConfigurationError, match="docker run -it"):
        command._prompt_personal_access_token()

    prompt.assert_not_called()


def test_hidden_token_prompt_uses_confirmation_in_interactive_terminal(monkeypatch):
    monkeypatch.setattr(command.sys.stdin, "isatty", lambda: True)
    prompt = MagicMock(return_value="secret-value")
    monkeypatch.setattr(command.typer, "prompt", prompt)

    assert command._prompt_personal_access_token() == "secret-value"
    prompt.assert_called_once_with(
        "Personal access token",
        hide_input=True,
        confirmation_prompt=True,
    )

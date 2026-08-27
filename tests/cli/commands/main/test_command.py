# tests/cli/commands/main/test_command.py

"""Tests for the root Custy command and its informational options."""

from typer.testing import CliRunner

from app.cli.commands.main import command
from app.cli.main import app

runner = CliRunner()


def test_main_callable_exists():
    """The root callback remains available for application registration."""

    assert callable(command.main)


def test_help_exits_successfully():
    """Explicit help renders usage information and reports success."""

    result = runner.invoke(app, ["--help", "--no-banner"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_no_subcommand_shows_help_and_exits_successfully():
    """A discovery invocation is valid and must not look like a failure."""

    result = runner.invoke(app, ["--no-banner"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_version_exits_successfully():
    """Explicit version output reports success for shell and Docker use."""

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "Custy" in result.output

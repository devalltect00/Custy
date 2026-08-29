# tests/logging/test_dry_run.py

"""
tests/logging/test_dry_run.py

Unit tests for dry-run helpers and Runner.
"""

import subprocess
from unittest.mock import MagicMock

import app.core.dry_run.dry_run as dry_run_module
from app.core.dry_run.dry_run import (
    Runner,
    format_command,
)


class TestDryRunHelpers:
    def test_format_command_list(self):
        assert format_command(["git", "status"]) == "git status"

    def test_format_command_string(self):
        assert format_command("git status") == "git status"


class TestRunner:
    def test_default_state(self):
        runner = Runner()

        assert runner.get_is_dry_run() is False
        assert runner.get_silent() is False

    def test_setters(self):
        runner = Runner()

        runner.set_is_dry_run(True)
        runner.set_silent(True)

        assert runner.get_is_dry_run() is True
        assert runner.get_silent() is True

    def test_run_dry_run(self):
        runner = Runner(is_dry_run=True)

        assert runner.run(["git", "status"]) is None

    def test_run_dry_run_logs_formatted_command(self, monkeypatch):
        """Simulated list commands are logged in shell-readable form."""

        logged = MagicMock()
        monkeypatch.setattr(dry_run_module, "log_dry_run", logged)

        Runner(is_dry_run=True).run(["git", "add", "."])

        logged.assert_called_once_with("git add .")

    def test_check_output_dry_run(self):
        runner = Runner(is_dry_run=True)

        assert runner.check_output(["git", "status"]) is None

    def test_check_output_dry_run_logs_formatted_command(self, monkeypatch):
        """Simulated output commands use the same readable logging."""

        logged = MagicMock()
        monkeypatch.setattr(dry_run_module, "log_dry_run", logged)

        Runner(is_dry_run=True).check_output(["git", "status"])

        logged.assert_called_once_with("git status")

    def test_read_only_command_executes_during_dry_run(self, monkeypatch):
        """Read-only discovery is not suppressed by dry-run mode."""

        runner = Runner(is_dry_run=True)
        proc = MagicMock(spec=subprocess.CompletedProcess)

        subprocess_run = MagicMock(return_value=proc)
        monkeypatch.setattr(subprocess, "run", subprocess_run)

        result = runner.run(
            ["git", "status"],
            read_only=True,
            capture_output=True,
        )

        assert result is proc
        subprocess_run.assert_called_once()

    def test_read_only_check_output_executes_during_dry_run(
        self,
        monkeypatch,
    ):
        """Read-only output collection remains available in previews."""

        runner = Runner(is_dry_run=True)
        check_output = MagicMock(return_value="main\n")
        monkeypatch.setattr(subprocess, "check_output", check_output)

        result = runner.check_output(
            ["git", "branch", "--show-current"],
            read_only=True,
            text=True,
        )

        assert result == "main\n"
        check_output.assert_called_once()

    def test_run_executes_subprocess(self, monkeypatch):
        runner = Runner()

        proc = MagicMock(spec=subprocess.CompletedProcess)

        monkeypatch.setattr(
            subprocess,
            "run",
            lambda *args, **kwargs: proc,
        )

        assert runner.run(["git", "status"]) is proc

    def test_run_adds_safe_shell_default(self, monkeypatch):
        """Runner defaults to direct process execution without a shell."""

        subprocess_run = MagicMock(
            return_value=MagicMock(spec=subprocess.CompletedProcess)
        )
        monkeypatch.setattr(subprocess, "run", subprocess_run)

        Runner().run(["git", "status"])

        assert subprocess_run.call_args.kwargs["shell"] is False

    def test_run_preserves_explicit_shell_setting(self, monkeypatch):
        """An explicit shell setting is forwarded unchanged."""

        subprocess_run = MagicMock(
            return_value=MagicMock(spec=subprocess.CompletedProcess)
        )
        monkeypatch.setattr(subprocess, "run", subprocess_run)

        Runner().run("git status", shell=True)

        assert subprocess_run.call_args.kwargs["shell"] is True

    def test_run_invokes_error_callback(self, monkeypatch):
        """Handled process failures invoke the supplied callback."""

        callback = MagicMock()
        monkeypatch.setattr(
            subprocess,
            "run",
            MagicMock(
                side_effect=subprocess.CalledProcessError(
                    returncode=1,
                    cmd=["git", "status"],
                )
            ),
        )

        result = Runner().run(
            ["git", "status"],
            on_error=callback,
            check=True,
        )

        callback.assert_called_once_with()
        assert result.returncode == 1
        assert result.args == ["git", "status"]

    def test_check_output_decodes_bytes_by_default(self, monkeypatch):
        """Byte output is decoded when text output is expected."""

        monkeypatch.setattr(
            subprocess,
            "check_output",
            MagicMock(return_value=b"develop\n"),
        )

        result = Runner().check_output(["git", "status"])

        assert result == "develop\n"

    def test_check_output_preserves_bytes_when_text_disabled(self, monkeypatch):
        """Callers can explicitly request raw byte output."""

        monkeypatch.setattr(
            subprocess,
            "check_output",
            MagicMock(return_value=b"develop\n"),
        )

        result = Runner().check_output(
            ["git", "status"],
            text=False,
        )

        assert result == b"develop\n"

    def test_check_output_invokes_error_callback(self, monkeypatch):
        """Handled output failures invoke the supplied callback."""

        callback = MagicMock()
        monkeypatch.setattr(
            subprocess,
            "check_output",
            MagicMock(
                side_effect=subprocess.CalledProcessError(
                    returncode=1,
                    cmd=["git", "status"],
                )
            ),
        )

        result = Runner().check_output(
            ["git", "status"],
            on_error=callback,
        )

        callback.assert_called_once_with()
        assert result is None

    def test_silent_runner_suppresses_command_log(self, monkeypatch):
        """Silent execution does not emit the command trace."""

        command_log = MagicMock()
        monkeypatch.setattr(
            dry_run_module,
            "log_command_with_pointing",
            command_log,
        )
        monkeypatch.setattr(
            subprocess,
            "run",
            MagicMock(return_value=MagicMock(spec=subprocess.CompletedProcess)),
        )

        Runner(is_silent=True).run(["git", "status"])

        command_log.assert_not_called()

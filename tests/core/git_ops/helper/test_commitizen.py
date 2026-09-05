# tests/core/git_ops/helper/test_commitizen.py

"""Tests for optional Commitizen discovery and command diagnostics."""

from pathlib import Path
from unittest.mock import MagicMock

from app.core.git_ops.helper.commitizen import CommitizenHelper


class TestCommitizenInspection:
    """Validate configuration and executable detection independence."""

    def test_tool_without_configuration_is_not_configured(self, tmp_path: Path) -> None:
        """A global executable alone must not activate Commitizen."""

        inspection = CommitizenHelper(
            project_root=tmp_path,
            executable_resolver=lambda _: "cz",
        ).inspect()

        assert inspection.configured is False
        assert inspection.available is True

    def test_detects_valid_dedicated_toml(self, tmp_path: Path) -> None:
        """A valid .cz.toml is recognized as project configuration."""

        config_path = tmp_path / ".cz.toml"
        config_path.write_text(
            '[tool.commitizen]\nname = "cz_conventional_commits"\n',
            encoding="utf-8",
        )

        inspection = CommitizenHelper(
            project_root=tmp_path,
            executable_resolver=lambda _: "cz",
        ).inspect()

        assert inspection.config_path == config_path
        assert inspection.valid is True

    def test_reports_malformed_dedicated_toml(self, tmp_path: Path) -> None:
        """Malformed optional configuration is retained as a diagnostic."""

        config_path = tmp_path / ".cz.toml"
        config_path.write_text("[tool.commitizen\n", encoding="utf-8")

        inspection = CommitizenHelper(
            project_root=tmp_path,
            executable_resolver=lambda _: None,
        ).inspect()

        assert inspection.config_path == config_path
        assert inspection.valid is False
        assert inspection.config_error

    def test_detects_pyproject_section(self, tmp_path: Path) -> None:
        """Commitizen metadata embedded in pyproject.toml is recognized."""

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.commitizen]\nname = "cz_conventional_commits"\n',
            encoding="utf-8",
        )

        inspection = CommitizenHelper(
            project_root=tmp_path,
            executable_resolver=lambda _: "cz",
        ).inspect()

        assert inspection.config_path == pyproject
        assert inspection.valid is True


class TestCommitizenCommands:
    """Verify message validation captures rather than discards tool output."""

    def test_check_commit_uses_message_file_and_retains_stderr(
        self,
        tmp_path: Path,
    ) -> None:
        """A failed check remains a structured non-zero result."""

        helper = CommitizenHelper(
            project_root=tmp_path,
            executable_resolver=lambda _: "cz",
        )
        completed = MagicMock(
            returncode=1,
            stdout="",
            stderr="invalid commit message",
        )
        helper.runner.run = MagicMock(return_value=completed)
        message_file = tmp_path / "commit.txt"

        result = helper.check_commit(message_file)

        assert result.success is False
        assert result.stderr == "invalid commit message"
        helper.runner.run.assert_called_once()
        assert helper.runner.run.call_args.args[0] == [
            "cz",
            "check",
            "--commit-msg-file",
            str(message_file),
        ]

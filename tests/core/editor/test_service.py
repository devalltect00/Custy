# tests/core/editor/test_service.py

"""Unit tests for cross-platform editor discovery and launch behavior."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from app.core.editor import EditorService, EditorSettings
from app.core.exceptions.validation_error import ValidationError


def _completed(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Return a successful completed process for an editor command."""

    return subprocess.CompletedProcess(command, 0, "", "")


class TestEditorCandidateResolution:
    """Tests for environment and platform candidate ordering."""

    def test_environment_editors_precede_posix_defaults(self) -> None:
        """VISUAL and EDITOR take priority over built-in Linux candidates."""

        service = EditorService(
            environment={"VISUAL": "nvim -f", "EDITOR": "nano"},
            platform_name="linux",
            container_resolver=lambda: False,
        )

        candidates = service.resolve_candidates()

        assert [candidate.command for candidate in candidates] == [
            ("nvim", "-f"),
            ("nano",),
            ("micro",),
            ("vim",),
            ("vi",),
        ]
        assert candidates[0].requires_terminal is True

    def test_windows_defaults_do_not_include_terminal_editors(self) -> None:
        """Windows resolution uses VS Code followed by Notepad."""

        service = EditorService(
            environment={},
            platform_name="win32",
            container_resolver=lambda: False,
        )

        candidates = service.resolve_candidates()

        assert [candidate.command for candidate in candidates] == [
            ("code", "--wait"),
            ("notepad",),
        ]

    def test_configuration_can_disable_environment_and_builtin_fallback(self) -> None:
        """An explicit list can be the complete editor selection policy."""

        settings = EditorSettings.from_mapping(
            {
                "prefer_environment": False,
                "allow_fallback": False,
                "candidates": {"windows": ["notepad"]},
            }
        )
        service = EditorService(
            environment={"VISUAL": "code --wait"},
            platform_name="win32",
            settings=settings,
            container_resolver=lambda: False,
        )

        assert [candidate.command for candidate in service.resolve_candidates()] == [
            ("notepad",),
        ]


class TestEditorLaunch:
    """Tests for safe subprocess execution and fallback behavior."""

    def test_uses_environment_editor_without_shell(self, tmp_path: Path) -> None:
        """An installed VISUAL command runs with arguments and shell disabled."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("feat: test editor", encoding="utf-8")
        runner = MagicMock(
            return_value=_completed(["custom-editor", "--wait", str(message_file)])
        )
        resolver = MagicMock(return_value="/usr/bin/custom-editor")
        service = EditorService(
            environment={"VISUAL": "custom-editor --wait"},
            platform_name="linux",
            executable_resolver=resolver,
            command_runner=runner,
            interactive_resolver=lambda: True,
            container_resolver=lambda: False,
        )

        selected = service.open_file(message_file, label="commit message")

        assert selected == ("custom-editor", "--wait")
        resolver.assert_called_once_with("custom-editor")
        runner.assert_called_once_with(
            ["/usr/bin/custom-editor", "--wait", str(message_file)],
            check=True,
            shell=False,
        )

    def test_falls_back_to_nano_in_interactive_linux(self, tmp_path: Path) -> None:
        """Nano is selected when VS Code is absent and a TTY is available."""

        message_file = tmp_path / "tag-message.txt"
        message_file.write_text("Release notes", encoding="utf-8")
        runner = MagicMock(return_value=_completed(["nano", str(message_file)]))
        resolver = MagicMock(
            side_effect=lambda executable: (
                "/usr/bin/nano" if executable == "nano" else None
            )
        )
        service = EditorService(
            environment={},
            platform_name="linux",
            executable_resolver=resolver,
            command_runner=runner,
            interactive_resolver=lambda: True,
            container_resolver=lambda: False,
        )

        selected = service.open_file(message_file, label="tag message")

        assert selected == ("nano",)
        assert resolver.call_args_list == [call("micro"), call("nano")]
        runner.assert_called_once_with(
            ["/usr/bin/nano", str(message_file)],
            check=True,
            shell=False,
        )

    def test_does_not_fallback_after_editor_process_failure(
        self,
        tmp_path: Path,
    ) -> None:
        """A started editor failure does not unexpectedly open another editor."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("fix: recover editor", encoding="utf-8")
        runner = MagicMock(
            side_effect=subprocess.CalledProcessError(1, ["micro"]),
        )
        service = EditorService(
            environment={},
            platform_name="linux",
            executable_resolver=lambda executable: f"/usr/bin/{executable}",
            command_runner=runner,
            interactive_resolver=lambda: True,
            container_resolver=lambda: False,
        )

        with pytest.raises(ValidationError) as error_info:
            service.open_file(message_file)

        assert error_info.value.code == "EDITOR_PROCESS_FAILED"
        assert runner.call_count == 1

    def test_falls_back_after_editor_spawn_failure(self, tmp_path: Path) -> None:
        """An operating-system launch failure advances to the next candidate."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("fix: recover editor", encoding="utf-8")
        runner = MagicMock(
            side_effect=[
                OSError("cannot start micro"),
                _completed(["nano", str(message_file)]),
            ]
        )
        service = EditorService(
            environment={},
            platform_name="linux",
            executable_resolver=lambda executable: f"/usr/bin/{executable}",
            command_runner=runner,
            interactive_resolver=lambda: True,
            container_resolver=lambda: False,
        )

        selected = service.open_file(message_file)

        assert selected == ("nano",)
        assert runner.call_count == 2

    def test_launches_resolved_windows_cmd_path(self, tmp_path: Path) -> None:
        """Windows launches the resolved VS Code CMD shim instead of bare code."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("fix: use vscode", encoding="utf-8")
        resolved_code = r"C:\Users\tester\VS Code\bin\code.CMD"
        runner = MagicMock(return_value=_completed([resolved_code, "--wait"]))
        service = EditorService(
            environment={},
            platform_name="win32",
            executable_resolver=lambda executable: (
                resolved_code if executable == "code" else None
            ),
            command_runner=runner,
            interactive_resolver=lambda: True,
            container_resolver=lambda: False,
        )

        selected = service.open_file(message_file)

        assert selected == ("code", "--wait")
        runner.assert_called_once_with(
            [resolved_code, "--wait", str(message_file)],
            check=True,
            shell=False,
        )

    def test_noninteractive_terminal_editor_has_actionable_error(
        self,
        tmp_path: Path,
    ) -> None:
        """A non-TTY run explains how Docker users can enable Nano."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("feat: prepared message", encoding="utf-8")
        service = EditorService(
            environment={},
            platform_name="linux",
            executable_resolver=lambda executable: (
                "/usr/bin/nano" if executable == "nano" else None
            ),
            interactive_resolver=lambda: False,
            container_resolver=lambda: False,
        )

        with pytest.raises(ValidationError) as error_info:
            service.open_file(message_file)

        error = error_info.value
        assert error.code == "EDITOR_LAUNCH_FAILED"
        assert "include -it" in (error.hint or "")
        assert error.context is not None
        assert error.context["interactive"] is False
        assert "interactive TTY required" in error.context["attempted"]

    def test_dry_run_does_not_resolve_or_launch_editor(self, tmp_path: Path) -> None:
        """Dry-run reports the intended editor without process execution."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("feat: preview", encoding="utf-8")
        resolver = MagicMock()
        runner = MagicMock()
        service = EditorService(
            environment={},
            platform_name="linux",
            executable_resolver=resolver,
            command_runner=runner,
            container_resolver=lambda: False,
        )

        selected = service.open_file(message_file, dry_run=True)

        assert selected == ("micro",)
        resolver.assert_not_called()
        runner.assert_not_called()

    def test_missing_message_file_is_rejected(self, tmp_path: Path) -> None:
        """A missing configured file fails before editor resolution."""

        service = EditorService(
            environment={},
            platform_name="linux",
            container_resolver=lambda: False,
        )

        with pytest.raises(ValidationError) as error_info:
            service.open_file(tmp_path / "missing.txt")

        assert error_info.value.code == "EDITOR_FILE_NOT_FOUND"

    def test_empty_policy_reports_actionable_error(self, tmp_path: Path) -> None:
        """Empty candidates without fallback fail as configuration intends."""

        message_file = tmp_path / "commit-message.txt"
        message_file.write_text("feat: no editor", encoding="utf-8")
        settings = EditorSettings.from_mapping(
            {
                "prefer_environment": False,
                "allow_fallback": False,
                "candidates": {"linux": []},
            }
        )
        service = EditorService(
            environment={},
            platform_name="linux",
            settings=settings,
            container_resolver=lambda: False,
        )

        with pytest.raises(ValidationError) as error_info:
            service.open_file(message_file)

        assert error_info.value.code == "EDITOR_LAUNCH_FAILED"
        assert error_info.value.context is not None
        assert error_info.value.context["attempted"] == "No editor candidates resolved."


class TestContainerEditorResolution:
    """Tests for container-specific configured editor commands."""

    def test_container_candidates_use_packaged_configuration(self) -> None:
        """Container editor commands load Custy's non-conflicting keybindings."""

        settings = EditorSettings.from_mapping(
            {
                "prefer_environment": False,
                "allow_fallback": False,
                "candidates": {"container": ["micro", "nano", "vim", "vi"]},
            }
        )
        service = EditorService(
            environment={},
            platform_name="linux",
            settings=settings,
            container_resolver=lambda: True,
        )

        assert [candidate.command for candidate in service.resolve_candidates()] == [
            ("micro", "-config-dir", "/etc/custy/editors/micro"),
            ("nano", "--rcfile", "/etc/custy/editors/nanorc"),
            ("vim", "-u", "/etc/custy/editors/vimrc"),
            ("vi", "-u", "/etc/custy/editors/vimrc"),
        ]

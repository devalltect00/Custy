# app/core/editor/service.py

"""Resolve and launch editors for interactive Custy workflows.

The service keeps platform detection, environment-variable handling, executable
discovery, terminal requirements, and subprocess behavior out of the workflow
orchestrator. Editor commands always run without a shell so paths and arguments
cannot be reinterpreted by a platform shell.
"""

from __future__ import annotations

import logging
import os
import shlex
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.core.editor.settings import EditorIdentifier, EditorSettings
from app.core.exceptions.validation_error import ValidationError

logger = logging.getLogger(__name__)

CommandRunner = Callable[..., subprocess.CompletedProcess[Any]]
ExecutableResolver = Callable[[str], str | None]
InteractiveResolver = Callable[[], bool]
ContainerResolver = Callable[[], bool]


@dataclass(frozen=True)
class EditorCandidate:
    """Describe one editor command that Custy may attempt.

    Args:
        command: Executable and arguments without the target file.
        source: Human-readable source of the candidate.
        requires_terminal: Whether the editor needs an interactive terminal.
    """

    command: tuple[str, ...]
    source: str
    requires_terminal: bool = False

    @property
    def display_name(self) -> str:
        """Return the command in a readable diagnostic form."""

        return " ".join(self.command)


class EditorService:
    """Open workflow message files with an available platform editor.

    Resolution order:
        1. ``VISUAL`` and ``EDITOR`` when environment precedence is enabled.
        2. Configured container or operating-system candidates.
        3. Built-in candidates when fallback is enabled.

    Terminal editors are skipped when standard input or output is not connected
    to a TTY. Project configuration uses known identifiers, while environment
    variables may provide an advanced custom command.
    """

    _TERMINAL_EDITORS = frozenset(
        {
            "nano",
            "micro",
            "vi",
            "vim",
            "nvim",
        }
    )

    def __init__(
        self,
        *,
        environment: Mapping[str, str] | None = None,
        platform_name: str | None = None,
        executable_resolver: ExecutableResolver = shutil.which,
        command_runner: CommandRunner = subprocess.run,
        interactive_resolver: InteractiveResolver | None = None,
        container_resolver: ContainerResolver | None = None,
        settings: EditorSettings | None = None,
    ) -> None:
        """Create an editor service with replaceable system dependencies.

        Args:
            environment: Environment used for ``VISUAL`` and ``EDITOR``.
            platform_name: Platform identifier such as ``win32`` or ``linux``.
            executable_resolver: Function used to locate an executable.
            command_runner: Function used to execute the selected command.
            interactive_resolver: Function that reports terminal availability.
            container_resolver: Function that reports container execution.
            settings: Validated editor ordering and fallback preferences.

        Notes:
            Dependency injection keeps editor behavior deterministic in tests
            without launching real applications.
        """

        self.environment = environment if environment is not None else os.environ
        self.platform_name = platform_name or sys.platform
        self.executable_resolver = executable_resolver
        self.command_runner = command_runner
        self.interactive_resolver = (
            interactive_resolver or self._standard_streams_are_interactive
        )
        self.container_resolver = container_resolver or self._running_in_container
        self.settings = settings or EditorSettings()

    def open_file(
        self,
        path: Path,
        *,
        label: str = "file",
        dry_run: bool = False,
    ) -> tuple[str, ...]:
        """Open a file and wait until the selected editor exits.

        Args:
            path: Existing file to open.
            label: Human-friendly file description used in messages.
            dry_run: Simulate editor launch without starting a process.

        Returns:
            The selected editor command, excluding the target file.

        Raises:
            ValidationError: If the file is missing or no editor can be used.

        Notes:
            Every command is executed with ``shell=False``. In Docker, use an
            interactive container (``-it``) for Nano or another terminal editor.
        """

        file_path = Path(path)
        if not file_path.is_file():
            raise ValidationError(
                message=f"The {label} file cannot be opened because it does not exist.",
                hint="Create or restore the configured message file, then retry.",
                code="EDITOR_FILE_NOT_FOUND",
                context={"file": str(file_path)},
            )

        candidates = self.resolve_candidates()
        if not candidates:
            self._raise_no_editor(file_path, interactive=False, attempted=[])

        if dry_run:
            selected = candidates[0]
            logger.info(
                "[dry_run](dry-run)[/dry_run] Would open %s with %s: %s",
                label,
                selected.display_name,
                file_path,
            )
            return selected.command

        interactive = self.interactive_resolver()
        attempted: list[str] = []

        for candidate in candidates:
            executable = candidate.command[0]

            if candidate.requires_terminal and not interactive:
                attempted.append(f"{candidate.display_name} (interactive TTY required)")
                continue

            resolved_executable = self.executable_resolver(executable)
            if resolved_executable is None:
                attempted.append(f"{candidate.display_name} (not installed)")
                logger.debug(
                    "Editor candidate unavailable: command=%s source=%s",
                    candidate.display_name,
                    candidate.source,
                )
                continue

            try:
                launch_command = [
                    resolved_executable,
                    *candidate.command[1:],
                    str(file_path),
                ]
                if attempted:
                    logger.info(
                        "📝 Using %s for %s after skipping: %s",
                        candidate.display_name,
                        label,
                        "; ".join(attempted),
                    )
                else:
                    logger.info(
                        "📝 Using %s for %s.",
                        candidate.display_name,
                        label,
                    )
                self.command_runner(
                    launch_command,
                    check=True,
                    shell=False,
                )
            except OSError as error:
                attempted.append(f"{candidate.display_name} ({error})")
                logger.debug(
                    "Editor launch failed: command=%s source=%s error=%s",
                    candidate.display_name,
                    candidate.source,
                    error,
                )
                continue
            except subprocess.CalledProcessError as error:
                raise ValidationError(
                    message=(
                        f"The selected editor exited with an error while editing "
                        f"the {label}."
                    ),
                    hint=(
                        "Review the editor output, then retry. Custy does not open "
                        "another editor after an editor process has started."
                    ),
                    code="EDITOR_PROCESS_FAILED",
                    context={
                        "file": str(file_path),
                        "editor": candidate.display_name,
                        "return_code": error.returncode,
                    },
                ) from error

            logger.info(
                "✅ Finished editing %s with %s.", label, candidate.display_name
            )
            return candidate.command

        self._raise_no_editor(file_path, interactive, attempted)

    def _raise_no_editor(
        self,
        file_path: Path,
        interactive: bool,
        attempted: list[str],
    ) -> None:
        """Raise a structured error when no candidate can be launched."""

        attempted_text = "; ".join(attempted) or "No editor candidates resolved."
        raise ValidationError(
            message="Unable to open an editor for the workflow message file.",
            hint=(
                "Review tool.custy.editor, or set VISUAL or EDITOR to an "
                "installed editor. When running Custy in Docker, include -it "
                "so a terminal editor can use the terminal."
            ),
            code="EDITOR_LAUNCH_FAILED",
            context={
                "file": str(file_path),
                "platform": self.platform_name,
                "interactive": interactive,
                "attempted": attempted_text,
            },
        )

    def resolve_candidates(self) -> tuple[EditorCandidate, ...]:
        """Return deduplicated environment and platform editor candidates.

        Returns:
            Editor candidates in deterministic preference order.
        """

        candidates: list[EditorCandidate] = []

        if self.settings.prefer_environment:
            for variable in ("VISUAL", "EDITOR"):
                raw_command = self.environment.get(variable, "").strip()
                if not raw_command:
                    continue

                command = self._split_command(raw_command)
                if command:
                    candidates.append(
                        EditorCandidate(
                            command=command,
                            source=variable,
                            requires_terminal=self._requires_terminal(command),
                        )
                    )

        selected_identifiers, source = self._configured_identifiers()
        candidates.extend(
            self._candidate_from_identifier(identifier, source)
            for identifier in selected_identifiers
        )

        if self.settings.allow_fallback:
            defaults = EditorSettings()
            fallback_identifiers = (
                defaults.container
                if self._is_container
                else (
                    defaults.windows
                    if self._is_windows
                    else defaults.macos if self._is_macos else defaults.linux
                )
            )
            candidates.extend(
                self._candidate_from_identifier(identifier, "built-in fallback")
                for identifier in fallback_identifiers
            )

        return self._deduplicate(candidates)

    def _configured_identifiers(
        self,
    ) -> tuple[tuple[EditorIdentifier, ...], str]:
        """Return the candidate list for the active runtime environment."""

        if self._is_container:
            return self.settings.container, "container configuration"
        if self._is_windows:
            return self.settings.windows, "Windows configuration"
        if self._is_macos:
            return self.settings.macos, "macOS configuration"
        return self.settings.linux, "Linux configuration"

    def _candidate_from_identifier(
        self,
        identifier: EditorIdentifier,
        source: str,
    ) -> EditorCandidate:
        """Build a platform-aware command for a supported editor identifier."""

        commands: dict[EditorIdentifier, tuple[str, ...]] = {
            EditorIdentifier.VSCODE: ("code", "--wait"),
            EditorIdentifier.NOTEPAD: ("notepad",),
            EditorIdentifier.MICRO: ("micro",),
            EditorIdentifier.NANO: ("nano",),
            EditorIdentifier.VIM: ("vim",),
            EditorIdentifier.VI: ("vi",),
            EditorIdentifier.NEOVIM: ("nvim",),
        }
        command = commands[identifier]

        if self._is_container:
            if identifier is EditorIdentifier.MICRO:
                command = (
                    "micro",
                    "-config-dir",
                    "/etc/custy/editors/micro",
                )
            elif identifier is EditorIdentifier.NANO:
                command = (
                    "nano",
                    "--rcfile",
                    "/etc/custy/editors/nanorc",
                )
            elif identifier in {EditorIdentifier.VIM, EditorIdentifier.VI}:
                command = (
                    command[0],
                    "-u",
                    "/etc/custy/editors/vimrc",
                )

        return EditorCandidate(
            command=command,
            source=source,
            requires_terminal=identifier
            in {
                EditorIdentifier.MICRO,
                EditorIdentifier.NANO,
                EditorIdentifier.VIM,
                EditorIdentifier.VI,
                EditorIdentifier.NEOVIM,
            },
        )

    @property
    def _is_windows(self) -> bool:
        """Return whether the configured platform is Windows."""

        return self.platform_name.lower().startswith("win")

    @property
    def _is_macos(self) -> bool:
        """Return whether the configured platform is macOS."""

        return self.platform_name.lower() == "darwin"

    @property
    def _is_container(self) -> bool:
        """Return whether the service is running inside a container."""

        return self.container_resolver()

    def _split_command(self, raw_command: str) -> tuple[str, ...]:
        """Split an editor environment value into executable arguments."""

        try:
            command = shlex.split(raw_command, posix=not self._is_windows)
        except ValueError as error:
            logger.warning("Ignoring invalid editor command %r: %s", raw_command, error)
            return ()

        return tuple(part.strip('"') for part in command if part)

    def _requires_terminal(self, command: tuple[str, ...]) -> bool:
        """Return whether a command names a known terminal editor."""

        executable_name = Path(command[0]).name.lower()
        return executable_name in self._TERMINAL_EDITORS

    def _deduplicate(
        self,
        candidates: list[EditorCandidate],
    ) -> tuple[EditorCandidate, ...]:
        """Remove repeated editor commands without changing preference order."""

        unique: list[EditorCandidate] = []
        seen: set[tuple[str, ...]] = set()

        for candidate in candidates:
            identity = tuple(
                part.lower() if self._is_windows else part for part in candidate.command
            )
            if identity in seen:
                continue
            seen.add(identity)
            unique.append(candidate)

        return tuple(unique)

    @staticmethod
    def _standard_streams_are_interactive() -> bool:
        """Return whether both standard input and output are terminal streams."""

        return sys.stdin.isatty() and sys.stdout.isatty()

    def _running_in_container(self) -> bool:
        """Detect a supported container runtime without external commands."""

        marker = self.environment.get("CUSTY_CONTAINER", "").strip().lower()
        if marker in {"1", "true", "yes", "on"}:
            return True
        return Path("/.dockerenv").exists()

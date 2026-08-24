# app/core/dry_run/dry_run.py

import subprocess
import logging
from collections.abc import Callable
# from rich import print as rprint

# from colorama import Fore, Style, init

##### Avoid import this, because the error appear. Errors might be looks like: 
#####   ImportError: cannot import name 'DryRunSupport' from partially initialized module
#####   'app.core.helper.dry_run' (most likely due to a circular import)
##### or something like that
# from app.utils import setup_logging 

from typing import Union, List

# init(autoreset=True)
# setup_logging(level=logging.INFO)
# logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def format_command(command: Union[str, List[str]]) -> str:
    """
    Convert command into a clean shell-like string.
    """
    if isinstance(command, list):
        return " ".join(command)
    return command

def log_command(command: str):
    logger.debug(
        "[primary]cmd[/primary]: [text]%s[/text]",
        command
    )

def log_command_with_pointing(command: str):
    logger.debug(
        "[pointing]→[/pointing] [text]%s[/text]",
        command
    )

def log_dry_run(command: str):
    logger.info(
        "[dry_run](dry-run)[/dry_run] "
        "[success]✔[/success] "
        "Simulated: [text]%s[/text]",
        command
    )


class Runner:
    """Execute subprocess commands with explicit dry-run semantics.

    Dry-run mode skips commands by default because callers are assumed to
    request a mutation. Callers must explicitly mark read-only discovery with
    ``read_only=True`` when it is safe and useful to execute during a preview.
    """

    def __init__(self, is_dry_run: bool = False, is_silent: bool = False):
        self.is_dry_run: bool = is_dry_run
        self.silent: bool = is_silent

    def set_is_dry_run(self, is_dry_run: bool) -> None:
        self.is_dry_run = is_dry_run

    def get_is_dry_run(self) -> bool:
        return self.is_dry_run

    def set_silent(self, is_silent: bool) -> None:
        self.silent = is_silent

    def get_silent(self) -> bool:
        return self.silent

    def run(
        self,
        command: Union[str, List[str]],
        on_error: Callable[[], None] | None = None,
        *,
        read_only: bool = False,
        **kwargs,
    ) -> subprocess.CompletedProcess | None:
        """Run a command or simulate it during dry-run mode.

        Args:
            command:
                Command passed to ``subprocess.run``.

            on_error:
                Optional callback invoked for a failed command.

            read_only:
                Execute the command during dry-run because it performs only
                discovery and cannot mutate project or remote state.

            **kwargs:
                Additional ``subprocess.run`` keyword arguments.

        Returns:
            Completed process for executed commands, otherwise ``None`` for a
            simulated mutation or handled command failure.
        """
        # If user did not pass `shell`, ue default
        if "shell" not in kwargs:
            kwargs["shell"] = False  # safest default

        # command = command if isinstance(command, str) else " ".join(command)

        if not self.is_dry_run or read_only:
            if not self.get_silent():
                # print(f"{Fore.YELLOW}→{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{command}{Style.RESET_ALL}",)
                # rprint(
                #     # f"{Fore.YELLOW}→{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{command}{Style.RESET_ALL}",
                #     f"[yellow]→[/yellow] [white]{command}[/white]"
                # )
                # cmd_str = " ".join(command)
                # logger.debug("[yellow]cmd[/yellow]: [white]%s[/white]", cmd_str)
                # logger.debug("[yellow]cmd[/yellow]: [white]%s[/white]", command)
                cmd_str = format_command(command=command)
                log_command_with_pointing(cmd_str)
                # log_command(cmd_str)
            try:
                # Avoid `shell=False` when passing **untrusted input**, to prevent shell injection attacks.
                result = subprocess.run(command, **kwargs)
                return result
            except subprocess.CalledProcessError:
                if on_error:
                    on_error()
                return None
        else:
            # logger.info(f"{Fore.CYAN}(dry-run){Style.RESET_ALL} ✅ Simulated: {command}")
            # logger.info(f"[cyan](dry-run)[/cyan] ✅ Simulated: %s", command)
            log_dry_run(format_command(command))
            return None

    def check_output(
        self,
        command: Union[str, List[str]],
        on_error: Callable[[], None] | None = None,
        *,
        read_only: bool = False,
        **kwargs,
    ) -> str | None:
        """Return command output or simulate a mutating command.

        Args:
            command:
                Command passed to ``subprocess.check_output``.

            on_error:
                Optional callback invoked for a failed command.

            read_only:
                Execute the command during dry-run because it performs only
                discovery.

            **kwargs:
                Additional ``subprocess.check_output`` keyword arguments.

        Returns:
            Command output, or ``None`` when the command is simulated or its
            failure is handled.
        """
        # If user did not pass `shell`, ue default
        if "shell" not in kwargs:
            kwargs["shell"] = False  # safest default

        if not self.is_dry_run or read_only:
            if not self.get_silent():
                # logger.debug(f"{Fore.YELLOW}→{Style.RESET_ALL} {command}")
                # rprint(
                #     # f"{Fore.YELLOW}→{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{command}{Style.RESET_ALL}",
                #     f"[yellow]→[/yellow] {command}"
                # )
                # cmd_str = " ".join(command)
                # logger.debug("[yellow]→[/yellow] %s", cmd_str)
                # logger.debug("[pointing]→[/pointing] %s", command)
                cmd_str = format_command(command=command)
                # log_command_with_pointing(command)
                log_command_with_pointing(cmd_str)
                # log_command(cmd_str)
            try:
                # Avoid `shell=False` when passing **untrusted input**, to prevent shell injection attacks.
                output = subprocess.check_output(command, **kwargs)
                return (
                    output.decode()
                    if isinstance(output, bytes) and kwargs.get("text", True)
                    else output
                )
            except subprocess.CalledProcessError:
                if on_error:
                    on_error()
                return None
        else:
            # logger.info(f"[cyan](dry-run)[/cyan] ✅ Simulated: %s", command)
            log_dry_run(format_command(command))
            return None

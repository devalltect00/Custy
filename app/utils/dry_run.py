# app\utils\dry_run.py

import subprocess
from collections.abc import Callable

from colorama import Fore, Style


class Runner:
    def __init__(self, is_dry_run: bool = False):
        self.is_dry_run: bool = is_dry_run
        self.silent: bool = False

    def run(
        self,
        command: str,
        on_error: Callable[[], None] | None = None,
        **kwargs,
    ) -> subprocess.CompletedProcess | None:
        """
        Run a shell command and handle any error with a custom function.

        Additional subprocess.run() arguments can be passed via kwargs.
        """
        # If user did not pass `shell`, ue default
        if "shell" not in kwargs:
            kwargs["shell"] = False  # safest default

        # command = command if isinstance(command, str) else " ".join(command)

        if not self.is_dry_run:
            if not self.silent:
                print(
                    f"{Fore.YELLOW}→{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{command}{Style.RESET_ALL}",
                )
            try:
                # Avoid `shell=False` when passing **untrusted input**, to prevent shell injection attacks.
                result = subprocess.run(command, **kwargs)
                return result
            except subprocess.CalledProcessError:
                if on_error:
                    on_error()
                return None
        else:
            print(f"{Fore.CYAN}(dry-run){Style.RESET_ALL} ✅ Simulated: {command}")
            return None

    def check_output(
        self,
        command: str,
        on_error: Callable[[], None] | None = None,
        **kwargs,
    ) -> str | None:
        """ """
        # If user did not pass `shell`, ue default
        if "shell" not in kwargs:
            kwargs["shell"] = False  # safest default

        if not self.is_dry_run:
            if not self.silent:
                print(f"{Fore.YELLOW}→{Style.RESET_ALL} {command}")

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
            print(f"{Fore.CYAN}(dry-run){Style.RESET_ALL} ✅ Simulated: {command}")
            return None

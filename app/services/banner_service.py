# app/services/banner_service.py

import pathlib
from importlib.metadata import PackageNotFoundError, version

from rich import print
from pyfiglet import Figlet

from app.theme import theme


class BannerService:
    def __init__(self, package_name: str = "", font: str = "cosmic"):
        self.package_name = package_name
        self.font = font

    # -------------------------
    # VERSION RESOLUTION
    # -------------------------
    def get_version(self) -> str:
        try:
            return version(self.package_name)
        except PackageNotFoundError:
            return self._get_local_version()

    def _get_local_version(self) -> str:
        try:
            here = pathlib.Path(__file__).resolve()
            version_path = here.parent.parent / "__version__.py"

            if version_path.exists():
                with open(version_path) as f:
                    for line in f:
                        if "__version__" in line:
                            return line.split("=")[-1].strip().strip('"')
        except Exception:
            pass

        return "0.0.0"

    # -------------------------
    # BANNER RENDER
    # -------------------------
    def render_banner(self) -> str:
        fig = Figlet(font=self.font)
        name = self.package_name.replace("-", " ").replace("_", " ").upper()
        return fig.renderText(name)

    def render_version(self) -> str:
        return f"v{self.get_version()}"

    # -------------------------
    # DISPLAY
    # -------------------------
    def show(self):
        banner = self.render_banner()
        version = self.render_version()

        # BOLD_ORANGE = "\033[1;38;5;208m"
        # BOLD_WHITE = "\033[1;97m"
        # RESET = "\033[0m"

        # print(f"\n{BOLD_ORANGE}{banner}{RESET}")
        # print(f"{BOLD_WHITE}{version.center(57)}{RESET}\n")

        print(f"\n[bold {theme.primary}]{banner}[/bold {theme.primary}]")
        print(f"[{theme.secondary}]{version.center(theme.center)}[/{theme.secondary}]\n")

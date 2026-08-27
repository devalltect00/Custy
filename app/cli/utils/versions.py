# app/cli/utils/versions.py

import typer
import typer.rich_utils
from rich import print as rprint

from app.theme import theme
from app.ui.banner import banner


def get_version():
    __version__ = banner.get_version()
    return __version__


def version_callback(value: bool):
    if value:
        __version__ = banner.get_version()
        rprint(
            f"[{theme.primary}]Custy[/{theme.primary}]: [{theme.secondary}]{__version__}[/{theme.secondary}]"
        )
        raise typer.Exit(
            code=0,
        )

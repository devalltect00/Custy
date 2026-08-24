# app/cli/main.py

"""
Main CLI application.

Entrypoint for Custy.
"""

from app.cli.commands import (
    main_command,
    init_command,
    validate_command,
    git_ops_command,
    changelog_command,
    workflow_command,
    version_command,
    backup_command,
    cleanup_command,
)
import typer
from rich.console import Console
import typer.rich_utils
from typer.main import get_command
from typing import Annotated
from rich import print as rprint
import logging
import sys

from app.theme import theme
# from app.cli.commands import push, misc
from app.cli.utils import banner, version_callback
from app.ui.console import console
from app.utils import setup_logging
from app.cli.context.app_context import AppContext, get_context
from app.cli.constants.args import CliArgs
from app.config.config_loader import get_config

from .commands.main.options import *
from .commands.main.resolver import resolve_main_args

from app.cli.commands.run import command

typer.rich_utils._console = console

app = typer.Typer(
    add_help_option=False,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

# @app.callback()
# def main(
#     no_banner: bool = typer.Option(False, "--no-banner", help="Disable banner"),
# ):
#     if not no_banner:
#         show_banner()


app.callback(invoke_without_command=True)(main_command.main)

# =========================
# Sub-apps
# Groups (multi-command)
# =========================
# Register command groups
# app.add_typer(push.app, name="push", help="Push commits and tags to remote repository.")
# app.add_typer(misc.app, name="misc", help="Miscellaneous commands.")
app.add_typer(changelog_command.app, name="changelog")
app.add_typer(workflow_command.app, name="workflow")
app.add_typer(version_command.app, name="version")
app.add_typer(backup_command.app, name="backup")
app.add_typer(cleanup_command.app, name="cleanup")
# app.add_typer(commit_tag_command.app, name="commit-tag")

# =========================
# Direct commands
# Single commands
# =========================
app.command(name="init")(init_command.init)
app.command(name="validate")(validate_command.validate)
app.command(name="commit")(git_ops_command.commit)
app.command(name="tag")(git_ops_command.tag)
app.command(name="push")(git_ops_command.push)
# app.command(name="changelog")(changelog_command.generate)

# =========================
# Pipeline executor
# =========================
app.command(name="run")(command.run)

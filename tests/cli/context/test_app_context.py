# tests/cli/context/test_app_context.py

"""
tests/cli/context/test_app_context.py

Unit tests for AppContext and get_context().
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.cli.context.app_context import AppContext, get_context
from app.cli.constants.enums import LogLevelChoices


class TestAppContext:

    def test_defaults(self):
        ctx = AppContext()

        assert ctx.dry_run is False
        assert ctx.debug is False
        assert ctx.log_level == LogLevelChoices.INFO
        assert ctx.validated is False
        assert ctx.data == {}

    def test_update_from_args(self):
        ctx = AppContext()

        args = SimpleNamespace(
            dry_run=True,
            log_level=LogLevelChoices.DEBUG,
            commit_message_file="commit.txt",
            tag_message_file="tag.txt",
            version_file="version.py",
            no_debug=False,
        )

        ctx.update_from_args(args, debug_flag=True)

        assert ctx.dry_run is True
        assert ctx.log_level == LogLevelChoices.DEBUG
        assert ctx.commit_message_file == "commit.txt"
        assert ctx.tag_message_file == "tag.txt"
        assert ctx.version_file == "version.py"
        assert ctx.debug is True
        assert ctx.args is args

    def test_update_from_args_without_debug(self):
        ctx = AppContext()

        args = SimpleNamespace(
            dry_run=False,
            log_level=LogLevelChoices.INFO,
        )

        ctx.update_from_args(args, debug_flag=False)

        assert ctx.debug is False

    def test_get_context_creates_context(self):
        typer_ctx = MagicMock()
        typer_ctx.obj = None

        result = get_context(typer_ctx)

        assert isinstance(result, AppContext)
        assert typer_ctx.obj is result
        assert result.typer_ctx is typer_ctx

    def test_get_context_reuses_existing_context(self):
        existing = AppContext()

        typer_ctx = MagicMock()
        typer_ctx.obj = existing

        result = get_context(typer_ctx)

        assert result is existing
        assert result.typer_ctx is typer_ctx

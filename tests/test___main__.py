# tests/test___main__.py

"""
tests/test___main__.py

Unit tests for the Custy CLI entrypoint.

These tests verify that the module entrypoint delegates execution to the
Typer application and that the module-level main() function acts as the
single CLI entrypoint.
"""

from unittest.mock import MagicMock

from app import __main__


class TestMain:
    """Tests for the application entrypoint."""

    # ==========================================================
    # main()
    # ==========================================================

    def test_main_invokes_protected_error_boundary(
        self,
        monkeypatch,
    ):
        """Runs the lazy CLI callback through centralized error handling."""

        handler = MagicMock()

        monkeypatch.setattr(
            __main__,
            "handle_cli_errors",
            handler,
        )

        __main__.main()

        handler.assert_called_once_with(__main__._load_and_run_cli)

    # ==========================================================
    # __main__
    # ==========================================================

    # def test_running_module_executes_main(
    #     self,
    #     monkeypatch,
    # ):
    #     """Executes main() when the module is run as '__main__'."""

    #     called = False

    #     def fake_main():
    #         nonlocal called
    #         called = True

    #     monkeypatch.setattr(
    #         __main__,
    #         "main",
    #         fake_main,
    #     )

    #     runpy.run_module(
    #         "app.__main__",
    #         run_name="__main__",
    #     )

    #     assert called is True

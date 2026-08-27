# app/__main__.py

"""Protected entry point for the Custy CLI.

Usage:
    python -m app ...
"""

from app.cli.error_handler import handle_cli_errors


def _load_and_run_cli() -> None:
    """Import and invoke the Typer application inside the error boundary."""

    from app.cli.main import app

    app()


def main() -> None:
    """Run Custy with centralized user-facing exception handling."""

    handle_cli_errors(_load_and_run_cli)


if __name__ == "__main__":
    main()

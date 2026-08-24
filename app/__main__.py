# app/__main__.py

"""
Entrypoint for Custy CLI.

Usage:
    python -m app ...
"""

from app.cli.main import app

def main():
    app()

if __name__ == "__main__":
    main()

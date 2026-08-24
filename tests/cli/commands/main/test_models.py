# tests/cli/commands/main/test_models.py

"""Tests for app.cli.commands.main.models."""
from app.cli.commands.main.models import MainArgs
from app.cli.constants import LogLevelChoices

def test_main_args_construction():
    args=MainArgs(False,False,None,True,False,LogLevelChoices.INFO)
    assert args.dry_run is True
    assert args.log_level==LogLevelChoices.INFO

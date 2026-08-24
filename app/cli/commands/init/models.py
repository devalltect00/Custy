# app/cli/commands/init/models.py

from dataclasses import dataclass

from app.cli.constants import InitMode

@dataclass
class InitArgs:
  mode: InitMode
  force_init: bool
  ask: bool

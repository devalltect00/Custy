# app\utils\dry_run_support.py

from .dry_run import Runner


class DryRunSupport:
    def __init__(self, dry_run: bool = False):
        self.runner = Runner(dry_run)

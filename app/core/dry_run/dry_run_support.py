# app/core/dry_run/dry_run_support.py

from .dry_run import Runner


class DryRunSupport:
    def __init__(self, dry_run: bool = False, is_silent: bool = False):
        self.runner = Runner(dry_run, is_silent)

# tests/logging/test_dry_run_support.py

"""
tests/logging/test_dry_run_support.py

Unit tests for DryRunSupport.
"""

from app.core.dry_run.dry_run import Runner
from app.core.dry_run.dry_run_support import DryRunSupport


class TestDryRunSupport:

    def test_default_runner(self):
        support = DryRunSupport()

        assert isinstance(support.runner, Runner)
        assert support.runner.get_is_dry_run() is False
        assert support.runner.get_silent() is False

    def test_custom_flags(self):
        support = DryRunSupport(
            dry_run=True,
            is_silent=True,
        )

        assert support.runner.get_is_dry_run() is True
        assert support.runner.get_silent() is True

    def test_runner_is_reusable(self):
        support = DryRunSupport()

        support.runner.set_is_dry_run(True)

        assert support.runner.get_is_dry_run() is True

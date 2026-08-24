# tests/cli/constants/test_enums.py

"""
tests/cli/constants/test_enums.py

Unit tests for CLI enums.
"""

from app.cli.constants.enums import (
    StrategyChoices,
    BumpChoices,
    StageModeChoices,
    LogLevelChoices,
    CleanupTypeChoices,
    InitMode,
    StepChoices,
)


class TestEnums:

    def test_strategy_values(self):
        assert StrategyChoices.SEMVER.value == "semver"
        assert StrategyChoices.PEP440.value == "pep440"

    def test_bump_values(self):
        assert BumpChoices.PATCH.value == "patch"
        assert BumpChoices.AUTO.value == "auto"

    def test_stage_mode_values(self):
        assert StageModeChoices.ALL.value == "all"
        assert StageModeChoices.UPDATE.value == "update"
        assert StageModeChoices.MANUAL.value == "manual"

    def test_log_level_case_insensitive(self):
        assert LogLevelChoices("debug") is LogLevelChoices.DEBUG
        assert LogLevelChoices("INFO") is LogLevelChoices.INFO

    def test_cleanup_values(self):
        assert CleanupTypeChoices.ALL.value == "all"
        assert CleanupTypeChoices.BRANCH.value == "branch"

    def test_init_modes(self):
        assert InitMode.ALL.value == "all"
        assert InitMode.CONFIG.value == "config"

    def test_step_choices(self):
        values = {e.value for e in StepChoices}
        assert {"commit", "tag", "push", "dev", "release", "full"} == values

# tests/config/test_config_resolution.py

"""
tests/config/test_config_resolution.py

Additional tests focused on ConfigLoader.resolve().
"""

import pytest

from app.config.config_loader import ConfigLoader
from app.core.shared import ConfigurationError

CONFIG = """
[tool.custy.cli.execution]
dry_run = true

[tool.custy.logging]
level = "warning"

[tool.custy.git]
auto_push = false
"""


class TestResolvePriority:
    @pytest.fixture
    def loader(self, tmp_path):
        path = tmp_path / "config.toml"
        path.write_text(CONFIG)
        return ConfigLoader(path)

    def test_cli_overrides_config(self, loader):
        assert loader.resolve("debug", ["logging", "level"], "info") == "debug"

    def test_config_overrides_default(self, loader):
        assert loader.resolve(None, ["logging", "level"], "info") == "warning"

    def test_default_used_when_missing(self, loader):
        assert loader.resolve(None, ["missing", "value"], "fallback") == "fallback"

    def test_false_is_preserved(self, loader):
        assert loader.resolve(False, ["git", "auto_push"], True) is False

    def test_false_can_fallback_to_config(self, loader):
        assert (
            loader.resolve(
                False,
                ["cli", "execution", "dry_run"],
                treat_false_as_none=True,
            )
            is True
        )

    def test_required_missing(self, loader):
        with pytest.raises(ConfigurationError):
            loader.resolve(None, ["does", "not", "exist"], required=True)

    def test_required_with_cli(self, loader):
        assert loader.resolve(123, ["missing"], required=True) == 123

    def test_required_with_config(self, loader):
        assert loader.resolve(None, ["logging", "level"], required=True) == "warning"

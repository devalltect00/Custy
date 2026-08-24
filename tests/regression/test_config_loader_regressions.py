# tests/regression/test_config_loader_regressions.py

"""
Regression tests for ConfigLoader.

These tests protect the public API and behaviour of the
configuration loader.
"""

from app.config.config_loader import ConfigLoader


class TestConfigLoaderRegressions:
    """
    Regression tests for ConfigLoader.
    """

    def test_loader_can_be_created(self):
        loader = ConfigLoader()

        assert loader is not None

    def test_multiple_loaders_are_independent(self):
        first = ConfigLoader()
        second = ConfigLoader()

        assert first is not second

    def test_expected_public_api_exists(self):
        loader = ConfigLoader()

        assert hasattr(loader, "get")
        assert hasattr(loader, "require")
        assert hasattr(loader, "get_section")
        assert hasattr(loader, "resolve")

    def test_missing_value_returns_default(self):
        loader = ConfigLoader()

        assert loader.get(
            "does_not_exist",
            default="hello",
        ) == "hello"

    def test_missing_nested_value_returns_default(self):
        loader = ConfigLoader()

        assert loader.get(
            "a",
            "b",
            "c",
            default=123,
        ) == 123

    def test_missing_section_returns_empty_dict(self):
        loader = ConfigLoader()

        assert loader.get_section("unknown") == {}

    def test_resolve_prefers_cli_value(self):
        loader = ConfigLoader()

        value = loader.resolve(
            cli_value="cli",
            config_keys=["git", "default_remote"],
            default="origin",
        )

        assert value == "cli"

    def test_resolve_returns_default_when_missing(self):
        loader = ConfigLoader()

        value = loader.resolve(
            cli_value=None,
            config_keys=["missing", "value"],
            default="fallback",
        )

        assert value == "fallback"

    def test_repr_and_str_do_not_raise(self):
        loader = ConfigLoader()

        repr(loader)
        str(loader)

# app/config/config_loader.py

"""
Configuration loader for Custy.

This module provides a centralized configuration system for
loading, validating, and accessing values from:

    .config/custy/config.toml

Features:
    - TOML configuration loading
    - Safe nested configuration access
    - Required configuration validation
    - Configuration section retrieval
    - CLI → Config → Default value resolution
    - Shared singleton configuration access

Configuration Priority:

    1. CLI argument
    2. Configuration file
    3. Default value

Example:

    from app.config.config_loader import get_config

    config = get_config()

    auto_push = config.get("git", "auto_push")
    project_source = config.require(
        "project",
        "project_source",
    )
"""

from __future__ import annotations

import logging
import tomllib
from pathlib import Path
from typing import Any

from app.constants.path import CUSTY_SETTINGS
from app.core.shared import ConfigurationError

logger = logging.getLogger("custy.config")


class ConfigLoader:
    """
    Load and access Custy configuration.

    This class loads configuration from:

        .config/custy/config.toml

    and provides helper methods for and provides helper
    methods for retrieving, validating, and resolving
    configuration values.

    Available functionality:

    - get()
        Retrieve nested configuration values safely.

    - require()
        Retrieve a required configuration value and
        raise an exception if it does not exist.

    - get_section()
        Retrieve an entire configuration section.

    - resolve()
        Resolve values using the standard priority:

            CLI argument
            → Configuration file
            → Default value

    Example:

        config = ConfigLoader()

        project_source = config.get(
            "project",
            "project_source",
        )

        auto_push = config.require(
            "git",
            "auto_push",
        )

        template = config.resolve(
            cli_value=template_path,
            config_keys=[
                "cli",
                "templates",
                "commit_message",
            ],
            default="templates/commit.txt",
        )
    """

    def __init__(
        self,
        filename: Path = CUSTY_SETTINGS,
    ) -> None:
        """
        Initialize configuration loader.

        Args:
            filename:
                Path to configuration file.
        """
        self.filename = filename
        self.config: dict[str, Any] = self._load()

    # ---------------------------------------------------------
    # Core Loader
    # ---------------------------------------------------------

    def _load(self) -> dict[str, Any]:
        """
        Load TOML configuration.

        Returns:
            dict: Parsed configuration dictionary.

        Raises:
            ConfigurationError:
                If the configuration file contains
                invalid TOML or cannot be loaded.
        """
        path = Path(self.filename)

        if not path.exists():
            logger.warning(
                "Config file not found: %s",
                self.filename,
            )
            return {}

        try:
            with path.open("rb") as file:
                raw = tomllib.load(file)

            return raw.get("tool", {}).get("custy", {})

        except tomllib.TOMLDecodeError as exc:
            raise ConfigurationError(
                "Invalid TOML format in '%s': %s"
                % (
                    self.filename,
                    exc,
                )
            ) from exc

        except Exception as exc:
            raise ConfigurationError(
                "Failed to load config '%s': %s"
                % (
                    self.filename,
                    exc,
                )
            ) from exc

    # ---------------------------------------------------------
    # Access Helpers
    # ---------------------------------------------------------

    def get(
        self,
        *keys: str,
        default: Any = None,
    ) -> Any:
        """
        Safely retrieve a nested configuration value.

        Example:

            config.get(
                "cli",
                "templates",
                "commit_message",
            )

        Args:
            *keys:
                Nested configuration keys.

            default:
                Default value returned when the
                configuration value is missing.

        Returns:
            any: Configuration value or default.
        """
        value: Any = self.config

        for key in keys:
            if not isinstance(
                value,
                dict,
            ):
                return default

            value = value.get(key)

        return value if value is not None else default

    def require(
        self,
        *keys: str,
    ) -> Any:
        """
        Retrieve a required configuration value.

        Example:

            config.require(
                "git",
                "auto_push",
            )

        Raises:
            ConfigurationError:
                If the value does not exist.
        """
        value = self.get(
            *keys,
            default=None,
        )

        if value is None:
            raise ConfigurationError(f"Missing required config: {'.'.join(keys)}")

        return value

    def get_section(
        self,
        *keys: str,
    ) -> dict[str, Any]:
        """
        Retrieve a configuration section.

        Example:

            config.get_section(
                "cli",
                "templates",
            )

        Returns:
            dict: Section dictionary.

            Returns an empty dictionary if the
            section does not exist.
        """
        value = self.get(
            *keys,
            default={},
        )

        return value if isinstance(value, dict) else {}

    # ---------------------------------------------------------
    # Resolution Helpers
    # ---------------------------------------------------------

    def resolve(
        self,
        cli_value: Any,
        config_keys: list[str],
        default: Any = None,
        *,
        treat_false_as_none: bool = False,
        required: bool = False,
    ) -> Any:
        """
        Resolve a value using Custy's configuration priority.

        Priority:

            1. CLI argument
            2. Configuration file
            3. Default value

        Args:
            cli_value:
                Value provided by CLI.

            config_keys:
                Configuration path.

            default:
                Default fallback value.

            treat_false_as_none:
                Treat False as missing.

            required:
                Raise an exception if no value
                can be resolved.

        ---------------------------------------------------------
        🧪 EXAMPLE USAGE
        ---------------------------------------------------------
        result = config.resolve(
            cli_value=message,
            config_keys=["cli", "templates", "commit_message"],
            default="default.txt"
        )

        ---------------------------------------------------------
        📊 EXAMPLE RESULTS
        ---------------------------------------------------------

        Case 1:
            CLI: "custom.txt"
            Config: "config.txt"
            → Result: "custom.txt"

        Case 2:
            CLI: None
            Config: "config.txt"
            → Result: "config.txt"

        Case 3:
            CLI: None
            Config: None
            Default: "default.txt"
            → Result: "default.txt"

        Case 4 (required=True):
            CLI: None
            Config: None
            → ❌ Raises ValueError

        ---------------------------------------------------------
        ⚙️ PARAMETERS
        ---------------------------------------------------------
        treat_false_as_none:
            Useful for flags like:
                --no-cache (False should fallback to config)

        required:
            If True → raise error when no value found

        ---------------------------------------------------------

        Returns:
            Any:
                The resolved value.

        Raises:
            ConfigurationError:
                When required=True and no value is found or
                no value can be resolved.
        """

        # Handle special case (optional)
        if treat_false_as_none and cli_value is False:
            cli_value = None

        # 1. CLI
        if cli_value is not None:
            return cli_value

        # 2. Config
        config_value = self.get(
            *config_keys,
            default=None,
        )

        if config_value is not None:
            return config_value

        # Required
        if required:
            raise ConfigurationError(
                f"Missing required config: {'.'.join(config_keys)}"
            )

        # 3. Default
        return default


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

_config_instance: ConfigLoader | None = None


def get_config() -> ConfigLoader:
    """
    Get the shared ConfigLoader instance.

    The configuration file is loaded only once and
    reused throughout the application.

    Returns:
        ConfigLoader:
            Shared ConfigLoader instance.

    Example:
        config = get_config()
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = ConfigLoader()

    return _config_instance

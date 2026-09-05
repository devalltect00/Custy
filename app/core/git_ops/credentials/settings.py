# app/core/git_ops/credentials/settings.py

"""Load and validate ``tool.custy.git.credentials`` configuration."""

from __future__ import annotations

import re
from collections.abc import Mapping

from app.config.config_loader import ConfigLoader
from app.core.shared import ConfigurationError

from .models import (
    CredentialMode,
    CredentialProvider,
    CredentialSettings,
    CredentialSource,
    ProviderCredentialSettings,
)

_ENVIRONMENT_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PROVIDER_DEFAULTS = {
    CredentialProvider.GITHUB: {
        "host": "github.com",
        "username": "x-access-token",
        "token_file": "github.token",
        "token_env": "CUSTY_GITHUB_TOKEN",
    },
    CredentialProvider.GITLAB: {
        "host": "gitlab.com",
        "username": "oauth2",
        "token_file": "gitlab.token",
        "token_env": "CUSTY_GITLAB_TOKEN",
    },
}


class CredentialSettingsLoader:
    """Convert the free-form TOML section into strict credential settings."""

    def __init__(self, config: ConfigLoader) -> None:
        """Initialize the loader with the active project configuration."""

        self.config = config

    def load(self) -> CredentialSettings:
        """Return validated settings with backward-compatible native defaults.

        Raises:
            ConfigurationError: If any configured value has an invalid type or
                unsupported value.
        """

        raw = self.config.get("git", "credentials", default=None)
        if raw is None:
            raw = {}
        if not isinstance(raw, Mapping):
            raise ConfigurationError("tool.custy.git.credentials must be a TOML table.")

        mode = self._read_enum(
            raw,
            "mode",
            CredentialMode,
            CredentialMode.NATIVE,
        )
        source_order = self._read_source_order(raw)

        providers: dict[CredentialProvider, ProviderCredentialSettings] = {}
        for provider in CredentialProvider:
            provider_raw = raw.get(provider.value, {})
            if not isinstance(provider_raw, Mapping):
                raise ConfigurationError(
                    f"tool.custy.git.credentials.{provider.value} must be a TOML table."
                )
            defaults = _PROVIDER_DEFAULTS[provider]
            username = self._read_text(
                provider_raw,
                "username",
                str(defaults["username"]),
                prefix=f"tool.custy.git.credentials.{provider.value}",
            )
            token_file = self._read_text(
                provider_raw,
                "token_file",
                str(defaults["token_file"]),
                prefix=f"tool.custy.git.credentials.{provider.value}",
            )
            token_env = self._read_text(
                provider_raw,
                "token_env",
                str(defaults["token_env"]),
                prefix=f"tool.custy.git.credentials.{provider.value}",
            )
            self._validate_single_line(username, f"{provider.value}.username", 1024)
            self._validate_single_line(token_file, f"{provider.value}.token_file", 4096)
            if not _ENVIRONMENT_NAME.fullmatch(token_env):
                raise ConfigurationError(
                    f"tool.custy.git.credentials.{provider.value}.token_env "
                    "must be a valid environment-variable name."
                )

            providers[provider] = ProviderCredentialSettings(
                provider=provider,
                host=str(defaults["host"]),
                enabled=self._read_bool(
                    provider_raw,
                    "enabled",
                    False,
                    prefix=f"tool.custy.git.credentials.{provider.value}",
                ),
                username=username,
                token_file=token_file,
                token_env=token_env,
            )

        return CredentialSettings(
            mode=mode,
            container_only=self._read_bool(
                raw,
                "container_only",
                True,
                prefix="tool.custy.git.credentials",
            ),
            source_order=source_order,
            interactive_fallback=self._read_bool(
                raw,
                "interactive_fallback",
                True,
                prefix="tool.custy.git.credentials",
            ),
            fail_non_interactive=self._read_bool(
                raw,
                "fail_non_interactive",
                True,
                prefix="tool.custy.git.credentials",
            ),
            providers=providers,
        )

    @staticmethod
    def _read_bool(
        raw: Mapping[str, object],
        key: str,
        default: bool,
        *,
        prefix: str,
    ) -> bool:
        """Read a strict boolean without accepting truthy strings or numbers."""

        value = raw.get(key, default)
        if not isinstance(value, bool):
            raise ConfigurationError(f"{prefix}.{key} must be a boolean.")
        return value

    @staticmethod
    def _read_text(
        raw: Mapping[str, object],
        key: str,
        default: str,
        *,
        prefix: str,
    ) -> str:
        """Read and normalize one required text value."""

        value = raw.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ConfigurationError(f"{prefix}.{key} must be a non-empty string.")
        return value.strip()

    @staticmethod
    def _read_enum(raw, key, enum_type, default):
        """Read a string-backed enum and report supported values."""

        value = raw.get(key, default.value)
        if not isinstance(value, str):
            raise ConfigurationError(
                f"tool.custy.git.credentials.{key} must be a string."
            )
        try:
            return enum_type(value.strip().lower())
        except ValueError as exc:
            supported = ", ".join(item.value for item in enum_type)
            raise ConfigurationError(
                f"Unsupported tool.custy.git.credentials.{key}: {value!r}. "
                f"Choose one of: {supported}."
            ) from exc

    @staticmethod
    def _read_source_order(raw: Mapping[str, object]) -> tuple[CredentialSource, ...]:
        """Read a non-empty, duplicate-free external source priority list."""

        value = raw.get("source_order", ["file", "environment"])
        if not isinstance(value, list) or not value:
            raise ConfigurationError(
                "tool.custy.git.credentials.source_order must be a non-empty array."
            )

        sources: list[CredentialSource] = []
        for item in value:
            if not isinstance(item, str):
                raise ConfigurationError(
                    "tool.custy.git.credentials.source_order must contain strings."
                )
            try:
                source = CredentialSource(item.strip().lower())
            except ValueError as exc:
                raise ConfigurationError(
                    "tool.custy.git.credentials.source_order supports only "
                    "'file' and 'environment'."
                ) from exc
            if source not in sources:
                sources.append(source)
        return tuple(sources)

    @staticmethod
    def _validate_single_line(value: str, field_name: str, maximum: int) -> None:
        """Reject control characters and oversized credential metadata."""

        if "\x00" in value or "\n" in value or "\r" in value:
            raise ConfigurationError(
                f"tool.custy.git.credentials.{field_name} must contain one line."
            )
        if len(value) > maximum:
            raise ConfigurationError(
                f"tool.custy.git.credentials.{field_name} is too long."
            )

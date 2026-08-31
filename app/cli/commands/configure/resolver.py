# app/cli/commands/configure/resolver.py

"""Normalization helpers for credential configuration commands."""

import re

from app.cli.commands.configure.models import CredentialSetupArgs
from app.core.git_ops.credentials import CredentialProvider, CredentialSource
from app.core.shared import ConfigurationError

_ENVIRONMENT_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def resolve_provider(value: str | CredentialProvider) -> CredentialProvider:
    """Resolve a supported provider name with a useful error."""

    try:
        return (
            value
            if isinstance(value, CredentialProvider)
            else CredentialProvider(value)
        )
    except ValueError as exc:
        raise ConfigurationError(
            "Unsupported credential provider. Choose 'github' or 'gitlab'."
        ) from exc


def resolve_source(value: str | CredentialSource) -> CredentialSource:
    """Resolve a supported external source name with a useful error."""

    try:
        return value if isinstance(value, CredentialSource) else CredentialSource(value)
    except ValueError as exc:
        raise ConfigurationError(
            "Unsupported credential source. Choose 'file' or 'environment'."
        ) from exc


def resolve_setup_args(
    *,
    provider: CredentialProvider,
    source: CredentialSource,
    username: str | None,
    token_file: str | None,
    token_env: str | None,
    replace: bool,
) -> CredentialSetupArgs:
    """Normalize public CLI values without touching credential material."""

    normalized_username = username.strip() if username else None
    normalized_file = token_file.strip() if token_file else None
    normalized_environment = token_env.strip() if token_env else None
    if normalized_environment and not _ENVIRONMENT_NAME.fullmatch(
        normalized_environment
    ):
        raise ConfigurationError(
            "--token-env must be a valid environment-variable name."
        )
    return CredentialSetupArgs(
        provider=provider,
        source=source,
        username=normalized_username,
        token_file=normalized_file,
        token_env=normalized_environment,
        replace=replace,
    )

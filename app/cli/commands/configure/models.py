# app/cli/commands/configure/models.py

"""Resolved argument models for credential configuration commands."""

from dataclasses import dataclass

from app.core.git_ops.credentials import CredentialProvider, CredentialSource


@dataclass(frozen=True, slots=True)
class CredentialSetupArgs:
    """Normalized non-secret settings for one credential provider."""

    provider: CredentialProvider
    source: CredentialSource
    username: str | None
    token_file: str | None
    token_env: str | None
    replace: bool

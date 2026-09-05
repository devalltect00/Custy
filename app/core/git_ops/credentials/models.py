# app/core/git_ops/credentials/models.py

"""Typed models for Custy's optional Git credential fallback."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class CredentialMode(StrEnum):
    """Select whether Custy participates in Git credential resolution."""

    NATIVE = "native"
    AUTO = "auto"


class CredentialSource(StrEnum):
    """External locations from which a provider token may be read."""

    FILE = "file"
    ENVIRONMENT = "environment"


class CredentialProvider(StrEnum):
    """Public hosting providers supported by the managed fallback."""

    GITHUB = "github"
    GITLAB = "gitlab"


@dataclass(frozen=True, slots=True)
class ProviderCredentialSettings:
    """Validated settings for one supported Git hosting provider."""

    provider: CredentialProvider
    host: str
    enabled: bool
    username: str
    token_file: str
    token_env: str


@dataclass(frozen=True, slots=True)
class CredentialSettings:
    """Validated project policy for optional credential fallback."""

    mode: CredentialMode
    container_only: bool
    source_order: tuple[CredentialSource, ...]
    interactive_fallback: bool
    fail_non_interactive: bool
    providers: dict[CredentialProvider, ProviderCredentialSettings]


@dataclass(frozen=True, slots=True)
class CredentialMaterial:
    """Resolved username and token kept out of normal representations."""

    provider: CredentialProvider
    username: str
    source: CredentialSource
    token: str = field(repr=False)
    token_path: Path | None = None


@dataclass(frozen=True, slots=True)
class CredentialPlan:
    """Per-push plan that preserves native Git credential precedence."""

    provider: CredentialProvider | None = None
    source: CredentialSource | None = None
    helper: str | None = None
    environment: dict[str, str] = field(default_factory=dict)
    terminal_passthrough: bool = False
    reason: str = "native Git authentication"


@dataclass(frozen=True, slots=True)
class CredentialProviderStatus:
    """Non-secret status information shown by the configure command."""

    provider: CredentialProvider
    enabled: bool
    username: str
    token_path: Path
    file_status: str
    environment_name: str
    environment_status: str

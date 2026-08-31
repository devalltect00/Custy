# app/core/git_ops/credentials/resolver.py

"""Resolve provider credentials and per-push Git environment policy."""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Mapping
from urllib.parse import urlsplit

from .models import (
    CredentialMaterial,
    CredentialMode,
    CredentialPlan,
    CredentialProvider,
    CredentialSettings,
    CredentialSource,
)
from .store import CredentialStore

_SCP_REMOTE = re.compile(r"^(?:[^@/\s]+@)?(?P<host>[^:/\s]+):(?P<path>.+)$")


class CredentialResolver:
    """Apply native-first credential policy to one Git remote URL."""

    def __init__(
        self,
        settings: CredentialSettings,
        store: CredentialStore,
        *,
        environment: Mapping[str, str] | None = None,
        is_container: bool | None = None,
        is_interactive: bool | None = None,
    ) -> None:
        """Initialize runtime facts without reading credential values eagerly."""

        self.settings = settings
        self.store = store
        self.environment = environment if environment is not None else os.environ
        self.is_container = (
            is_container
            if is_container is not None
            else bool(self.environment.get("CUSTY_CONTAINER", "").strip())
        )
        self.is_interactive = (
            is_interactive if is_interactive is not None else sys.stdin.isatty()
        )

    def plan(self, remote_url: str) -> CredentialPlan:
        """Return a non-secret per-push helper and prompt plan."""

        material = self.resolve_material(remote_url)
        environment: dict[str, str] = {}
        prompt_allowed = self.settings.interactive_fallback and self.is_interactive
        if self.settings.fail_non_interactive and not prompt_allowed:
            environment["GIT_TERMINAL_PROMPT"] = "0"

        if material is None:
            return CredentialPlan(
                environment=environment,
                terminal_passthrough=prompt_allowed,
                reason=(
                    "native Git authentication with interactive fallback"
                    if prompt_allowed
                    else "native Git authentication without terminal prompting"
                ),
            )

        return CredentialPlan(
            provider=material.provider,
            source=material.source,
            helper="custy",
            environment=environment,
            reason=f"native Git helpers followed by Custy {material.source.value}",
        )

    def resolve_material(self, remote_url: str) -> CredentialMaterial | None:
        """Resolve external material only when provider policy is active."""

        context = self._provider_for_url(remote_url)
        if context is None:
            return None
        provider, scheme = context
        if scheme != "https" or self.settings.mode is CredentialMode.NATIVE:
            return None
        if self.settings.container_only and not self.is_container:
            return None

        provider_settings = self.settings.providers[provider]
        if not provider_settings.enabled:
            return None

        for source in self.settings.source_order:
            if source is CredentialSource.FILE:
                token = self.store.read_token_file(provider_settings.token_file)
                if token is not None:
                    return CredentialMaterial(
                        provider=provider,
                        username=provider_settings.username,
                        source=source,
                        token=token,
                        token_path=self.store.resolve_token_path(
                            provider_settings.token_file
                        ),
                    )
            elif source is CredentialSource.ENVIRONMENT:
                token = self.store.read_environment_token(provider_settings.token_env)
                if token is not None:
                    return CredentialMaterial(
                        provider=provider,
                        username=provider_settings.username,
                        source=source,
                        token=token,
                    )
        return None

    def _provider_for_url(
        self,
        remote_url: str,
    ) -> tuple[CredentialProvider, str] | None:
        """Map exact public GitHub or GitLab hosts and identify SSH remotes."""

        remote_url = remote_url.strip()
        if not remote_url:
            return None

        scp_match = _SCP_REMOTE.match(remote_url)
        if scp_match and "://" not in remote_url:
            host = scp_match.group("host").lower()
            scheme = "ssh"
        else:
            parsed = urlsplit(remote_url)
            host = (parsed.hostname or "").lower()
            scheme = parsed.scheme.lower()

        for provider, settings in self.settings.providers.items():
            if host == settings.host:
                return provider, scheme
        return None

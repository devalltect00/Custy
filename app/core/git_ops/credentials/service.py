# app/core/git_ops/credentials/service.py

"""High-level setup, status, and per-push credential orchestration."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Mapping
from pathlib import Path

from tomlkit import dumps, parse, table

from app.config.config_loader import ConfigLoader, get_config
from app.core.shared import ConfigurationError

from .models import (
    CredentialPlan,
    CredentialProvider,
    CredentialProviderStatus,
    CredentialSource,
)
from .resolver import CredentialResolver
from .settings import CredentialSettingsLoader
from .store import CredentialStore


class CredentialService:
    """Coordinate safe external storage and project credential preferences."""

    def __init__(
        self,
        config: ConfigLoader | None = None,
        *,
        project_root: Path | None = None,
        environment: Mapping[str, str] | None = None,
        credential_root: Path | None = None,
        is_container: bool | None = None,
        is_interactive: bool | None = None,
    ) -> None:
        """Initialize the service without reading any token material."""

        self.config = config or get_config()
        self.environment = environment if environment is not None else os.environ
        self.store = CredentialStore(
            project_root=project_root,
            environment=self.environment,
            credential_root=credential_root,
        )
        self._is_container = is_container
        self._is_interactive = is_interactive

    @property
    def settings(self):
        """Load current settings so a new CLI invocation sees project edits."""

        return CredentialSettingsLoader(self.config).load()

    def plan_for_remote(self, remote_url: str) -> CredentialPlan:
        """Build a non-secret, native-first plan for one push operation."""

        resolver = CredentialResolver(
            self.settings,
            self.store,
            environment=self.environment,
            is_container=self._is_container,
            is_interactive=self._is_interactive,
        )
        return resolver.plan(remote_url)

    def is_managed_fallback_active(self) -> bool:
        """Return whether this runtime may use Custy's external fallback.

        This check intentionally does not read a token file or environment
        token. It lets dry-run and native-only paths remain secret-free and
        keeps the default Git execution path unchanged.
        """

        settings = self.settings
        if settings.mode.value != "auto":
            return False
        is_container = (
            self._is_container
            if self._is_container is not None
            else bool(self.environment.get("CUSTY_CONTAINER", "").strip())
        )
        if settings.container_only and not is_container:
            return False
        return any(provider.enabled for provider in settings.providers.values())

    def material_for_helper(self, remote_url: str):
        """Resolve material for the Git credential protocol helper process."""

        resolver = CredentialResolver(
            self.settings,
            self.store,
            environment=self.environment,
            is_container=self._is_container,
            is_interactive=self._is_interactive,
        )
        return resolver.resolve_material(remote_url)

    def set_provider(
        self,
        provider: CredentialProvider,
        *,
        source: CredentialSource,
        token: str | None = None,
        token_file: str | None = None,
        token_env: str | None = None,
        username: str | None = None,
        replace: bool = False,
        dry_run: bool = False,
    ) -> Path | None:
        """Enable a provider and optionally store a hidden token externally.

        The token value is never written to ``config.toml``. File-backed setup
        writes it under the external credential root; environment-backed setup
        stores only the environment-variable name.
        """

        self.ensure_initialized_config()
        settings = self.settings
        current = settings.providers[provider]
        selected_file = token_file or current.token_file
        selected_env = token_env or current.token_env
        selected_username = username or current.username

        stored_path: Path | None = None
        if source is CredentialSource.FILE:
            if token is None:
                raise ConfigurationError(
                    "A token is required when configuring the file credential source."
                )
            stored_path = self.store.write_token_file(
                selected_file,
                token,
                replace=replace,
                dry_run=dry_run,
            )

        self._update_config(
            provider,
            enabled=True,
            username=selected_username,
            token_file=selected_file,
            token_env=selected_env,
            preferred_source=source,
            dry_run=dry_run,
        )
        return stored_path

    def remove_provider(
        self,
        provider: CredentialProvider,
        *,
        delete_file: bool = False,
        dry_run: bool = False,
    ) -> tuple[Path, bool]:
        """Disable one provider and delete its file only when explicitly asked."""

        self.ensure_initialized_config()
        current = self.settings.providers[provider]
        path = self.store.resolve_token_path(current.token_file)
        deleted = False
        if delete_file:
            deleted = self.store.delete_token_file(
                current.token_file,
                dry_run=dry_run,
            )
        self._update_config(provider, enabled=False, dry_run=dry_run)
        return path, deleted

    def statuses(self, *, dry_run: bool = False) -> list[CredentialProviderStatus]:
        """Return source availability without exposing credential values.

        Dry-run reports presence only and never opens token files.
        """

        statuses: list[CredentialProviderStatus] = []
        for provider, provider_settings in self.settings.providers.items():
            path = self.store.resolve_token_path(provider_settings.token_file)
            if not path.exists():
                file_status = "missing"
            elif dry_run:
                file_status = "present (not validated in dry-run)"
            else:
                try:
                    self.store.read_token_file(provider_settings.token_file)
                    file_status = "valid"
                except ConfigurationError:
                    file_status = "invalid"
            environment_status = (
                "available"
                if self.environment.get(provider_settings.token_env)
                else "missing"
            )
            statuses.append(
                CredentialProviderStatus(
                    provider=provider,
                    enabled=provider_settings.enabled,
                    username=provider_settings.username,
                    token_path=path,
                    file_status=file_status,
                    environment_name=provider_settings.token_env,
                    environment_status=environment_status,
                )
            )
        return statuses

    def ensure_initialized_config(self) -> None:
        """Validate project configuration before any external file mutation.

        Raises:
            ConfigurationError: If the project configuration is missing,
                unreadable, or invalid TOML.
        """

        path = Path(self.config.filename)
        if not path.is_file():
            raise ConfigurationError(
                "Custy configuration is not initialized. "
                "Run 'custy init --mode config' first."
            )
        try:
            parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            raise ConfigurationError(
                f"Custy configuration cannot be updated safely: {path}: {exc}"
            ) from exc

    def _update_config(
        self,
        provider: CredentialProvider,
        *,
        enabled: bool,
        username: str | None = None,
        token_file: str | None = None,
        token_env: str | None = None,
        preferred_source: CredentialSource | None = None,
        dry_run: bool = False,
    ) -> None:
        """Update only the credential policy in the user-owned TOML document."""

        path = Path(self.config.filename)
        if not path.is_file():
            raise ConfigurationError(
                "Custy configuration is not initialized. Run 'custy init --mode config' first."
            )
        try:
            document = parse(path.read_text(encoding="utf-8"))
            tool = document.setdefault("tool", table())
            custy = tool.setdefault("custy", table())
            git = custy.setdefault("git", table())
            credentials = git.setdefault("credentials", table())
            credentials["mode"] = (
                "auto" if enabled else credentials.get("mode", "native")
            )
            credentials.setdefault("container_only", True)
            credentials.setdefault("interactive_fallback", True)
            credentials.setdefault("fail_non_interactive", True)
            if preferred_source is not None:
                existing = list(credentials.get("source_order", []))
                ordered = [preferred_source.value]
                ordered.extend(item for item in existing if item not in ordered)
                for source in CredentialSource:
                    if source.value not in ordered:
                        ordered.append(source.value)
                credentials["source_order"] = ordered

            provider_table = credentials.setdefault(provider.value, table())
            provider_table["enabled"] = enabled
            if username is not None:
                provider_table["username"] = username
            if token_file is not None:
                provider_table["token_file"] = token_file
            if token_env is not None:
                provider_table["token_env"] = token_env
            rendered = dumps(document)
        except (OSError, ValueError, TypeError) as exc:
            raise ConfigurationError(
                f"Unable to prepare credential configuration update: {exc}"
            ) from exc

        if dry_run:
            return
        self._atomic_write(path, rendered)
        self.config.config = ConfigLoader(path).config

    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        """Replace the TOML document atomically in its existing directory."""

        temporary_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                prefix=f".{path.name}.",
                suffix=".tmp",
                dir=path.parent,
                delete=False,
            ) as temporary:
                temporary_name = temporary.name
                temporary.write(content.rstrip() + "\n")
            os.replace(temporary_name, path)
        except OSError as exc:
            if temporary_name:
                Path(temporary_name).unlink(missing_ok=True)
            raise ConfigurationError(
                f"Unable to update credential configuration at {path}: {exc}"
            ) from exc

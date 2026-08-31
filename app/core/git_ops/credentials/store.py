# app/core/git_ops/credentials/store.py

"""Secure external token-file and environment access for Git credentials."""

from __future__ import annotations

import os
import stat
import tempfile
from collections.abc import Mapping
from pathlib import Path

from app.core.shared import ConfigurationError

MAX_TOKEN_BYTES = 16 * 1024
CREDENTIAL_DIRECTORY_ENV = "CUSTY_CREDENTIALS_DIR"


class CredentialStore:
    """Read and write tokens outside the target project without logging them."""

    def __init__(
        self,
        *,
        project_root: Path | None = None,
        environment: Mapping[str, str] | None = None,
        credential_root: Path | None = None,
    ) -> None:
        """Initialize paths and environment used by the external store."""

        self.project_root = (project_root or Path.cwd()).resolve()
        self.environment = environment if environment is not None else os.environ
        self._credential_root = credential_root

    def credential_root(self) -> Path:
        """Return the platform or runtime-specific external credential root."""

        if self._credential_root is not None:
            return self._credential_root.expanduser().resolve()

        configured = self.environment.get(CREDENTIAL_DIRECTORY_ENV, "").strip()
        if configured:
            path = Path(configured).expanduser()
            if not path.is_absolute():
                path = Path.home() / path
            return path.resolve()

        if self.environment.get("CUSTY_CONTAINER", "").strip():
            return Path("/run/secrets/custy")

        if os.name == "nt":
            local_app_data = self.environment.get("LOCALAPPDATA", "").strip()
            base = (
                Path(local_app_data)
                if local_app_data
                else Path.home() / "AppData/Local"
            )
            return (base / "Custy" / "credentials").resolve()

        data_home = self.environment.get("XDG_DATA_HOME", "").strip()
        base = (
            Path(data_home).expanduser() if data_home else Path.home() / ".local/share"
        )
        return (base / "custy" / "credentials").resolve()

    def resolve_token_path(self, token_file: str) -> Path:
        """Resolve a provider filename and enforce the external-store boundary."""

        raw = Path(token_file).expanduser()
        candidate = raw if raw.is_absolute() else self.credential_root() / raw
        if candidate.is_symlink():
            raise ConfigurationError(
                f"Credential token file must not be a symbolic link: {candidate}"
            )
        resolved = candidate.resolve(strict=False)
        if self._is_within(resolved, self.project_root):
            raise ConfigurationError(
                "Credential token files must be stored outside the target project."
            )
        return resolved

    def read_token_file(self, token_file: str) -> str | None:
        """Read one validated token, returning ``None`` when the file is absent."""

        path = self.resolve_token_path(token_file)
        if not path.exists():
            return None
        if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
            raise ConfigurationError(
                f"Credential token path is not a regular file: {path}"
            )
        if path.stat().st_size > MAX_TOKEN_BYTES:
            raise ConfigurationError(f"Credential token file is too large: {path}")
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise ConfigurationError(
                f"Credential token file cannot be read safely: {path}"
            ) from exc
        return self.validate_token(content, source=f"token file {path}")

    def read_environment_token(self, name: str) -> str | None:
        """Read and validate a token from a named environment variable."""

        value = self.environment.get(name)
        if value is None or value == "":
            return None
        return self.validate_token(value, source=f"environment variable {name}")

    def write_token_file(
        self,
        token_file: str,
        token: str,
        *,
        replace: bool = False,
        dry_run: bool = False,
    ) -> Path:
        """Atomically write a validated token with restrictive file permissions."""

        value = self.validate_token(token, source="interactive token")
        path = self.resolve_token_path(token_file)
        if path.exists() and not replace:
            raise ConfigurationError(
                f"Credential token file already exists: {path}. "
                "Use the explicit replace option after reviewing the target."
            )
        if dry_run:
            return path

        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
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
                temporary.write(value + "\n")
            os.chmod(temporary_name, 0o600)
            os.replace(temporary_name, path)
            os.chmod(path, 0o600)
        except OSError as exc:
            if temporary_name:
                Path(temporary_name).unlink(missing_ok=True)
            raise ConfigurationError(
                f"Unable to store the credential token at {path}: {exc}"
            ) from exc
        return path

    def delete_token_file(self, token_file: str, *, dry_run: bool = False) -> bool:
        """Delete an external regular token file after explicit authorization."""

        path = self.resolve_token_path(token_file)
        if not path.exists():
            return False
        if path.is_symlink() or not path.is_file():
            raise ConfigurationError(
                f"Credential token path is not a removable regular file: {path}"
            )
        if not dry_run:
            path.unlink()
        return True

    @staticmethod
    def validate_token(value: str, *, source: str) -> str:
        """Validate a token as one non-empty UTF-8-compatible logical line."""

        encoded = value.encode("utf-8")
        if len(encoded) > MAX_TOKEN_BYTES:
            raise ConfigurationError(f"Credential from {source} exceeds 16 KiB.")
        normalized = value.rstrip("\r\n")
        if not normalized or "\n" in normalized or "\r" in normalized:
            raise ConfigurationError(
                f"Credential from {source} must contain exactly one non-empty line."
            )
        if "\x00" in normalized:
            raise ConfigurationError(f"Credential from {source} contains a NUL byte.")
        if normalized != normalized.strip():
            raise ConfigurationError(
                f"Credential from {source} must not contain surrounding whitespace."
            )
        return normalized

    @staticmethod
    def _is_within(path: Path, parent: Path) -> bool:
        """Return whether ``path`` is equal to or contained by ``parent``."""

        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False

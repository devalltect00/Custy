# app/core/git_ops/credentials/helper.py

"""Git credential-protocol entry point for Custy's optional fallback."""

from __future__ import annotations

import sys

from app.core.shared import CustyError

from .service import CredentialService

MAX_PROTOCOL_BYTES = 16 * 1024


def _read_request() -> dict[str, str]:
    """Read a bounded Git credential request from standard input."""

    request: dict[str, str] = {}
    consumed = 0
    for line in sys.stdin:
        consumed += len(line.encode("utf-8"))
        if consumed > MAX_PROTOCOL_BYTES:
            raise ValueError("Git credential request is too large.")
        line = line.rstrip("\r\n")
        if not line:
            break
        key, separator, value = line.partition("=")
        if separator and key:
            request[key] = value
    return request


def _remote_url(request: dict[str, str]) -> str:
    """Build the URL information required for exact provider matching."""

    protocol = request.get("protocol", "")
    host = request.get("host", "")
    path = request.get("path", "")
    suffix = f"/{path}" if path else ""
    return f"{protocol}://{host}{suffix}"


def run(operation: str) -> int:
    """Handle one ``get``, ``store``, or ``erase`` credential operation."""

    request = _read_request()
    if operation != "get":
        return 0

    material = CredentialService().material_for_helper(_remote_url(request))
    if material is None:
        return 0

    sys.stdout.write(f"username={material.username}\n")
    sys.stdout.write(f"password={material.token}\n\n")
    sys.stdout.flush()
    return 0


def main() -> None:
    """Run the helper without ever copying credential values into errors."""

    operation = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "get"
    try:
        raise SystemExit(run(operation))
    except (CustyError, OSError, UnicodeError, ValueError) as exc:
        print(f"git-credential-custy: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()

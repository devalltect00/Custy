#!/usr/bin/env python3
# scripts/repository/src/sync_metadata.py

"""Sync GitHub/GitLab metadata using configurable git remote candidates.

Run from the repository root (the directory containing pyproject.toml):
    py scripts/repository/sync_metadata.py --dry-run
    py scripts/repository/sync_metadata.py

Edit GITHUB_REMOTES and GITLAB_REMOTES below. Names are tried in order;
the first remote with a valid URL for that provider wins. These are
fallback candidates, not a list of repositories to update. Discovery uses
each remote's first fetch URL, as returned by `git remote get-url`.

Metadata still comes from:
    [project].description
    [tool.devalltect.github].topics
    [tool.devalltect.gitlab].topics

An empty/missing topics array clears the provider's existing topics.
GitHub uses the first 20 topics, matching the original script.
Requires git, authenticated gh/glab, and Python 3.9+ (tomli before 3.11).
Dry runs only need git and Python; they make no API requests.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Python 3.9 / 3.10
    except ImportError:
        sys.exit("Python < 3.11 requires: pip install tomli")


# User configuration: change remote names here, not inside the functions.
PYPROJECT = Path("pyproject.toml")
## GITHUB_REMOTES = ["github", "origin", "upstream"]
## GITLAB_REMOTES = ["gitlab", "origin", "upstream"]
## GITHUB_TOPIC_LIMIT = 20
GITHUB_REMOTES = ["origin"]
GITLAB_REMOTES = ["backup"]
GITHUB_TOPIC_LIMIT = 50


@dataclass(frozen=True)
class Provider:
    """Data describing a provider; discovery itself is provider-independent."""

    key: str
    label: str
    remotes: Sequence[str]
    hostname: str
    host_aliases: tuple[str, ...] = ()
    allow_subgroups: bool = False


# Aliases must refer to the same service as hostname, which is used for APIs.
# An SSH config host alias can be listed here explicitly if needed.
GITHUB = Provider(
    key="github",
    label="GitHub",
    remotes=GITHUB_REMOTES,
    hostname="github.com",
    host_aliases=("www.github.com",),
)
GITLAB = Provider(
    key="gitlab",
    label="GitLab",
    remotes=GITLAB_REMOTES,
    hostname="gitlab.com",
    host_aliases=("www.gitlab.com",),
    allow_subgroups=True,
)


# Metadata loading: repository URLs are deliberately not read from TOML.
def load_pyproject() -> dict:
    if not PYPROJECT.is_file():
        raise ValueError(f"{PYPROJECT} not found; run from the repository root")
    with PYPROJECT.open("rb") as file:
        return tomllib.load(file)


def get_description(data: dict) -> str:
    description = data.get("project", {}).get("description", "")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("[project].description must be a nonempty string")
    return description.strip()


def get_topics(data: dict, provider: str) -> list[str]:
    topics = (
        data.get("tool", {}).get("devalltect", {}).get(provider, {}).get("topics", [])
    )
    if not isinstance(topics, list):
        raise ValueError(f"[tool.devalltect.{provider}].topics must be a TOML array")
    # Preserve the original topic normalization.
    return [
        str(topic).strip().lower().replace(" ", "-")
        for topic in topics
        if str(topic).strip()
    ]


# Pure parsing: no git calls, metadata loading, or network requests.
def normalize_repository_url(url: str, provider: Provider) -> str:
    """Return owner/repo or group[/subgroup]/project from a clone URL.

    Accept HTTPS, HTTP, SSH, git://, and scp-style [user@]host:path.
    Validate the host for every format, including scp-style SSH.
    """
    url = url.strip()
    if not url or any(character.isspace() for character in url):
        raise ValueError("empty URL or unescaped whitespace in URL")

    if "://" in url:
        try:
            parsed = urlsplit(url)
            hostname = parsed.hostname
            # Accessing port also validates malformed/out-of-range ports.
            _ = parsed.port
        except ValueError:
            raise ValueError("malformed remote URL") from None
        if parsed.scheme not in {"https", "http", "ssh", "git"}:
            raise ValueError("unsupported remote URL scheme")
        if parsed.query or parsed.fragment:
            raise ValueError("expected a clone URL without a query or fragment")
        path = parsed.path
    else:
        match = re.fullmatch(r"(?:[^@/:\s]+@)?([^@/:\s]+):(.+)", url)
        if not match:
            raise ValueError("expected a clone URL, not a local path or identifier")
        hostname, path = match.groups()

    accepted_hosts = {
        host.lower() for host in (provider.hostname, *provider.host_aliases)
    }
    if not hostname or hostname.lower() not in accepted_hosts:
        raise ValueError(f"remote does not point to {provider.label}")

    path = unquote(path).strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = path.split("/")
    if len(parts) < 2 or (not provider.allow_subgroups and len(parts) != 2):
        expected = (
            "group[/subgroup]/project" if provider.allow_subgroups else "owner/repo"
        )
        raise ValueError(f"expected a {expected} repository path")
    # Reject empty/traversal segments, web UI paths (/-/), and characters
    # that could be interpreted as API endpoint syntax or CLI placeholders.
    if any(
        part in {"", ".", "..", "-"} or not re.fullmatch(r"[\w.-]+", part)
        for part in parts
    ):
        raise ValueError("invalid repository path segment")
    return "/".join(parts)


# Shared discovery: the same algorithm is used for both providers.
def discover_repository(provider: Provider) -> str:
    """Try configured remote names in order; return the first valid match."""
    if not provider.remotes:
        raise ValueError(f"No remote candidates configured for {provider.label}")

    result = subprocess.run(
        ["git", "remote"], capture_output=True, text=True, check=True
    )
    available_remotes = set(result.stdout.splitlines())
    failures = []
    for remote in provider.remotes:
        if remote not in available_remotes:
            failures.append(f"{remote!r}: not found")
            continue
        result = subprocess.run(
            ["git", "remote", "get-url", "--", remote],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            failures.append(f"{remote!r}: could not read URL")
            continue
        try:
            repository = normalize_repository_url(result.stdout, provider)
        except ValueError as error:
            # Do not print remote URLs; they may contain embedded credentials.
            failures.append(f"{remote!r}: {error}")
            continue
        print(f"{provider.label}: using remote {remote!r} -> {repository}")
        return repository

    raise ValueError(
        f"No valid {provider.label} remote found. Tried: " + "; ".join(failures)
    )


# Sync logic: only normalized identifiers reach the API endpoints.
def run(*args: str, payload: dict, dry_run: bool = False) -> None:
    print("+", " ".join(args), flush=True)
    print("  JSON:", json.dumps(payload, ensure_ascii=True), flush=True)
    if not dry_run:
        subprocess.run(
            args,
            input=json.dumps(payload),
            text=True,
            encoding="utf-8",
            check=True,
        )


def show_metadata(
    provider: Provider, repository: str, description: str, topics: list[str]
) -> None:
    print(f"\n{provider.label}")
    print(f"Repository:  {repository}")
    print(f"Description: {description}")
    print(f"Topics:      {', '.join(topics) or '(none)'}")


def sync_github(
    repository: str, description: str, topics: list[str], *, dry_run: bool = False
) -> None:
    show_metadata(GITHUB, repository, description, topics)
    endpoint = f"repos/{quote(repository, safe='/')}"
    run(
        "gh",
        "api",
        "--hostname",
        GITHUB.hostname,
        "--method",
        "PATCH",
        endpoint,
        "--input",
        "-",
        payload={"description": description},
        dry_run=dry_run,
    )
    if len(topics) > GITHUB_TOPIC_LIMIT:
        print(f"GitHub: using only the first {GITHUB_TOPIC_LIMIT} topics.")
    # JSON sends an actual empty array when all topics should be removed.
    run(
        "gh",
        "api",
        "--hostname",
        GITHUB.hostname,
        "--method",
        "PUT",
        f"{endpoint}/topics",
        "--input",
        "-",
        payload={"names": topics[:GITHUB_TOPIC_LIMIT]},
        dry_run=dry_run,
    )


def sync_gitlab(
    repository: str, description: str, topics: list[str], *, dry_run: bool = False
) -> None:
    show_metadata(GITLAB, repository, description, topics)
    project_id = quote(repository, safe="")
    run(
        "glab",
        "api",
        "--hostname",
        GITLAB.hostname,
        "--method",
        "PUT",
        f"projects/{project_id}",
        "--input",
        "-",
        # Raw stdin input may not get a JSON content type automatically.
        "--header",
        "Content-Type: application/json",
        payload={"description": description, "topics": topics},
        dry_run=dry_run,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show discovered repositories and API payloads without updating them",
    )
    args = parser.parse_args()

    data = load_pyproject()
    description = get_description(data)
    github_topics = get_topics(data, GITHUB.key)
    gitlab_topics = get_topics(data, GITLAB.key)

    # Resolve both providers before making any remote changes.
    github_repository = discover_repository(GITHUB)
    gitlab_repository = discover_repository(GITLAB)
    if not args.dry_run:
        missing = [command for command in ("gh", "glab") if not shutil.which(command)]
        if missing:
            raise ValueError("Required CLI tools not found: " + ", ".join(missing))

    sync_github(github_repository, description, github_topics, dry_run=args.dry_run)
    sync_gitlab(gitlab_repository, description, gitlab_topics, dry_run=args.dry_run)
    if args.dry_run:
        print("\nDry run complete. No repository metadata was changed.")
    else:
        print("\nRepository metadata synchronized successfully.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(
            f"ERROR: {error.cmd[0]} failed (exit {error.returncode}). "
            "Any earlier successful API updates remain applied.",
            file=sys.stderr,
        )
        if error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as error:
        sys.exit(f"ERROR: {error}")

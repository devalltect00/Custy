# app/cli/commands/configure/options.py

"""Reusable Typer options for ``custy configure credentials``."""

from typing import Annotated

import typer

from app.core.git_ops.credentials import CredentialProvider, CredentialSource

ProviderOption = Annotated[
    CredentialProvider,
    typer.Option(
        "--provider",
        help="Supported token provider: github or gitlab.",
        case_sensitive=False,
        rich_help_panel="Credential Provider",
    ),
]

SourceOption = Annotated[
    CredentialSource,
    typer.Option(
        "--source",
        help="External token source: file or environment.",
        case_sensitive=False,
        rich_help_panel="Credential Source",
    ),
]

UsernameOption = Annotated[
    str | None,
    typer.Option(
        "--username",
        help="HTTPS username sent with the provider token; this is not secret.",
        rich_help_panel="Credential Provider",
    ),
]

TokenFileOption = Annotated[
    str | None,
    typer.Option(
        "--token-file",
        help=(
            "Filename under the external credential directory, or an approved "
            "absolute path outside the project."
        ),
        rich_help_panel="Credential Source",
    ),
]

TokenEnvironmentOption = Annotated[
    str | None,
    typer.Option(
        "--token-env",
        help="Name of the environment variable that supplies the token.",
        rich_help_panel="Credential Source",
    ),
]

ReplaceOption = Annotated[
    bool,
    typer.Option(
        "--replace",
        help="Explicitly replace an existing external token file.",
        rich_help_panel="Safety",
    ),
]

DeleteFileOption = Annotated[
    bool,
    typer.Option(
        "--delete-file",
        help="Also delete the provider's external token file.",
        rich_help_panel="Safety",
    ),
]

RemoteOption = Annotated[
    str,
    typer.Option(
        "--remote",
        help="Git remote to test with read-only git ls-remote.",
        rich_help_panel="Remote Access",
    ),
]

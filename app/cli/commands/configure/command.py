# app/cli/commands/configure/command.py

"""CLI commands for safe, optional Git credential fallback configuration."""

from __future__ import annotations

import sys

import typer
from rich.table import Table

from app.cli.commands.configure.options import (
    DeleteFileOption,
    ProviderOption,
    RemoteOption,
    ReplaceOption,
    SourceOption,
    TokenEnvironmentOption,
    TokenFileOption,
    UsernameOption,
)
from app.cli.commands.configure.resolver import (
    resolve_provider,
    resolve_setup_args,
    resolve_source,
)
from app.cli.context.app_context import get_context
from app.config.config_loader import get_config
from app.core.git_ops.credentials import (
    CredentialProvider,
    CredentialService,
    CredentialSource,
)
from app.core.git_ops.git.factory import create_git_service
from app.core.shared import ConfigurationError
from app.ui.console import console

app = typer.Typer(
    help="Configure user-managed Custy preferences.",
    no_args_is_help=True,
)
credentials_app = typer.Typer(
    help="Configure optional HTTPS token fallback for Git pushes.",
    invoke_without_command=True,
)
app.add_typer(credentials_app, name="credentials")


def _service() -> CredentialService:
    """Build a credential service against the active project configuration."""

    return CredentialService(config=get_config())


def _prompt_personal_access_token() -> str:
    """Read and confirm a token only through a controllable terminal prompt.

    Raises:
        ConfigurationError: If standard input is not attached to an
            interactive terminal that can protect hidden input.

    Notes:
        Docker callers must allocate both interactive input and a TTY with
        ``docker run -it``. Custy deliberately refuses Python's echoed-input
        fallback so a token cannot be exposed accidentally.
    """

    if not sys.stdin.isatty():
        raise ConfigurationError(
            "A hidden personal access token prompt requires an interactive "
            "terminal. For Docker, rerun with 'docker run -it'. Alternatively, "
            "configure '--source environment' and pass the named variable "
            "through a secret-aware runtime."
        )
    return typer.prompt(
        "Personal access token",
        hide_input=True,
        confirmation_prompt=True,
    )


def _print_policy_summary() -> None:
    """Explain the native-first boundary before an interactive setup."""

    console.print(
        "[bold cyan]Git credential fallback setup[/bold cyan]\n\n"
        "Custy keeps normal Git and SSH authentication first. In an enabled "
        "container workflow, a token file or environment variable is used only "
        "as an HTTPS fallback. Tokens are never written to config.toml or "
        "printed by this command."
    )


def _apply_setup(
    ctx: typer.Context,
    *,
    provider: CredentialProvider,
    source: CredentialSource,
    username: str | None,
    token_file: str | None,
    token_env: str | None,
    replace: bool,
    token: str | None,
) -> None:
    """Apply one normalized provider setup and render a safe result."""

    args = resolve_setup_args(
        provider=provider,
        source=source,
        username=username,
        token_file=token_file,
        token_env=token_env,
        replace=replace,
    )
    app_context = get_context(ctx)
    service = _service()
    stored_path = service.set_provider(
        args.provider,
        source=args.source,
        token=token,
        token_file=args.token_file,
        token_env=args.token_env,
        username=args.username,
        replace=args.replace,
        dry_run=app_context.dry_run,
    )

    if app_context.dry_run:
        console.print(
            "[dry_run](dry-run)[/dry_run] Credential policy and external "
            "storage were not changed."
        )
    else:
        console.print(f"[green]✅ {provider.value.title()} fallback enabled.[/green]")
    if stored_path is not None:
        label = "Would store token at" if app_context.dry_run else "Token stored at"
        console.print(f"[dim]{label}: {stored_path}[/dim]")
    elif source is CredentialSource.ENVIRONMENT:
        environment_name = (
            args.token_env or service.settings.providers[provider].token_env
        )
        console.print(
            f"[dim]Supply {environment_name} to the Custy process or container "
            "when pushing.[/dim]"
        )
    console.print(
        "[cyan]Next:[/cyan] custy configure credentials status\n"
        "[cyan]Test:[/cyan] custy configure credentials test --remote origin"
    )


@credentials_app.callback(invoke_without_command=True)
def credentials(ctx: typer.Context) -> None:
    """Configure native-first GitHub or GitLab HTTPS token fallback.

    Normal Git credential helpers and SSH remain the first choice. Custy reads
    an enabled external token only for a supported HTTPS remote and only in the
    configured runtime boundary. Run this command without a subcommand for a
    guided setup.
    """

    if ctx.invoked_subcommand is not None:
        return

    _print_policy_summary()
    provider = resolve_provider(
        typer.prompt("Provider", default=CredentialProvider.GITHUB.value).lower()
    )
    source = resolve_source(
        typer.prompt("Token source", default=CredentialSource.FILE.value).lower()
    )
    service = _service()
    service.ensure_initialized_config()
    defaults = service.settings.providers[provider]
    username = typer.prompt("HTTPS username", default=defaults.username)

    token: str | None = None
    token_file: str | None = None
    token_env: str | None = None
    replace = False
    if source is CredentialSource.FILE:
        token_file = typer.prompt(
            "External token filename", default=defaults.token_file
        )
        target = service.store.resolve_token_path(token_file)
        if target.exists():
            replace = typer.confirm(
                f"External token file already exists at {target}. Replace it?",
                default=False,
            )
            if not replace:
                raise typer.Abort()
        token = _prompt_personal_access_token()
    else:
        token_env = typer.prompt(
            "Environment variable name",
            default=defaults.token_env,
        )

    _apply_setup(
        ctx,
        provider=provider,
        source=source,
        username=username,
        token_file=token_file,
        token_env=token_env,
        replace=replace,
        token=token,
    )


@credentials_app.command(name="set")
def set_credentials(
    ctx: typer.Context,
    provider: ProviderOption,
    source: SourceOption = CredentialSource.FILE,
    username: UsernameOption = None,
    token_file: TokenFileOption = None,
    token_env: TokenEnvironmentOption = None,
    replace: ReplaceOption = False,
) -> None:
    """Enable one provider using a hidden prompt or environment variable.

    File mode prompts securely for the token. There is deliberately no
    ``--token`` option, preventing secrets from entering shell history or the
    process list. Environment mode stores only the variable name.
    """

    _service().ensure_initialized_config()
    token = None
    if source is CredentialSource.FILE:
        token = _prompt_personal_access_token()
    _apply_setup(
        ctx,
        provider=provider,
        source=source,
        username=username,
        token_file=token_file,
        token_env=token_env,
        replace=replace,
        token=token,
    )


@credentials_app.command(name="status")
def credential_status(ctx: typer.Context) -> None:
    """Show policy and source availability without displaying tokens."""

    app_context = get_context(ctx)
    service = _service()
    settings = service.settings
    console.print(
        f"[bold]Mode:[/bold] {settings.mode.value}  "
        f"[bold]Container only:[/bold] {settings.container_only}  "
        f"[bold]Sources:[/bold] "
        f"{', '.join(source.value for source in settings.source_order)}"
    )
    console.print(f"[dim]External root: {service.store.credential_root()}[/dim]")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Provider")
    table.add_column("Enabled")
    table.add_column("Username")
    table.add_column("Token file")
    table.add_column("Environment")
    for status in service.statuses(dry_run=app_context.dry_run):
        table.add_row(
            status.provider.value,
            "yes" if status.enabled else "no",
            status.username,
            f"{status.file_status}\n{status.token_path}",
            f"{status.environment_status}\n{status.environment_name}",
        )
    console.print(table)
    console.print("[dim]Token values are never displayed.[/dim]")


@credentials_app.command(name="test")
def test_credentials(
    ctx: typer.Context,
    remote: RemoteOption = "origin",
) -> None:
    """Test read-only access to one remote with the active policy."""

    app_context = get_context(ctx)
    service = create_git_service(dry_run=app_context.dry_run)
    service.test_remote_access(remote)
    if app_context.dry_run:
        console.print(
            f"[dry_run](dry-run)[/dry_run] Would test remote '{remote}' "
            "without reading credentials or contacting it."
        )
    else:
        console.print(f"[green]✅ Read-only access to '{remote}' succeeded.[/green]")


@credentials_app.command(name="remove")
def remove_credentials(
    ctx: typer.Context,
    provider: ProviderOption,
    delete_file: DeleteFileOption = False,
) -> None:
    """Disable one provider; delete its token file only when requested."""

    app_context = get_context(ctx)
    path, deleted = _service().remove_provider(
        provider,
        delete_file=delete_file,
        dry_run=app_context.dry_run,
    )
    if app_context.dry_run:
        action = "disable the provider"
        if delete_file:
            action += f" and delete {path}"
        console.print(f"[dry_run](dry-run)[/dry_run] Would {action}.")
        return

    console.print(f"[green]✅ {provider.value.title()} fallback disabled.[/green]")
    if delete_file:
        result = "Deleted" if deleted else "No file found at"
        console.print(f"[dim]{result}: {path}[/dim]")
    else:
        console.print(
            f"[dim]External token file was preserved: {path}. "
            "Use --delete-file for explicit removal.[/dim]"
        )

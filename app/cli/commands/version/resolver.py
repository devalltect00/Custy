# app/cli/commands/version/resolver.py

from app.cli.commands.version.models import VersionArgs

from app.cli.constants import StrategyChoices
from app.core.git_ops.helper import detect_project_strategy

def resolve_version_args(config, cli_args) -> VersionArgs:
  return VersionArgs(
    version_file=config.resolve(
        cli_args.version_file,
        ["cli", "paths", "version_file"],
        "app/__version__.py",
    ),
    tag=cli_args.tag,
    strategy=config.resolve(
        cli_args.strategy,
        ["cli", "versioning", "strategy"],
        detect_project_strategy(no_debug=True) or StrategyChoices.SEMVER,
    ),
    bump=config.resolve(
        cli_args.bump,
        ["cli", "versioning", "bump"],
        None,
    ),
  )

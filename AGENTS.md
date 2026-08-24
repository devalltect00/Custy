# AGENTS.md

## Project overview

Custy is a configuration-driven Python CLI for repeatable project and Git release workflows. It supports project initialization and validation, version updates, changelog generation, commit/tag/push operations, reusable pipelines, backups, cleanup, dry-run previews, and multi-remote synchronization.

The application is intended for both interactive use and automation. Preserve predictable CLI behavior, clear terminal output, safe defaults, and configuration compatibility.

## Supported user-facing commands

Primary direct commands include:

```text
custy init
custy validate
custy version update
custy changelog generate
custy backup ...
custy cleanup ...
custy commit
custy tag
custy push
custy run ...
```

Public `custy run` steps and profiles are:

```text
commit
tag
push
dev
release
full
```

Do not present internal pipeline entries as supported public profiles. `custy workflow branch` is experimental; changes to it must retain a clear experimental warning.

## Technology and packaging

- Python 3.14+
- Typer and Rich
- Pydantic and TOML/TOMLKit configuration handling
- Jinja2 templates
- setuptools and setuptools-scm
- Ruff and Black
- Pytest and pytest-cov
- Docker, Docker Compose, and Make helpers

The console entry point is defined in `pyproject.toml`. Package data under `app/templates/` must remain included in distributions.

## Project structure

```text
app/
├── cli/          CLI commands, arguments, option resolution, and presentation
├── config/       Configuration models, loading, and resolution
├── core/         Application behavior and domain workflows
├── templates/    Configuration and message templates copied by custy init
├── ui/           Shared terminal UI and progress presentation
└── __main__.py   Module execution entry point

tests/
├── cli/
├── config/
└── core/

docs/             Repository-local notes and supporting documentation
make/             Make command modules
```

The CLI entry point is `app/cli/main.py`. Keep CLI parsing and presentation in `app/cli/`; keep reusable behavior in `app/core/`. Shared terminal presentation belongs in `app/ui/`.

For a fuller inventory, see `docs/project_structure.md` when that file is current.

## Configuration and templates

Custy uses `.config/custy/config.toml` in the target project. Users may edit this generated configuration.

The source templates shipped with Custy live under:

```text
app/templates/config.toml
app/templates/changelog/
app/templates/examples/
```

`custy init` copies these resources into `.config/custy/`. Template-copying code must support nested directories as well as individual files. Treat `app/templates/` as application-owned defaults and `.config/custy/` as user-owned configuration after initialization.

When adding or changing a configuration field:

1. Update the source template and configuration model/resolution logic.
2. Preserve compatible defaults where practical.
3. Add tests for precedence, validation, and missing values.
4. Update the canonical Custy documentation.

## Dry-run contract

When `--dry-run` is enabled:

- Read-only discovery and validation may execute.
- Mutating local and remote operations must be simulated.
- The command must explain what would happen without changing project or Git state.
- Diagnostic logging may still write to the configured log destination.

Without `--dry-run`, the command performs the requested mutations after its normal validation and confirmation rules. New commands and pipeline steps must preserve this contract and include tests for both modes.

## Coding standards

- Follow PEP 8 and existing project conventions.
- Use type hints whenever practical.
- Prefer `pathlib` over `os.path`.
- Keep functions focused and responsibilities separated.
- Prefer composition and straightforward code over unnecessary abstraction.
- Use dataclasses when they clarify data ownership.
- Do not change public CLI behavior without discussing the impact.
- Ignore and preserve temporary or reference Python files whose names end in forms such as `copy.py`, `_copy.py`, `_temp.py`, or `_temp_before.py` unless explicitly asked to work on them.

Every new public file, class, function, and method should have useful documentation. Use this section order when applicable:

1. Description
2. Logic
3. Args
4. Returns
5. Raises
6. Notes
7. Examples

Avoid placeholder implementations and incomplete examples.

## Logging standards

Use logging when it improves troubleshooting or observability:

- `CRITICAL`: the application cannot continue safely.
- `ERROR`: an operation failed.
- `WARNING`: a recoverable issue or fallback occurred.
- `INFO`: an important workflow state changed.
- `DEBUG`: detailed execution flow or resolved values.

When useful, include structured counts or timing such as `execution_time_ms`, `processed_files`, `success_count`, `error_count`, `retry_count`, or `validation_count`. Do not expose secrets or credentials.

## Testing and validation

All behavior changes require proportionate tests. Follow the existing feature-oriented layout under `tests/cli`, `tests/config`, and `tests/core`; do not create a parallel test taxonomy without a clear need.

Prefer the project virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest
```

On Windows systems where the default pytest temporary directory has inherited ACL problems, use a repository-local base directory:

```powershell
.\venv\Scripts\python.exe -m pytest --basetemp=.pytest-tmp-validation
```

Use targeted tests first, then the full suite. Relevant packaging or runtime changes should also be checked through the applicable Docker Compose and Make targets. Do not run commands, install dependencies, or mutate external services without the user's approval.

## Documentation

The canonical user documentation is maintained in the separate Devalltect documentation hub:

- English: https://devalltect00.github.io/devalltect-docs/docs/custy
- Indonesian: https://devalltect00.github.io/devalltect-docs/id/docs/custy

The local `docs/` directory contains repository-specific notes, histories, and supporting material; it is not automatically the canonical user guide.

Update the external documentation when changing commands, options, profiles, configuration, dry-run behavior, installation, output, or troubleshooting guidance. Keep English and Indonesian behaviorally aligned while leaving command names, flags, configuration keys, paths, and code identifiers untranslated.

## Development workflow

Work in clear phases:

1. Analyze the current implementation and configuration.
2. Describe the design, affected files, compatibility, and risks.
3. Implement focused changes with logging where useful.
4. Add or update tests and documentation.
5. Validate the smallest relevant scope, followed by broader checks when approved.

Before editing files or executing commands, explain the intended action and obtain user confirmation. At each meaningful phase, report completed work, remaining work, required context, and recommended documentation updates.

## Git workflow

Primary branches:

```text
main
develop
```

Suggested working branches:

```text
feature/<name>
bugfix/<name>
release/<version>
```

Do not perform Git commits, tags, pushes, rebases, history rewrites, or release operations unless explicitly requested and approved.

## Do not

- Do not remove tests or documentation without justification.
- Do not modify `CHANGELOG.md` or bump the project version unless explicitly requested.
- Do not silently weaken dry-run guarantees or confirmation safeguards.
- Do not invent missing code, files, configuration, or behavior.
- Do not overwrite user-managed `.config/custy/` content unexpectedly.
- Do not introduce architectural changes without explaining responsibilities, dependencies, and trade-offs.
- Do not treat Docker image replay or historical tag recovery as a core Custy responsibility; those are release-maintenance activities performed by external tooling.

## Completion report

Before completing implementation work, verify and report:

1. What changed and why
2. Files added, modified, or removed
3. Tests and commands run, including results
4. Documentation changes or remaining documentation work
5. Known limitations, missing context, and the next recommended step


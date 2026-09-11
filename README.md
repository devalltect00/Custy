# 🧠 Custy — Git Workflow and Release Automation CLI

<p align="center">
  <img src="docs/assets/custy.png" alt="Custy command-line interface" width="690">
</p>

[![GitHub CI](https://github.com/devalltect00/Custy/actions/workflows/ci.yml/badge.svg)](https://github.com/devalltect00/Custy/actions/workflows/ci.yml)
[![Docker production image](https://github.com/devalltect00/Custy/actions/workflows/docker-prod.yml/badge.svg)](https://github.com/devalltect00/Custy/actions/workflows/docker-prod.yml)
[![GitLab pipeline](https://gitlab.com/devalltects-group/custy/badges/main/pipeline.svg)](https://gitlab.com/devalltects-group/custy/-/pipelines)
[![Coverage](https://gitlab.com/devalltects-group/custy/badges/main/coverage.svg)](https://gitlab.com/devalltects-group/custy/-/graphs/main/charts)
[![Latest release](https://img.shields.io/github/v/release/devalltect00/Custy?display_name=tag)](https://github.com/devalltect00/Custy/releases)
[![GHCR](https://img.shields.io/badge/container-GHCR-2496ED?logo=docker&logoColor=white)](https://github.com/devalltect00/Custy/pkgs/container/custy)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/github/license/devalltect00/Custy)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-English%20%7C%20Bahasa%20Indonesia-success)](https://devalltect00.github.io/devalltect-docs/docs/custy)

**Custy** is a Python developer-productivity CLI for config-driven Git
workflow and release automation. It initializes project resources, validates
repository readiness, manages versions, generates changelogs, creates commits
and tags, synchronizes multiple remotes, and combines those operations into
repeatable development and release pipelines.

Custy supports SemVer, PEP 440, date-based, and Git-count version strategies.
Its Typer and Rich interface also provides dry-run safety, configurable
templates, backup and cleanup tools, and an experimental workflow-policy layer.

---

## ℹ️ Project Metadata

| Property                     | Value                                                        |
| ---------------------------- | ------------------------------------------------------------ |
| Project                      | Custy                                                        |
| Current version              | `v2.1.1`                                                     |
| Python package               | `custy`                                                      |
| Package compatibility        | Python 3.14+                                                 |
| Standard development runtime | Python 3.14                                                  |
| CLI framework                | Typer and Rich                                               |
| Version strategies           | SemVer, PEP 440, date-based, and Git-count                   |
| Distribution                 | Source, release artifacts, private GitLab PyPI, Docker, GHCR |
| Documentation                | English and Bahasa Indonesia through Devalltect Docs         |
| License                      | MIT                                                          |
| Maintainer                   | Devalltect / Rizky Fernandes                                 |

---

## ✨ Features

- ⚙️ Configuration-driven behavior through `.config/custy/config.toml`
- 📦 Project initialization for configuration, templates, and examples
- ✅ Repository, configuration, version, and commit-message validation
- 🔢 SemVer, PEP 440, date-based, and Git-count version strategies
- 📝 Configurable `CHANGELOG.md` generation using Jinja templates
- 🧩 Structured commit and annotated tag workflows
- 🌐 Primary, backup, and multi-remote push support
- 🧱 Focused `commit`, `tag`, `push`, `dev`, `release`, and `full` profiles
- 🔎 Automatic project and version-file discovery with explicit overrides
- 🔐 Native Git authentication first, with an optional container token fallback
- 🧪 Global dry-run, debug, and configurable logging options
- 🧰 Commit/tag-message backup and stale-resource cleanup commands
- 🐳 Local Docker, Docker Compose, GHCR, and Makefile workflows
- 🚧 Experimental branch and release workflow-policy checks

---

## 🚀 Quick Start

After installing Custy, initialize its project resources and validate the
repository:

```bash
custy init
custy validate
```

Preview the daily development profile:

```bash
custy --dry-run run dev
```

Review the plan before removing `--dry-run` for a live operation.

Preview a release pipeline without applying its side effects:

```bash
custy --dry-run run release
```

Dry-run still performs read-only discovery, such as file inspection and Git
or configured-remote queries, so its preview reflects the current repository.
File writes, deletions, editor launches, Git mutations, and remote mutations
are simulated. Normal diagnostic logs may still be written.

Use `custy --help` or `custy <command> --help` to inspect the available commands
and options.

---

## 🧪 Installation and Distribution

Choose the method that fits your environment. Custy is currently distributed
from its source repositories, release artifacts, container registries, and a
private GitLab PyPI registry for authorized users. The private Python registry
is distinct from GHCR container images and does not require a public PyPI release.

### Requirements

For a local Python installation:

- Python 3.14 or newer
- Git
- `pip` through the selected Python interpreter
- A virtual environment is recommended

Docker already provides Python, Git, and Custy inside the image. Install Docker
only when you want to use the container method. Make is optional and is used by
the repository's development helpers.

### Method 1: Install from a local source checkout

This is the recommended method for Custy contributors and local development.

**Windows PowerShell**

```powershell
git clone https://github.com/devalltect00/Custy.git
Set-Location Custy
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

**Linux and macOS**

```bash
git clone https://github.com/devalltect00/Custy.git
cd Custy
python3.14 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Install contributor and local documentation dependencies when needed:

```bash
python -m pip install -e ".[dev,docs]"
```

### Method 2: Install directly from Git

Use a version tag for a reproducible installation into another project or
environment:

```bash
python -m pip install "git+https://github.com/devalltect00/Custy.git@v<version>"
```

Install the latest `main` branch when you intentionally want current source:

```bash
python -m pip install "git+https://github.com/devalltect00/Custy.git@main"
```

The GitLab mirror can be used in the same way:

```bash
python -m pip install "git+https://gitlab.com/devalltects-group/custy.git@main"
```

Replace `v<version>` with an available release tag such as `v1.2.3`.

### Method 3: Install a GitHub Release artifact

The [GitHub Releases page](https://github.com/devalltect00/Custy/releases)
provides versioned Python distribution artifacts generated by the release
workflow. Download a wheel or source archive, then install the local file:

```bash
python -m pip install ./custy-<version>-py3-none-any.whl
```

or:

```bash
python -m pip install ./custy-<version>.tar.gz
```

### Method 4: Run the GitHub Packages image with Docker

Container images are distributed through **GitHub Packages / GitHub Container
Registry (GHCR)**. They are referenced by GitHub Releases, but are pulled from
GHCR rather than downloaded as release assets.

Pull the latest production image:

```bash
docker pull ghcr.io/devalltect00/custy:latest
```

For reproducible use, replace `latest` with an available version tag such as
`v1.2.3`. Development and immutable commit images may also be published with
`dev` and `sha-<commit>` tags.

Custy operates on a Git repository, so mount the project you want to manage at
`/workspace`.

**Windows PowerShell**

```powershell
docker run --rm -it `
  --volume "${PWD}:/workspace" `
  --workdir /workspace `
  ghcr.io/devalltect00/custy:latest --help
```

**Linux and macOS**

```bash
docker run --rm -it \
  --volume "$(pwd):/workspace" \
  --workdir /workspace \
  ghcr.io/devalltect00/custy:latest --help
```

Pass Custy arguments after the image name. For example:

```bash
docker run --rm -it \
  --volume "$(pwd):/workspace" \
  --workdir /workspace \
  ghcr.io/devalltect00/custy:v<version> --dry-run run release
```

The image contains Git, but authenticated fetch, push, and multi-remote
operations still require suitable repository credentials inside the container.
Do not mount or copy credentials into an image; provide them securely at
runtime.

### Method 5: Install from the private GitLab Python registry

Choose a version already published in the target project's registry. In an
activated virtual environment, replace the placeholders:

```text
python -m pip install --index-url "https://gitlab.com/api/v4/projects/<project-id>/packages/pypi/simple" "custy==<package-version>"
custy --help
```

Use a deploy token with `read_package_registry`. Supply credentials through
[pip authentication](https://pip.pypa.io/en/stable/topics/authentication/),
not committed files or shared command history. The package version is PEP 440:
for example, `v2.1.0` becomes `2.1.0`.
Use `--index-url`, not `--extra-index-url`; review
[GitLab package forwarding](https://docs.gitlab.com/user/packages/pypi_repository/#package-request-forwarding-security-notice)
if dependencies must stay private.

See [installation and registry guidance](docs/guides/gitlab_package_registry.md) for authentication,
other installation methods, and registry setup.

### Verify the selected method

For a Python installation:

```bash
custy --help
custy --version
```

For Docker:

```bash
docker run --rm ghcr.io/devalltect00/custy:latest --version
```

---

## 🛠️ Makefile Commands

The Makefile is optional and contains local, Docker, Compose, registry, testing,
quality, documentation, and release helpers. Use its built-in help instead of
relying on a copied command list that may become outdated:

```bash
make help
```

Use a focused help view for one workflow family:

```bash
make help-local
make help-docker
make help-compose
make help-remote
```

For example, the remote-image helpers can pull and run Custy from GHCR:

```bash
make r-custy-pull
make r-custy-run-release
```

The same remote catalog exposes the current Reflow workflows, including safe
preview targets:

```bash
make r-reflow-releases-recover-dryrun
make r-reflow-tags-convert-dryrun
make r-reflow-dockerize-dryrun
```

Start with `make help-local` for environment setup, tests, formatting,
documentation, builds, and local Custy commands.

---

## 📦 CLI Usage Examples

### Initialize and validate a project

```bash
custy init
custy validate
```

### Generate a changelog

```bash
custy changelog generate
```

### Commit, tag, and push separately

```bash
custy commit --auto-stage
custy tag --bump patch
custy push --all-remote
```

### Run composed pipelines

```bash
custy run dev
custy run release
custy run full
```

Run `custy run --help` before choosing a supported profile.

---

## 🧼 Maintenance and Supporting Commands

| Command                           | Purpose                                         |
| --------------------------------- | ----------------------------------------------- |
| `custy configure credentials`     | Manage optional container credential fallback   |
| `custy backup commit`             | Back up the commit-message template             |
| `custy backup tag`                | Back up the tag-message template                |
| `custy backup all`                | Back up both message templates                  |
| `custy cleanup backups`           | Remove old message-template backups             |
| `custy cleanup branches`          | Remove matching temporary branches              |
| `custy cleanup all`               | Run backup and branch cleanup together          |
| `custy version update`            | Resolve and synchronize project versions        |
| `custy changelog generate`        | Generate `CHANGELOG.md` from repository history |
| `custy workflow branch --enforce` | Enforce experimental workflow policy checks     |

Use each command's `--help` output before running an operation that changes the
repository. Global options such as `--dry-run` must appear before the command.

---

## 🧰 Documentation

- 🌐 [Custy documentation portal](https://devalltect00.github.io/devalltect-docs/docs/custy)
- 🚀 [Getting started](https://devalltect00.github.io/devalltect-docs/docs/custy/getting-started/overview)
- 🖥️ [Command guides](https://devalltect00.github.io/devalltect-docs/docs/custy/commands/overview)
- ⚙️ [Configuration reference](https://devalltect00.github.io/devalltect-docs/docs/custy/configuration/overview)
- 🧱 [Pipeline guides](https://devalltect00.github.io/devalltect-docs/docs/custy/pipelines/overview)
- 🇮🇩 [Dokumentasi Bahasa Indonesia](https://devalltect00.github.io/devalltect-docs/id/docs/custy)
- 📘 [Local usage notes](docs/HOW_TO_USE.md)
- 📖 [Local CLI command reference](docs/cli_commands_custy.md)
- 🛠️ [Local Make workflow guide](docs/guides/make_workflows.md)

---

## ⚙️ Repository Metadata Helper (Maintainers)

The optional [metadata sync script](scripts/repository/src/sync_metadata.py)
is source-checkout tooling, not an installed application command. Run it from
this repository's root:

```bash
python scripts/repository/src/sync_metadata.py --dry-run
```

It reads `[project].description` and the separate
`[tool.devalltect.github].topics` / `[tool.devalltect.gitlab].topics` tables
in `pyproject.toml`. Package `keywords` are not repository topics.

Review `GITHUB_REMOTES` and `GITLAB_REMOTES` in the script: the current
defaults are `origin` and `backup`. Each list contains fallback candidates;
the first valid fetch URL selects one repository per provider. Both providers
must resolve. This helper currently targets GitHub.com and GitLab.com.

Dry-run uses Python and read-only Git discovery; it does not call provider
APIs. Live synchronization additionally needs authenticated `gh` and `glab`
with access to update those repositories. Their authentication is separate from
Custy's optional Git credential fallback.

Before removing `--dry-run`, review the targets and metadata carefully:
the live helper does not ask for confirmation, replaces the topic lists, and
clears existing topics when a list is empty or missing. A failure can leave
earlier updates applied; there is no cross-provider rollback.

Known follow-up: the script's docstring still shows the old path, and its
GitHub topic-limit constant is 50 despite
[GitHub's maximum of 20 topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).
Use the path above and keep the GitHub list within 20 until corrected.
These issues and isolated test coverage are tracked in the
[TODO history](docs/TODO_tracking_history.md).

---

## 📁 Project Structure

See [`docs/project_structure.md`](docs/project_structure.md) for the detailed
repository layout.

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the contributor workflow.

---

## 🔐 Security

See [`SECURITY.md`](SECURITY.md) for the security policy and reporting process.

---

## 📃 Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.

---

## 📜 License

Custy is open-source software licensed under the [MIT License](LICENSE).

📧 Contact: `devalltect00@gmail.com`

---

_Crafted with ❤️ by Devalltect / Rizky Fernandes_

<!-- docs/badges.md -->

# 🏷️ Project Badges

This document describes the badges used by Custy and the project capability represented by each badge.

## 📖 Documentation Strategy

Custy supports two complementary documentation paths:

- The Custy source repository retains **MkDocs** support for local project documentation through the `docs` optional dependency and the `make docs-serve` and `make docs-build` helpers.
- The canonical public documentation is published through the shared **Devalltect Docusaurus portal**, which provides unified navigation and complete English and Indonesian Custy documentation.

This separation keeps local contributor tooling available while giving users one consistent public documentation experience.

---

## 📦 Repository

| Icon | Preview                                                                                                                                   | Description                          | Category   |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------- |
| 🐙   | [![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/devalltect00/Custy)                         | Primary source code repository       | Repository |
| 📦   | [![Release](https://img.shields.io/github/v/release/devalltect00/Custy?display_name=tag)](https://github.com/devalltect00/Custy/releases) | Latest published GitHub release      | Repository |
| 🏷️   | [![Tag](https://img.shields.io/github/v/tag/devalltect00/Custy)](https://github.com/devalltect00/Custy/tags)                              | Latest Git tag                       | Repository |
| ⭐   | [![Stars](https://img.shields.io/github/stars/devalltect00/Custy?style=social)](https://github.com/devalltect00/Custy/stargazers)         | GitHub star count                    | Repository |
| 🍴   | [![Forks](https://img.shields.io/github/forks/devalltect00/Custy?style=social)](https://github.com/devalltect00/Custy/forks)              | GitHub fork count                    | Repository |
| 📄   | [![License](https://img.shields.io/github/license/devalltect00/Custy)](../LICENSE)                                                        | MIT license from repository metadata | Repository |
| 🐞   | [![Issues](https://img.shields.io/github/issues/devalltect00/Custy)](https://github.com/devalltect00/Custy/issues)                        | Open GitHub issues                   | Repository |
| 🦊   | [![GitLab](https://img.shields.io/badge/mirror-GitLab-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/devalltects-group/custy)    | GitLab mirror and pipeline project   | Repository |

---

## 🚀 CI/CD & Quality

| Icon | Preview                                                                                                                                                  | Description                                | Category |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------- |
| 🏗️   | [![GitHub CI](https://github.com/devalltect00/Custy/actions/workflows/ci.yml/badge.svg)](https://github.com/devalltect00/Custy/actions/workflows/ci.yml) | Python 3.14 validation with GitHub Actions | CI/CD    |
| ✅   | [![GitLab Pipeline](https://gitlab.com/devalltects-group/custy/badges/main/pipeline.svg)](https://gitlab.com/devalltects-group/custy/-/pipelines)        | GitLab pipeline status                     | CI/CD    |
| 🧪   | [![Coverage](https://gitlab.com/devalltects-group/custy/badges/main/coverage.svg)](https://gitlab.com/devalltects-group/custy/-/graphs/main/charts)      | Test coverage reporting                    | Quality  |
| 🧼   | [![Ruff](https://img.shields.io/badge/lint-Ruff-261230?logo=ruff)](https://docs.astral.sh/ruff/)                                                         | Linting and primary formatting             | Quality  |
| ⚫   | [![Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://black.readthedocs.io/)                                                    | Compatible formatting checks               | Quality  |
| 🧪   | [![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](https://pytest.org/)                                                           | Automated testing                          | Quality  |

---

## 📚 Documentation

| Icon | Preview                                                                                                                                             | Description                             | Category      |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------- |
| 📚   | [![Documentation](https://img.shields.io/badge/docs-online-success.svg)](https://devalltect00.github.io/devalltect-docs/docs/custy)                 | Public Custy documentation              | Documentation |
| 📖   | [![Docusaurus](https://img.shields.io/badge/docs-Docusaurus-3EA6FF?logo=docusaurus)](https://docusaurus.io/)                                        | Canonical documentation portal          | Documentation |
| 🇺🇸   | [![English](https://img.shields.io/badge/locale-English-blue.svg)](https://devalltect00.github.io/devalltect-docs/docs/custy)                       | Default English documentation           | Documentation |
| 🇮🇩   | [![Bahasa Indonesia](https://img.shields.io/badge/locale-Bahasa%20Indonesia-red.svg)](https://devalltect00.github.io/devalltect-docs/id/docs/custy) | Complete Indonesian documentation       | Documentation |
| 📝   | [![MkDocs](https://img.shields.io/badge/local%20docs-MkDocs-success.svg)](https://www.mkdocs.org/)                                                  | Optional local repository documentation | Documentation |
| 🌐   | [![GitHub Pages](https://img.shields.io/badge/hosted%20on-GitHub%20Pages-181717?logo=github)](https://devalltect00.github.io/devalltect-docs)       | Public documentation hosting            | Documentation |

---

## 🛠️ Developer Experience

| Icon | Preview                                                                                                        | Description                                 | Category |
| ---- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | -------- |
| 🐳   | ![Docker](https://img.shields.io/badge/docker-supported-2496ED?logo=docker&logoColor=white)                    | Docker development and production workflows | DevEx    |
| 🚢   | ![Docker Release](https://img.shields.io/badge/docker-release%20images-2496ED?logo=docker&logoColor=white)     | Version-tagged release images               | DevEx    |
| 🔖   | ![Docker Commit](https://img.shields.io/badge/docker-commit%2Fsha%20images-1D63ED?logo=docker&logoColor=white) | Commit and SHA image workflows              | DevEx    |
| 📦   | ![Docker Compose](https://img.shields.io/badge/docker--compose-supported-2496ED.svg)                           | Docker Compose helpers                      | DevEx    |
| 🐙   | ![GHCR](https://img.shields.io/badge/registry-GHCR-blue?logo=github)                                           | GitHub Container Registry support           | DevEx    |
| 🦊   | ![GitLab Registry](https://img.shields.io/badge/registry-GitLab-FC6D26?logo=gitlab&logoColor=white)            | GitLab Container Registry support           | DevEx    |
| 🛠️   | ![Makefile](https://img.shields.io/badge/makefile-supported-success.svg)                                       | Discoverable Make-based automation          | DevEx    |
| 🔗   | ![Pre-Commit](https://img.shields.io/badge/git--hooks-pre--commit-success.svg)                                 | Pre-commit hook automation                  | DevEx    |
| 🧰   | ![Commitizen](https://img.shields.io/badge/commitizen-optional-brightgreen.svg)                                | Optional conventional commit workflow       | DevEx    |

---

## 📦 Distribution

| Icon | Preview                                                                                         | Description                                     | Category     |
| ---- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ |
| 🚀   | ![Releases](https://img.shields.io/badge/releases-supported-success.svg)                        | GitHub release artifacts                        | Distribution |
| 🐍   | ![pip](https://img.shields.io/badge/pip-source%20install-blue.svg)                              | Local, editable, and Git source installation    | Distribution |
| 📄   | ![Wheel](https://img.shields.io/badge/wheel-supported-success.svg)                              | Python wheel distribution                       | Distribution |
| 📦   | ![sdist](https://img.shields.io/badge/sdist-supported-success.svg)                              | Python source distribution                      | Distribution |
| 🏷️   | ![Dynamic Version](https://img.shields.io/badge/version-dynamic%20from%20Git%20tags-3F4551.svg) | Package version supplied by setuptools-scm      | Distribution |
| 🔢   | ![Versioning](https://img.shields.io/badge/versioning-SemVer%20%7C%20PEP%20440-blueviolet.svg)  | SemVer, PEP 440, date, and Git-count strategies | Distribution |

---

## ⚙️ Technology Stack

| Icon | Preview                                                                                   | Description                       | Category   |
| ---- | ----------------------------------------------------------------------------------------- | --------------------------------- | ---------- |
| 🐍   | ![Python](https://img.shields.io/badge/python-3.14+-3776AB?logo=python&logoColor=white)   | Required Python version           | Technology |
| ⚡   | ![Typer](https://img.shields.io/badge/CLI-Typer-009688.svg)                               | CLI framework                     | Technology |
| 🎨   | ![Rich](https://img.shields.io/badge/UI-Rich-FAE742.svg)                                  | Terminal presentation framework   | Technology |
| 🌳   | ![Git](https://img.shields.io/badge/git-required-F05032?logo=git&logoColor=white)         | Repository and release operations | Technology |
| 🧩   | ![Pydantic](https://img.shields.io/badge/validation-Pydantic-E92063.svg)                  | Typed data validation             | Technology |
| 📝   | ![Jinja](https://img.shields.io/badge/templates-Jinja-B41717?logo=jinja&logoColor=white)  | Changelog and message templates   | Technology |
| 🐳   | ![Docker](https://img.shields.io/badge/docker-enabled-2496ED?logo=docker&logoColor=white) | Container integration             | Technology |

---

## ✨ Project Features

| Icon | Preview                                                                                     | Description                                        | Category |
| ---- | ------------------------------------------------------------------------------------------- | -------------------------------------------------- | -------- |
| 🔧   | ![Developer Tool](https://img.shields.io/badge/category-developer--tool-orange.svg)         | Developer productivity CLI                         | Feature  |
| 🔄   | ![Git Automation](https://img.shields.io/badge/git-workflow%20automation-blue.svg)          | Validation, commit, tag, push, and synchronization | Feature  |
| 📝   | ![Changelog](https://img.shields.io/badge/changelog-generated-success.svg)                  | Configurable changelog generation                  | Feature  |
| 🔢   | ![Versioning](https://img.shields.io/badge/versioning-multiple%20strategies-blueviolet.svg) | SemVer, PEP 440, date, and Git-count workflows     | Feature  |
| 🌐   | ![Multi Remote](https://img.shields.io/badge/git-multi--remote-success.svg)                 | Primary and backup remote synchronization          | Feature  |
| 🧱   | ![Pipelines](https://img.shields.io/badge/pipelines-profile--driven-blue.svg)               | Development, release, full, and focused profiles   | Feature  |
| 🧰   | ![Maintenance](https://img.shields.io/badge/maintenance-backup%20%7C%20cleanup-success.svg) | Backup and cleanup operations                      | Feature  |
| 💻   | ![CLI](https://img.shields.io/badge/interface-CLI-success.svg)                              | Typer-based command-line interface                 | Feature  |
| 🤖   | ![Automation](https://img.shields.io/badge/automation-release%20orchestration-blue.svg)     | Release and CI/CD orchestration                    | Feature  |

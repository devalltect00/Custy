<!-- docs/TODO_tracking_history.md -->

# TODO

Tracks short-term development tasks, improvements, tasks and ideas .

---

## Features

### ✅ Completed

- _(Nothing yet)_

---

### 🧩 In Progress

#### General

- [x] add .github workflow file
  - [x] add ci.yml file
  - [x] add docker-dev.yml file
  - [x] add docker-prod.yml file
  - [x] add release.yml file
- [x] add .gitlab workflow file
  - [x] add ci.yml file
  - [x] add docker-dev.yml file
  - [x] add docker-prod.yml file
  - [x] add release.yml file
- [x] add gitlab-ci.yml
- [x] add ignore files
  - [x] add .gitignore
  - [x] add .dockerignore
  - [x] add .prettierignore
- [x] use logs for external logs
- [x] add .vscode/
  - [x] add .vscode/launch.json
  - [x] add .vscode/settings.json
- [~] add config or meta data
  - [x] add .pre-commit-config.yaml
  - [x] add .prettierrc.json
  - [x] add AGENTS.md
  - [x] add CONTRIBUTING.md
  - [x] add LICENSE
  - [x] add pyproject.toml
  - [x] add requirements.txt
  - [x] add SECURITY.md
  - [x] add TODO.md
  - [x] add README.md
  - [~] Add CHANGELOG.md.
- [x] add docker compose files
  - [x] add docker-compose.dev.yml files
  - [x] add docker-compose.prod.yml files
  - [x] add docker-compose.yml files
  - [x] add Dockerfile
- [x] add example_command.txt
- [x] add Makefile
- [x] add Testing
- [-] add mkdocs.yml
- [-] add documentations (Use devalltect00-docs project or website instead)
  - [-] Add the docs/badges.md
  - [-] Add the docs/configuration.md
  - [-] Add the docs/how-to-use.md
  - [-] Add the docs/index.md
  - [-] Add the docs/infrastructure.md
  - [-] Add the docs/installation.md
  - [-] Add the docs/usage.md
  - [-] Add the docs/project_structure.md
  - [-] Add the diagrams to docs/diagrams/
- [x] Using .config/ path instead from tools/ path
- [x] add banner
- [x] Fix init
- [x] General project cleanup and consistency pass.
- [x] Update pyproject.toml description
- [x] Update CONTRIBUTING.md description
- [x] Refactor GitHelper
- [x] Make sure app run well
- [x] fix `custy --help`
- [x] Makefile the help message
- [x] on workflow command. Give message to ignore it for now. still in development. better noy run this command now. or it is a alpha version. give warning
- [x] Update help message for each command
- [x] Using ui panel on init command
- [x] Update Makefile
- [x] error exception on CLI when command is missing
- [-] Ignore format tab to 4 with black or ruff
- [-] Remove app/config/custy_config_loader.py (I will keep it as backups)

#### Features related

- [x] Refactor workflow_engine
- [x] Refactor `./app/git_commit_tagger.py` file or GitCommitTagger class where on previous version it is a nig class, giant class or maybe we can call it a god class. and on previous version it is hard to extend, read, iimprovement. hard to add new features or mayeb change or remove it/them. With new update it is better under `.\app\core\workflow\workflow_engine.py`
- [x] Refactor `./app/__main__.py` file, where on the previous version it combined CLI or frontend some is just like service or maybe even backend or whatever. Hard to read and extend. and now with new updates we can seperate between frontend on `.\app\cli\`and backend on `.\app\core\`
- [x] Refactor directories and some files under `./app/utils/`. On previous version all the core things or backends or the logic get from here. The naming `utils` it quite confusing. after the updates we can seperate the files, features, code, etc. So not all the core things or backends or the logic things should be under `./app/utils/`. Many files moved and refactored here.
- [x] Move custom configurations from `.\.custor.toml` into `.\.config\custy\config.toml`
- [x] Logging improvement
- [x] Adding external log features
- [x] Update and fixed changelog generator features.
- [x] Setup docker
- [x] Setup docker compose
- [x] Update `.gitignore` file
- [x] added new and Update github workflow. some files under `.github` added updated
- [x] Update and improve gitlab workflow. `.gitlab-ci.yml` updated and `.gitlab` added
- [x] Use pre commit tools and add new file i.e. `.pre-commit-config.yaml` file.
- [x] Add prettier configuration. `.prettierignore` and `.prettierrc.json` files added.
- [x] Add Some others meta data, files, or configurations.
- [x] Added `.vscode/` and allow git to track changes on this directory.
- [x] Add new and update tests
- [x] On `./tools/`, `project_structure/` removed and `./tools\generate_diagram` added.
- [x] Update `Makefile` and `./make/` added
- [x] `.agents` added
- [x] Improvement, (add, fixed, removed etc) UI/UX on CLI console. Such as add colors, tables format, CLI help message or commands message, progress visualization, etc.
- [x] Update and refactor project or code structure.
- [x] Update some metadata files or anythings, for examples `pyproject.toml` file, etc
- [x] On `./app/` directory now we have seperated and individual group of files or component or whatever it is. If we seacrh for ui things, it is under `./app/ui`. If we search for theme related we can search under `./app/`. and any other improvement code or project structure
- [x] With new update, The code or app use some several code design or design patter. Some of the features or files or class or whatever use strategy pattern, some use pipeline design pattern, factory design pattern, etc.
- [x] The CLI command now improvement. The all possible command if we/user run the custy especially the `custy run` command. All list possible command on `.\app\core\pipeline\profiles.py`. With new improvement it not just help user that use the app but also help developer extend, improve or whatever the features so much easier and more flexible.
- [x] On current `./.config\custy\config.toml` file, on this version, there's a lot changes on the configuration than old `./.custor.toml` file
- [x] Adding new cli command such as `custy init` etc. and also add, update, removed some cli command' options.

Notes:
The `docs/` directory seems old and deprecated. But I will keep it as backups.

Also I still keep some files that deprecated and not used as backups for example `app\__main__.deprecated.py` file, etc.

Last time configuration using `./.custor.toml` file and files under `./templates/`.After updates, all personal preferences or personal configuration stores and you can find on `./.config/` directory.

With this new feature it is not just improve user experience, but also improvement as developer and for developer also. For example like improve code or project structure, improvement on code. So the developer also can easily or more easy to read, extend, add new features, remove features, find bugs, analyze bugs, fix bugs, etc.

==================

refactor Makefile help message
gitlab pipeline
fix why app error when run the command

---

### 🧠 Planned

- _(Nothing yet)_

---

### 🔭 Future

- [ ] Adding features convertion between pep440, semver, custom tags
- [ ] Adding logic to check if "github_image" and "gitlab_image" valid url and valid image name

---

### 🗑️ Cancelled / Dropped

- _(Nothing yet)_

---

## ⚖️ Considerations

- _(Nothing yet)_

---

## 💡 Ideas

- _(Nothing yet)_

---

## 🧾 Notes

### TODO.md

Keep this file concise, status-driven, and updated during each milestone.

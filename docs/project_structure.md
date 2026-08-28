# Project Structure

# Repository Overview

This repository follows a modular structure commonly used in modern projects.

Common directories include:

- `app/` — Main application source code.
- `.config/` — Project configuration files.
- `.github/` — GitHub-related configuration.
- `.vscode/` — Visual Studio Code workspace settings.
- `docs/` — Project documentation and technical references.
- `tests/` — Automated tests.
- `data/` — Input datasets or static data.
- `output/` — Generated outputs from the application.
- `scripts/` — Utility scripts for development or automation.
- `tools/` — Development tools and automation utilities.
- `templates/` — Reusable templates used by the project.

---

# Repository Structure

(project type: ProjectType.PYTHON)

```text
.
├── .agents
│   └── skills
│       └── follow-custy-guidelines
│           ├── agents
│           │   └── openai.yaml
│           └── SKILL.md
├── .config
│   ├── custy
│   │   ├── templates
│   │   │   ├── backups
│   │   │   │   ├── commit
│   │   │   │   └── tag
│   │   │   ├── changelog
│   │   │   │   └── changelog.j2
│   │   │   ├── examples
│   │   │   │   ├── commit_message
│   │   │   │   └── tag_message
│   │   │   ├── commit-message.txt
│   │   │   └── tag-message.txt
│   │   └── config.toml
│   ├── doc_gen
│   │   └── config.toml
│   ├── path_header_scanner
│   │   └── config.toml
│   └── reflow
│       └── config.toml
├── .gitlab
│   ├── ci.yml
│   ├── docker-dev.yml
│   ├── docker-prod.yml
│   └── release.yml
├── .pre-commit-cache
│   ├── repo049zwjsu
│   │   ├── build/ ... (collapsed)
│   │   ├── py_env-python3
│   │   │   ├── Include
│   │   │   ├── Lib
│   │   │   │   └── site-packages
│   │   │   ├── Scripts
│   │   │   │   ├── activate
│   │   │   │   ├── activate.bat
│   │   │   │   ├── activate.fish
│   │   │   │   ├── activate.nu
│   │   │   │   ├── activate.ps1
│   │   │   │   ├── activate.xsh
│   │   │   │   ├── activate_this.py
│   │   │   │   ├── deactivate.bat
│   │   │   │   ├── pip-3.14.exe
│   │   │   │   ├── pip.exe
│   │   │   │   ├── pip3.14.exe
│   │   │   │   ├── pip3.exe
│   │   │   │   ├── pydoc.bat
│   │   │   │   ├── python.exe
│   │   │   │   ├── python3
│   │   │   │   ├── python3.exe
│   │   │   │   ├── pythonw.exe
│   │   │   │   ├── pythonw3.exe
│   │   │   │   ├── ruff.exe
│   │   │   │   └── venvlauncher.exe
│   │   │   ├── .gitignore
│   │   │   ├── .install_state_v1
│   │   │   ├── .install_state_v2
│   │   │   ├── CACHEDIR.TAG
│   │   │   └── pyvenv.cfg
│   │   ├── .gitignore
│   │   ├── .pre-commit-hooks.yaml
│   │   ├── LICENSE-APACHE
│   │   ├── LICENSE-MIT
│   │   ├── mirror.py
│   │   ├── pyproject.toml
│   │   └── README.md
│   ├── repo328yitur
│   │   ├── action
│   │   │   └── main.py
│   │   ├── autoload
│   │   │   └── black.vim
│   │   ├── docs
│   │   │   ├── _static
│   │   │   │   ├── license.svg
│   │   │   │   ├── logo2-readme.png
│   │   │   │   ├── logo2.png
│   │   │   │   └── pypi_template.svg
│   │   │   ├── compatible_configs
│   │   │   │   ├── flake8
│   │   │   │   ├── isort
│   │   │   │   ├── pycodestyle
│   │   │   │   └── pylint
│   │   │   ├── contributing
│   │   │   │   ├── gauging_changes.md
│   │   │   │   ├── index.md
│   │   │   │   ├── issue_triage.md
│   │   │   │   ├── release_process.md
│   │   │   │   └── the_basics.md
│   │   │   ├── guides
│   │   │   │   ├── index.md
│   │   │   │   ├── introducing_black_to_your_project.md
│   │   │   │   ├── using_black_with_jupyter_notebooks.md
│   │   │   │   └── using_black_with_other_tools.md
│   │   │   ├── integrations
│   │   │   │   ├── doctest_formatting.md
│   │   │   │   ├── editors.md
│   │   │   │   ├── github_actions.md
│   │   │   │   ├── index.md
│   │   │   │   └── source_version_control.md
│   │   │   ├── the_black_code_style
│   │   │   │   ├── current_style.md
│   │   │   │   ├── future_style.md
│   │   │   │   └── index.md
│   │   │   ├── usage_and_configuration
│   │   │   │   ├── black_as_a_server.md
│   │   │   │   ├── black_docker_image.md
│   │   │   │   ├── file_collection_and_discovery.md
│   │   │   │   ├── index.md
│   │   │   │   └── the_basics.md
│   │   │   ├── authors.md
│   │   │   ├── change_log.md
│   │   │   ├── conf.py
│   │   │   ├── faq.md
│   │   │   ├── getting_started.md
│   │   │   ├── index.md
│   │   │   ├── license.md
│   │   │   ├── make.bat
│   │   │   └── Makefile
│   │   ├── plugin
│   │   │   └── black.vim
│   │   ├── profiling
│   │   │   ├── dict_big.py
│   │   │   ├── dict_huge.py
│   │   │   ├── list_big.py
│   │   │   ├── list_huge.py
│   │   │   ├── mix_big.py
│   │   │   ├── mix_huge.py
│   │   │   └── mix_small.py
│   │   ├── py_env-python3
│   │   │   ├── Include
│   │   │   ├── Lib
│   │   │   │   └── site-packages
│   │   │   ├── Scripts
│   │   │   │   ├── activate
│   │   │   │   ├── activate.bat
│   │   │   │   ├── activate.fish
│   │   │   │   ├── activate.nu
│   │   │   │   ├── activate.ps1
│   │   │   │   ├── activate.xsh
│   │   │   │   ├── activate_this.py
│   │   │   │   ├── black.exe
│   │   │   │   ├── blackd.exe
│   │   │   │   ├── deactivate.bat
│   │   │   │   ├── pip-3.14.exe
│   │   │   │   ├── pip.exe
│   │   │   │   ├── pip3.14.exe
│   │   │   │   ├── pip3.exe
│   │   │   │   ├── pydoc.bat
│   │   │   │   ├── python.exe
│   │   │   │   ├── python3
│   │   │   │   ├── python3.exe
│   │   │   │   ├── pythonw.exe
│   │   │   │   ├── pythonw3.exe
│   │   │   │   └── venvlauncher.exe
│   │   │   ├── .gitignore
│   │   │   ├── .install_state_v1
│   │   │   ├── .install_state_v2
│   │   │   ├── CACHEDIR.TAG
│   │   │   └── pyvenv.cfg
│   │   ├── scripts
│   │   │   ├── __init__.py
│   │   │   ├── check_pre_commit_rev_in_example.py
│   │   │   ├── check_version_in_basics_example.py
│   │   │   ├── diff_shades_gha_helper.py
│   │   │   ├── fuzz.py
│   │   │   ├── generate_schema.py
│   │   │   ├── make_width_table.py
│   │   │   ├── migrate-black.py
│   │   │   ├── release.py
│   │   │   └── release_tests.py
│   │   ├── src
│   │   │   ├── black
│   │   │   │   ├── resources
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __main__.py
│   │   │   │   ├── _width_table.py
│   │   │   │   ├── brackets.py
│   │   │   │   ├── cache.py
│   │   │   │   ├── comments.py
│   │   │   │   ├── concurrency.py
│   │   │   │   ├── const.py
│   │   │   │   ├── debug.py
│   │   │   │   ├── files.py
│   │   │   │   ├── handle_ipynb_magics.py
│   │   │   │   ├── linegen.py
│   │   │   │   ├── lines.py
│   │   │   │   ├── mode.py
│   │   │   │   ├── nodes.py
│   │   │   │   ├── numerics.py
│   │   │   │   ├── output.py
│   │   │   │   ├── parsing.py
│   │   │   │   ├── py.typed
│   │   │   │   ├── ranges.py
│   │   │   │   ├── report.py
│   │   │   │   ├── rusty.py
│   │   │   │   ├── schema.py
│   │   │   │   ├── strings.py
│   │   │   │   └── trans.py
│   │   │   ├── blackd
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __main__.py
│   │   │   │   ├── client.py
│   │   │   │   └── middlewares.py
│   │   │   ├── blib2to3
│   │   │   │   ├── pgen2
│   │   │   │   ├── __init__.py
│   │   │   │   ├── Grammar.txt
│   │   │   │   ├── LICENSE
│   │   │   │   ├── PatternGrammar.txt
│   │   │   │   ├── pygram.py
│   │   │   │   ├── pytree.py
│   │   │   │   └── README
│   │   │   ├── _black_version.py
│   │   │   └── _black_version.pyi
│   │   ├── tests
│   │   │   ├── data
│   │   │   │   ├── cases
│   │   │   │   ├── gitignore_used_on_multiple_sources
│   │   │   │   ├── ignore_directory_gitignore_tests
│   │   │   │   ├── ignore_subfolders_gitignore_tests
│   │   │   │   ├── include_exclude_tests
│   │   │   │   ├── invalid_gitignore_tests
│   │   │   │   ├── invalid_nested_gitignore_tests
│   │   │   │   ├── jupyter
│   │   │   │   ├── line_ranges_formatted
│   │   │   │   ├── miscellaneous
│   │   │   │   ├── nested_gitignore_tests
│   │   │   │   ├── project_metadata
│   │   │   │   ├── empty_pyproject.toml
│   │   │   │   ├── incorrect_spelling.toml
│   │   │   │   └── invalid_line_ranges.toml
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── empty.toml
│   │   │   ├── optional.py
│   │   │   ├── test.toml
│   │   │   ├── test_black.py
│   │   │   ├── test_blackd.py
│   │   │   ├── test_concurrency_manager_shutdown.py
│   │   │   ├── test_docs.py
│   │   │   ├── test_format.py
│   │   │   ├── test_ipynb.py
│   │   │   ├── test_no_ipynb.py
│   │   │   ├── test_ranges.py
│   │   │   ├── test_schema.py
│   │   │   ├── test_tokenize.py
│   │   │   ├── test_trans.py
│   │   │   └── util.py
│   │   ├── .flake8
│   │   ├── .git_archival.txt
│   │   ├── .gitattributes
│   │   ├── .gitignore
│   │   ├── .pre-commit-config.yaml
│   │   ├── .pre-commit-hooks.yaml
│   │   ├── .prettierrc.yaml
│   │   ├── .readthedocs.yaml
│   │   ├── action.yml
│   │   ├── AUTHORS.md
│   │   ├── CHANGES.md
│   │   ├── CITATION.cff
│   │   ├── CONTRIBUTING.md
│   │   ├── Dockerfile
│   │   ├── LICENSE
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   ├── SECURITY.md
│   │   └── tox.ini
│   ├── repoyo4pcer9
│   │   ├── build/ ... (collapsed)
│   │   ├── pre_commit_hooks
│   │   │   ├── __init__.py
│   │   │   ├── check_added_large_files.py
│   │   │   ├── check_ast.py
│   │   │   ├── check_builtin_literals.py
│   │   │   ├── check_case_conflict.py
│   │   │   ├── check_docstring_first.py
│   │   │   ├── check_executables_have_shebangs.py
│   │   │   ├── check_json.py
│   │   │   ├── check_merge_conflict.py
│   │   │   ├── check_shebang_scripts_are_executable.py
│   │   │   ├── check_symlinks.py
│   │   │   ├── check_toml.py
│   │   │   ├── check_vcs_permalinks.py
│   │   │   ├── check_xml.py
│   │   │   ├── check_yaml.py
│   │   │   ├── debug_statement_hook.py
│   │   │   ├── destroyed_symlinks.py
│   │   │   ├── detect_aws_credentials.py
│   │   │   ├── detect_private_key.py
│   │   │   ├── end_of_file_fixer.py
│   │   │   ├── file_contents_sorter.py
│   │   │   ├── fix_byte_order_marker.py
│   │   │   ├── forbid_new_submodules.py
│   │   │   ├── mixed_line_ending.py
│   │   │   ├── no_commit_to_branch.py
│   │   │   ├── pretty_format_json.py
│   │   │   ├── removed.py
│   │   │   ├── requirements_txt_fixer.py
│   │   │   ├── sort_simple_yaml.py
│   │   │   ├── string_fixer.py
│   │   │   ├── tests_should_end_in_test.py
│   │   │   ├── trailing_whitespace_fixer.py
│   │   │   └── util.py
│   │   ├── py_env-python3
│   │   │   ├── Include
│   │   │   ├── Lib
│   │   │   │   └── site-packages
│   │   │   ├── Scripts
│   │   │   │   ├── activate
│   │   │   │   ├── activate.bat
│   │   │   │   ├── activate.fish
│   │   │   │   ├── activate.nu
│   │   │   │   ├── activate.ps1
│   │   │   │   ├── activate.xsh
│   │   │   │   ├── activate_this.py
│   │   │   │   ├── check-added-large-files.exe
│   │   │   │   ├── check-ast.exe
│   │   │   │   ├── check-builtin-literals.exe
│   │   │   │   ├── check-case-conflict.exe
│   │   │   │   ├── check-docstring-first.exe
│   │   │   │   ├── check-executables-have-shebangs.exe
│   │   │   │   ├── check-json.exe
│   │   │   │   ├── check-merge-conflict.exe
│   │   │   │   ├── check-shebang-scripts-are-executable.exe
│   │   │   │   ├── check-symlinks.exe
│   │   │   │   ├── check-toml.exe
│   │   │   │   ├── check-vcs-permalinks.exe
│   │   │   │   ├── check-xml.exe
│   │   │   │   ├── check-yaml.exe
│   │   │   │   ├── deactivate.bat
│   │   │   │   ├── debug-statement-hook.exe
│   │   │   │   ├── destroyed-symlinks.exe
│   │   │   │   ├── detect-aws-credentials.exe
│   │   │   │   ├── detect-private-key.exe
│   │   │   │   ├── double-quote-string-fixer.exe
│   │   │   │   ├── end-of-file-fixer.exe
│   │   │   │   ├── file-contents-sorter.exe
│   │   │   │   ├── fix-byte-order-marker.exe
│   │   │   │   ├── forbid-new-submodules.exe
│   │   │   │   ├── mixed-line-ending.exe
│   │   │   │   ├── name-tests-test.exe
│   │   │   │   ├── no-commit-to-branch.exe
│   │   │   │   ├── pip-3.14.exe
│   │   │   │   ├── pip.exe
│   │   │   │   ├── pip3.14.exe
│   │   │   │   ├── pip3.exe
│   │   │   │   ├── pre-commit-hooks-removed.exe
│   │   │   │   ├── pretty-format-json.exe
│   │   │   │   ├── pydoc.bat
│   │   │   │   ├── python.exe
│   │   │   │   ├── python3
│   │   │   │   ├── python3.exe
│   │   │   │   ├── pythonw.exe
│   │   │   │   ├── pythonw3.exe
│   │   │   │   ├── requirements-txt-fixer.exe
│   │   │   │   ├── sort-simple-yaml.exe
│   │   │   │   ├── trailing-whitespace-fixer.exe
│   │   │   │   └── venvlauncher.exe
│   │   │   ├── .gitignore
│   │   │   ├── .install_state_v1
│   │   │   ├── .install_state_v2
│   │   │   ├── CACHEDIR.TAG
│   │   │   └── pyvenv.cfg
│   │   ├── testing
│   │   │   ├── resources
│   │   │   │   ├── aws_config_with_multiple_sections.ini
│   │   │   │   ├── aws_config_with_secret.ini
│   │   │   │   ├── aws_config_with_secret_and_session_token.ini
│   │   │   │   ├── aws_config_with_session_token.ini
│   │   │   │   ├── aws_config_without_secrets.ini
│   │   │   │   ├── aws_config_without_secrets_with_spaces.ini
│   │   │   │   ├── bad_json.notjson
│   │   │   │   ├── bad_json_latin1.nonjson
│   │   │   │   ├── bad_xml.notxml
│   │   │   │   ├── bad_yaml.notyaml
│   │   │   │   ├── cannot_parse_ast.notpy
│   │   │   │   ├── does_exist
│   │   │   │   ├── duplicate_key_json.notjson
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── non_ascii_pretty_formatted_json.json
│   │   │   │   ├── nonsense.txt
│   │   │   │   ├── not_pretty_formatted_json.json
│   │   │   │   ├── ok_json.json
│   │   │   │   ├── ok_xml.xml
│   │   │   │   ├── ok_yaml.yaml
│   │   │   │   ├── pretty_formatted_json.json
│   │   │   │   ├── tab_pretty_formatted_json.json
│   │   │   │   ├── top_sorted_json.json
│   │   │   │   └── unsorted_pretty_formatted_json.json
│   │   │   ├── __init__.py
│   │   │   └── util.py
│   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── check_added_large_files_test.py
│   │   │   ├── check_ast_test.py
│   │   │   ├── check_builtin_literals_test.py
│   │   │   ├── check_case_conflict_test.py
│   │   │   ├── check_docstring_first_test.py
│   │   │   ├── check_executables_have_shebangs_test.py
│   │   │   ├── check_illegal_windows_names_test.py
│   │   │   ├── check_json_test.py
│   │   │   ├── check_merge_conflict_test.py
│   │   │   ├── check_shebang_scripts_are_executable_test.py
│   │   │   ├── check_symlinks_test.py
│   │   │   ├── check_toml_test.py
│   │   │   ├── check_vcs_permalinks_test.py
│   │   │   ├── check_xml_test.py
│   │   │   ├── check_yaml_test.py
│   │   │   ├── conftest.py
│   │   │   ├── debug_statement_hook_test.py
│   │   │   ├── destroyed_symlinks_test.py
│   │   │   ├── detect_aws_credentials_test.py
│   │   │   ├── detect_private_key_test.py
│   │   │   ├── end_of_file_fixer_test.py
│   │   │   ├── file_contents_sorter_test.py
│   │   │   ├── fix_byte_order_marker_test.py
│   │   │   ├── forbid_new_submodules_test.py
│   │   │   ├── mixed_line_ending_test.py
│   │   │   ├── no_commit_to_branch_test.py
│   │   │   ├── pretty_format_json_test.py
│   │   │   ├── readme_test.py
│   │   │   ├── removed_test.py
│   │   │   ├── requirements_txt_fixer_test.py
│   │   │   ├── sort_simple_yaml_test.py
│   │   │   ├── string_fixer_test.py
│   │   │   ├── tests_should_end_in_test_test.py
│   │   │   ├── trailing_whitespace_fixer_test.py
│   │   │   └── util_test.py
│   │   ├── .gitignore
│   │   ├── .pre-commit-config.yaml
│   │   ├── .pre-commit-hooks.yaml
│   │   ├── CHANGELOG.md
│   │   ├── LICENSE
│   │   ├── README.md
│   │   ├── requirements-dev.txt
│   │   ├── setup.cfg
│   │   ├── setup.py
│   │   └── tox.ini
│   ├── .lock
│   ├── db.db
│   └── README
├── .ruff_cache/ ... (collapsed)
├── .venv/ ... (collapsed)
├── app
│   ├── builders
│   │   └── git_tool_builder.deprecated.py
│   ├── cli
│   │   ├── commands
│   │   │   ├── backup
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── changelog
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── cleanup
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── configure
│   │   │   ├── git_ops
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── init
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── main
│   │   │   │   ├── command.py
│   │   │   │   ├── help.old.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── run
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── validate
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── version
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   ├── workflow
│   │   │   │   ├── command.py
│   │   │   │   ├── models.py
│   │   │   │   ├── options.py
│   │   │   │   └── resolver.py
│   │   │   └── __init__.py
│   │   ├── constants
│   │   │   ├── __init__.py
│   │   │   ├── args.py
│   │   │   ├── completions.py
│   │   │   └── enums.py
│   │   ├── context
│   │   │   └── app_context.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   └── versions.py
│   │   ├── __init__.py
│   │   ├── error_handler.py
│   │   └── main.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   └── custy_config_loader.py
│   ├── constants
│   │   ├── git_workflow_rules.py
│   │   ├── path.py
│   │   └── resolver.py
│   ├── core
│   │   ├── backup
│   │   │   ├── __init__.py
│   │   │   └── backup_manager.py
│   │   ├── branch_workflow
│   │   │   ├── __init__.py
│   │   │   └── branch_workflow_manager.py
│   │   ├── build/ ... (collapsed)
│   │   ├── changelog
│   │   │   ├── config
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   └── resolver.py
│   │   │   ├── integration
│   │   │   │   ├── generation.py
│   │   │   │   ├── pending_commit_integrator.py
│   │   │   │   └── placement.py
│   │   │   ├── models
│   │   │   │   ├── changelog.py
│   │   │   │   ├── commit.py
│   │   │   │   ├── commit_group.py
│   │   │   │   ├── commit_scope.py
│   │   │   │   ├── commit_section.py
│   │   │   │   ├── commit_subsection.py
│   │   │   │   ├── contributors.py
│   │   │   │   ├── metadata.py
│   │   │   │   ├── release.py
│   │   │   │   ├── statistics.py
│   │   │   │   └── template.py
│   │   │   ├── old
│   │   │   │   ├── __init__.py
│   │   │   │   ├── changelog_cleaner.py
│   │   │   │   ├── changelog_generator.py
│   │   │   │   ├── message_aggregator.py
│   │   │   │   ├── message_providers.py
│   │   │   │   └── pipeline.py
│   │   │   ├── parsing
│   │   │   │   └── patterns.py
│   │   │   ├── processing
│   │   │   │   ├── cleaner.py
│   │   │   │   ├── commit_scope_grouper.py
│   │   │   │   ├── commit_type_grouper.py
│   │   │   │   ├── deduplicator.py
│   │   │   │   ├── expander.py
│   │   │   │   ├── parser.py
│   │   │   │   ├── pipeline.py
│   │   │   │   └── tag_behavior.py
│   │   │   ├── providers
│   │   │   │   ├── base.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── git_provider.py
│   │   │   │   └── pending_commit_provider.py
│   │   │   ├── rendering
│   │   │   │   ├── context.py
│   │   │   │   ├── jinja_renderer.py
│   │   │   │   ├── renderer.py
│   │   │   │   └── template_loader.py
│   │   │   ├── sorting
│   │   │   │   ├── base.py
│   │   │   │   └── release_sorter.py
│   │   │   └── generator.py
│   │   ├── cleanup
│   │   │   ├── backups
│   │   │   ├── branch
│   │   │   │   ├── display.py
│   │   │   │   ├── exceptions.py
│   │   │   │   ├── handler.py
│   │   │   │   ├── models.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── branch_cleaner.py
│   │   │   └── handle_cleanup_branches.py
│   │   ├── decorators
│   │   │   └── log_decorators.py
│   │   ├── Docs
│   │   │   └── docs_generator.dev.py
│   │   ├── dry_run
│   │   │   ├── __init__.py
│   │   │   ├── dry_run.py
│   │   │   └── dry_run_support.py
│   │   ├── editor
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── settings.py
│   │   ├── exceptions
│   │   │   └── validation_error.py
│   │   ├── files
│   │   │   ├── __init__.py
│   │   │   └── update_files.py
│   │   ├── git_ops
│   │   │   ├── commit
│   │   │   │   └── validator.py
│   │   │   ├── credentials
│   │   │   ├── engine
│   │   │   │   ├── __init__.py
│   │   │   │   └── git_workflow_engine.deprecated.py
│   │   │   ├── git
│   │   │   │   ├── executor.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── protocol.py
│   │   │   │   ├── result.py
│   │   │   │   └── service.py
│   │   │   ├── helper
│   │   │   │   ├── __init__.py
│   │   │   │   ├── commitizen.py
│   │   │   │   ├── git_helper.deprecated.py
│   │   │   │   ├── git_helper.py
│   │   │   │   ├── git_helper1.deprecated.py
│   │   │   │   ├── pep440_helper.py
│   │   │   │   ├── project_detector.py
│   │   │   │   ├── semver_helper.deprecated.py
│   │   │   │   ├── semver_helper.py
│   │   │   │   ├── version_helper_base.py
│   │   │   │   └── version_utils.py
│   │   │   ├── hooks
│   │   │   ├── tag_sorter
│   │   │   │   ├── base.py
│   │   │   │   ├── date_sorter.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── git_count_sorter.py
│   │   │   │   ├── pep440_sorter.py
│   │   │   │   └── semver_sorter.py
│   │   │   ├── tag_strategy
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── commitizen_strategy.py
│   │   │   │   ├── date_strategy.py
│   │   │   │   ├── git_count_strategy.py
│   │   │   │   ├── pep440_strategy.py
│   │   │   │   └── semver_strategy.py
│   │   │   ├── versioning
│   │   │   │   ├── builder
│   │   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   └── version_bridge.py
│   │   │   └── __init__.py
│   │   ├── initialize
│   │   │   ├── builder
│   │   │   │   └── init_builder.py
│   │   │   ├── models
│   │   │   │   ├── init_config.py
│   │   │   │   ├── init_spec.py
│   │   │   │   ├── initialization_result.py
│   │   │   │   ├── template_dir.py
│   │   │   │   └── template_file.py
│   │   │   ├── presenters
│   │   │   │   └── initialization_presenter.py
│   │   │   ├── services
│   │   │   │   └── scaffold_generator.py
│   │   │   ├── loader.py
│   │   │   ├── main.py
│   │   │   └── registry.py
│   │   ├── pipeline
│   │   │   ├── decorators
│   │   │   │   └── log_step.py
│   │   │   ├── steps
│   │   │   │   ├── backup
│   │   │   │   ├── initialization
│   │   │   │   ├── validation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── apply_version_step.py
│   │   │   │   ├── backup_step.py
│   │   │   │   ├── base_step.py
│   │   │   │   ├── cleanup_backups_step.py
│   │   │   │   ├── cleanup_branches_step.py
│   │   │   │   ├── commit_step.py
│   │   │   │   ├── edit_files_step.py
│   │   │   │   ├── finalize_workflow_step.py
│   │   │   │   ├── generate_artifacts_step.py
│   │   │   │   ├── generate_changelog_step.py
│   │   │   │   ├── I sent you many files.md
│   │   │   │   ├── prepare_tag_message_step.py
│   │   │   │   ├── prepare_version_step.py
│   │   │   │   ├── push_step.py
│   │   │   │   ├── stage_step.py
│   │   │   │   ├── tag_step.py
│   │   │   │   ├── validate_edited_step.py
│   │   │   │   ├── validate_step.py
│   │   │   │   └── workflow_init_step.py
│   │   │   ├── builder.py
│   │   │   ├── command_resolver.py
│   │   │   ├── context.py
│   │   │   ├── pipeline.py
│   │   │   ├── profiles.py
│   │   │   ├── progress.py
│   │   │   ├── registry.py
│   │   │   └── step_registry.py
│   │   ├── project
│   │   │   ├── __init__.py
│   │   │   └── detector.py
│   │   ├── shared
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   └── result.py
│   │   ├── workflow
│   │   │   ├── workflow_builder.py
│   │   │   ├── workflow_config.py
│   │   │   └── workflow_engine.py
│   │   └── __init__.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── validation.py
│   ├── services
│   │   ├── __init__.py
│   │   └── banner_service.py
│   ├── templates
│   │   ├── changelog
│   │   │   └── changelog.j2
│   │   ├── examples
│   │   │   ├── commit_message
│   │   │   │   ├── since_custy_v1
│   │   │   │   └── since_custy_v2
│   │   │   └── tag_message
│   │   │       ├── since_custy_v1
│   │   │       └── since_custy_v2
│   │   ├── gitignore
│   │   │   └── .gitignore.template
│   │   ├── __version__.py
│   │   └── config.toml
│   ├── theme
│   │   ├── __init__.py
│   │   └── theme.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── banner.py
│   │   ├── console.py
│   │   ├── exceptions.py
│   │   ├── panels.py
│   │   ├── progress.py
│   │   └── tables.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── cli_formatter.py
│   │   ├── logging.old.py
│   │   ├── logging.old1.py
│   │   ├── logging.py
│   │   ├── parsing.py
│   │   └── progress.py
│   ├── __init__.py
│   ├── __main__.deprecated.py
│   ├── __main__.py
│   └── __version__.py
├── build/ ... (collapsed)
├── dist/ ... (collapsed)
├── docker
│   └── editors
│       ├── micro
│       │   └── bindings.json
│       ├── nanorc
│       └── vimrc
├── docs
│   ├── docs_v1
│   │   ├── git
│   │   │   ├── command.md
│   │   │   ├── commit_message.md
│   │   │   └── git_workflow_cases.md
│   │   ├── Q&A
│   │   │   └── git
│   │   │       ├── branch workflow.md
│   │   │       ├── changelogs approach.md
│   │   │       ├── comparison commit and tag message.md
│   │   │       ├── footer section on tag message.md
│   │   │       └── switching version.md
│   │   ├── utils
│   │   │   └── workflow_manager.md
│   │   └── versioning
│   │       ├── full_git_strategy_with_pep440.md
│   │       ├── git_branch_lifecycle.png
│   │       ├── git_branching_strategy_pep440.md
│   │       ├── git_dual_remote_strategy.md
│   │       ├── pep449_commit_type_reference.md
│   │       ├── versinoing_stages_guide.md
│   │       └── versioning.md
│   ├── docs_v2
│   │   └── ALL.md
│   ├── guides
│   │   ├── changelog
│   │   │   ├── core
│   │   │   │   ├── CHANGELOG_WORKFLOW.md
│   │   │   │   ├── DEVELOPER_GUIDE.md
│   │   │   │   ├── SYSTEM_WORKFLOW.md
│   │   │   │   └── USER_GUIDE.md
│   │   │   ├── diagrams
│   │   │   │   ├── 1_system_overview.mmd
│   │   │   │   ├── 2_commit_processing_flow.mmd
│   │   │   │   ├── 3_changelog_generation_flow.mmd
│   │   │   │   ├── 4_template_integration_flow.mmd
│   │   │   │   ├── 5_configuration_influence_flow.mmd
│   │   │   │   └── DIAGRAMS.md
│   │   │   └── images
│   │   │       ├── 1_system_overview.png
│   │   │       ├── 2_commit_processing_flow.png
│   │   │       ├── 3_changelog_generation_flow.png
│   │   │       ├── 4_template_integration_flow.png
│   │   │       └── 5_configuration_influence_flow.png
│   │   ├── cli
│   │   │   ├── 1
│   │   │   │   ├── ALL.md
│   │   │   │   ├── architecture_overview.md
│   │   │   │   ├── developer_guide.md
│   │   │   │   ├── mermaid_flow.md
│   │   │   │   └── system_core.md
│   │   │   └── 2
│   │   │       ├── ALL.md
│   │   │       ├── architecture.md
│   │   │       ├── cli_usage.md
│   │   │       ├── developer_guide.md
│   │   │       ├── flow_diagram.md
│   │   │       └── pipeline.md
│   │   ├── git_helper
│   │   │   ├── core
│   │   │   │   ├── architecture_overview.md
│   │   │   │   ├── developer_guide.md
│   │   │   │   └── workflow_and_fail_safe.md
│   │   │   ├── diagrams
│   │   │   │   └── architecture_diagram.md
│   │   │   └── ALL.md
│   │   ├── GitWorkflowEngine
│   │   │   └── custy_pipeline_system
│   │   │       ├── ALL.md
│   │   │       ├── architecture_diagram.md
│   │   │       └── developer_guide.md
│   │   ├── installation
│   │   │   └── auto_completion
│   │   │       └── auto_completion.md
│   │   ├── new_workflow_engine
│   │   │   ├── ALL.md
│   │   │   ├── diagrams.md
│   │   │   └── workflow_engine.md
│   │   └── make_workflows.md
│   ├── temp/ ... (collapsed)
│   ├── badges.md
│   ├── cli_commands_custy.md
│   ├── HOW_TO_USE.md
│   ├── project_structure.md
│   ├── references.md
│   ├── TODO.md
│   ├── TODO_tracking_history.md
│   ├── TODO_tracking_history_v2.0.0-rc.1.md
│   ├── TODO_tracking_history_v2.0.0.md
│   └── TODO_tracking_history_v2.1.0.md
├── logs/ ... (collapsed)
├── make
│   ├── backups
│   │   └── Full_Makefile - 25082026
│   └── core
│       ├── build_publish
│       │   ├── command.mk
│       │   └── help.mk
│       ├── ci
│       │   ├── command.mk
│       │   └── help.mk
│       ├── cleanup
│       │   ├── command.mk
│       │   └── help.mk
│       ├── compose
│       │   ├── command
│       │   │   ├── common.mk
│       │   │   └── core.mk
│       │   └── help.mk
│       ├── docker
│       │   ├── command
│       │   │   ├── common.mk
│       │   │   └── core.mk
│       │   └── help.mk
│       ├── documentation
│       │   ├── command.mk
│       │   └── help.mk
│       ├── examples
│       │   └── help.mk
│       ├── git
│       │   ├── command.mk
│       │   └── help.mk
│       ├── help
│       │   ├── command.mk
│       │   ├── helper.mk
│       │   └── variable.mk
│       ├── helpers
│       │   ├── common.mk
│       │   └── registry.mk
│       ├── lint_format
│       │   ├── command.mk
│       │   └── help.mk
│       ├── local
│       │   ├── command.mk
│       │   └── help.mk
│       ├── qa
│       │   ├── command.mk
│       │   └── help.mk
│       ├── remote
│       │   ├── command
│       │   │   ├── registry.mk
│       │   │   └── runtime.mk
│       │   └── help.mk
│       ├── setup_install
│       │   ├── command.mk
│       │   └── help.mk
│       ├── testing
│       │   ├── command.mk
│       │   └── help.mk
│       └── variables
│           ├── help.mk
│           └── variable.mk
├── scripts
│   ├── ci
│   └── docs
│       └── venv/ ... (collapsed)
├── tests
│   ├── cli
│   │   ├── commands
│   │   │   ├── backup
│   │   │   │   ├── test_command_backup.py
│   │   │   │   ├── test_models_backup.py
│   │   │   │   ├── test_options_backup.py
│   │   │   │   └── test_resolver_backup.py
│   │   │   ├── changelog
│   │   │   │   ├── test_command_changelog.py
│   │   │   │   ├── test_models_changelog.py
│   │   │   │   ├── test_options_changelog.py
│   │   │   │   └── test_resolver_changelog.py
│   │   │   ├── cleanup
│   │   │   │   ├── test_command_cleanup.py
│   │   │   │   ├── test_models_cleanup.py
│   │   │   │   ├── test_options_cleanup.py
│   │   │   │   └── test_resolver_cleanup.py
│   │   │   ├── configure
│   │   │   ├── git_ops
│   │   │   │   ├── test_command_git_ops.py
│   │   │   │   ├── test_models_git_ops.py
│   │   │   │   ├── test_options_git_ops.py
│   │   │   │   └── test_resolver_git_ops.py
│   │   │   ├── init
│   │   │   │   ├── test_command.py
│   │   │   │   ├── test_models.py
│   │   │   │   ├── test_options.py
│   │   │   │   └── test_resolver.py
│   │   │   ├── main
│   │   │   │   ├── test_command.py
│   │   │   │   ├── test_models.py
│   │   │   │   ├── test_options.py
│   │   │   │   └── test_resolver.py
│   │   │   ├── run
│   │   │   │   ├── test_command_run.py
│   │   │   │   ├── test_models_run.py
│   │   │   │   ├── test_options_run.py
│   │   │   │   └── test_resolver_run.py
│   │   │   ├── validate
│   │   │   │   ├── test_command_validate.py
│   │   │   │   ├── test_models_validate.py
│   │   │   │   ├── test_options_validate.py
│   │   │   │   └── test_resolver_validate.py
│   │   │   ├── version
│   │   │   │   ├── test_command_version.py
│   │   │   │   ├── test_models_version.py
│   │   │   │   ├── test_options_version.py
│   │   │   │   └── test_resolver_version.py
│   │   │   └── workflow
│   │   │       ├── test_command_workflow.py
│   │   │       ├── test_models_workflow.py
│   │   │       ├── test_options_workflow.py
│   │   │       └── test_resolver_workflow.py
│   │   ├── constants
│   │   │   ├── test_args.py
│   │   │   ├── test_completions.py
│   │   │   └── test_enums.py
│   │   ├── context
│   │   │   └── test_app_context.py
│   │   ├── utils
│   │   │   ├── test_completion.py
│   │   │   └── test_validators.py
│   │   ├── test_error_handler.py
│   │   └── test_main.py
│   ├── config
│   │   ├── test_config_loader.py
│   │   └── test_config_resolution.py
│   ├── constants
│   │   ├── test_git_workflow_rules.py
│   │   └── test_path.py
│   ├── core
│   │   ├── backup
│   │   │   └── test_backup_manager.py
│   │   ├── branch_workflow
│   │   │   └── test_branch_workflow_manager.py
│   │   ├── build/ ... (collapsed)
│   │   ├── changelog
│   │   │   ├── test_generator.py
│   │   │   ├── test_processing.py
│   │   │   ├── test_release_sorter.py
│   │   │   ├── test_rendering.py
│   │   │   └── test_template_loader.py
│   │   ├── cleanup
│   │   │   ├── backups
│   │   │   └── branch
│   │   │       ├── test_display.py
│   │   │       ├── test_handler.py
│   │   │       ├── test_models.py
│   │   │       └── test_service.py
│   │   ├── editor
│   │   │   ├── test_docker_assets.py
│   │   │   ├── test_service.py
│   │   │   └── test_settings.py
│   │   ├── files
│   │   │   └── test_cross_project_version_updates.py
│   │   ├── git_ops
│   │   │   ├── commit
│   │   │   ├── credentials
│   │   │   ├── git
│   │   │   │   ├── test_executor_commit.py
│   │   │   │   ├── test_executor_core.py
│   │   │   │   ├── test_executor_log.py
│   │   │   │   ├── test_executor_runner.py
│   │   │   │   ├── test_factory.py
│   │   │   │   ├── test_protocol.py
│   │   │   │   ├── test_result.py
│   │   │   │   ├── test_service_advanced.py
│   │   │   │   ├── test_service_basic.py
│   │   │   │   ├── test_service_branch.py
│   │   │   │   ├── test_service_changelog.py
│   │   │   │   ├── test_service_commit.py
│   │   │   │   ├── test_service_diff.py
│   │   │   │   ├── test_service_log.py
│   │   │   │   ├── test_service_parser.py
│   │   │   │   ├── test_service_push.py
│   │   │   │   ├── test_service_remote.py
│   │   │   │   ├── test_service_stage.py
│   │   │   │   ├── test_service_tag.py
│   │   │   │   └── test_service_tags.py
│   │   │   ├── helper
│   │   │   ├── hooks
│   │   │   ├── tag_sorter
│   │   │   │   ├── test_date_sorter.py
│   │   │   │   ├── test_factory.py
│   │   │   │   ├── test_git_count_sorter.py
│   │   │   │   ├── test_pep440_sorter.py
│   │   │   │   └── test_semver_sorter.py
│   │   │   └── tag_strategy
│   │   │       ├── test_base.py
│   │   │       ├── test_commitizen_strategy.py
│   │   │       ├── test_date_strategy.py
│   │   │       ├── test_git_count_strategy.py
│   │   │       ├── test_pep440_strategy.py
│   │   │       └── test_semver_strategy.py
│   │   ├── initialize
│   │   │   └── models
│   │   │       ├── test_init_builder.py
│   │   │       ├── test_initialization_presenter.py
│   │   │       ├── test_loader.py
│   │   │       ├── test_main.py
│   │   │       ├── test_models.py
│   │   │       ├── test_registry.py
│   │   │       └── test_scaffold_generator.py
│   │   ├── pipeline
│   │   │   ├── steps
│   │   │   │   ├── backup
│   │   │   │   ├── cleanup
│   │   │   │   ├── initialization
│   │   │   │   ├── validation
│   │   │   │   ├── test_apply_version_step.py
│   │   │   │   ├── test_backup_tag_message_step.py
│   │   │   │   ├── test_commit_step.py
│   │   │   │   ├── test_edit_files_step.py
│   │   │   │   ├── test_finalize_workflow_step.py
│   │   │   │   ├── test_generate_artifacts_step.py
│   │   │   │   ├── test_generate_changelog_step.py
│   │   │   │   ├── test_prepare_tag_message_step.py
│   │   │   │   ├── test_prepare_version_step.py
│   │   │   │   ├── test_push_step.py
│   │   │   │   ├── test_stage_step.py
│   │   │   │   ├── test_tag_step.py
│   │   │   │   ├── test_validate_edited_step.py
│   │   │   │   └── test_workflow_init_step.py
│   │   │   ├── test_command_resolver.py
│   │   │   ├── test_pipeline_builder.py
│   │   │   ├── test_pipeline_runtime.py
│   │   │   └── test_profiles.py
│   │   ├── project
│   │   │   └── test_detector.py
│   │   └── workflow
│   │       ├── conftest.py
│   │       ├── test_workflow_backup.py
│   │       ├── test_workflow_builder.py
│   │       ├── test_workflow_changelog.py
│   │       ├── test_workflow_cleanup.py
│   │       ├── test_workflow_commit.py
│   │       ├── test_workflow_commit_errors.py
│   │       ├── test_workflow_config.py
│   │       ├── test_workflow_engine.py
│   │       ├── test_workflow_orchestration.py
│   │       ├── test_workflow_push.py
│   │       ├── test_workflow_push_remote.py
│   │       ├── test_workflow_push_resolve.py
│   │       ├── test_workflow_stage.py
│   │       ├── test_workflow_stage_changes.py
│   │       ├── test_workflow_stage_validation.py
│   │       ├── test_workflow_tag.py
│   │       ├── test_workflow_validation.py
│   │       └── test_workflow_versioning.py
│   ├── data
│   │   ├── changelog
│   │   │   └── .gitkeep
│   │   ├── commits
│   │   │   └── .gitkeep
│   │   ├── configs
│   │   │   └── .gitkeep
│   │   ├── git
│   │   │   └── .gitkeep
│   │   ├── templates
│   │   │   └── .gitkeep
│   │   ├── versions
│   │   │   └── .gitkeep
│   │   └── workflow
│   │       └── .gitkeep
│   ├── fixtures
│   │   ├── changelog
│   │   │   └── ideal_output.md
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── filesystem.py
│   │   ├── git.py
│   │   ├── pipeline.py
│   │   ├── project.py
│   │   ├── templates.py
│   │   ├── version.py
│   │   └── workflow.py
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── assertions.py
│   │   ├── cli.py
│   │   ├── filesystem.py
│   │   └── git.py
│   ├── integration
│   │   ├── test_backup_flow.py
│   │   ├── test_cleanup_flow.py
│   │   ├── test_cross_project_startup.py
│   │   ├── test_dev_flow.py
│   │   ├── test_init_flow.py
│   │   ├── test_release_flow.py
│   │   ├── test_run_profiles.py
│   │   ├── test_validate_flow.py
│   │   └── test_workflow_flow.py
│   ├── logging
│   │   ├── test_dry_run.py
│   │   ├── test_dry_run_support.py
│   │   └── test_logging.py
│   ├── regression
│   │   ├── test_command_resolver_regressions.py
│   │   ├── test_config_loader_regressions.py
│   │   ├── test_make_reflow_workflows.py
│   │   ├── test_pipeline_builder_regressions.py
│   │   ├── test_pipeline_regressions.py
│   │   ├── test_release_builder_regressions.py
│   │   ├── test_step_registry_regressions.py
│   │   ├── test_version_builder_regressions.py
│   │   └── test_workflow_builder_regressions.py
│   ├── services
│   │   └── test_banner_service.py
│   ├── snapshots
│   │   └── cli
│   │       └── README.md
│   ├── theme
│   │   └── test_theme.py
│   ├── ui
│   │   ├── test_banner.py
│   │   ├── test_console.py
│   │   ├── test_exceptions.py
│   │   ├── test_panels.py
│   │   ├── test_progress.py
│   │   └── test_tables.py
│   ├── utils
│   │   ├── test_logging_formatter.py
│   │   ├── test_logging_setup.py
│   │   └── test_parsing.py
│   ├── __init__.py
│   ├── CHANGELOG.md
│   ├── conftest.py
│   ├── README.md
│   ├── REVIEW.md
│   └── test___main__.py
├── tools
│   ├── generate_ignore
│   │   ├── __init__.py
│   │   ├── __version__.py
│   │   └── generate_ignore_files.py
│   └── __init__.py
├── venv/ ... (collapsed)
├── .coverage
├── .cz.toml
├── .cz_changelog.j2
├── .dockerignore
├── .editorconfig
├── .gitignore
├── .gitlab-ci.yml
├── .pre-commit-config.yaml
├── .prettierignore
├── .prettierrc.json
├── .projectignore
├── AGENTS.md
├── CHANGELOG.md
├── CHANGES FOR THIS ANOTHER.txt
├── CHANGES FOR THIS.txt
├── CONTRIBUTING.md
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docker-compose.yml
├── Dockerfile
├── example-command.txt
├── LICENSE
├── Makefile
├── NOTES_WHILE_DEVELOPMENT.md
├── pyproject.toml
├── README.md
├── requirements.txt
├── SECURITY.md
├── temp_todo.md
├── TODO.md
└── WHAT_TO_DO.md
```

---

## Root Files

| File | Description |
|------|-------------|
| `README.md` | Project overview and introduction. |
| `CHANGELOG.md` | History of notable changes between releases. |
| `LICENSE` | Project license information. |
| `CONTRIBUTING.md` | Guidelines for contributing to the project. |
| `SECURITY.md` | Security policy and vulnerability reporting instructions. |
| `TODO.md` | Pending tasks and future improvements. |
| `AGENTS.md` | Instructions and guidance for AI agents and automation tools. |
| `pyproject.toml` | Main Python project configuration file. |
| `requirements.txt` | Python package dependencies. |
| `Makefile` | Defines common development, testing, and build commands. |
| `Dockerfile` | Container image build instructions. |
| `docker-compose.yml` | Default multi-container Docker configuration. |
| `docker-compose.dev.yml` | Development Docker Compose configuration. |
| `docker-compose.prod.yml` | Production Docker Compose configuration. |
| `.gitignore` | Specifies files and directories ignored by Git. |
| `.dockerignore` | Specifies files excluded from Docker build context. |
| `.editorconfig` | Editor configuration for consistent coding styles. |
| `.prettierrc.json` | Prettier code formatting configuration. |
| `.prettierignore` | Files ignored by Prettier. |
| `.pre-commit-config.yaml` | Pre-commit hooks configuration. |
| `.projectignore` | Ignore rules for project utilities and scanners. |
| `.cz.toml` | Configuration for Commitizen commit conventions. |
| `.cz_changelog.j2` | Commitizen changelog template. |
| `.gitlab-ci.yml` | GitLab CI/CD pipeline configuration. |

---

## Directory Details

### `.config/`
Project configuration files.

Stores reusable configuration files used by the project.
Helps keep the repository root clean and organized.

Common examples:
- .config/tool-config/
- .config/templates/
- .config/settings/

### `app/`
Main application source code.

Contains the core implementation of the project.
May include business logic, services, modules, and utilities.

### `docs/`
Project documentation and technical references.

The documentation folder usually contains structured knowledge about the project.

Common documentation sections:
- docs/architecture        → system design and architecture diagrams
- docs/development         → development guides and workflows
- docs/system              → detailed technical documentation
- docs/reference           → command references and APIs
- docs/user-guide          → instructions for end users
- docs/diagrams            → visual architecture diagrams
- docs/phases              → project phases and planning
- docs/Q&A                 → common questions and explanations

Common files:
- PROJECT_STRUCTURE.md
- DEVELOPMENT_GUIDE.md
- HOW_TO_USE.md
- TODO.md
- CLI_COMMAND.md
- references.md
- badges.md

### `scripts/`
Utility scripts for development or automation.

May include deployment scripts, maintenance tools, or helpers.

### `tests/`
Automated tests.

Contains unit tests and integration tests.
Ensures code reliability and correctness.

### `tools/`
Development tools and automation utilities.

Contains scripts used during development and maintenance.

Common examples:
- tools/generate_ignore     → generate .gitignore, .dockerignore
- tools/project_structure   → generate PROJECT_STRUCTURE.md
- tools/git_commit          → commit and tagging automation tools


---

## Notes

- Temporary files, caches, and environment directories are excluded.
- Structure is generated automatically using DocGen.

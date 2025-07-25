```
=====
/root (project type: python)
├── .cz.toml
├── .cz_changelog.j2
├── .editorconfig
├── .gitignore
├── .projectignore
├── Makefile
├── README.md
├── app
│   ├── __init__.py
│   ├── __main__.py
│   ├── __version__.py
│   ├── backups
│   │   ├── commit-msg_%Y0723_114112.bak.txt
│   │   ├── commit-msg_%Y0723_115008.bak.txt
│   │   └── commit-msg_%Y0723_171525.bak.txt
│   ├── commit-msg.txt
│   ├── git_commit_tagger.py
│   └── utils
│       ├── __init__.py
│       ├── changelog_generator.py
│       ├── commitizen.py
│       ├── dry_run.py
│       ├── dry_run_support.py
│       ├── git.py
│       └── tag_strategy
│           ├── __init__.py
│           ├── base.py
│           ├── commitizen_strategy.py
│           ├── date_strategy.py
│           ├── git_count_strategy.py
│           └── semver_strategy.py
├── docs
│   ├── cli_commands_custy.md
│   └── project_structure.md
├── pyproject.toml
├── requirements.txt
├── templates
│   ├── .gitignore.template
│   ├── changelog.j2
│   ├── commit-msg.example.txt
│   ├── commit-msg.template.txt
│   └── commit-msg1.example.txt
└── tools
    ├── __init__.py
    ├── generate_ignore
    │   ├── __init__.py
    │   ├── __version__.py
    │   └── generate_ignore_files.py
    ├── project_structure
    │   ├── __init__.py
    │   ├── __version__.py
    │   └── print_project_structure.py
    └── templates
        └── changelog.j2
```
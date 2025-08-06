```
=====
/root (project type: python)
├── .custor.toml
├── .cz.toml
├── .cz_changelog.j2
├── .editorconfig
├── .gitignore
├── .gitlab-ci.yml
├── .projectignore
├── CHANGELOG.md
├── Makefile
├── README.md
├── app
│   ├── __init__.py
│   ├── __main__.py
│   ├── __version__.py
│   ├── debug_tag_release_notes.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── validation_error.py
│   ├── git_commit_tagger.py
│   └── utils
│       ├── __init__.py
│       ├── backup_manager.py
│       ├── branch_cleaner.py
│       ├── changelog_generator.py
│       ├── cli_formatter.py
│       ├── commitizen.py
│       ├── config.py
│       ├── dry_run.py
│       ├── dry_run_support.py
│       ├── git.py
│       ├── pep440_helper.py
│       ├── project_detector.py
│       ├── semver_helper.py
│       ├── tag_strategy
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── commitizen_strategy.py
│       │   ├── date_strategy.py
│       │   ├── git_count_strategy.py
│       │   ├── pep440_strategy.py
│       │   └── semver_strategy.py
│       ├── version_helper_base.py
│       ├── version_utils.py
│       ├── versioning
│       │   ├── __init__.py
│       │   ├── builder
│       │   │   ├── __init__.py
│       │   │   └── release_builder.py
│       │   └── models
│       │       ├── __init__.py
│       │       ├── release_info.py
│       │       └── version_type.py
│       └── workflow_manager.py
├── build
│   ├── bdist.win-amd64
│   └── lib
│       └── app
│           ├── __init__.py
│           ├── __main__.py
│           ├── __version__.py
│           ├── debug_tag_release_notes.py
│           ├── errors
│           │   ├── __init__.py
│           │   └── validation_error.py
│           ├── git_commit_tagger.py
│           └── utils
│               ├── __init__.py
│               ├── backup_manager.py
│               ├── branch_cleaner.py
│               ├── changelog_generator.py
│               ├── commitizen.py
│               ├── config.py
│               ├── dry_run.py
│               ├── dry_run_support.py
│               ├── git.py
│               ├── pep440_helper.py
│               ├── project_detector.py
│               ├── semver_helper.py
│               ├── tag_strategy
│               │   ├── __init__.py
│               │   ├── base.py
│               │   ├── commitizen_strategy.py
│               │   ├── date_strategy.py
│               │   ├── git_count_strategy.py
│               │   ├── pep440_strategy.py
│               │   └── semver_strategy.py
│               ├── version_helper_base.py
│               ├── version_utils.py
│               ├── versioning
│               │   ├── __init__.py
│               │   ├── builder
│               │   │   ├── __init__.py
│               │   │   └── release_builder.py
│               │   └── models
│               │       ├── __init__.py
│               │       ├── release_info.py
│               │       └── version_type.py
│               └── workflow_manager.py
├── docs
│   ├── HOW_TO_USE.md
│   ├── Q&A
│   │   └── git
│   │       ├── branch workflow.md
│   │       ├── changelogs approach.md
│   │       ├── comparison commit and tag message.md
│   │       ├── footer section on tag message.md
│   │       └── switching version.md
│   ├── TODO.md
│   ├── badges.md
│   ├── cli_commands_custy.md
│   ├── git
│   │   ├── command.md
│   │   ├── commit_message.md
│   │   └── git_workflow_cases.md
│   ├── project_structure.md
│   ├── references.md
│   ├── utils
│   │   └── workflow_manager.md
│   └── versioning
│       ├── full_git_strategy_with_pep440.md
│       ├── git_branch_lifecycle.png
│       ├── git_branching_strategy_pep440.md
│       ├── git_dual_remote_strategy.md
│       ├── pep449_commit_type_reference.md
│       ├── versinoing_stages_guide.md
│       └── versioning.md
├── pyproject.toml
├── requirements.txt
├── templates
│   ├── backups
│   │   ├── commit
│   │   │   ├── commit-msg_20250804_134558.bak.txt
│   │   │   ├── commit-msg_20250804_142626.bak.txt
│   │   │   ├── commit-msg_20250805_002110.bak.txt
│   │   │   ├── commit-msg_20250806_175301.bak.txt
│   │   │   ├── commit-msg_20250806_183332.bak.txt
│   │   │   ├── commit-msg_20250806_184348.bak.txt
│   │   │   ├── commit-msg_20250806_184527.bak.txt
│   │   │   ├── commit-msg_20250806_192529.bak.txt
│   │   │   ├── commit-msg_20250806_200816.bak.txt
│   │   │   └── commit-msg_20250806_204642.bak.txt
│   │   └── tag
│   │       ├── tag-msg_20250806_184157.bak.txt
│   │       ├── tag-msg_20250806_184527.bak.txt
│   │       ├── tag-msg_20250806_192317.bak.txt
│   │       ├── tag-msg_20250806_192732.bak.txt
│   │       ├── tag-msg_20250806_203458.bak.txt
│   │       ├── tag-msg_20250806_203754.bak.txt
│   │       ├── tag-msg_20250806_204642.bak.txt
│   │       ├── tag-msg_20250806_212013.bak.txt
│   │       ├── tag-msg_20250806_212329.bak.txt
│   │       └── tag-msg_20250806_213432.bak.txt
│   ├── changelog
│   │   └── changelog.j2
│   ├── commit-msg.txt
│   ├── example
│   │   ├── commit-msg
│   │   │   ├── commit-msg.example.txt
│   │   │   ├── commit-msg.template.txt
│   │   │   ├── commit-msg1.example.txt
│   │   │   ├── commit-msg1.template.txt
│   │   │   ├── commit-msg2.example.txt
│   │   │   ├── commit-msg_beta.example.txt
│   │   │   ├── commit-msg_beta1.example.txt
│   │   │   ├── commit-msg_beta_breaking_changes.example.txt
│   │   │   ├── commit-msg_final--no-changes.example.txt
│   │   │   ├── commit-msg_final.example.txt
│   │   │   ├── commit-msg_final1.example.txt
│   │   │   ├── commit-msg_final_refactor.example.txt
│   │   │   └── commit-msg_rc.example.txt
│   │   ├── gitignore
│   │   │   └── .gitignore.template
│   │   └── tag-msg
│   │       ├── tag-msg_alpha.example.txt
│   │       ├── tag-msg_beta.example.txt
│   │       ├── tag-msg_beta1.example.txt
│   │       ├── tag-msg_beta_breaking_changes.example.txt
│   │       ├── tag-msg_final--no-changes.example.txt
│   │       ├── tag-msg_final.example.txt
│   │       ├── tag-msg_final1.example.txt
│   │       ├── tag-msg_final_refactor.example.txt
│   │       ├── tag-msg_rc.example.txt
│   │       └── tag-msg_rc1.example.txt
│   └── tag-msg.txt
├── tests
│   ├── __init__.py
│   ├── test_pep440_helper.py
│   ├── test_semver_helper.py
│   ├── test_version_transition_case.py
│   └── test_workflow_cases.py
└── tools
    ├── __init__.py
    ├── generate_ignore
    │   ├── __init__.py
    │   ├── __version__.py
    │   └── generate_ignore_files.py
    └── project_structure
        ├── __init__.py
        ├── __version__.py
        └── print_project_structure.py
```
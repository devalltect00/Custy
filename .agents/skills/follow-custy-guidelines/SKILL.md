---
name: follow-custy-guidelines
description: Apply Custy repository permissions, path-specific write policies, AGENTS.md guidance, source-discovery workflow, Python environment rules, coding and documentation standards, logging practices, route metadata requirements, UI/UX guidance, validation workflow, and change-reporting requirements. Use for every task that reads, analyzes, debugs, tests, runs, or changes files in the custy-2 project, especially work under app/, src/, app/cli/, app/core/, or tests/.
---

# Follow Custy Guidelines

## Overview

Apply these rules together with the repository's `AGENTS.md`. Treat the user's latest explicit instruction as authoritative if it changes the permitted scope.

## Obtain Permission Before Actions

1. Before editing, creating, deleting, renaming, moving, or formatting files, tell the user exactly what is intended and ask for confirmation.
2. Before executing any terminal, command-prompt, Git, Python, test, formatter, linter, or application command, explain the command's purpose and ask for confirmation.
3. Read-only file inspection does not require separate confirmation when the user has already authorized reading the repository.
4. Treat a clear instruction such as "start," "make this change," or "run the tests" as confirmation for that stated action and scope. Do not repeatedly ask within the same approved action.
5. Ask again before expanding the scope, performing a materially different action, or doing anything destructive or externally visible.
6. Never infer permission to modify unrelated files.
7. Keep a user-granted permission active for its stated paths, operations, and scope until the user changes or revokes it. Apply this persistence while the permission remains available in the current conversation or continuing task context; otherwise fall back to the stored path policy.

## Read AGENTS.md as a Project Reference

1. Read the repository-root `AGENTS.md` before source analysis, implementation, debugging, testing, or command execution.
2. Use `AGENTS.md` as the primary reference for project purpose, technology, structure, coding standards, documentation style, logging, testing, architecture, Git practices, and completion requirements.
3. Apply `AGENTS.md` together with this skill. Do not treat information in `AGENTS.md` as permission to change a path that this skill protects.
4. If `AGENTS.md` points to unfinished content under `docs/`, treat the link as context only and keep the `docs/` protection in force.
5. If the two files appear to conflict, follow the permission precedence below or ask the user when the correct result is unclear.

## Apply Path-Specific Permissions

Use repository-relative paths. Apply each directory rule recursively to its descendants.

### Permission Meanings

- **Read by default:** Read, inspect, search, and analyze the path without asking. Ask before adding, editing, formatting, replacing, moving, renaming, or deleting anything. After permission is granted, keep it active for the approved operations and scope until the user changes or revokes it.
- **Task-approved write:** After the user approves a task, add or edit files within the path as needed for that task without requesting approval for every individual file.
- **Standing full access:** Read, create, add, edit, modify, format, replace, move, rename, or delete the specified file when relevant to the user's task without requesting additional path-level permission. Do not make unrelated or unnecessary changes.
- **Explicit removal:** Ask for explicit approval before deleting, moving, or renaming a file unless the approved task clearly includes that operation and exact scope.
- **Protected:** Do not add, edit, delete, move, rename, or format files in the path without a specific user override.
- **Default rules:** Apply the general permission requirements in this skill.

### Path Policy

| Path | Permission | Purpose and guidance |
| --- | --- | --- |
| `app/**` | Read by default | Active application source. Ask before any operation that changes files. |
| `app/cli/**` | Read by default | Primary CLI and user-facing application layer. Ask before changes and preserve public CLI behavior unless explicitly approved. |
| `app/core/**` | Read by default | Primary core/backend logic. Ask before changes and preserve clear separation from the CLI layer. |
| `.config/custy/**` | Read by default | Custy configuration and templates. Ask before any operation that changes files. |
| `.agents/skills/**` | Read by default | Project-specific Codex skills. Ask before adding, updating, moving, or removing skill content. |
| `tests/**` | Task-approved write; explicit removal | Add or update tests for approved behavior changes. Do not remove tests merely to make checks pass. |
| `TODO.md` | Standing full access | Maintain the project's task list as needed, including creating, editing, moving, renaming, or removing it when relevant to the user's task. |
| `docs/**` | Protected | Documentation is under development and may be incomplete or unrelated. |
| Backup or temporary Python files | Protected | Preserve personal reference copies and exclude them from active implementation. |
| All other repository paths | Default rules | Ask before making changes unless the user's approved task explicitly includes the path. |

Treat filenames ending in ` copy.py`, `_copy.py`, `_temp.py`, `_temp_before.py`, or similar obvious backup suffixes as protected backup or temporary Python files.

Path authorization is behavioral guidance only. Never use it to bypass system security, sandbox restrictions, required approvals, or a narrower current user instruction.

## Follow Permission Precedence

Apply rules in this order, from highest to lowest priority:

1. System security, sandbox, and tool restrictions
2. The user's latest explicit instruction for the current task
3. File-specific policy or permission
4. Directory-specific policy or permission
5. General rules in this skill and `AGENTS.md`

If applicable rules conflict at the same level or the permitted scope is unclear, stop and ask the user before changing anything.

## Recognize Useful User Permission Requests

Interpret instructions such as these as scoped authorization:

- "Grant edit permission for `app/cli` and `tests`. Do not delete anything."
- "Read `app/core`, but do not modify it."
- "You may add and edit files under `app/core` until I revoke this permission. Ask before moving or deleting files."
- "Revoke edit permission for `app/core`; return it to read by default."
- "For this task, allow changes only to `tests/test_example.py`."

Apply these examples by meaning; do not require the user to use exact wording.

## Understand the Source Before Changing It

On the first source-code task in a session:

1. Build a high-level understanding of the application before implementing a change.
2. Focus source discovery on `app/`, `src/`, or another directory that clearly contains active application code.
3. For Custy, treat `app/cli/` as the primary command-line UI layer and `app/core/` as the primary core/backend layer.
4. Trace the relevant entry points, control flow, data flow, dependencies, and tests across those active source directories.
5. Keep discovery proportional to the task; understand the whole workflow around the requested feature without reading unrelated generated or dependency code.
6. Do not rely on the unfinished `docs/` tree as the source of truth.

## Ignore Backup and Temporary Python Files

Treat obvious backup/reference copies as inactive code, including filenames ending in patterns such as:

- ` copy.py`
- `_copy.py`
- `_temp.py`
- `_temp_before.py`
- Similar suffixes that clearly mark a copied, temporary, or previous-version file

Do not edit, delete, rename, format, import, or treat these files as active implementation. Leave them untouched for the user's reference. If a filename is ambiguous, ask before acting on it.

## Protect Documentation Under Development

Do not add, edit, rename, move, or remove anything under `docs/` unless the user later gives explicit permission that overrides this rule. The directory is under development and may contain incomplete, missing, or unrelated material.

## Use a Project Virtual Environment

For Python work:

1. Always use an existing project virtual environment rather than a global Python installation.
2. Prefer `venv/`. If it is unavailable, look for an existing `env/`, `.venv/`, or versioned environment such as `venv3_14/` or `venv3_13/`.
3. Use the selected environment's Python and executable paths for Python, pytest, linters, formatters, package operations, and application commands.
4. Account for an existing editable installation such as `pip install -e .`; do not reinstall packages without a reason and approval.
5. If no usable virtual environment exists, tell the user and offer either instructions for manual creation or creation by Codex. Do not create one without confirmation.
6. In Custy, run the `custy` command from the selected environment when approved and useful for reproducing bugs or checking application quality.

Examples for the preferred Windows environment include:

```powershell
venv\Scripts\python.exe -m pytest
venv\Scripts\custy.exe --help
```

Treat these as examples, not pre-authorization to execute commands.

## Follow a Complete Work Cycle

For implementation or debugging work:

1. Understand the affected workflow.
2. Describe the intended changes and validation, then obtain confirmation.
3. Make only the approved, focused changes.
4. Add or update tests for changed behavior when applicable.
5. Run focused validation first, followed by broader relevant checks when justified and approved.
6. Finish the current agreed plan before starting a new plan. If blocked or new evidence invalidates the plan, explain why and explicitly revise it rather than silently abandoning it.
7. Do not change public CLI behavior, versions, changelogs, or unrelated files without explicit authorization.

## Document Python Code

Add clear internal documentation to every newly created source file, class, function, and method. When modifying existing code, add or improve documentation for affected public or non-obvious interfaces when needed.

1. Add a module docstring that explains the file's responsibility.
2. Add class docstrings that explain purpose, important state, and behavior.
3. Add function and method docstrings that describe behavior and contracts.
4. Use sections such as `Args`, `Returns`, `Raises`, `Notes`, `Examples`, and `Logic` when they provide useful information.
5. Include types and meaningful descriptions. Document real exceptions and edge cases rather than inventing guarantees.
6. Keep docstrings accurate, concise, and synchronized with the implementation.
7. Avoid empty boilerplate when a section does not apply, unless the surrounding codebase consistently requires it.

Preferred style:

```python
def update_version(new_version: str) -> None:
    """Update the configured version from a semantic-version tag.

    Args:
        new_version: Semantic version, optionally prefixed with ``v``.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        RuntimeError: If the version cannot be updated safely.

    Notes:
        Remove a leading ``v`` before writing the value.
    """
```

## Use Logging Deliberately

1. Use the project's existing logging approach when logs materially help diagnosis or operations.
2. Log useful debug context, informational lifecycle events, warnings, and errors at appropriate levels.
3. Prefer structured, actionable messages that identify the operation and relevant safe context.
4. Avoid duplicate noise, excessive logs, secrets, credentials, tokens, and sensitive user data.
5. Preserve exception context when logging failures.

## Build Backend or Web-Service Routes Carefully

When the project contains HTTP or service routes:

1. Provide route `summary` and `description` metadata when supported by the framework.
2. Add useful route logging through the project's logger when it improves debugging or observability.
3. Do not log secrets, credentials, raw tokens, or sensitive request bodies.
4. Document request parameters, response behavior, expected errors, authorization needs, and important side effects.
5. Add tests for successful requests, validation failures, expected errors, and authorization behavior when applicable.

## Keep UI and UX Clear

For CLI or other user-facing work:

1. Prefer clear, friendly, concise, and actionable language.
2. Use terminology consistently across commands, prompts, help text, errors, and documentation strings.
3. Explain what went wrong and what the user can do next.
4. Preserve accessibility, sensible defaults, predictable navigation, and safe confirmation for consequential actions.
5. Avoid exposing internal implementation details unless they help the user resolve a problem.

## Report the Result

After any completed action, summarize:

- What was added
- What was changed
- What was removed
- Which files were affected
- Which checks or commands ran and their outcomes
- Anything not completed, skipped, or still requiring user action

State explicitly when nothing was removed or when no files outside the approved scope were touched.

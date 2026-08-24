# Temporary v2.0.0 Release Checklist

> Temporary personal checklist. Delete this file before staging the stable
> release commit.

## 1. Confirm the RC Baseline

- [ ] Confirm the `v2.0.0-rc.1` commit, annotated tag, and remote release are complete.
- [ ] Confirm the working branch and remotes are the intended stable-release destinations.
- [ ] Confirm there are no unreviewed user-facing changes after RC.1.

## 2. Manual Repository Cleanup

- [ ] Delete `CHANGES FOR THIS ANOTHER.txt`.
- [ ] Delete `CHANGES FOR THIS.txt`.
- [ ] Delete `NOTES_WHILE_DEVELOPMENT.txt`.
- [ ] Delete `WHAT_TO_DO.txt`.
- [ ] Delete the completed root `TODO.md`.
- [ ] Delete the version-specific `docs/TODO.md`.
- [ ] Review any additional candidate files individually before deleting them.
- [ ] Keep `docs/TODO_tracking_history.md` as the long-term history and roadmap archive.

## 3. Review Stable Release Content

- [ ] Review `docs/TODO_tracking_history.md` after cleanup and update pending checkboxes if needed.
- [ ] Review the final internal commit message and public tag message for accuracy.
- [ ] Ensure user-preference and temporary-file updates are not described as project release changes.
- [ ] Review the final working-tree diff and ensure no temporary or personal files are staged.

## 4. Final Validation

- [ ] Run the complete Custy test suite in the project virtual environment.
- [ ] Run the approved linting, formatting, packaging, and configuration checks.
- [ ] Run `custy validate`.
- [ ] Preview the intended release operation with the global `--dry-run` option.
- [ ] Verify version files, generated changelog content, commit message, tag message, configured remotes, and diagnostic-log destination.
- [ ] Confirm `custy workflow` remains documented as experimental and is not used unintentionally.

## 5. Stable Release

- [ ] Delete this `temp_todo.md` file before staging the release commit.
- [ ] Create the stable release commit with the reviewed commit-message template.
- [ ] Create the SemVer tag `v2.0.0` with the reviewed tag-message template.
- [ ] Push the intended branch and tag to the correct remotes.
- [ ] Verify GitHub and GitLab release pages, artifacts, packages, and container images.
- [ ] Confirm the public documentation and installation instructions resolve correctly.

## 6. After Release

- [ ] Record any post-release issue separately instead of rewriting the published tag.
- [ ] Start a new concise TODO for work planned after v2.0.0, if needed.

# tests/core/changelog/test_processing.py

"""
Unit tests for semantic changelog message processing.

These tests cover body-section expansion, core filtering,
generic fallback handling, and content-aware deduplication.
"""

from app.core.changelog.config.models import (
    BreakingConfig,
    ChangelogConfig,
    CoreConfig,
    RenderingConfig,
    TypeMappingConfig,
)
from app.core.changelog.processing.pipeline import ChangelogProcessingPipeline


def _config() -> ChangelogConfig:
    """
    Build changelog configuration used by processing tests.

    Returns:
        Test changelog configuration.
    """

    return ChangelogConfig(
        core=CoreConfig(
            ignore_merge_commits=True,
            ignore_types=["chore"],
        ),
        rendering=RenderingConfig(
            deduplicate=True,
            generic_scopes=["", "main", "core", "general", "release"],
        ),
        breaking=BreakingConfig(
            enabled=True,
            keywords=["BREAKING CHANGE"],
        ),
        type_mapping=TypeMappingConfig(
            mapping={
                "feat": "✨ Features",
                "fix": "🐛 Bug Fixes",
                "improvement": "🧠 Improvements",
                "template": "📄 Templates",
                "docs": "📚 Documentation",
            }
        ),
    )


def test_expands_body_sections_into_semantic_groups() -> None:
    """
    One rich commit body produces separate semantic groups.
    """

    message = """feat(main): prepare release

Release narrative.

### ✨ Features
- Added workflow validation.

### 🐛 Bug Fixes
#### Workflow
- Prevented unsafe execution.

### 📄 Templates
- Expanded the commit template.
"""

    groups = ChangelogProcessingPipeline(_config()).process_messages([message])

    assert [group.commit_type for group in groups] == [
        "feat",
        "fix",
        "template",
    ]
    assert groups[0].scopes[0].commits[0].sections[0].items == [
        "Added workflow validation."
    ]
    assert groups[1].scopes[0].commits[0].sections[0].subsections[
        0
    ].title == "Workflow"


def test_filters_merge_and_ignored_commit_types() -> None:
    """
    Merge commits and configured ignored types do not render.
    """

    groups = ChangelogProcessingPipeline(_config()).process_messages(
        [
            "Merge branch 'release' into main",
            "chore(core): internal cleanup",
            "fix(core): preserve user-facing fix",
        ]
    )

    assert [group.commit_type for group in groups] == ["fix"]
    assert groups[0].scopes[0].commits[0].subject == "preserve user-facing fix"


def test_uses_top_level_body_bullets_without_required_headings() -> None:
    """
    A simple commit body bullet becomes the rendered change item.
    """

    groups = ChangelogProcessingPipeline(_config()).process_messages(
        ["fix(core): correct typo\n\n- Corrected typo in README."]
    )

    commit = groups[0].scopes[0].commits[0]

    assert commit.sections[0].title == ""
    assert commit.sections[0].items == ["Corrected typo in README."]


def test_keeps_same_subject_when_bodies_are_different() -> None:
    """
    Content-aware deduplication preserves distinct changes.
    """

    groups = ChangelogProcessingPipeline(_config()).process_messages(
        [
            "fix(core): validation\n\n- Fixed branch validation.",
            "fix(core): validation\n\n- Fixed tag validation.",
        ]
    )

    assert len(groups[0].scopes[0].commits) == 2


def test_filters_shell_transcripts_and_empty_version_announcements() -> None:
    """
    Terminal transcripts and version-only placeholders do not render.
    """

    groups = ChangelogProcessingPipeline(_config()).process_messages(
        [
            "(venv) D:\\project>git log --oneline --graph\n\n* abc123 fixed",
            "refactor(workflow): 1.10.6rc2",
            "fixed",
            "docs(changelog): update changelog",
            "fix(workflow): keep this change",
        ]
    )

    assert [group.commit_type for group in groups] == ["fix"]
    assert groups[0].scopes[0].commits[0].subject == "keep this change"


def test_normalizes_singular_and_plural_ux_improvement_sections() -> None:
    """
    UX Improvement headings share the Improvements group.
    """

    message = """feat(main): improve interaction

### UX Improvement
- Add confirmation.

### UX Improvements
- Improve prompts.
"""

    groups = ChangelogProcessingPipeline(_config()).process_messages([message])

    assert [group.commit_type for group in groups] == ["improvement"]
    assert len(groups[0].scopes[0].commits) == 2


def test_normalizes_descriptive_semantic_section_titles() -> None:
    """
    Descriptive historical headings map to standard change groups.
    """

    message = """feat(main): reorganize project

### Template Enhancements
- Add template examples.

### Makefile Improvements
- Improve Makefile commands.

### Logic Refinement
- Refine version validation.

### Maintenance Structure
- Reorganize the application structure.
"""

    groups = ChangelogProcessingPipeline(_config()).process_messages([message])

    assert [group.commit_type for group in groups] == [
        "template",
        "improvement",
        "refactor",
    ]

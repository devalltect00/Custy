# tests/core/changelog/test_rendering.py

"""
Unit and golden-output tests for changelog rendering.
"""

from pathlib import Path

from app.core.changelog.config.models import (
    ChangelogConfig,
    LinksConfig,
    RenderingConfig,
    ScopeMappingConfig,
    TypeMappingConfig,
)
from app.core.changelog.models.changelog import Changelog
from app.core.changelog.models.metadata import ReleaseMetadata
from app.core.changelog.models.release import Release
from app.core.changelog.processing.pipeline import ChangelogProcessingPipeline
from app.core.changelog.rendering.jinja_renderer import JinjaRenderer
from app.core.changelog.rendering.template_loader import load_changelog_template


def _config() -> ChangelogConfig:
    """
    Build configuration matching the approved ideal fixture.

    Returns:
        Rendering test configuration.
    """

    return ChangelogConfig(
        links=LinksConfig(
            repository="https://github.com/devalltect00/Custy",
            enable_compare=True,
        ),
        rendering=RenderingConfig(
            show_title=False,
            show_description=False,
            bullet="-",
            indent=0,
            generic_scopes=[
                "",
                "main",
                "core",
                "general",
                "changelog",
                "release",
            ],
        ),
        scope_mapping=ScopeMappingConfig(
            mapping={"main": "core"},
        ),
        type_mapping=TypeMappingConfig(
            mapping={
                "fix": "🐛 Bug Fixes",
                "improvement": "🧠 Improvements",
                "template": "📄 Templates",
                "docs": "📚 Documentation",
            }
        ),
    )


def test_renders_the_approved_ideal_structure() -> None:
    """
    The real domain model renders exactly as the golden fixture.
    """

    config = _config()
    message = """fix(main): consolidated release changes

### 🐛 Bug Fixes
- Prevent unsafe execution when staged files exist.
- Prevented unsafe execution when staged files exist.
- Added confirmation before continuing.
- Improved merge validation.

### 🧠 Improvements
- Safer tagging.
- Better merge logic.
- Better user prompts.

### 📄 Templates
- Expanded commit template.
- Expanded the commit template.
- Expanded tag template.

### 📚 Documentation
- Updated project structure.
"""
    groups = ChangelogProcessingPipeline(config).process_messages([message])
    release = Release(
        version="1.10.6",
        release_date="2025-08-06",
        compare_url=("https://github.com/devalltect00/Custy/compare/1.10.5...1.10.6"),
        status="Stable Release",
        summary=(
            "Final release of Custy 1.10.6.\n\n"
            "This release focuses on workflow safety, merge validation, "
            "template improvements, and documentation."
        ),
        promoted_from=[
            "1.10.6rc4",
            "1.10.6rc3",
            "1.10.6rc2",
            "1.10.6rc1",
            "1.10.6b1",
        ],
        groups=groups,
        metadata=ReleaseMetadata(
            tags={"Tags": ["`#release`", "#workflow"]},
            classifications=["bugfix", "docs", "template", "stable"],
        ),
    )
    renderer = JinjaRenderer(
        template=load_changelog_template(),
        config=config,
    )

    rendered = renderer.render(Changelog(releases=[release]))
    expected = Path("tests/fixtures/changelog/ideal_output.md").read_text(
        encoding="utf-8"
    )

    assert rendered == expected
    assert "    -" not in rendered
    assert "#workflow" not in rendered

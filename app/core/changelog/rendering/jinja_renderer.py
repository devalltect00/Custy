# app/core/changelog/rendering/jinja_renderer.py

"""
Jinja Changelog Renderer

Renders a changelog using a Jinja2 template.
"""

from __future__ import annotations

import re

from jinja2 import (
    StrictUndefined,
    Template,
)

from app.core.changelog.config.models import (
    ChangelogConfig,
)
from app.core.changelog.models.changelog import (
    Changelog,
)
from app.core.changelog.rendering.context import (
    ChangelogRenderContext,
)
from app.core.changelog.rendering.renderer import (
    ChangelogRenderer,
)


class JinjaRenderer(
    ChangelogRenderer,
):
    """
    Render changelogs using Jinja2.
    """

    def __init__(
        self,
        *,
        template: str,
        config: ChangelogConfig,
    ) -> None:
        """
        Initialize the renderer.

        Args:
            template:
                Jinja template source.

            config:
                Changelog rendering configuration.
        """

        self._template = Template(
            template,
            undefined=StrictUndefined,
        )

        self._config = config

    def render(
        self,
        changelog: Changelog,
    ) -> str:
        """
        Render a changelog.

        Args:
            changelog:
                Changelog to render.

        Returns:
            Rendered markdown.
        """

        context = ChangelogRenderContext(
            changelog=changelog,
            config=self._config,
        )

        rendered = self._template.render(
            context=context,
        ).strip()

        rendered = "\n".join(line.rstrip() for line in rendered.splitlines())

        rendered = re.sub(
            r"\n{3,}",
            "\n\n",
            rendered,
        )

        item_prefix = (
            " " * self._config.rendering.indent + self._config.rendering.bullet + " "
        )
        escaped_prefix = re.escape(item_prefix)

        rendered = re.sub(
            rf"(?m)^({escaped_prefix}[^\n]+)\n\n(?={escaped_prefix})",
            r"\1\n",
            rendered,
        )

        return f"{rendered}\n" if rendered else ""

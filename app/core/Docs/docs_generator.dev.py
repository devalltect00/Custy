# app/core/Docs/docs_generator.dev.py

import ast
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)


class DocsGenerator:
    """
    Generate developer documentation from source code.
    """

    def __init__(self, source_dir: str = "app/utils", output_dir: str = "docs") -> None:
        """
        Args:
            source_dir (str): Directory to scan for Python files
            output_dir (str): Directory to write docs
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def generate_all(self) -> None:
        """
        Generate all documentation files.
        """
        logger.info("Generating developer docs...")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        api_docs = self._generate_api_docs()
        pipeline_docs = self._generate_pipeline_docs()

        (self.output_dir / "API.md").write_text(api_docs, encoding="utf-8")
        (self.output_dir / "PIPELINE.md").write_text(pipeline_docs, encoding="utf-8")

        logger.info("Docs generated successfully.")

    # ==========================================================
    # API DOCS
    # ==========================================================

    def _generate_api_docs(self) -> str:
        """
        Generate API documentation from Python classes.

        Returns:
            str: Markdown content
        """
        content = ["# 📦 API Documentation\n"]

        for file in self._get_python_files():
            classes = self._extract_classes(file)

            for cls in classes:
                content.append(self._format_class(cls))

        return "\n".join(content)

    # ==========================================================
    # PIPELINE DOCS
    # ==========================================================

    def _generate_pipeline_docs(self) -> str:
        """
        Generate pipeline documentation.

        Returns:
            str: Markdown content
        """
        content = ["# 🔄 Pipeline Documentation\n"]

        pipeline_file = self.source_dir / "pipeline.py"

        if not pipeline_file.exists():
            return "\n".join(content)

        classes = self._extract_classes(pipeline_file)

        content.append("## Stages\n")

        for cls in classes:
            if cls["name"].endswith("Stage"):
                content.append(f"### {cls['name']}")
                if cls["doc"]:
                    content.append(cls["doc"])
                content.append("")

        return "\n".join(content)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def _get_python_files(self) -> List[Path]:
        return list(self.source_dir.glob("*.py"))

    def _extract_classes(self, filepath: Path) -> List[Dict]:
        """
        Extract class definitions from a file.

        Args:
            filepath (Path): Python file

        Returns:
            list[dict]: Class info
        """
        try:
            tree = ast.parse(filepath.read_text(encoding="utf-8"))
        except Exception:
            logger.exception(f"Failed parsing {filepath}")
            return []

        classes = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                cls = {
                    "name": node.name,
                    "doc": ast.get_docstring(node),
                    "methods": self._extract_methods(node),
                }
                classes.append(cls)

        return classes

    def _extract_methods(self, class_node: ast.ClassDef) -> List[Dict]:
        methods = []

        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                methods.append({
                    "name": node.name,
                    "doc": ast.get_docstring(node),
                })

        return methods

    def _format_class(self, cls: Dict) -> str:
        """
        Convert class info into markdown.

        Args:
            cls (dict): Class metadata

        Returns:
            str: Markdown block
        """
        lines = [f"## {cls['name']}\n"]

        if cls["doc"]:
            lines.append(cls["doc"] + "\n")

        if cls["methods"]:
            lines.append("### Methods\n")

            for m in cls["methods"]:
                lines.append(f"#### {m['name']}")
                if m["doc"]:
                    lines.append(m["doc"])
                lines.append("")

        return "\n".join(lines)

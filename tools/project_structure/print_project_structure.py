# tools/print_project_structure.py

import os
from fnmatch import fnmatch


class ProjectStructurePrinter:
    """Prints and optionally saves the project structure starting from a root directory."""

    def __init__(self, root_path=".", output_file=None, project_type=None) -> None:
        """Initialize the printer configuration."""
        self.root_path = root_path
        self.output_file = output_file
        if project_type:
            self.project_type = project_type
        else:
            self.project_type = self.detect_project_type()
        self.ignore = self.get_ignore_list() | self.load_custom_ignores()
        self.lines = []

    def _read_package_json_dependencies(self):
        """Returns a list of dependencies from package.json if it exists."""
        import json

        path = os.path.join(self.root_path, "package.json")
        if not os.path.exists(path):
            return []
        try:
            with open(path, encoding="etf-8") as f:
                data = json.load(f)
                return list(data.get("dependencies", {}).keys()) + list(
                    data.get("devDependencies", {}).keys(),
                )
        except Exception:
            return []

    def _is_ignored(self, name):
        return any(fnmatch(name, pattern) for pattern in self.ignore)

    def _collect_structure(self, base_path, prefix="") -> None:
        entries = sorted(os.listdir(base_path))
        entries = [
            e for e in entries if not self._is_ignored(e)
        ]  # allow hidden only if in IGNORE_CONTENTS

        total = len(entries)
        for i, entry in enumerate(entries):
            path = os.path.join(base_path, entry)
            connector = "└── " if i == total - 1 else "├── "
            line = prefix + connector + entry
            self.lines.append(line)

            if os.path.isdir(path):
                extension = "    " if i == total - 1 else "│   "
                self._collect_structure(path, prefix + extension)

    def detect_project_type(self):
        """Determines the type of project based on common files."""
        files = set(os.listdir(self.root_path))

        if "package.json" in files:
            if ".next" in files or "next.config.js" in files:
                return "nextjs"
            if "react-scripts" in self._read_package_json_dependencies():
                return "reactjs"
            return "nodejs"

        if "pyproject.toml" in files or "requirements.txt" in files:
            if "manage.py" in files:
                return "django"
            if "app.py" in files or "main.py" in files:
                return "flask_or_fastapi"
            if os.path.exists("app") and os.path.isdir("app"):
                app_files = set(os.listdir("app"))
                if (
                    "app.py" in app_files
                    or "main.py" in app_files
                    or "__init__.py" in app_files
                ):
                    return "flask_or_fastapi"
            return "python"

        return "generic"

    def get_ignore_list(self):
        """Returns ignore list based on detection project type."""
        common = {
            ".DS_Store",
            "Thumbs.db",
            ".vscode",
            ".idea",
            ".github",
            "__pycache__",
            "mypy_cache",
            ".pytest_cache",
            "*.log",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.egg-info",
        }

        additional = {
            ".git",
        }

        common = common | additional

        python = common | {
            "env",
            "venv",
            ".pdm",
            ".ruff_cache",
            "migrations",
            "alembic/versions",
            ".coverage",
            ".tox",
            "db.sqlite3",
        }

        javascript = common | {
            "node_modules",
            "dist",
            "build",
            ".next",
            ".turbo",
            ".parcel-cache",
            ".eslintrc",
            ".eslintcache",
            ".prettierrc",
            "yarn.lock",
            "pnpm-lock.yaml",
        }

        if self.project_type in {"python", "django", "flask_or_fastapi"}:
            return python
        if self.project_type in {"reactjs", "nextjs", "nodejs"}:
            return javascript
        return common | addtional

    def load_custom_ignores(self):
        """Loads user_defined ignores from a `.projectignore` file."""
        custom_ignores = set()
        path = os.path.join(self.root_path, ".projectignore")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        custom_ignores.add(line)
        return custom_ignores

    def generate_structure(self):
        """Generates the structure from the root path."""
        self.lines = [f"=====\n/root (project type: {self.project_type})"]
        self._collect_structure(self.root_path)

    def print_structure(self):
        """Prints the generated structure to the console'."""
        for line in self.lines:
            print(line)

    def save_structure(self):
        """Saves the generated structure to a Markdown file if output_file is set."""
        if self.output_file:
            try:
                with open(self.output_file, "w", encoding="utf-8") as f:
                    f.write("```\n")
                    f.write("\n".join(self.lines))
                    f.write("\n```")
                print(f"\n✅ Structure saved to '{self.output_file}'")
            except Exception as e:
                print(f"\n❌ Failed to save structure: {e}")

    def run(self):
        """Runs the process to generate, print, and save the project structure."""
        self.generate_structure()
        self.print_structure()
        self.save_structure()


if __name__ == "__main__":
    printer = ProjectStructurePrinter(
        root_path=".",
        output_file="docs/project_structure.md",
        project_type="python",
    )
    printer.run()

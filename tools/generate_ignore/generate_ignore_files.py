# tools/generate_ignore/generate_ignore_files.py

import os

GITIGNORE_TEMPLATES = {
    "python": """
# ===========================
# ⚙️ Byte-compiled / optimized / DLL files
# ===========================
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
env/
venv/

# Distribution / packaging
build/
dist/
*.egg-info/

# Logs and local files
*.log
*.sqlite3

# VSCode
.vscode/

# IDEs
.idea/

# Others
.env
""",
    "django": """
# ===========================
# ⚙️ Django
# ===========================
*.py[cod]
__pycache__/
db.sqlite3
.env
/static/
/media/
/migrations/
/venv/
/env/
*.log
*.pot
*.pyc
*.pyo
*.pyd
.idea/
.vscode/
*.sqlite3
""",
    "flask_or_fastapi": """
# ===========================
# ⚙️ Flask or FastAPI
# ===========================
instance/
*.db
*.sqlite3
.env
*.log
""",
    "nodejs": """
node_modules/
dist/
build/
.env
*.log
.npm
.pnpm
.cache/
.vscode/
.idea/
""",
    "reactjs": """
node_modules/
build/
.env
*.log
.vscode/
.idea/
""",
    "nextjs": """
node_modules/
.next/
out/
.env
*.log
.vscode/
.idea/
""",
}


DOCKERIGNORE_TEMPLATES = {
    "python": """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
env/
venv/

# Distribution / packaging
build/
dist/
*.egg-info/

# Others
*.pyc
*.pyo
*.pyd
*.db
.env
.env.*
.vscode/
.idea/
*.log
*.egg-info/
*.sqlite3
""",
    "django": """
# Django-specific
db.sqlite3
media/
staticfiles/
migrations/
.env
*.log
""",
    "flask_or_fastapi": """
# Flask or FastAPI
instance/
*.db
*.sqlite3
.env
*.log
""",
    "nodejs": """
node_modules/
npm-debug.log
.env
.env.*
.vscode/
.idea/
.next/
dist/
build/
*.log
""",
    "reactjs": """
node_modules/
build/
.env
.env.*
.vscode/
.idea/
*.log
""",
    "nextjs": """
node_modules/
.next/
out/
.env
.env.*
.vscode/
.idea/
*.log
""",
}

root_path = "."


def read_package_json_dependencies():
    """Returns a list of dependencies from package.json if it exists."""
    import json

    path = os.path.join(root_path, "package.json")
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


def detect_project_type():
    """Determines the type of project based on common files."""
    files = set(os.listdir(root_path))

    if "package.json" in files:
        if ".next" in files or "next.config.js" in files:
            return "nextjs"
        if "react-scripts" in read_package_json_dependencies():
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


def read_optional_file(file_path):
    """Reads optional file if present (e.g., .gitignore.append, .gitignore.template)."""
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            return f.read().strip()
    return ""


def write_file(filename, content):
    """Writes the ignore file and optionally appends content."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"✅ Created {filename}")
    except Exception as e:
        print(f"❌ Failed to write {filename}: {e}")


def load_custom_ignores():
    """
    Loads user-defined ignores from a `.projectignore` file
    """
    custom_ignores = set()
    path = os.path.join(root_path, ".projectignore")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    custom_ignores.add(line)
    return custom_ignores


def generate_ignore_files(project_type=None):
    if not project_type:
        project_type = detect_project_type()
    print(f"📁 Detected project type: {project_type}")

    # --- .gitignore Generation ---

    # Step 1: Load your main .gitignore.template
    base_gitignore = read_optional_file(
        "templates/example/gitignore/.gitignore.template",
    )
    if not base_gitignore:
        print(
            "❌ Missing templates/example/gitignore/.gitignore.template. Please create one.",
        )
        return

    # Step 2: Append project specific rules
    project_gitignore = GITIGNORE_TEMPLATES.get(project_type, "")
    if project_gitignore:
        base_gitignore += f"\n\n# Project specific ignores ({project_type})\n{project_gitignore.strip()}"

    # Step 3 Optional .gitignore.append
    custom_gitignore = read_optional_file(
        "templates/example/gitignore/.gitignore.append",
    )
    if custom_gitignore:
        base_gitignore += f"\n\n# Custom ignore entries\n{custom_gitignore.strip()}"

    # Step 4 Optional .projectignore
    projectignore = load_custom_ignores()
    if projectignore:
        custom_lines = "\n".join(sorted(projectignore))
        base_gitignore += f"\n\n# Custom .projectignore\n{custom_lines}"

    # Final write
    write_file(".gitignore", base_gitignore)

    # --- .dockerignore Generation ---]

    # Step 1: Load your main .gitignore.template
    base_dockerignore = read_optional_file("templates/.dockerignore.template")
    if not base_dockerignore:
        print("❌ Missing templates/.dockerignore.template. Please create one.")
        return

    # Step 2: Append project specific rules
    project_dockerignore = DOCKERIGNORE_TEMPLATES.get(project_type, "")
    if project_dockerignore:
        base_dockerignore += f"\n\n# Project specific ignores ({project_type})\n{project_dockerignore.strip()}"

    # Step 3 Optional .dockerignore.append
    custom_dockerignore = read_optional_file(".dockerignore.append")
    if custom_dockerignore:
        base_dockerignore += (
            f"\n\n# Custom ignore entries\n{custom_dockerignore.strip()}"
        )

    # Step 4 Optional .projectignore
    projectignore = load_custom_ignores()
    if projectignore:
        custom_lines = "\n".join(sorted(projectignore))
        base_dockerignore += f"\n\n# Custom .projectignore\n{custom_lines}"

    # Final write
    write_file(".dockerignore")


if __name__ == "__main__":
    generate_ignore_files(project_type="python")

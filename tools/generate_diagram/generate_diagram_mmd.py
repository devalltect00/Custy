import re
from pathlib import Path

INPUT = Path("docs\\changelog\\diagrams\\DIAGRAMS.md")
OUTPUT_DIR = Path("docs\\changelog\\diagrams")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read the markdown file content
content = INPUT.read_text(encoding="utf-8")


def slugify(text: str) -> str:
    """
    Convert a section title into a safe filename.

    Steps:
    - Remove emojis and special characters
    - Remove numbering prefixes (e.g., '1. ')
    - Convert to lowercase
    - Replace spaces with underscores
    """
    text = re.sub(r"[^\w\s-]", "", text)  # Remove emoji/symbols
    text = re.sub(r"^\d+\.\s*", "", text)  # Remove numbering (e.g., '1. ')
    text = text.lower().strip().replace(" ", "_")  # Normalize format
    return text


# Split content into sections based on level-1 headings (# ...)
sections = re.split(r"(?=^#\s+)", content, flags=re.MULTILINE)

for section in sections:
    # Extract the section title
    title_match = re.match(r"#\s+(.*)", section)
    if not title_match:
        continue

    raw_title = title_match.group(1)
    filename_slug = slugify(raw_title)

    # Extract all Mermaid code blocks within this section
    blocks = re.findall(r"```mermaid(.*?)```", section, re.DOTALL)

    # Skip sections without Mermaid diagrams
    if not blocks:
        continue

    for i, block in enumerate(blocks, 1):
        # Add suffix if multiple diagrams exist in the same section
        suffix = f"_{i}" if len(blocks) > 1 else ""

        filename = OUTPUT_DIR / f"{filename_slug}{suffix}.mmd"

        print(f"Processing: {raw_title} -> {filename.name}")

        # Write the Mermaid diagram to a .mmd file
        filename.write_text(block.strip(), encoding="utf-8")

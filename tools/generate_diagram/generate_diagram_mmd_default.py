import re
from pathlib import Path

INPUT = Path("docs\\changelog\\diagrams\\DIAGRAMS.md")
OUTPUT_DIR = Path("docs\\changelog\\diagrams")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

content = INPUT.read_text(encoding="utf-8")

blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)

for i, block in enumerate(blocks, 1):
    filename = OUTPUT_DIR / f"diagram_{i}.mmd"
    filename.write_text(block.strip(), encoding="utf-8")
    print(f"Created: {filename}")

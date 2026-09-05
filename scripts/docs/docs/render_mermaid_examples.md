<!-- scripts/docs/docs/render_mermaid_examples.md -->

python scripts/docs/render_mermaid.py --input-dir docs --input-glob \*.mmd --recursive --output-dir docs/diagrams/generated-recursive --clean --no-progress --input-dir docs --output-dir docs\diagrams\generated-recursive --format png

python scripts/docs/render_mermaid.py --format svg --output-dir docs/diagrams/generated-svg --clean --no-progress --input-dir docs\diagrams --output-dir docs\diagrams\generated-svg --format svg

python scripts/docs/render_mermaid.py --format svg --output-dir docs/diagrams/generated-svg --clean --input-dir docs\diagrams --output-dir docs\diagrams\generated-pdf --format pdf

python scripts/docs/render_mermaid.py

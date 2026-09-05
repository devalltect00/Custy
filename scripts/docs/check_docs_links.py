# scripts/docs/check_docs_links.py

"""
scripts/docs/check_docs_links.py

Purpose:
- Validate internal Markdown links across all files under `docs/`.
- Detect broken relative links before publishing docs or merging changes.

What this script checks:
1) Scans every `*.md` file inside the `docs/` directory recursively.
2) Extracts Markdown links in the form: [label](target).
3) Ignores non-local links:
   - http://...
   - https://...
   - mailto:...
   - #anchor-only links
4) Removes anchor fragments from local links (e.g., file.md#section -> file.md).
5) Resolves each local link to a file path relative to the current Markdown file.
6) Reports all unresolved paths as broken links.

Output:
- `NO_BROKEN_MD_LINKS`
  when no broken local links are found.
- `BROKEN_LINKS_FOUND`
  followed by lines like:
  docs/some/page.md -> ../missing-file.md

Usage:
    python scripts/docs/check_docs_links.py

Notes:
- This script focuses on local Markdown path existence checks.
- It does not validate external URLs or heading-anchor correctness inside files.
"""

import pathlib
import re

root = pathlib.Path("docs")
md_files = sorted(root.rglob("*.md"))
pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

broken = []

for md in md_files:
    text = md.read_text(encoding="utf-8", errors="ignore")
    for match in pattern.finditer(text):
        target = match.group(1).strip()

        # Skip external and anchor-only links.
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue

        # Remove markdown anchor fragment, if any.
        target_no_anchor = target.split("#", 1)[0].strip()
        if not target_no_anchor:
            continue

        # Resolve absolute-style docs link or relative link.
        if target_no_anchor.startswith("/"):
            candidate = pathlib.Path(".") / target_no_anchor.lstrip("/")
        else:
            candidate = md.parent / target_no_anchor

        if not candidate.exists():
            broken.append((str(md).replace("\\", "/"), target))

if broken:
    print("BROKEN_LINKS_FOUND")
    for src, target in broken:
        print(f"{src} -> {target}")
else:
    print("NO_BROKEN_MD_LINKS")

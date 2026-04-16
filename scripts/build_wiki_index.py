#!/usr/bin/env python3
"""
build_wiki_index.py — generate top-level index.html for the wiki.

Usage: build_wiki_index.py OUT_DIR SUBWIKI1 SUBWIKI2 ...

Reads each sub-wiki's index.md (or SCHEMA.md for the domain line) and emits
an HTML index linking to each sub-wiki's index.html plus a brief summary.
"""
import re
import sys
from pathlib import Path
from datetime import date


def read_first_line_after(path: Path, marker: str) -> str:
    if not path.is_file():
        return ""
    text = path.read_text()
    m = re.search(rf"{marker}\s*\n(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def display_title(sw_dir: Path, fallback: str) -> str:
    schema = sw_dir / "SCHEMA.md"
    if schema.is_file():
        text = schema.read_text()
        m = re.search(r"## Title\s*\n(.+)$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return fallback


def domain_summary(sw_dir: Path) -> str:
    schema = sw_dir / "SCHEMA.md"
    if not schema.is_file():
        return ""
    text = schema.read_text()
    m = re.search(r"## Domain\s*\n(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        # First non-blank line of the Domain section
        for line in m.group(1).strip().splitlines():
            if line.strip():
                return line.strip()
    return ""


def page_count(sw_dir: Path) -> int:
    return sum(1 for _ in sw_dir.rglob("*.md"))


def main():
    if len(sys.argv) < 3:
        print("Usage: build_wiki_index.py OUT_DIR SUBWIKI1 [SUBWIKI2 ...]", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(sys.argv[1]).resolve()
    subwikis = sys.argv[2:]

    today = date.today().isoformat()

    print(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>JOS LLM Wiki</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       max-width: 50em; margin: 2em auto; padding: 0 1em; line-height: 1.5; }}
h1 {{ border-bottom: 2px solid #ccc; padding-bottom: 0.3em; }}
.subwiki {{ margin: 1.5em 0; padding: 1em; background: #f8f8f8;
          border-left: 4px solid #4a90e2; border-radius: 4px; }}
.subwiki h2 {{ margin-top: 0; }}
.subwiki h2 a {{ text-decoration: none; color: #4a90e2; }}
.subwiki h2 a:hover {{ text-decoration: underline; }}
.meta {{ color: #666; font-size: 0.9em; }}
.footer {{ margin-top: 3em; color: #888; font-size: 0.85em; border-top: 1px solid #ddd;
         padding-top: 1em; }}
</style>
</head>
<body>
<h1>JOS LLM Wiki</h1>

<p>An interlinked, agent-friendly knowledge base on physics-based sound
synthesis, signal processing, and adjacent topics. Each sub-wiki is an
independent collection with its own SCHEMA, index, and log. Built from
markdown sources designed for both human and LLM consumption.</p>
""")

    for sw in subwikis:
        sw_dir = out_dir / sw
        if not sw_dir.is_dir():
            continue
        domain = domain_summary(sw_dir)
        n_pages = page_count(sw_dir)
        index_html = f"{sw}/index.html"
        title = display_title(sw_dir, sw.replace("_", " ").title())
        print(f"""<div class="subwiki">
<h2><a href="{index_html}">{title}</a></h2>
<p>{domain}</p>
<p class="meta">{n_pages} pages · <a href="{index_html}">browse index</a></p>
</div>""")

    print(f"""
<div class="footer">
<p>Source: <a href="https://github.com/josmithiii/wiki">github.com/josmithiii/wiki</a>
&middot; Last built: {today}</p>
</div>
</body>
</html>""")


if __name__ == "__main__":
    main()

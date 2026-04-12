#!/usr/bin/env python3
"""
build_wiki.py — render the LLM wiki to a static HTML site.

Usage: build_wiki.py OUT_DIR SUBWIKI1 SUBWIKI2 ...

For each .md file in OUT_DIR/<subwiki>/:
  1. Resolve [[wikilinks]] across all sub-wikis to relative .html paths.
     Cross-wiki targets like [[modal_synthesis/comparisons/foo]] also work.
  2. Convert via pandoc (gfm → html5 standalone) into a sibling .html file.
  3. Leave the original .md alongside (so Obsidian users can still browse).

Wikilink resolution rules:
  - [[bare-name]]                 → search all sub-wikis for bare-name.md
  - [[subdir/bare-name]]          → match wikilinks ending in subdir/bare-name.md
  - [[subwiki/path/bare-name]]    → exact path under OUT_DIR
  - [[bare-name|Display Text]]    → use Display Text as link label
"""
import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path

PANDOC_OPTS = [
    "--from=gfm+tex_math_dollars",
    "--to=html5",
    "--standalone",
    "--toc",
    "--toc-depth=2",
    "--metadata=lang:en",
    "--wrap=preserve",
    "--mathjax",
]

WIKI_CSS = """\
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
       Helvetica, Arial, sans-serif; color: #222; line-height: 1.5; }
.wiki-layout { display: flex; min-height: 100vh; align-items: stretch; }
.wiki-nav {
  width: 260px; flex-shrink: 0;
  padding: 1.5em 1em 2em 1.2em;
  background: #f5f5f2;
  border-right: 1px solid #ddd;
  font-size: 0.9em;
  position: sticky; top: 0; align-self: flex-start;
  max-height: 100vh; overflow-y: auto;
}
.wiki-nav .wiki-nav-top { display: block; margin-bottom: 1em;
                          font-weight: 600; color: #4a90e2; text-decoration: none; }
.wiki-nav .wiki-nav-top:hover { text-decoration: underline; }
.wiki-nav h3 { margin: 1em 0 0.4em 0; font-size: 0.8em;
               text-transform: uppercase; letter-spacing: 0.05em; color: #666; }
.wiki-nav ul { list-style: none; padding-left: 0; margin: 0.2em 0; }
.wiki-nav li { margin: 0.15em 0; }
.wiki-nav li.current > a { font-weight: 700; color: #000; }
.wiki-nav a { color: #346; text-decoration: none; }
.wiki-nav a:hover { text-decoration: underline; }
.wiki-nav .depth-1 { padding-left: 1em; }
.wiki-nav .depth-2 { padding-left: 2em; }
.wiki-nav .depth-3 { padding-left: 3em; }
.wiki-content {
  flex: 1; min-width: 0;
  padding: 2em clamp(1em, 4vw, 3em);
  max-width: 60em;
}
.wiki-content #TOC { background: #fafaf7; border-left: 3px solid #ccc;
                     padding: 0.5em 1em; margin: 1em 0; font-size: 0.9em; }
.wiki-content pre { background: #f5f5f2; padding: 0.8em 1em; overflow-x: auto;
                    border-radius: 4px; }
.wiki-content code { background: #f0f0ec; padding: 0.1em 0.3em; border-radius: 3px; }
.wiki-content pre code { background: none; padding: 0; }
.wiki-content h1 { border-bottom: 2px solid #ccc; padding-bottom: 0.3em; }
@media (max-width: 700px) {
  .wiki-layout { flex-direction: column; }
  .wiki-nav { width: auto; max-height: none; border-right: none;
              border-bottom: 1px solid #ddd; position: static; }
}
"""

PAGE_LABEL_OVERRIDES = {
    "index": "Home",
    "README": "Home",
    "SCHEMA": "Schema",
    "TODO": "TODO",
    "log": "Log",
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def collect_md_files(out_dir: Path, subwikis: list[str]) -> dict[str, Path]:
    """Build a map: bare filename (without .md) -> absolute Path."""
    by_bare: dict[str, list[Path]] = {}
    by_relpath: dict[str, Path] = {}  # 'modal_synthesis/concepts/foo' -> Path
    for sw in subwikis:
        sw_dir = out_dir / sw
        if not sw_dir.is_dir():
            continue
        for md in sw_dir.rglob("*.md"):
            bare = md.stem
            by_bare.setdefault(bare, []).append(md)
            rel = md.relative_to(out_dir).with_suffix("")
            by_relpath[str(rel)] = md
    return by_bare, by_relpath


def resolve_wikilink(target: str, source_md: Path, out_dir: Path,
                     by_bare, by_relpath) -> str:
    """Return a relative HTML path from source_md to the target .md."""
    target = target.strip()
    # Strip optional .md extension
    if target.endswith(".md"):
        target = target[:-3]

    # Try exact relative-path match first (e.g. "modal_synthesis/comparisons/waveguide-vs-modal")
    if target in by_relpath:
        dst = by_relpath[target]
    else:
        # Match suffix path: "comparisons/waveguide-vs-modal"
        suffix_matches = [p for k, p in by_relpath.items() if k.endswith("/" + target)]
        if len(suffix_matches) == 1:
            dst = suffix_matches[0]
        else:
            # Bare-name lookup
            bare = target.split("/")[-1]
            candidates = by_bare.get(bare, [])
            if not candidates:
                return None  # broken link
            if len(candidates) > 1:
                # Prefer one in the same sub-wiki as source_md
                source_sw = source_md.relative_to(out_dir).parts[0]
                same = [c for c in candidates if c.relative_to(out_dir).parts[0] == source_sw]
                if same:
                    dst = same[0]
                else:
                    dst = candidates[0]
            else:
                dst = candidates[0]

    # Compute relative HTML path from source_md's directory to dst (with .html)
    dst_html = dst.with_suffix(".html")
    rel = os.path.relpath(dst_html, source_md.parent)
    return rel


def split_protecting_code(content: str) -> list[tuple[bool, str]]:
    """Split content into (is_code, text) chunks. Code chunks are left untouched.

    Code regions are: fenced code blocks (``` ... ```) and inline code (`...`).
    """
    out = []
    i = 0
    n = len(content)
    while i < n:
        # Fenced code block
        if content.startswith("```", i):
            end = content.find("```", i + 3)
            if end == -1:
                out.append((True, content[i:]))
                return out
            end += 3
            out.append((True, content[i:end]))
            i = end
            continue
        # Inline code
        if content[i] == "`":
            j = content.find("`", i + 1)
            if j == -1:
                out.append((False, content[i:]))
                return out
            out.append((True, content[i:j+1]))
            i = j + 1
            continue
        # Plain text — accumulate until next code marker
        j = i
        while j < n and content[j] != "`":
            j += 1
        out.append((False, content[i:j]))
        i = j
    return out


def convert_wikilinks(content: str, source_md: Path, out_dir: Path,
                      by_bare, by_relpath) -> tuple[str, list[str]]:
    """Replace [[wikilinks]] with markdown links. Return (new_content, broken_links).

    Wikilinks inside code spans/blocks are left untouched.
    """
    broken = []

    def replace(m):
        inner = m.group(1)
        if "|" in inner:
            target, display = inner.split("|", 1)
        else:
            target = inner
            display = inner.split("/")[-1]
        rel = resolve_wikilink(target, source_md, out_dir, by_bare, by_relpath)
        if rel is None:
            broken.append(target)
            return f"[{display}](#broken-link-{target})"
        return f"[{display}]({rel})"

    parts = split_protecting_code(content)
    rebuilt = []
    for is_code, text in parts:
        if is_code:
            rebuilt.append(text)
        else:
            rebuilt.append(WIKILINK_RE.sub(replace, text))
    return "".join(rebuilt), broken


def collect_subwiki_pages(out_dir: Path, subwikis: list[str]) -> dict[str, list[Path]]:
    """Map subwiki name -> sorted list of .md files in that subwiki."""
    tree: dict[str, list[Path]] = {}
    for sw in subwikis:
        sw_dir = out_dir / sw
        if not sw_dir.is_dir():
            continue
        tree[sw] = sorted(sw_dir.rglob("*.md"))
    return tree


def page_label(md: Path) -> str:
    return PAGE_LABEL_OVERRIDES.get(md.stem, md.stem.replace("_", " ").replace("-", " "))


def build_sidebar(page_md: Path, out_dir: Path, subwiki_pages: dict[str, list[Path]]) -> tuple[str, str]:
    """Return (before_body, after_body) raw-HTML wrappers for one page.

    The sidebar lists the current sub-wiki's pages with links relative to
    page_md's directory. If the page is at the top level (no sub-wiki),
    the sidebar shows all sub-wiki indexes.
    """
    page_dir = page_md.parent
    page_rel = page_md.relative_to(out_dir)
    parts = page_rel.parts
    current_sw = parts[0] if len(parts) > 1 else None

    def rel(target: Path) -> str:
        return os.path.relpath(target, page_dir)

    lines = ['<div class="wiki-layout">', '<aside class="wiki-nav">']
    top_index = out_dir / "index.html"
    lines.append(f'<a class="wiki-nav-top" href="{rel(top_index)}">&larr; All wikis</a>')

    if current_sw and current_sw in subwiki_pages:
        sw_dir = out_dir / current_sw
        lines.append(f'<h3>{current_sw.replace("_", " ")}</h3>')
        lines.append('<ul>')
        for md in subwiki_pages[current_sw]:
            html = md.with_suffix(".html")
            sub_rel = md.relative_to(sw_dir)
            depth = len(sub_rel.parts) - 1
            cls = f' class="depth-{depth}"' if depth else ''
            if md == page_md:
                cls = (cls[:-1] + ' current"') if cls else ' class="current"'
            label = page_label(md)
            lines.append(f'<li{cls}><a href="{rel(html)}">{label}</a></li>')
        lines.append('</ul>')
    else:
        lines.append('<h3>Sub-wikis</h3>')
        lines.append('<ul>')
        for sw, pages in subwiki_pages.items():
            sw_index = out_dir / sw / "index.html"
            if sw_index.is_file() or any(p.stem == "index" for p in pages):
                lines.append(f'<li><a href="{rel(sw_index)}">{sw.replace("_", " ")}</a></li>')
        lines.append('</ul>')

    lines.append('</aside>')
    lines.append('<main class="wiki-content">')
    before = "\n".join(lines) + "\n\n"
    after = "\n\n</main>\n</div>\n"
    return before, after


def render_one(md_path: Path, out_dir: Path, by_bare, by_relpath,
               subwiki_pages: dict[str, list[Path]]) -> int:
    content = md_path.read_text()
    new_content, broken = convert_wikilinks(content, md_path, out_dir, by_bare, by_relpath)
    if broken:
        rel = md_path.relative_to(out_dir)
        for b in broken:
            print(f"  *** broken wikilink in {rel}: [[{b}]]", file=sys.stderr)

    before, after = build_sidebar(md_path, out_dir, subwiki_pages)

    html_path = md_path.with_suffix(".html")
    title = extract_title(content) or md_path.stem
    css_rel = os.path.relpath(out_dir / "wiki.css", md_path.parent)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as bf, \
         tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as af:
        bf.write(before)
        af.write(after)
        before_path, after_path = bf.name, af.name
    try:
        proc = subprocess.run(
            ["pandoc", *PANDOC_OPTS,
             "--metadata", f"title={title}",
             f"--css={css_rel}",
             f"--include-before-body={before_path}",
             f"--include-after-body={after_path}",
             "-o", str(html_path)],
            input=new_content, text=True, capture_output=True,
        )
    finally:
        os.unlink(before_path)
        os.unlink(after_path)
    if proc.returncode != 0:
        print(f"*** pandoc failed for {md_path}", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        return 1
    return 0


def extract_title(content: str) -> str | None:
    """Pull title from YAML frontmatter or first H1."""
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip('"')
    m = re.search(r"^# (.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) < 3:
        print("Usage: build_wiki.py OUT_DIR SUBWIKI1 [SUBWIKI2 ...]", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(sys.argv[1]).resolve()
    subwikis = sys.argv[2:]

    if not out_dir.is_dir():
        print(f"*** {out_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    by_bare, by_relpath = collect_md_files(out_dir, subwikis)
    subwiki_pages = collect_subwiki_pages(out_dir, subwikis)
    print(f"  found {sum(len(v) for v in by_bare.values())} markdown files across {len(subwikis)} sub-wikis")

    # Write shared stylesheet
    (out_dir / "wiki.css").write_text(WIKI_CSS)

    errors = 0
    rendered = 0
    for sw in subwikis:
        sw_dir = out_dir / sw
        if not sw_dir.is_dir():
            continue
        for md in sorted(sw_dir.rglob("*.md")):
            errors += render_one(md, out_dir, by_bare, by_relpath, subwiki_pages)
            rendered += 1

    # Render top-level README.md if present
    top_readme = out_dir / "README.md"
    if top_readme.is_file():
        errors += render_one(top_readme, out_dir, by_bare, by_relpath, subwiki_pages)
        rendered += 1

    print(f"  rendered {rendered} HTML files ({errors} errors)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

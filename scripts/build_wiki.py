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
from pathlib import Path

PANDOC_OPTS = [
    "--from=gfm",
    "--to=html5",
    "--standalone",
    "--toc",
    "--toc-depth=2",
    "--metadata=lang:en",
    "--wrap=preserve",
]

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


def render_one(md_path: Path, out_dir: Path, by_bare, by_relpath) -> int:
    content = md_path.read_text()
    new_content, broken = convert_wikilinks(content, md_path, out_dir, by_bare, by_relpath)
    if broken:
        rel = md_path.relative_to(out_dir)
        for b in broken:
            print(f"  *** broken wikilink in {rel}: [[{b}]]", file=sys.stderr)

    html_path = md_path.with_suffix(".html")
    title = extract_title(content) or md_path.stem

    proc = subprocess.run(
        ["pandoc", *PANDOC_OPTS,
         "--metadata", f"title={title}",
         "-o", str(html_path)],
        input=new_content, text=True, capture_output=True,
    )
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
    print(f"  found {sum(len(v) for v in by_bare.values())} markdown files across {len(subwikis)} sub-wikis")

    errors = 0
    rendered = 0
    for sw in subwikis:
        sw_dir = out_dir / sw
        if not sw_dir.is_dir():
            continue
        for md in sorted(sw_dir.rglob("*.md")):
            errors += render_one(md, out_dir, by_bare, by_relpath)
            rendered += 1

    # Render top-level README.md if present
    top_readme = out_dir / "README.md"
    if top_readme.is_file():
        errors += render_one(top_readme, out_dir, by_bare, by_relpath)
        rendered += 1

    print(f"  rendered {rendered} HTML files ({errors} errors)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

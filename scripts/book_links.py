#!/usr/bin/env python3
"""
book_links.py - catalog and check deep links into the JOS online books.

The four books are served one HTML page per section (latex2html) at
    https://ccrma.stanford.edu/~jos/<book>/<Page_Name>.html
for <book> in mdft, filters, pasp, sasp. Page names follow section titles,
so they change when a section is retitled. This script keeps a committed
catalog of the valid page names and fails the build when a wiki page links
to a book page that is not in it.

Usage:
  book_links.py check WIKI_ROOT SUBWIKI1 [SUBWIKI2 ...]
      Verify every book URL in WIKI_ROOT/<subwiki>/**/*.md against the
      catalog. Exits 1 (after listing every bad link) if any is unknown.
  book_links.py update-catalog [BOOK_SRC_ROOT]
      Regenerate jos_books/catalog/<book>.tsv from the local latex2html
      output at BOOK_SRC_ROOT/<book>/<book>HTML/ (default root: /w).
  book_links.py usage WIKI_ROOT SUBWIKI1 [SUBWIKI2 ...]
      Print, for each book chapter, the wiki pages that link into it and
      how many links each has - the data behind the "-> wiki pages" lists
      on the hub pages in jos_books/entities/.

Catalog format: one line per page,
    <Page_Name>.html<TAB><page title><TAB><parent page name>
The parent (the page's "up" link) disambiguates sections that share a title,
e.g. pasp Wave_Digital_Filters.html (a section of the lumped-models chapter)
versus Wave_Digital_Filters_I.html (the appendix, whose parent is pasp.html).
"""
import html
import re
import sys
from pathlib import Path

BOOKS: tuple[str, ...] = ("mdft", "filters", "pasp", "sasp")
BASE_URL = "https://ccrma.stanford.edu/~jos"
CATALOG_DIR = Path(__file__).resolve().parent.parent / "jos_books" / "catalog"

# A book URL up to the end of the page name (an optional #fragment is not checked).
BOOK_URL_RE = re.compile(
    r"https?://ccrma\.stanford\.edu/~jos/(" + "|".join(BOOKS) + r")(/[^\s)\]>\"'`#|]*)?"
)
TITLE_RE = re.compile(r"<TITLE>(.*?)</TITLE>", re.DOTALL | re.IGNORECASE)
UP_RE = re.compile(r'<LINK\s+REL="up"\s+HREF="([^"]*)"', re.IGNORECASE)
SKIP_DIRS = {"raw", "_archive", ".obsidian", "incoming-pdfs"}


def _load_column(catalog_dir: Path, column: int) -> dict[str, dict[str, str]]:
    """Return {book: {page_name: <field `column` of its catalog line>}}."""
    catalog: dict[str, dict[str, str]] = {}
    for book in BOOKS:
        path = catalog_dir / f"{book}.tsv"
        if not path.is_file():
            print(f"*** missing book catalog {path} - run: make book-catalog", file=sys.stderr)
            sys.exit(1)
        pages: dict[str, str] = {}
        for line in path.read_text().splitlines():
            if line.strip():
                fields = line.split("\t")
                pages[fields[0]] = fields[column] if len(fields) > column else ""
        catalog[book] = pages
    return catalog


def load_catalog(catalog_dir: Path | None = None) -> dict[str, dict[str, str]]:
    """Return {book: {page_name: title}}. Exits 1 if a catalog file is missing."""
    return _load_column(catalog_dir or CATALOG_DIR, 1)


def load_parents(catalog_dir: Path | None = None) -> dict[str, dict[str, str]]:
    """Return {book: {page_name: parent page name}} ("" for the top pages)."""
    return _load_column(catalog_dir or CATALOG_DIR, 2)


def chapter_of(book: str, page: str, parents: dict[str, dict[str, str]]) -> str:
    """The chapter-level page (a child of <book>.html) that `page` sits under.

    A chapter page is its own chapter; a page with no recorded parent is
    returned unchanged.
    """
    tops = {f"{book}.html", "index.html", ""}
    seen: set[str] = set()
    while parents[book].get(page, "") not in tops and page not in seen:
        seen.add(page)
        page = parents[book][page]
    return page


def find_book_links(text: str) -> list[tuple[str, str]]:
    """Return [(book, page_name)] for every book URL in text.

    page_name is "" for a link to the book's top page (.../~jos/pasp/ or
    .../~jos/pasp). URLs written as placeholders (a page ending in "..." or
    starting with "<" or "{") are skipped.
    """
    out: list[tuple[str, str]] = []
    for m in BOOK_URL_RE.finditer(text):
        book, rest = m.group(1), (m.group(2) or "")
        if text[m.end():m.end() + 1].isalnum():
            continue  # a longer name, e.g. .../~jos/pasptalk/ is not the pasp book
        page = rest.lstrip("/")
        if page.endswith("..") or page.startswith(("<", "{")):
            continue  # template placeholder: ".../sasp/..." or ".../sasp/<Page_Name>.html"
        page = page.rstrip(".,;:")
        out.append((book, page))
    return out


def bad_links(text: str, catalog: dict[str, dict[str, str]]) -> list[str]:
    """Book URLs in text whose page is not in the catalog, as "book/page" strings."""
    return [f"{book}/{page}" for book, page in find_book_links(text)
            if page and page not in catalog[book]]


def wiki_markdown_files(root: Path, subwikis: list[str]) -> list[Path]:
    files: list[Path] = []
    for sw in subwikis:
        sw_dir = root / sw
        if not sw_dir.is_dir():
            print(f"*** sub-wiki directory {sw_dir} does not exist", file=sys.stderr)
            sys.exit(1)
        for md in sorted(sw_dir.rglob("*.md")):
            if not SKIP_DIRS.intersection(md.relative_to(root).parts):
                files.append(md)
    return files


def check(root: Path, subwikis: list[str]) -> int:
    catalog = load_catalog()
    n_links = 0
    n_bad = 0
    pages_with_links = 0
    for md in wiki_markdown_files(root, subwikis):
        text = md.read_text()
        links = find_book_links(text)
        if links:
            pages_with_links += 1
        n_links += len(links)
        for bad in bad_links(text, catalog):
            n_bad += 1
            print(f"  *** unknown book page in {md.relative_to(root)}: {BASE_URL}/{bad}",
                  file=sys.stderr)
    print(f"  book links: {n_links} in {pages_with_links} pages ({n_bad} unknown)")
    return 1 if n_bad else 0


# Pages that list or catalog links rather than build on a book chapter.
USAGE_SKIP_STEMS = {"index", "log", "SCHEMA", "TODO", "source-papers", "pending-sources"}


def chapter_usage(root: Path, subwikis: list[str], parents: dict[str, dict[str, str]]
                  ) -> dict[str, dict[str, dict[str, int]]]:
    """Return {book: {chapter page: {wiki page path (no .md): link count}}}."""
    usage: dict[str, dict[str, dict[str, int]]] = {book: {} for book in BOOKS}
    for md in wiki_markdown_files(root, subwikis):
        if md.stem in USAGE_SKIP_STEMS:
            continue
        rel = str(md.relative_to(root).with_suffix(""))
        for book, page in find_book_links(md.read_text()):
            if not page or page not in parents[book]:
                continue  # top-page links carry no chapter; unknown pages are check()'s job
            chapter = chapter_of(book, page, parents)
            pages = usage[book].setdefault(chapter, {})
            pages[rel] = pages.get(rel, 0) + 1
    return usage


def print_usage(root: Path, subwikis: list[str]) -> None:
    titles = load_catalog()
    usage = chapter_usage(root, subwikis, load_parents())
    for book in BOOKS:
        print(f"== {book}")
        for chapter in sorted(usage[book], key=lambda c: titles[book].get(c, c)):
            pages = usage[book][chapter]
            print(f"  {titles[book].get(chapter, chapter)} ({chapter})")
            for rel, n in sorted(pages.items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"    {n:2d}  {rel}")


def update_catalog(src_root: Path) -> None:
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    for book in BOOKS:
        html_dir = src_root / book / f"{book}HTML"
        if not html_dir.is_dir():
            print(f"*** {html_dir} does not exist - build the book HTML first", file=sys.stderr)
            sys.exit(1)
        lines: list[str] = []
        for page in sorted(html_dir.glob("*.html")):
            head = page.read_text(errors="replace")[:8000]
            m = TITLE_RE.search(head)
            if not m:
                print(f"*** no <TITLE> in {page}", file=sys.stderr)
                sys.exit(1)
            title = html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())
            up = UP_RE.search(head)
            lines.append(f"{page.name}\t{title}\t{up.group(1) if up else ''}")
        out = CATALOG_DIR / f"{book}.tsv"
        out.write_text("\n".join(lines) + "\n")
        print(f"  {book}: {len(lines)} pages -> {out}")


def main() -> None:
    args = sys.argv[1:]
    if len(args) >= 3 and args[0] == "check":
        sys.exit(check(Path(args[1]).resolve(), args[2:]))
    if len(args) >= 3 and args[0] == "usage":
        print_usage(Path(args[1]).resolve(), args[2:])
        return
    if args and args[0] == "update-catalog" and len(args) <= 2:
        update_catalog(Path(args[1] if len(args) == 2 else "/w"))
        return
    print(__doc__, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

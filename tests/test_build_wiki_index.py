"""Unit tests for scripts/build_wiki_index.py."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_wiki_index as bwi  # noqa: E402

SCHEMA = """# Wiki Schema

## Title
Alpha Things

## Domain One-Line Summary
All about alpha.

## Domain
Alpha -- the long description.
Second line.

## Conventions
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_schema_fields(tmp_path: Path) -> None:
    write(tmp_path / "alpha" / "SCHEMA.md", SCHEMA)
    write(tmp_path / "alpha" / "index.md", "# Index\n")
    assert bwi.display_title(tmp_path / "alpha", "Fallback") == "Alpha Things"
    assert bwi.one_line_summary(tmp_path / "alpha") == "All about alpha."
    assert bwi.domain_summary(tmp_path / "alpha") == "Alpha -- the long description."
    assert bwi.page_count(tmp_path / "alpha") == 2
    assert bwi.display_title(tmp_path / "missing", "Fallback") == "Fallback"


def test_books_paragraph_links_every_book_and_hub() -> None:
    html = bwi.books_paragraph()
    for key, hub, _short, _title in bwi.BOOKS:
        assert f'href="https://ccrma.stanford.edu/~jos/{key}/"' in html
        assert f'href="jos_books/entities/{hub}.html"' in html
    assert 'href="jos_books/queries/book-topic-finder.html"' in html


def test_book_hub_pages_exist_in_repo() -> None:
    """The front page links hub pages by name; they must exist."""
    root = Path(__file__).resolve().parents[1]
    for _key, hub, _short, _title in bwi.BOOKS:
        assert (root / bwi.BOOKS_SUBWIKI / "entities" / f"{hub}.md").is_file()
    assert (root / bwi.BOOKS_SUBWIKI / "queries" / "book-topic-finder.md").is_file()


def test_main_emits_books_paragraph_only_with_books_subwiki(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / "alpha" / "SCHEMA.md", SCHEMA)
    monkeypatch.setattr(sys, "argv", ["build_wiki_index.py", str(tmp_path), "alpha"])
    bwi.main()
    out = capsys.readouterr().out
    assert "<b>Books:</b>" not in out
    assert '<a href="alpha/index.html">Alpha Things</a>' in out

    write(tmp_path / "jos_books" / "SCHEMA.md", SCHEMA.replace("Alpha Things", "JOS Online Books"))
    monkeypatch.setattr(sys, "argv", ["build_wiki_index.py", str(tmp_path), "alpha", "jos_books"])
    bwi.main()
    out = capsys.readouterr().out
    assert "<b>Books:</b>" in out
    assert '<a href="jos_books/index.html">JOS Online Books</a>' in out

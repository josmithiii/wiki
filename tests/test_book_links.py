"""Unit tests for scripts/book_links.py: book-URL extraction, catalog checking,
catalog generation, and the committed catalog itself."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import book_links as bl  # noqa: E402

BASE = "https://ccrma.stanford.edu/~jos"
CATALOG: dict[str, dict[str, str]] = {
    "mdft": {"Sampling_Theorem.html": "Sampling Theorem"},
    "filters": {"Allpass_Filters.html": "Allpass Filters"},
    "pasp": {"Digital_Waveguides.html": "Digital Waveguides",
             "_Traveling_Waves_Lumped_Systems.html": "``Traveling Waves'' in Lumped Systems"},
    "sasp": {"Welch_s_Method.html": "Welch's Method"},
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_find_book_links_forms() -> None:
    text = (
        f"A markdown link [Digital Waveguides]({BASE}/pasp/Digital_Waveguides.html), "
        f"a bare one {BASE}/sasp/Welch_s_Method.html. "
        f"With a fragment: <{BASE}/filters/Allpass_Filters.html#sec>. "
        f"Leading underscore: ({BASE}/pasp/_Traveling_Waves_Lumped_Systems.html) "
        f"http scheme: http://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html\n"
    )
    assert bl.find_book_links(text) == [
        ("pasp", "Digital_Waveguides.html"),
        ("sasp", "Welch_s_Method.html"),
        ("filters", "Allpass_Filters.html"),
        ("pasp", "_Traveling_Waves_Lumped_Systems.html"),
        ("mdft", "Sampling_Theorem.html"),
    ]


def test_find_book_links_top_pages_and_non_books() -> None:
    text = (
        f"Top pages: {BASE}/pasp/ and `{BASE}/sasp/`. and {BASE}/mdft\n"
        f"Template placeholders: {BASE}/sasp/... {BASE}/sasp/<Page_Name>.html "
        f"{BASE}/pasp/{{page}}.html\n"
        f"Not the four books: {BASE}/wiki/graph.html {BASE}/fp/ {BASE}/pasptalk/x.html "
        f"{BASE}/filtersfoo\n"
    )
    assert bl.find_book_links(text) == [("pasp", ""), ("sasp", ""), ("mdft", "")]


def test_bad_links_reports_only_unknown_pages() -> None:
    text = (
        f"[ok]({BASE}/pasp/Digital_Waveguides.html) [top]({BASE}/pasp/) "
        f"[dead]({BASE}/pasp/Damping.html) [wrong book]({BASE}/sasp/Digital_Waveguides.html)"
    )
    assert bl.bad_links(text, CATALOG) == ["pasp/Damping.html", "sasp/Digital_Waveguides.html"]


def test_update_and_load_catalog_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src = tmp_path / "w"
    for book in bl.BOOKS:
        write(src / book / f"{book}HTML" / "Some_Page.html",
              '<HTML><HEAD>\n<TITLE>Some\n  Page &amp; More</TITLE>\n'
              '<LINK REL="up" HREF="Parent_Page.html">\n</HEAD></HTML>\n')
        write(src / book / f"{book}HTML" / f"{book}.html", "<TITLE>THE BOOK</TITLE>")
        write(src / book / f"{book}HTML" / "img1.png", "not html")
    monkeypatch.setattr(bl, "CATALOG_DIR", tmp_path / "catalog")
    bl.update_catalog(src)
    assert (tmp_path / "catalog" / "pasp.tsv").read_text() == (
        "Some_Page.html\tSome Page & More\tParent_Page.html\npasp.html\tTHE BOOK\t\n")
    catalog = bl.load_catalog(tmp_path / "catalog")
    assert set(catalog) == set(bl.BOOKS)
    assert catalog["sasp"] == {"Some_Page.html": "Some Page & More", "sasp.html": "THE BOOK"}


def test_update_catalog_fails_loudly_without_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bl, "CATALOG_DIR", tmp_path / "catalog")
    with pytest.raises(SystemExit) as exc:
        bl.update_catalog(tmp_path / "no-such-root")
    assert exc.value.code == 1


def test_load_catalog_fails_loudly_when_missing(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exc:
        bl.load_catalog(tmp_path)
    assert exc.value.code == 1


def test_check_counts_and_exit_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                      capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(bl, "load_catalog", lambda: CATALOG)
    write(tmp_path / "alpha" / "concepts" / "good.md",
          f"[a]({BASE}/pasp/Digital_Waveguides.html) [b]({BASE}/filters/Allpass_Filters.html)\n")
    write(tmp_path / "alpha" / "raw" / "ignored.md", f"{BASE}/pasp/No_Such_Page.html\n")
    assert bl.check(tmp_path, ["alpha"]) == 0
    assert "book links: 2 in 1 pages (0 unknown)" in capsys.readouterr().out

    write(tmp_path / "alpha" / "concepts" / "bad.md", f"[x]({BASE}/mdft/No_Such_Page.html)\n")
    assert bl.check(tmp_path, ["alpha"]) == 1
    captured = capsys.readouterr()
    assert "*** unknown book page in alpha/concepts/bad.md" in captured.err
    assert f"{BASE}/mdft/No_Such_Page.html" in captured.err
    assert "(1 unknown)" in captured.out


def test_check_fails_loudly_on_missing_subwiki(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bl, "load_catalog", lambda: CATALOG)
    with pytest.raises(SystemExit) as exc:
        bl.check(tmp_path, ["nope"])
    assert exc.value.code == 1


PARENTS: dict[str, dict[str, str]] = {
    "mdft": {"mdft.html": "", "Sampling_Theory.html": "mdft.html",
             "Sampling_Theorem.html": "Sampling_Theory.html"},
    "filters": {"Allpass_Filters.html": "filters.html"},
    "pasp": {"index.html": "", "Acoustic_Modeling_Digital_Delay.html": "pasp.html",
             "Digital_Waveguides.html": "Acoustic_Modeling_Digital_Delay.html",
             "Physical_Outputs.html": "Digital_Waveguides.html",
             "Orphan.html": ""},
    "sasp": {},
}


def test_chapter_of_walks_up_to_the_chapter_page() -> None:
    assert bl.chapter_of("pasp", "Physical_Outputs.html", PARENTS) == "Acoustic_Modeling_Digital_Delay.html"
    assert bl.chapter_of("pasp", "Acoustic_Modeling_Digital_Delay.html", PARENTS) == "Acoustic_Modeling_Digital_Delay.html"
    assert bl.chapter_of("mdft", "Sampling_Theorem.html", PARENTS) == "Sampling_Theory.html"
    assert bl.chapter_of("pasp", "Orphan.html", PARENTS) == "Orphan.html"


def test_chapter_usage_counts_links_per_wiki_page(tmp_path: Path) -> None:
    write(tmp_path / "alpha" / "concepts" / "strings.md",
          f"[a]({BASE}/pasp/Digital_Waveguides.html) [b]({BASE}/pasp/Physical_Outputs.html) "
          f"[c]({BASE}/mdft/Sampling_Theorem.html) [top]({BASE}/pasp/) [dead]({BASE}/pasp/Nope.html)\n")
    write(tmp_path / "alpha" / "concepts" / "reverb.md", f"[a]({BASE}/filters/Allpass_Filters.html)\n")
    write(tmp_path / "alpha" / "index.md", f"[a]({BASE}/filters/Allpass_Filters.html)\n")
    write(tmp_path / "alpha" / "entities" / "source-papers.md", f"{BASE}/filters/Allpass_Filters.html\n")
    assert bl.chapter_usage(tmp_path, ["alpha"], PARENTS) == {
        "mdft": {"Sampling_Theory.html": {"alpha/concepts/strings": 1}},
        "filters": {"Allpass_Filters.html": {"alpha/concepts/reverb": 1}},
        "pasp": {"Acoustic_Modeling_Digital_Delay.html": {"alpha/concepts/strings": 2}},
        "sasp": {},
    }


def test_committed_parents_reach_a_chapter() -> None:
    """Every cataloged page resolves to a chapter whose parent is a top page."""
    parents = bl.load_parents()
    for book in bl.BOOKS:
        tops = {f"{book}.html", "index.html", ""}
        for page in parents[book]:
            assert parents[book][bl.chapter_of(book, page, parents)] in tops, (book, page)
    assert bl.chapter_of("pasp", "Wave_Digital_Filters_I.html", parents) == "Wave_Digital_Filters_I.html"
    assert bl.chapter_of("pasp", "Wave_Digital_Filters.html", parents) == "Introduction_Physical_Signal_Models.html"


def test_committed_catalog_is_complete() -> None:
    """The catalog in the repo covers all four books and their top pages."""
    catalog = bl.load_catalog()
    for book in bl.BOOKS:
        assert len(catalog[book]) > 250, book
        assert f"{book}.html" in catalog[book]
        assert "index.html" in catalog[book]
    assert catalog["pasp"]["Digital_Waveguides.html"] == "Digital Waveguides"
    assert catalog["sasp"]["Welch_s_Method.html"] == "Welch's Method"


def test_wiki_book_links_all_resolve() -> None:
    """Every book URL in the real wiki pages is in the committed catalog."""
    root = Path(__file__).resolve().parents[1]
    catalog = bl.load_catalog()
    subwikis = [d.name for d in sorted(root.iterdir())
                if (d / "SCHEMA.md").is_file() and (d / "index.md").is_file()]
    assert "jos_books" in subwikis
    bad = {str(md.relative_to(root)): bl.bad_links(md.read_text(), catalog)
           for md in bl.wiki_markdown_files(root, subwikis)}
    assert {k: v for k, v in bad.items() if v} == {}

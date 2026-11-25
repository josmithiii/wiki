"""Unit tests for scripts/build_wiki.py: wikilink conversion and error counting."""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_wiki as bw  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def wiki(tmp_path: Path) -> Path:
    write(tmp_path / "alpha" / "concepts" / "foo.md", "# Foo\n")
    write(tmp_path / "alpha" / "concepts" / "bar.md", "# Bar\n\n## Some Heading\n")
    write(tmp_path / "beta" / "entities" / "bar.md", "# Other Bar\n")
    return tmp_path


def convert(wiki: Path, text: str, src: str = "alpha/concepts/foo.md") -> tuple[str, list[str]]:
    by_bare, by_relpath = bw.collect_md_files(wiki, ["alpha", "beta"])
    return bw.convert_wikilinks(text, wiki / src, wiki, by_bare, by_relpath)


def test_wikilink_forms(wiki: Path) -> None:
    out, broken = convert(wiki, "[[bar]] [[bar|The Bar]] [[bar#some-heading]] [[#top]] "
                                "[[beta/entities/bar|B]] [[entities/bar]]")
    assert broken == []
    assert out == ("[bar](bar.html) [The Bar](bar.html) [bar](bar.html#some-heading) "
                   "[top](#top) [B](../../beta/entities/bar.html) "
                   "[bar](../../beta/entities/bar.html)")


def test_bare_name_prefers_same_subwiki(wiki: Path) -> None:
    out, _ = convert(wiki, "[[bar]]", src="beta/entities/bar.md")
    assert out == "[bar](bar.html)"
    out, _ = convert(wiki, "[[foo]]", src="beta/entities/bar.md")
    assert out == "[foo](../../alpha/concepts/foo.html)"


def test_code_spans_are_left_alone(wiki: Path) -> None:
    text = "`[[nope]]` and\n```\n[[nope-either]]\n```\n"
    out, broken = convert(wiki, text)
    assert out == text
    assert broken == []


def test_broken_links_are_reported(wiki: Path) -> None:
    out, broken = convert(wiki, "[[missing]] and [[also-missing|x]] and [[bar]]")
    assert broken == ["missing", "also-missing"]
    assert "(#broken-link-missing)" in out


@pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")
def test_render_one_counts_broken_links_as_errors(wiki: Path, capsys: pytest.CaptureFixture[str]) -> None:
    by_bare, by_relpath = bw.collect_md_files(wiki, ["alpha", "beta"])
    pages = bw.collect_subwiki_pages(wiki, ["alpha", "beta"])
    good = wiki / "alpha" / "concepts" / "foo.md"
    good.write_text("---\ntitle: Foo\n---\n# Foo\nSee [[bar]].\n")
    assert bw.render_one(good, wiki, by_bare, by_relpath, pages) == 0
    assert 'href="bar.html"' in good.with_suffix(".html").read_text()

    bad = wiki / "alpha" / "concepts" / "bar.md"
    bad.write_text("# Bar\n[[missing-one]] [[missing-two]] [[foo]]\n")
    assert bw.render_one(bad, wiki, by_bare, by_relpath, pages) == 2
    assert "*** broken wikilink in alpha/concepts/bar.md: [[missing-one]]" in capsys.readouterr().err
    assert bad.with_suffix(".html").is_file()  # still rendered, with dead anchors

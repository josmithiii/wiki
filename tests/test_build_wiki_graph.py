"""Unit tests for scripts/build_wiki_graph.py on a tiny synthetic wiki."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_wiki_graph as bwg  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def wiki(tmp_path: Path) -> Path:
    sw = tmp_path / "alpha"
    write(sw / "index.md", "# Index\n[[foo]] [[bar]]\n")
    write(sw / "SCHEMA.md", "# Schema\n[[foo]]\n")
    write(sw / "concepts" / "foo.md",
          "---\ntitle: Foo Page\ntype: concept\ntags: [a, b]\n---\n# Foo\n"
          "See [[bar]] and [[entities/source-papers#paper-one]] and [[bar]] again.\n"
          "Not a link: `[[bar]]`\n")
    write(sw / "concepts" / "bar.md",
          "---\ntitle: Bar\ntype: comparison\n---\n# Bar\n[[foo|Foo!]] [[#local]]\n")
    write(sw / "entities" / "source-papers.md",
          "---\ntitle: Sources\ntype: entity\n---\n# Sources\nPreamble links [[foo]].\n\n"
          "## Group\n\n### paper-one\nAbout [[bar]].\n\n### paper-two\nLinks [[#paper-one]] and [[missing-page]].\n")
    other = tmp_path / "beta"
    write(other / "concepts" / "baz.md", "---\ntype: concept\n---\n# Baz\n[[alpha/concepts/foo]]\n")
    return tmp_path


def test_nodes_and_types(wiki: Path) -> None:
    g = bwg.build_graph(wiki, ["alpha", "beta"])
    ids = {n["id"]: n for n in g["nodes"]}
    assert set(ids) == {
        "alpha/concepts/foo", "alpha/concepts/bar", "alpha/entities/source-papers",
        "alpha/entities/source-papers#paper-one", "alpha/entities/source-papers#paper-two",
        "beta/concepts/baz",
    }
    assert ids["alpha/concepts/foo"]["type"] == "concept"
    assert ids["alpha/concepts/foo"]["title"] == "Foo Page"
    assert ids["alpha/concepts/foo"]["tags"] == ["a", "b"]
    assert ids["alpha/concepts/foo"]["href"] == "alpha/concepts/foo.html"
    assert ids["alpha/entities/source-papers#paper-one"]["type"] == "source"
    assert ids["alpha/entities/source-papers#paper-one"]["href"] == "alpha/entities/source-papers.html#paper-one"
    assert ids["beta/concepts/baz"]["topic"] == "beta"
    assert g["types"] == ["comparison", "concept", "entity", "source"]
    assert g["topics"] == ["alpha", "beta"]


def test_edges(wiki: Path) -> None:
    g = bwg.build_graph(wiki, ["alpha", "beta"])
    edges = {(e["source"], e["target"]) for e in g["edges"]}
    assert edges == {
        ("alpha/concepts/foo", "alpha/concepts/bar"),                       # deduped, code span ignored
        ("alpha/concepts/foo", "alpha/entities/source-papers#paper-one"),   # anchored link -> section node
        ("alpha/concepts/bar", "alpha/concepts/foo"),                       # display override
        ("alpha/entities/source-papers", "alpha/concepts/foo"),             # preamble -> parent node
        ("alpha/entities/source-papers#paper-one", "alpha/concepts/bar"),   # section body -> section node
        ("alpha/entities/source-papers#paper-two", "alpha/entities/source-papers#paper-one"),  # [[#anchor]]
        ("beta/concepts/baz", "alpha/concepts/foo"),                        # cross-sub-wiki
    }
    ids = {n["id"]: n for n in g["nodes"]}
    assert ids["alpha/concepts/foo"]["links_out"] == 2
    assert ids["alpha/concepts/foo"]["links_in"] == 3


def test_render_inlines_data_and_d3(wiki: Path) -> None:
    g = bwg.build_graph(wiki, ["alpha", "beta"])
    out = wiki / "graph.html"
    bwg.render(g, out)
    html = out.read_text()
    assert "GRAPH_DATA_PLACEHOLDER" not in html
    assert "<!--D3_INLINE-->" not in html
    assert "d3js.org v7" in html
    assert json.dumps(g) in html
    assert "wiki-graph-423gl.html" in html


def test_slugify_matches_pandoc_style() -> None:
    assert bwg.slugify("paper-Foo Bar (2026)") == "paper-foo-bar-2026"


CITATION_CASES = [
    ('**"Title"** - Michele Ducceschi, Riccardo Russo, Craig J. Webb (University of Bologna) · DAFx26 · `raw/x.txt`',
     ["Michele Ducceschi", "Riccardo Russo", "Craig J. Webb"]),
    ('**"Title"** — Jean Laroche & Mark Dolson · *IEEE TSAP* 7(3), 1999',
     ["Jean Laroche", "Mark Dolson"]),
    ('**"Title"** — Wang et al. (NTU) · arXiv 2024',
     ["Wang"]),
    ('**"Title"** - Georg Essl (University of Wisconsin - Milwaukee) - DAFx26, Cambridge MA, Sept 2026 - `raw/p.txt`',
     ["Georg Essl"]),
    ('**"Title"** — Widrow, Glover, McCool · *Proc. IEEE* 1975',
     ["Widrow", "Glover", "McCool"]),
    ('**"Title"** -- A. One and B. Two · Venue',
     ["A. One", "B. Two"]),
    ('No citation line here.\n- Tags: a, b\n', []),
]


@pytest.mark.parametrize("body,expected", CITATION_CASES)
def test_parse_authors(body: str, expected: list[str]) -> None:
    assert bwg.parse_authors(body) == expected


def test_parse_section_tags() -> None:
    body = "**\"T\"** - A · V\n\n- Bullet\n- Tags: modal, `string`, 'dsp', reference\n"
    assert bwg.parse_section_tags(body) == ["modal", "string", "dsp", "reference"]
    assert bwg.parse_section_tags("no tags") == []


def test_source_nodes_carry_authors_and_tags(tmp_path: Path) -> None:
    write(tmp_path / "w" / "entities" / "source-papers.md",
          "---\ntype: entity\n---\n# S\n\n### paper-x-2026\n\n"
          "**\"X\"** - Ann Author, Bob Writer (Uni) · DAFx26\n\n- Tags: modal, reference\n")
    g = bwg.build_graph(tmp_path, ["w"])
    node = next(n for n in g["nodes"] if n["id"].endswith("#paper-x-2026"))
    assert node["authors"] == ["Ann Author", "Bob Writer"]
    assert node["tags"] == ["modal", "reference"]
    assert "reference" in g["role_tags"]
    page = next(n for n in g["nodes"] if n["id"] == "w/entities/source-papers")
    assert page["authors"] == []

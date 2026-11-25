# Codex instructions for `~/wiki/`

## Wikilink resolution rules

`[[wikilinks]]` are resolved by `scripts/build_wiki.py`. They MUST point to a real target or `make rebuild` will print `*** broken wikilink ...` and the link will render as a dead anchor.

Valid forms (from `build_wiki.py` docstring):

- `[[bare-name]]` -- matches `bare-name.md` anywhere in any sub-wiki
- `[[subdir/bare-name]]` -- matches a wikilink ending in `subdir/bare-name.md`
- `[[subwiki/path/bare-name]]` -- exact path under the wiki root
- `[[name|Display Text]]` -- display override
- `[[page#heading]]` -- anchor within another page (heading slug)
- `[[#heading]]` -- anchor within the current page (heading slug)

### Common failure mode: section is not a page

A `### some-heading` inside a multi-entity page (e.g., `entities/source-papers.md`) is NOT a standalone page. Writing `[[some-heading]]` will break -- it looks for `some-heading.md`.

**When referring to a section of a page, use anchor syntax:**

- Same file: `[[#paper-guicking-anvc-overview]]`
- Other file: `[[source-papers#paper-guicking-anvc-overview]]`

The anchor slug must match the heading text exactly (lowercase with hyphens, as pandoc generates).

## Links into the JOS online books

The four books (mdft, filters, pasp, sasp) are online one HTML page per section: `https://ccrma.stanford.edu/~jos/<book>/<Page_Name>.html`. Page names follow section titles and CANNOT be guessed (`pasp/Damping.html` does not exist).

- Look the page name up: `grep -i 'group delay' jos_books/catalog/*.tsv` (columns: page name, title, parent page - the parent tells `Foo.html` from `Foo_I.html`).
- Topical pages end with a `## JOS online books` section: one bullet per book, the hub wikilink first (`[[jos_books/entities/pasp-book|PASP]]`, likewise `mdft-book`, `filters-book`, `sasp-book`), then 2-6 deep links whose text is the book section's title. Leave the section out when no book section really covers the topic.
- `make book-links` checks every book URL against the catalog; the convention in full is in `jos_books/SCHEMA.md`.

## Before committing wiki changes

Run `make rebuild` and confirm `(0 errors)`, `(0 unknown)` book links, and no `*** broken wikilink` or `*** unknown book page` lines; the build exits 1 on either. Fix broken links before committing - they are always fixable (rename target, use anchor syntax, or remove the link). Run `make test` after touching `scripts/`.

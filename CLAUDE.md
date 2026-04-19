# Claude instructions for `~/wiki/`

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

## Before committing wiki changes

Run `make rebuild` and confirm `(0 errors)` and no `*** broken wikilink` lines. Fix broken links before committing -- they are always fixable (rename target, use anchor syntax, or remove the link).

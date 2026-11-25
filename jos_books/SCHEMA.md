# Wiki Schema

## Title
JOS Online Books

## Domain One-Line Summary
Hub pages for Julius O. Smith III's four online books (MDFT, Filters, PASP, SASP): chapter maps, deep links, and pointers to the wiki pages that build on each chapter.

## Domain
Hub pages for the four-book music signal processing series by Julius O. Smith III - *Mathematics of the DFT* (MDFT), *Introduction to Digital Filters* (Filters), *Physical Audio Signal Processing* (PASP), and *Spectral Audio Signal Processing* (SASP) - all free online at `https://ccrma.stanford.edu/~jos/`.  This sub-wiki does not re-distill the books (the topical sub-wikis do that); it maps each book's chapters to their online pages and to the wiki pages that draw on them, and it holds the catalog of valid book page names that the build checks every book link against.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** - start from `index.md` or `queries/book-topic-finder`
- **Split pages at ~100 lines** - a hub page that outgrows this gets a per-part page
- **Never read `catalog/*.tsv` whole** (2,096 lines in all) - `grep` it

## The books

| Key | Book | Online | Local LaTeX source |
|-----|------|--------|--------------------|
| `mdft` | Mathematics of the Discrete Fourier Transform (DFT), 2nd ed. | `https://ccrma.stanford.edu/~jos/mdft/` | `/w/mdft/` |
| `filters` | Introduction to Digital Filters | `https://ccrma.stanford.edu/~jos/filters/` | `/w/filters/` |
| `pasp` | Physical Audio Signal Processing | `https://ccrma.stanford.edu/~jos/pasp/` | `/w/pasp/` |
| `sasp` | Spectral Audio Signal Processing | `https://ccrma.stanford.edu/~jos/sasp/` | `/w/sasp/` |

Each book is served one HTML page per section:
`https://ccrma.stanford.edu/~jos/<key>/<Page_Name>.html`.  Page names are
derived from section titles by latex2html, so guessing them fails often
(`Damping.html`, `Excitation.html` and `Impulse_Response.html` were all
guessed, and all dead).

## Linking to the books (applies to every sub-wiki)
1. **Find the page name in the catalog**, never by guessing:
   `grep -i 'group delay' jos_books/catalog/*.tsv`.  Columns are
   page name, page title, parent page.  When a title repeats (`Foo.html`,
   `Foo_I.html`), the parent column says which is the chapter and which is a
   subsection elsewhere.
2. **End each topical page with a `## JOS online books` section**, one bullet
   per book, the hub page first and then 2-6 deep links whose text is the
   book section's title:
   `- [[jos_books/entities/pasp-book|PASP]]: [Lagrange Interpolation](https://ccrma.stanford.edu/~jos/pasp/Lagrange_Interpolation.html), ...`
   Omit the section when no book section genuinely covers the topic.
3. **Link inline** where the text relies on a specific book result.
4. **In frontmatter `sources:`** list the online URL (and, for pages distilled
   from the LaTeX, the `/w/<key>/<file>.tex` path as well).
5. **Check**: `make book-links` (also run by `make rebuild`) exits 1 on any
   book URL whose page is not in the catalog.

## Maintaining the catalog
- `make book-catalog` regenerates `catalog/<key>.tsv` from the local
  latex2html output in `/w/<key>/<key>HTML/`.  Run it after a book's HTML is
  rebuilt *and uploaded*, then `make book-links` to find links that the
  rebuild renamed.
- The catalog was last verified against the live site on 2026-11-25
  (all 2,096 pages returned HTTP 200).

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `pasp-book.md`)
- Every page starts with YAML frontmatter (title, created, updated, type, tags, sources)
- Hub pages use bullet lists, not tables, for chapter maps (aliased
  `[[target|text]]` wikilinks contain a `|`, which breaks table cells)
- Wikilinks into other sub-wikis carry the sub-wiki prefix:
  `[[waveguide_synthesis/concepts/string-modeling|string-modeling]]`
- New text uses ` - ` for a dash, never `--`
- When updating a page, bump `updated`; append every action to `log.md`

## Tag Taxonomy
- book - one of the four online books
- mdft - Mathematics of the DFT
- filters - Introduction to Digital Filters
- pasp - Physical Audio Signal Processing
- sasp - Spectral Audio Signal Processing
- dsp-foundations - prerequisite math and filter theory
- physical-modeling - waveguide, modal, lumped, and wave digital modeling
- spectral - FFT-based analysis and synthesis
- reference - lookup tables and link maps
- overview - orientation pages

## Directory Structure
- `entities/` - one hub page per book
- `concepts/` - how the books relate to each other and to the sub-wikis
- `queries/` - topic-to-section lookup
- `catalog/` - `<key>.tsv` page catalogs (generated; do not hand-edit)

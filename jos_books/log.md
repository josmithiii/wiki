# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-11-25] create | Wiki initialized
- Domain: hub pages for the four JOS online books (MDFT, Filters, PASP, SASP)
- Why: an audit found the books thinly integrated - 13 of 133 pages linked
  PASP or SASP online (3 of those 16 links were dead guesses), no page
  linked MDFT or Filters, and SASP-derived pages cited only local
  `/w/sasp/*.tex` paths that the public site cannot follow
- Created SCHEMA.md (the book-linking convention for all sub-wikis),
  index.md, log.md
- Created entities/mdft-book, filters-book, pasp-book, sasp-book (chapter
  and appendix maps with deep links and pointers to the wiki pages built
  on each chapter)
- Created concepts/book-series-overview and queries/book-topic-finder
- Generated catalog/{mdft,filters,pasp,sasp}.tsv (2,096 page names with
  titles and parent pages) from `/w/<book>/<book>HTML/` via
  `scripts/book_links.py update-catalog`; every cataloged page verified
  live (HTTP 200) on ccrma.stanford.edu the same day
- `make rebuild` now runs `make book-links`, which fails the build on a
  book URL that is not in the catalog

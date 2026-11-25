# Wiki Index

> Hub pages for the four JOS online books and the catalog of their page names.
> Read this first to find the right book section or the wiki pages built on it.
> Last updated: 2026-11-25 | Total pages: 6

## Entities (one per book)
- [[mdft-book]] - *Mathematics of the DFT*: chapter map; complex sinusoids, DFT theorems, sampling, dB, correlation
- [[filters-book]] - *Introduction to Digital Filters*: chapter map; z transform, poles/zeros, allpass, state space, bilinear transform
- [[pasp-book]] - *Physical Audio Signal Processing*: chapter map; delay effects, reverb, waveguides, lumped and wave digital models
- [[sasp-book]] - *Spectral Audio Signal Processing*: chapter map; windows, STFT, sinusoidal modeling, filter banks

## Concepts
- [[book-series-overview]] - how the four books depend on each other and map onto the sub-wikis; how to cite

## Queries
- [[book-topic-finder]] - topic -> book section(s) -> wiki page, for about 45 common topics

## Catalog (generated data, not pages)
- `catalog/mdft.tsv` (301 pages), `catalog/filters.tsv` (386), `catalog/pasp.tsv` (793), `catalog/sasp.tsv` (616)
- Columns: page name, page title, parent page.  `grep -i` it; never read it whole.
- Deep-link form: `https://ccrma.stanford.edu/~jos/<book>/<Page_Name>.html`
- `make book-links` checks every book link in the wiki; `make book-catalog` regenerates the catalog (see SCHEMA.md)

## Sub-wikis that build on the books
- [[waveguide_synthesis/index|waveguide_synthesis]] (PASP), [[modal_synthesis/index|modal_synthesis]] (PASP, Filters), [[spectral_processing/index|spectral_processing]] (SASP, MDFT), [[virtual_analog/index|virtual_analog]] (Filters, PASP), [[active_absorbers/index|active_absorbers]] (PASP, Filters, MDFT)

# Wiki Schema

## Domain
Physics-based synthesis using measured or computed modes of vibration.
Covers modal analysis, resonator networks, impact synthesis, physical modeling,
instrument acoustics, room acoustics, and perceptual/computational aspects.
Adjacent: waveguide synthesis, FEM/BEM methods, signal processing, AI/ML for modal data.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** — if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** (not the usual 200) — break into sub-topics with cross-links
- **Keep index.md entries to one short line each** — the index must fit in context alongside a few pages
- **Prefer dense, scannable content** — bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `modal-analysis.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources:
  - https://example.com/original-source-url
  - raw/articles/local-copy.md
---
```

## Source Attribution
- When ingesting web sources, save the raw content to `raw/` AND record the
  original URL in the page's `sources:` frontmatter list.
- In the page body, cite sources using markdown footnotes:
  ```markdown
  Modal synthesis sums decaying sinusoids[^1].

  [^1]: https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html
  ```
- The local wiki links to raw files for offline reading; footnotes give the
  original URL. The export converter strips raw links and keeps only URLs.

## Tag Taxonomy

### Core Modal
- modal — modal analysis, mode shapes, resonant modes
- eigenmode — eigenvectors/eigenvalues, natural frequencies
- resonator — resonator bank, filter bank synthesis
- damping — loss factors, decay rates, Q-factor
- impulse-response — measured or synthesized IRs

### Physics / Math
- acoustics — sound radiation, acoustic modes
- vibration — structural vibration, plates, bars, membranes
- wave-equation — PDE solutions, numerical methods
- fem — finite element method
- bem — boundary element method
- rigid-body — rigid-body dynamics, contact models

### Synthesis Techniques
- physical-modeling — general physics-based synthesis umbrella
- waveguide — digital waveguide synthesis (adjacent/related)
- additive — additive sinusoidal synthesis
- impact — impact/collision synthesis
- friction — friction/bowing synthesis
- modal-synthesis — the core synthesis paradigm of this wiki

### Instruments / Objects
- string — string instruments
- percussion — percussion, drums, plates, bells
- wind — wind instruments, tubes, bore
- voice — vocal tract, singing synthesis
- room — room acoustics, architectural acoustics
- material — material properties (density, Young's modulus, etc.)

### Computation / Software
- dsp — digital signal processing
- gpu — GPU-accelerated computation
- realtime — real-time synthesis constraints
- dataset — measured/simulated datasets
- open-source — open-source implementations

### AI/ML
- ml — machine learning applied to modal synthesis
- neural — neural network models
- differentiable — differentiable physical models
- inference — fast inference / model compression

### People/Orgs
- person — researcher, composer
- company — commercial entity
- lab — academic lab

### Meta
- comparison — side-by-side analysis
- tutorial — how-to, worked example
- reference — mathematical reference, formula sheet
- history — historical development

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~100 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report

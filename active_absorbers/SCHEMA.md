# Wiki Schema

## Domain
Active absorbers and active noise control (ANC) — using loudspeakers,
sensors, and real-time control to cancel or reshape acoustic energy
rather than absorbing it passively. Covers active absorbers, active
impedance control, ANC headphones, feedforward/feedback controllers,
adaptive filters (LMS/FxLMS), secondary-path modeling, stability,
causality constraints, and acoustic metamaterial/hybrid approaches.
Adjacent: room acoustics, loudspeaker design, adaptive signal processing,
feedback control theory.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** — if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** (not the usual 200) — break into sub-topics with cross-links
- **Keep index.md entries to one short line each** — the index must fit in context alongside a few pages
- **Prefer dense, scannable content** — bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `fxlms-algorithm.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **All math must be written in LaTeX**, using `$...$` for inline and
  `$$...$$` for display equations (rendered via MathJax by the HTML build).
  Use `\begin{aligned}...\end{aligned}` for multi-line equations.
  Do not use plain-text notation like `rho`, `Gamma_i`, `mu`, or
  indented ASCII equations — write `$\rho$`, `$\Gamma_i$`, `$\mu$` instead.

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
  - raw/papers/local-copy.pdf
---
```

## Source Attribution
- When ingesting PDFs or web sources, keep the raw file in `raw/` AND record
  the original DOI/URL in the page's `sources:` frontmatter list.
- In the page body, cite sources using markdown footnotes.
- Raw PDFs must be converted to text via `pdf2txt.py` before distilling —
  never read PDFs directly.

## Tag Taxonomy

### Core ANC / Active Absorption
- anc — active noise control (general)
- active-absorber — tunable/active acoustic absorbers
- active-impedance — impedance matching / synthesis via feedback
- feedforward — feedforward controller topology
- feedback — feedback controller topology
- hybrid-control — combined feedforward + feedback

### Algorithms / Adaptive DSP
- lms — least-mean-square adaptive filter
- fxlms — filtered-x LMS (for plant in control path)
- nlms — normalized LMS
- rls — recursive least squares
- secondary-path — secondary-path estimation / modeling
- causality — causal constraints, advance requirements
- stability — stability analysis of adaptive loops

### Actuators / Sensors
- loudspeaker — control actuator, driver design
- microphone — error/reference sensor
- transducer — general electroacoustic transduction
- array — multi-transducer spatial control

### Physics / Math
- acoustics — sound propagation, radiation
- impedance — acoustic / mechanical impedance
- wave-equation — PDE formulation, radiation
- room-modes — standing waves, modal response
- metamaterial — acoustic metamaterials, membrane absorbers

### Applications
- headphones — ANC headphones / earbuds
- duct — duct / HVAC noise control
- enclosure — active sound package, cabin noise
- room — room-mode control, active bass traps
- industrial — industrial / machinery noise

### Meta
- comparison — side-by-side analysis
- tutorial — how-to, worked example
- reference — mathematical reference, formula sheet
- history — historical development
- person — researcher
- lab — academic / industry lab

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

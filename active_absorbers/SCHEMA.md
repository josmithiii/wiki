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

See the top-level [`~/wiki/README.md`](../README.md) "PDF ingestion convention"
section for the cross-wiki rules. In summary for this wiki:

- Original PDFs live on the host at `/l/dttd/`, symlinked into
  `/l/dttd/ANC-Stuff/`. They are **not in this repo**.
- Text extractions live in `raw/` and are produced by `pdf2txt.py`.
  `raw/` is `.gitignore`d — it is local-only state, never committed.
- `raw/MANIFEST.md` is the text-file ↔ original-PDF mapping.
- `raw/SUMMARIES.md` holds dense per-source distillation notes keyed to
  planned entity pages.
- When ingesting a new source, record the original DOI/URL in the page's
  `sources:` YAML frontmatter list AND cite with markdown footnotes in the
  page body.
- **Never use `Read` on a PDF directly** — always go through `pdf2txt.py`.

### Staging free-to-download PDFs

When an agent locates free PDFs on the web (arXiv, author pages, open-access
mirrors), stage them in `incoming-pdfs/` inside this sub-wiki. The PDFs
themselves are **not committed**, but `incoming-pdfs/README.md` — which
maps each filename to its source URL and to the concept/entity page it
feeds — *is* committed so the provenance is visible in git history even
after the staging directory is deleted. JOS moves the PDFs into `/l/dttd/`,
symlinks into `ANC-Stuff/`, runs `pdf2txt.py` to populate `raw/`, and then
the staging directory is removed.

### Excluded-from-distillation sources

Some items in `raw/` are kept as raw context but intentionally **not**
distilled into entity pages (e.g., internal project working documents for
the rooftop-fan effort). These are enumerated in
[`raw/MANIFEST.md`](raw/MANIFEST.md) under "Excluded from wiki distillation"
and must not be promoted to entity pages without explicit instruction.

## Tag Taxonomy

### Core ANC / Active Absorption
- anc — active noise control (general)
- active-absorber — tunable/active acoustic absorbers
- active-impedance — impedance matching / synthesis via feedback
- feedforward — feedforward controller topology
- feedback — feedback controller topology
- hybrid-control — combined feedforward + feedback
- hybrid-passive — combined active + passive treatment (not a controller topology)
- tonal — narrowband / periodic (e.g. BPF) noise control
- repetitive-control — RC / ILC / IMC for strictly periodic disturbances

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
- fan-noise — rotating-machinery / cooling-fan / blade-passing-frequency noise
- psychoacoustic — perceptual weighting, tonality penalty, loudness-based cost
- passive — passive absorbers / silencers / barriers (used as context for hybrid and out-of-scope pointer pages)

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

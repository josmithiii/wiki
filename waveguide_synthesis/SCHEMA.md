# Wiki Schema

## Title
Waveguide and Wave Digital Synthesis and Effects

## Domain
Digital-waveguide and wave-digital synthesis and effects -- modeling acoustic wave propagation using bidirectional delay lines, scattering junctions, and related structures.  Covers string, wind, and vocal-tract instruments, artificial reverberation, waveguide meshes, mass-spring systems, virtual analog, and modern extensions (differentiable, ML-optimized). Adjacent: modal synthesis, finite-difference methods, spectral modeling, DDSP.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** -- if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** (not the usual 200) -- break into sub-topics with cross-links
- **Keep index.md entries to one short line each** -- the index must fit in context alongside a few pages
- **Prefer dense, scannable content** -- bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `scattering-junctions.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **All math must be written in LaTeX**, using `$...$` for inline and
  `$$...$$` for display equations (rendered via MathJax by the HTML build).
  Use `\begin{aligned}...\end{aligned}` for multi-line equations.
  Do not use plain-text notation like `rho`, `Gamma_i`, `f_1^+`, or
  indented ASCII equations -- write `$\rho$`, `$\Gamma_i$`, `$f_1^+$` instead.

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
- In the page body, cite sources using markdown footnotes.
- The local wiki links to raw files for offline reading; footnotes give the
  original URL.

## Tag Taxonomy

### Core Waveguide
- waveguide -- digital waveguide modeling
- delay-line -- delay lines, circular buffers, interpolation
- scattering -- scattering junctions, adaptors, wave variables
- traveling-wave -- left/right going waves, d'Alembert solution

### Physics / Math
- acoustics -- sound propagation, radiation
- wave-equation -- PDE solutions, d'Alembert, dispersion
- impedance -- wave impedance, reflection coefficients
- nonlinear -- reed, bow, lip, and other nonlinear elements
- damping -- frequency-dependent loss, loop filters

### Synthesis Techniques
- physical-modeling -- general physics-based synthesis umbrella
- modal-synthesis -- modal synthesis (adjacent/related)
- commuted -- commuted synthesis shortcut
- banded -- banded waveguides for stiff structures
- mesh -- 2D/3D waveguide meshes
- sdn -- scattering delay networks

### Instruments / Objects
- string -- string instruments (plucked, struck, bowed)
- wind -- wind instruments, tubes, bore
- brass -- brass instruments, lip-reed
- reed -- single/double reed, clarinet, oboe
- flute -- air-jet, flute, organ pipe
- voice -- vocal tract, singing synthesis
- percussion -- bars, plates via waveguide methods
- guitar -- acoustic/electric guitar models

### Reverb / Room
- reverb -- artificial reverberation
- fdn -- feedback delay networks
- room -- room acoustics

### Computation / Software
- dsp -- digital signal processing
- realtime -- real-time synthesis
- stk -- Synthesis Toolkit (Cook/Scavone)
- faust -- FAUST language implementations

### AI/ML
- ml -- machine learning for waveguide parameter estimation
- differentiable -- differentiable waveguide models
- optimization -- parameter optimization (classical, evolutionary, neural)

### People/Orgs
- person -- researcher, composer
- company -- commercial entity
- lab -- academic lab

### Meta
- comparison -- side-by-side analysis
- tutorial -- how-to, worked example
- reference -- mathematical reference, formula sheet
- history -- historical development

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~100 lines -- break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded -- move to `_archive/`, remove from index

## Update Policy
When new information conflicts with existing content:
1. Check the dates -- newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report

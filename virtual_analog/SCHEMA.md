# Wiki Schema

## Title
Virtual Analog Modeling and Neural Audio Deployment

## Domain One-Line Summary
Virtual analog modeling of filters, circuits and synthesizer oscillators; anti-aliasing; neural/black-box and grey-box VA; real-time deployment of VA and neural audio models.

## Domain
Virtual analog (VA) modeling -- digital emulation of analog audio hardware and
of classic analog synthesis techniques.  Covers trapezoidal/TPT-ZDF filter
structures and their time-varying stability, ladder and state-variable filters,
state-space and DAE circuit solvers referenced to SPICE, antiderivative
antialiasing (ADAA) and oversampling, alias-reduced and geometric oscillators,
oscillator synchronization, FM synthesis and FM parameter estimation, dynamic
range compressor modeling and datasets, black-box neural VA (RNN, WaveNet,
neural operators), grey-box hybrids, and the real-time/embedded deployment
constraints that decide what actually ships (Apple Silicon, mobile GPU, iOS,
ASIC).  Adjacent: waveguide and wave digital synthesis, spectral processing,
modal synthesis.

**Wave digital filters live in `waveguide_synthesis/` (the `wdf-*` pages) and
are cross-linked from here, not duplicated.**  WDFs are a scattering/wave-variable
formalism shared with digital waveguides, so the canonical treatment stays there;
this wiki links to [[wave-digital-filters]], [[wdf-adaptors]], [[wdf-elements]]
and [[wdf-applications]] whenever a VA topic needs them.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** -- if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** (not the usual 200) -- break into sub-topics with cross-links
- **Keep index.md entries to one short line each** -- the index must fit in context alongside a few pages
- **Prefer dense, scannable content** -- bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `ladder-filter-models.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **All math must be written in LaTeX**, using `$...$` for inline and
  `$$...$$` for display equations (rendered via MathJax by the HTML build).
  Use `\begin{aligned}...\end{aligned}` for multi-line equations.
  Do not use plain-text notation like `omega_c`, `z^-1`, or indented ASCII
  equations -- write `$\omega_c$`, `$z^{-1}$` instead.
- Plain ASCII punctuation in page text: no em-dashes (use ` - ` with spaces),
  straight quotes only.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources:
  - /l/dttd/<paper>.pdf
  - raw/<extraction>.txt
  - https://example.com/original-source-url
---
```

## Source Attribution
- Research PDFs are **not** stored in this repo. They live on the host at
  `/l/dttd/` (DAFx26 proceedings at `/l/dttd/DAFx26/`).  Cite the PDF path in
  the page's `sources:` list.
- Text extractions go in `raw/` (globally gitignored); `raw/MANIFEST.md` maps
  each extraction to its original PDF and `raw/SUMMARIES.md` holds short
  distillation notes.
- **Never use the `Read` tool on a PDF directly** -- read the `.txt` extraction.
- In the page body, cite sources using markdown footnotes or by linking the
  catalog section in [[entities/source-papers]].

## Tag Taxonomy

### Core VA
- va-filters -- virtual analog filter structures in general
- ladder-filter -- Moog / diode ladder filters
- tpt-zdf -- topology-preserving transform, zero-delay feedback, trapezoidal integration
- state-variable -- state-variable and Sallen-Key filters
- allpass -- allpass structures, phasers, modulated allpass chains
- stability -- BIBO/Lyapunov stability, time-varying coefficient stability
- time-varying -- modulated coefficients, parameter interpolation

### Circuit Modeling
- circuit-modeling -- lumped circuit emulation in general
- spice -- SPICE-referenced simulation and validation
- state-space -- state-space / DAE / MNA circuit formulations
- wdf -- wave digital filters (canonical pages live in `waveguide_synthesis/`)
- nonlinear -- diodes, transistors, saturators, clipping stages
- piecewise-linear -- canonical piecewise-linear (CPWL) nonlinearity models
- pedal -- guitar pedals, overdrive/distortion units
- amplifier -- guitar/tube amplifier modeling
- compressor -- dynamic range compressors, gain-reduction modeling

### Aliasing and Oscillators
- antialiasing -- aliasing suppression in general
- adaa -- antiderivative antialiasing
- oversampling -- oversampled nonlinear processing
- oscillator -- digital oscillator algorithms
- oscillator-sync -- hard/soft oscillator synchronization
- polyblep -- BLEP/BLAMP/polyBLEP corrections
- additive -- additive/Fourier-series oscillator synthesis
- wavetable -- wavetable and pulsetable synthesis
- fm-synthesis -- frequency modulation synthesis

### Machine Learning
- neural-va -- neural black-box virtual analog
- rnn -- recurrent networks (LSTM/GRU) for VA
- wavenet -- WaveNet-style convolutional models
- fno -- Fourier neural operators, sample-rate independence
- grey-box -- hybrid physics + neural models
- differentiable -- differentiable DSP, gradient-based fitting
- parameter-estimation -- inverse problems, preset/parameter recovery
- graph-neural-network -- GNN parameter encoders
- pruning -- sparsity, quantization, model compression
- dataset -- measured datasets released with a paper

### Deployment
- real-time -- real-time audio thread constraints
- embedded -- microcontrollers, embedded SoC targets
- ios -- iOS/iPhone deployment
- apple-silicon -- macOS/Apple Silicon inference
- gpu -- GPU / integrated-GPU inference
- asic -- custom silicon
- benchmark -- benchmarking methodology and results
- plugin -- VST/AU/JUCE plugin implementation

### People/Orgs
- person -- researcher, developer
- company -- commercial entity
- lab -- academic lab

### Meta
- comparison -- side-by-side analysis
- tutorial -- how-to, worked example
- reference -- mathematical reference, formula sheet
- history -- historical development

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Directory Structure
- `entities/` -- specific methods, tools, devices, source-paper catalog
- `concepts/` -- core theory and techniques
- `comparisons/` -- side-by-side analyses
- `queries/` -- curated entry points for common questions
- `raw/` -- text extractions of source PDFs (gitignored)

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

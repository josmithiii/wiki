# Wiki Schema

## Domain
Signal processing, physics-based sound synthesis, audio/music DSP, and related AI/ML topics.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** — if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** (not the usual 200) — break into sub-topics with cross-links
- **Keep index.md entries to one short line each** — the index must fit in context alongside a few pages
- **Prefer dense, scannable content** — bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
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
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy
- DSP: dsp, filter, transform, spectral, convolution, sampling
- Synthesis: physical-modeling, waveguide, modal, additive, subtractive, fm
- Audio: audio, spatial, reverb, effects, measurement
- Physics: acoustics, vibration, wave-equation, resonance
- AI/ML: model, training, inference, dataset, embedding, rl
- People/Orgs: person, company, lab, open-source
- Meta: comparison, timeline, tutorial, reference

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

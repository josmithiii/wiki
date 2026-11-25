---
title: Decisions Log
created: 2026-04-10
updated: 2026-11-25
type: decision
tags: [shared]
---

# Decisions Log

### 2026-04-10 — Shared project state via ~/wiki/projects/
**Context:** Alex Finn's Obsidian memory prompt highlighted a gap — no cross-agent shared state
**Chose:** Add a `projects` sub-wiki to the existing ~/wiki/ LLM Wiki system
**Over:** Obsidian vault (separate tool), periodic checkpointing (overkill for Claude Code)
**Why:** ~/wiki/ already exists and is mounted into Docker; all agents can read/write it; minimal new infrastructure

### 2026-09-08 - New virtual_analog sub-wiki for the DAFx26 VA papers
**Context:** DAFx26 pass-1 ingestion needed a home for VA filters, ADAA, oscillators and neural VA
**Chose:** A new `virtual_analog/` sub-wiki
**Over:** Folding virtual analog into `waveguide_synthesis/`
**Why:** VA filters, ADAA, oscillators and neural VA are not waveguide material, while wave digital filters are - so WDFs stay in `waveguide_synthesis/` (the `wdf-*` pages) and are cross-linked from `virtual_analog/` rather than duplicated


### 2026-11-25 - New jos_books sub-wiki of hub pages rather than distilling MDFT and Filters
**Context:** An editorial pass found the four JOS online books thinly integrated: 13 of 133 pages linked PASP or SASP online, 3 of those 16 links were dead (guessed page names), no page linked MDFT or Filters, and the SASP-derived pages cited only local `/w/sasp/*.tex` paths
**Chose:** A small `jos_books/` sub-wiki - one hub page per book (chapter map with deep links and pointers to the wiki pages built on each chapter), a series overview, a topic finder, and a committed catalog of all 2,096 valid book page names - plus a `## JOS online books` section of deep links at the end of each topical page, checked at build time by `make book-links`
**Over:** (a) new sub-wikis distilling MDFT and Filters page by page; (b) only adding URLs to page frontmatter
**Why:** (a) the book sections are already short, self-contained and hyperlinked, so re-distilling them would duplicate the source for little gain, and deep links route a reader there directly; (b) frontmatter is not rendered on the web site, and unchecked links had already rotted - latex2html names pages after section titles, so names cannot be guessed and can change when a book is rebuilt

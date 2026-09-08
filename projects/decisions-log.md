---
title: Decisions Log
created: 2026-04-10
updated: 2026-09-08
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


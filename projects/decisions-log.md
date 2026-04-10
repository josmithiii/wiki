---
title: Decisions Log
created: 2026-04-10
updated: 2026-04-10
type: decision
tags: [shared]
---

# Decisions Log

### 2026-04-10 — Shared project state via ~/wiki/projects/
**Context:** Alex Finn's Obsidian memory prompt highlighted a gap — no cross-agent shared state
**Chose:** Add a `projects` sub-wiki to the existing ~/wiki/ LLM Wiki system
**Over:** Obsidian vault (separate tool), periodic checkpointing (overkill for Claude Code)
**Why:** ~/wiki/ already exists and is mounted into Docker; all agents can read/write it; minimal new infrastructure

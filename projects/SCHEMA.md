# Wiki Schema — Projects

## Domain
Cross-agent shared project state: active projects, decisions, and coordination
between Claude Code, Hermes Agent, and Open Claw.

## Context Budget
This wiki is shared across agents with varying context sizes. Rules:
- **Read at most 3 wiki pages per query** — synthesize from index summaries first
- **Split pages at 100 lines** — break into sub-topics with cross-links
- **Keep index.md entries to one short line each**
- **Prefer dense, scannable content** — bullet points over prose

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `hermes-agent.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md`
- Every action must be appended to `log.md`

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: project | decision | status
tags: [from taxonomy below]
---
```

## Tag Taxonomy
- Scope: hermes-agent, open-claw, jos-juce-plugins, dsp, wiki
- Status: active, paused, completed, blocked
- Kind: feature, bug, infrastructure, research, documentation
- Agent: claude-code, hermes, open-claw, shared

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it.

## Project Lifecycle
- Add a project block when sustained multi-session work begins
- Update `Current:` and `Next:` as work progresses
- Set status to `completed` when done
- Remove completed entries after ~1 week to keep the file short

## Special Files

### project-state.md
Active projects and their current status. Each project gets a short block:
```
## project-name
- **Status:** active | paused | blocked | completed
- **Goal:** one-line summary
- **Current:** what's happening now
- **Next:** what comes next
- **Decided:** key decisions made (with dates)
```

### decisions-log.md
Append-only log of non-obvious decisions. Format:
```
### YYYY-MM-DD — decision-title
**Context:** why this came up
**Chose:** what we picked
**Over:** what we rejected
**Why:** the reasoning
```

## Who Reads/Writes
- **Claude Code (JOS sessions):** reads on session start when relevant; writes when
  project status changes or significant decisions are made
- **Hermes Agent (Docker):** reads on session start; writes during task execution
- **Open Claw:** reads on session start; writes from its own workspace

Agents should read `project-state.md` at session start when working on any
listed project. Agents should append to `decisions-log.md` when a non-obvious
architectural or design choice is made.

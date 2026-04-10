---
title: Project State
created: 2026-04-10
updated: 2026-04-10
type: status
tags: [shared]
---

# Active Projects

## hermes-agent
- **Status:** active
- **Goal:** Self-improving AI agent framework — JOS fork with Docker dev environment, local LLM support
- **Current:** Fixed model-switch bug (vendor-prefixed models on custom endpoints); added make task/sessions/resume targets; added ~/wiki/projects/ shared state
- **Next:** PR the model-switch fix upstream; continue Docker workflow refinement
- **Decided:** Use Docker for Hermes runtime, host Ollama natively on M4 Mac (2026-04-08); model_aliases in config.yaml for quick provider switching (2026-04-10)

## modal-synthesis-wiki
- **Status:** active
- **Goal:** Build comprehensive ~/wiki/modal_synthesis/ knowledge base — physics-based synthesis using measured or computed modes
- **Current:** 14 pages (10 concepts, 1 comparison, 1 entity + damping, excitation, real-time added 2026-04-10)
- **Next:** Add pages on nonlinear extensions, coupled-mode interactions, ML-accelerated modal parameter estimation

## open-claw
- **Status:** active
- **Goal:** AI agent (separate project, shares wiki with Hermes)
- **Current:** Unknown — needs status update from Open Claw sessions

## jos-juce-plugins
- **Status:** active
- **Goal:** JUCE audio plugins with jos-modules subtree
- **Current:** Unknown — needs status update from plugin sessions

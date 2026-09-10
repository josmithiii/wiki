---
title: Project State
created: 2026-04-10
updated: 2026-09-08
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

## dafx26-wiki-ingestion
- **Status:** active (pass 1 and pass 2 complete)
- **Goal:** Ingest the selected DAFx26 papers (29th Int. Conf. on Digital Audio Effects, Cambridge MA, 1-4 Sept 2026) into the shared LLM wiki
- **Current (2026-09-08):** Pass 1 (catalog only) done. Sources at /l/dttd/DAFx26/ with the annotated bibliography at /l/dttd/DAFx26/README_JOS.md and pdftotext extractions in /l/dttd/DAFx26/txt/. Mapping:
  - **virtual_analog/** - NEW sub-wiki. 16 catalog entries (papers 16, 18, 26, 27, 28, 29, 30, 31, 32, 33, 37, 45, 47, 49, demos 60, 67) plus cross-references to the three WDF papers. One concept page, concepts/virtual-analog-overview.md.
  - **waveguide_synthesis/** - new entities/source-papers.md with 14 entries (papers 01, 04, 05, 10, 23, 24, 25, 36, 38, 39, 43, demos 61, 68, 71); DAFx26 pointers added to 6 concept pages.
  - **modal_synthesis/** - new entities/source-papers.md with 13 full entries (papers 03, 06, 11, 40, 41, demo 72, challenges 76, 77, 82, 83, 86, 87, 88) plus one-line entries for challenges 78-81, 84, 85, 89-91; DAFx26 pointers added to 4 concept pages and the waveguide-vs-modal comparison.
  - **spectral_processing/** - 4 entries appended to entities/source-papers.md (papers 02, 21, 34, 44) plus a cross-reference to paper 49; DAFx26 pointers added to 3 concept pages.
- **Pass 2 (2026-09-10):** deep distillation done by four parallel agents, one per sub-wiki; 37 new pages, all under 100 lines, LaTeX math, footnoted to the pass-1 catalog anchors. virtual_analog/ 15 pages (tpt-zdf-filters, time-varying-filter-stability, moog-ladder-filter-models, ladder-nonlinearity-ablation, allpass-clipping-prevention, antiderivative-antialiasing, polyadaa, alias-free-oscillator-sync, hasy-asic, real-time-neural-inference-deployment, mobile-gpu-neural-audio, neural-model-compression, state-space-circuit-solvers, neural-va-architectures, fourier-neural-operators-va); waveguide_synthesis/ 11 (fdn-kronecker-feedback-matrices, nonlinear-and-time-varying-fdn-effects, differentiable-fdn-design, differentiable-karplus-strong, differentiable-kelly-lochbaum-tract, loopback-fm-time-varying-delay, bowed-string-finite-difference-models, wdf-code-generation, circular-buffer-topology-monodromy, sffdn-library, polymap-pickup-system; papers 35 and demo 73 added to the catalog); modal_synthesis/ 7 (sav-nonlinear-string-with-measured-body, era-bridge-admittance-identification, corpus-driven-parametric-modal-reverb, state-space-models-as-modal-resonator-banks, modes-of-non-orientable-surfaces, plate-reverb-parameter-estimation-challenge, modal-pole-harvesting-from-irs); spectral_processing/ 4 (nonstationary-sinusoidal-estimation-ddm, giant-fft-group-delay-domain, extrema-sampling-time-stretch, linear-phase-octave-filter-bank-implementation).
- **Next:** none scheduled. Candidates: the two-star papers not yet distilled (24, 25, 32, 33, 37, 30, 06/12 room acoustics), and a home for the spatial-audio set (07, 08, 12, 13, 15, 48, demo 57).
- **Decided:** New virtual_analog sub-wiki rather than folding VA into waveguide_synthesis (2026-09-08); wave digital filters stay in waveguide_synthesis and are cross-linked.


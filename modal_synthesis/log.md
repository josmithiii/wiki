# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-04-09] create | Wiki initialized
- Domain: Physics-based synthesis using measured or computed modes of vibration
- Structure created: SCHEMA.md, index.md, log.md
- Directories: raw/{articles,papers,transcripts,assets}, entities/, concepts/, comparisons/, queries/

## [2026-04-09] create | concepts/modal-synthesis-overview.md
## [2026-04-09] create | concepts/mode-shapes-and-eigenvalues.md
## [2026-04-09] create | concepts/resonator-bank-implementation.md
## [2026-04-09] create | concepts/impact-synthesis.md
## [2026-04-09] create | concepts/friction-synthesis.md
## [2026-04-09] create | concepts/modal-analysis-measurement.md
## [2026-04-09] create | concepts/fem-bem-for-modal-synthesis.md
## [2026-04-09] create | concepts/rigid-body-sound-synthesis.md
## [2026-04-09] create | concepts/gpu-modal-synthesis.md
## [2026-04-09] create | concepts/material-properties-and-modes.md
## [2026-04-09] create | comparisons/waveguide-vs-modal.md
## [2026-04-09] create | entities/realimpact-dataset.md
## [2026-04-09] update | index.md — added 11 pages
## [2026-04-09] update | log.md — batch log of session 1

## [2026-04-10] create | concepts/damping-models.md
- Viscous (Rayleigh), thermoelastic (Zener), structural/hysteretic, power-law, per-mode fitted
- DSP pole placement, Q-factor, T60 formulas; comparison table

## [2026-04-10] create | concepts/excitation-signals.md
- Impulse, shaped impulse, noise burst, continuous (noise/sinusoidal/bow-force/Hertz)
- Modal coupling via phi_n(x_drive); summary table; cross-refs to impact/friction pages

## [2026-04-10] create | concepts/realtime-modal-synthesis.md
- CPU/GPU budget, SIMD, perceptual mode reduction, LOD, latency budget, parameter modulation
- Known implementations (Modal, PhysX Audio, Resonance Audio, Modus)

## [2026-04-10] update | index.md — added 3 pages (total 14)

## [2026-04-10] fix | 10 factual errors from TODO audit
- modal-synthesis-overview: Rath & Rocchesso CPU not GPU; added James 2006
- gpu-modal-synthesis: Cook & Scavone was PhISEM/STK; retitled CUDA→fragment shader
- realimpact-dataset: corrected authors (Clarke et al.), venue (ICCV 2023), arXiv
- resonator-bank-implementation: fixed state variable s2_k→s1_k
- realtime-modal-synthesis: typo fix
- damping-models: added descriptive text to [^1]
- rigid-body-sound-synthesis: removed unrelated wind noise ref
- friction-synthesis: full Serafin PhD citation
- waveguide-vs-modal: K-S as special case of Smith waveguide model

## [2026-04-10] ingest | PASP LaTeX + 12 PDFs + 1 arXiv
- /w/pasp/modal.tex — JOS modal synthesis chapter
- /w/pasp/damping.tex — JOS damping/frequency-dependent loss
- Poirot-Bilbao EURASIP 2024 — nonlinear mode coupling
- Bilbao DAFx23 — coupled nonlinear resonators
- Bilbao 2015 — numerical collision modeling
- Bilbao ISMA 2024 — string/barrier collisions
- Bilbao DAFx24 — real-time guitar synthesis
- van Walstijn DAFx23 — tunable collisions
- Bhanuprakash DAFx24 — quadratic spline collisions
- Lee et al. 2024 — differentiable modal synth for strings
- Clarke et al. CoRL 2021 — DiffImpact
- Diaz et al. ICASSP 2023 — DDSP rigid-body modal
- Jin et al. SIGGRAPH 2024 — DiffSound
- Curtu et al. — guitar body modal analysis
- Clarke et al. CVPR 2023 — RealImpact (arXiv:2306.09944)
- Note: arXiv:2206.05931 in TODO was wrong ID (math paper, not NeuralSound)

## [2026-04-10] create | concepts/nonlinear-modal-synthesis.md
- Mode coupling (Poirot-Bilbao), collision power-law (Bilbao), energy quadratisation
## [2026-04-10] create | concepts/coupled-structures.md
- String-bridge-body coupling, delay loop expansion, commuted synthesis, state-space
## [2026-04-10] create | concepts/ml-modal-parameter-estimation.md
- NeuralSound, DiffSound, DiffImpact, DDSP rigid-body, DMSP strings
## [2026-04-10] create | concepts/radiation-and-directivity.md
- Radiation efficiency, acoustic transfer, directivity, near/far field
## [2026-04-10] create | concepts/stochastic-modal-synthesis.md
- SEA, Schroeder frequency, noise-band synthesis, mode density

## [2026-04-10] update | sources fields on 12 existing pages
## [2026-04-10] update | index.md — added 5 pages (total 19)

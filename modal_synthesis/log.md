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

# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-04-14 | Total pages: 10 concepts + 9 pending entities

## Entities
*Stubs — one line per source in `raw/`. Distilled summaries live in `raw/SUMMARIES.md`;*
*proper entity pages under `entities/` are to be created on demand.*

### Published references
- [paper-widrow-adaptive-noise-cancelling](entities/paper-widrow-adaptive-noise-cancelling.md) `[pending]` — Widrow et al. 1975: LMS adaptive filter + noise-cancelling architecture, ECG / antenna demos
- [paper-wise-leventhall-lf-anc](entities/paper-wise-leventhall-lf-anc.md) `[pending]` — Wise & Leventhall 2010: coherence-bound tutorial for LF duct/room ANC
- [paper-zhang-wang-deep-anc](entities/paper-zhang-wang-deep-anc.md) `[pending]` — Zhang & Wang 2021: CRN learns anti-noise spectrogram, absorbs loudspeaker nonlinearity
- [paper-andersen-oticon-hearing-aids](entities/paper-andersen-oticon-hearing-aids.md) `[pending]` — Andersen et al. 2021 (Oticon): DL postfilter replaces spectral suppression in commercial HAs
- [paper-gaikwad-ai-hearing-aids](entities/paper-gaikwad-ai-hearing-aids.md) `[pending]` — Gaikwad 2021: CNN+attention hearing-aid ANC, claims 12 dB SNR / 45% intelligibility gain
- [paper-khan-selective-nc-review](entities/paper-khan-selective-nc-review.md) `[pending]` — Khan et al. 2025 review: NMF→Transformer for selective NC, 18.3 dB SI-SDR SOTA
- [paper-sarkar-latent-fxlms](entities/paper-sarkar-latent-fxlms.md) `[pending]` — Sarkar et al. 2025: FxLMS update in autoencoder latent space, mixup-trained decoder accelerates convergence at equal MSE

### Patents
- [paper-guerci-fan-anc-patent](entities/paper-guerci-fan-anc-patent.md) `[pending]` — US 5,448,645 (1995): bandpass-at-BPF + speaker array, early tonal fan canceller
- [paper-abali-fan-phase-cancellation-patent](entities/paper-abali-fan-phase-cancellation-patent.md) `[pending]` — US 7,282,873 (2007): cancel multi-fan noise by controlling inter-fan **mechanical** phase

## Concepts

### Classical adaptive filtering
- [lms-algorithm](concepts/lms-algorithm.md) — Widrow–Hoff LMS + adaptive noise-cancelling architecture (distilled from Widrow 1975)
- [fxlms-algorithm](concepts/fxlms-algorithm.md) — Filtered-x LMS: LMS with secondary-path compensation for feedforward ANC; includes Latent FxLMS variant

### AI-based ANC approaches *(project focus)*
- [ai-anc-overview](concepts/ai-anc-overview.md) — **Map of the territory**: 7 categories of AI in ANC; start here
- [deep-anc-crn](concepts/deep-anc-crn.md) — NN *replaces* the adaptive filter: Zhang & Wang 2021 CRN predicts anti-noise spectrogram end-to-end
- [neural-system-identification](concepts/neural-system-identification.md) — NN *guides* the filter: autoencoder-constrained adaptation (parent framework of Latent FxLMS)
- [meta-learning-anc](concepts/meta-learning-anc.md) — NN *is* the update rule: learned optimizer replaces FxLMS weight update
- [neural-secondary-path](concepts/neural-secondary-path.md) — NN *learns the plant*: online / implicit / NNSI-based secondary-path modeling `[stub]`
- [pinn-virtual-sensing](concepts/pinn-virtual-sensing.md) — NN *replaces the sensor*: Helmholtz-constrained neural fields for virtual error signals `[stub]`
- [deep-rl-anc](concepts/deep-rl-anc.md) — NN *replaces the controller*: deep RL policies for constrained ANC arrays `[stub]`
- [transformer-se-anc](concepts/transformer-se-anc.md) — Transformer / Conformer / Mamba architectures for SE and selective NC — transfer points to neural ANC

## Comparisons

## Queries

## Raw Sources
- `raw/` — text extractions of ANC papers/patents (pdf2txt from `/l/dttd/ANC-Stuff/`)
- `raw/MANIFEST.md` — text-file ↔ original-PDF mapping; also lists 3 internal project documents excluded from distillation
- `raw/SUMMARIES.md` — short distillation notes for every distilled source, keyed to entity pages above

## Pending ingestion
- **Morgan 1980** (IEEE TASSP) — original FxLMS filtered-x analysis; referenced by `concepts/fxlms-algorithm.md`
- **Burgess 1981** (JASA) — first full adaptive duct-ANC simulation; referenced by `concepts/fxlms-algorithm.md`

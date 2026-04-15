# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-04-14 | Total pages: 10 concepts + 21 pending entities

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

### AI-ANC ingestion batch (2026-04-14)
*Stubs for the 12 AI-ANC papers just distilled into `raw/SUMMARIES.md`; each will become an entity page on demand.*

#### NNSI / neural adaptive filtering
- [paper-helwani-nnsi](entities/paper-helwani-nnsi.md) `[pending]` — Helwani et al. ICASSP 2023: topology-aware VAE + retraction-based manifold optimization; parent framework of Latent FxLMS

#### PINN virtual sensing
- [paper-zhang-pinn-anc](entities/paper-zhang-pinn-anc.md) `[pending]` — Zhang et al. 2023: **canonical PINN-for-ANC**; 8 monitoring mics outside ROI, FxLMS on virtual error signals, −13 dB over multi-point
- [paper-piml-sound-field-survey](entities/paper-piml-sound-field-survey.md) `[pending]` — Koyama et al. IEEE SPM 2024: 5-category taxonomy of physics-informed ML for sound-field estimation
- [paper-olivieri-volumetric-pinn](entities/paper-olivieri-volumetric-pinn.md) `[pending]` — Olivieri et al. 2024: time-domain PINN volumetric reconstruction of *broadband* speech signals on MeshRIR
- [paper-borrel-1d-pinn](entities/paper-borrel-1d-pinn.md) `[pending]` — Borrel-Jensen et al. 2021: early 1-D PINN with parameterized moving sources and frequency-dependent impedance (historical)
- [paper-chen-deepset-pinn](entities/paper-chen-deepset-pinn.md) `[pending]` — Chen et al. 2025: deep-set PINN enforcing reciprocity by construction; region-to-region ATF interpolation
- [paper-bi-point-neuron](entities/paper-bi-point-neuron.md) `[pending]` — Bi & Abhayapala 2024: Green's-function neuron; Helmholtz satisfied by construction, no PDE loss

#### Meta-learning ANC
- [paper-feng-meta-delayless-anc](entities/paper-feng-meta-delayless-anc.md) `[pending]` — Feng & So 2024: complex self-attention RNN as learned FxLMS gradient; strongest match to Sarkar ref [5]
- [paper-xiao-meta-sfanc](entities/paper-xiao-meta-sfanc.md) `[pending]` — Xiao et al. 2025: MAML over SFANC filter bank + ResNet noise classifier on ESC-50
- [paper-yang-coinit-meta-anc](entities/paper-yang-coinit-meta-anc.md) `[pending]` — Yang et al. 2026: joint MAML of control filter **and** secondary-path FIR; runtime algorithm unchanged (pure initialization)

#### Deep ANC / generative
- [paper-dai-speech-preserving-anc](entities/paper-dai-speech-preserving-anc.md) `[pending]` — Dai (thesis, Gan adv.) 2026: CRN + speech-preservation loss in reverberant environments
- [paper-luo-gfanc](entities/paper-luo-gfanc.md) `[pending]` — Luo et al. 2023: 1-D CNN outputs binary sub-filter selector; "generative fixed-filter" ANC

*(DRL-Control-Survey-2507.08196.txt is **not** promoted to an entity page — it contains no ANC content and is cited inline in `concepts/deep-rl-anc.md` as a general-DRL background reference only.)*

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

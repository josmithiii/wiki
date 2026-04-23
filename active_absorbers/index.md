# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-04-22 | Concepts: 15 · Source papers in catalog: 45

## Entities

All distilled source papers live in a single catalog —
[entities/source-papers.md](entities/source-papers.md) — with one section
per paper keyed by the slug used in the links below. If a single paper
later needs a standalone page (more depth than a bullet summary supports),
promote it to `entities/paper-<slug>.md` and leave the catalog entry as a
cross-link.

### Published references

- [paper-widrow-adaptive-noise-cancelling](entities/source-papers.md#paper-widrow-adaptive-noise-cancelling) — Widrow et al. 1975: LMS adaptive filter + noise-cancelling architecture, ECG / antenna demos
- [paper-wise-leventhall-lf-anc](entities/source-papers.md#paper-wise-leventhall-lf-anc) — Wise & Leventhall 2010: coherence-bound tutorial for LF duct/room ANC
- [paper-zhang-wang-deep-anc](entities/source-papers.md#paper-zhang-wang-deep-anc) — Zhang & Wang 2021: CRN learns anti-noise spectrogram, absorbs loudspeaker nonlinearity
- [paper-andersen-oticon-hearing-aids](entities/source-papers.md#paper-andersen-oticon-hearing-aids) — Andersen et al. 2021 (Oticon): DL postfilter replaces spectral suppression in commercial HAs
- [paper-gaikwad-ai-hearing-aids](entities/source-papers.md#paper-gaikwad-ai-hearing-aids) — Gaikwad 2021: CNN+attention hearing-aid ANC, claims 12 dB SNR / 45% intelligibility gain
- [paper-khan-selective-nc-review](entities/source-papers.md#paper-khan-selective-nc-review) — Khan et al. 2025 review: NMF→Transformer for selective NC, 18.3 dB SI-SDR SOTA
- [paper-sarkar-latent-fxlms](entities/source-papers.md#paper-sarkar-latent-fxlms) — Sarkar et al. 2025: FxLMS update in autoencoder latent space, mixup-trained decoder accelerates convergence at equal MSE

### Patents

- [paper-guerci-fan-anc-patent](entities/source-papers.md#paper-guerci-fan-anc-patent) — US 5,448,645 (1995): bandpass-at-BPF + speaker array, early tonal fan canceller
- [paper-abali-fan-phase-cancellation-patent](entities/source-papers.md#paper-abali-fan-phase-cancellation-patent) — US 7,282,873 (2007): cancel multi-fan noise by controlling inter-fan **mechanical** phase

### AI-ANC ingestion batch (2026-04-14)

*12 papers distilled into [source-papers.md](entities/source-papers.md).*

#### NNSI / neural adaptive filtering

- [paper-helwani-nnsi](entities/source-papers.md#paper-helwani-nnsi) — Helwani et al. ICASSP 2023: topology-aware VAE + retraction-based manifold optimization; parent framework of Latent FxLMS

#### PINN virtual sensing

- [paper-zhang-pinn-anc](entities/source-papers.md#paper-zhang-pinn-anc) — Zhang et al. 2023: **canonical PINN-for-ANC**; 8 monitoring mics outside ROI, FxLMS on virtual error signals, −13 dB over multi-point
- [paper-piml-sound-field-survey](entities/source-papers.md#paper-piml-sound-field-survey) — Koyama et al. IEEE SPM 2024: 5-category taxonomy of physics-informed ML for sound-field estimation
- [paper-olivieri-volumetric-pinn](entities/source-papers.md#paper-olivieri-volumetric-pinn) — Olivieri et al. 2024: time-domain PINN volumetric reconstruction of *broadband* speech signals on MeshRIR
- [paper-borrel-1d-pinn](entities/source-papers.md#paper-borrel-1d-pinn) — Borrel-Jensen et al. 2021: early 1-D PINN with parameterized moving sources and frequency-dependent impedance (historical)
- [paper-chen-deepset-pinn](entities/source-papers.md#paper-chen-deepset-pinn) — Chen et al. 2025: deep-set PINN enforcing reciprocity by construction; region-to-region ATF interpolation
- [paper-bi-point-neuron](entities/source-papers.md#paper-bi-point-neuron) — Bi & Abhayapala 2024: Green's-function neuron; Helmholtz satisfied by construction, no PDE loss

#### Meta-learning ANC

- [paper-feng-meta-delayless-anc](entities/source-papers.md#paper-feng-meta-delayless-anc) — Feng & So 2024: complex self-attention RNN as learned FxLMS gradient; strongest match to Sarkar ref [5]
- [paper-xiao-meta-sfanc](entities/source-papers.md#paper-xiao-meta-sfanc) — Xiao et al. 2025: MAML over SFANC filter bank + ResNet noise classifier on ESC-50
- [paper-yang-coinit-meta-anc](entities/source-papers.md#paper-yang-coinit-meta-anc) — Yang et al. 2026: joint MAML of control filter **and** secondary-path FIR; runtime algorithm unchanged (pure initialization)

#### Deep ANC / generative

- [paper-dai-speech-preserving-anc](entities/source-papers.md#paper-dai-speech-preserving-anc) — Dai (thesis, Gan adv.) 2026: CRN + speech-preservation loss in reverberant environments
- [paper-luo-gfanc](entities/source-papers.md#paper-luo-gfanc) — Luo et al. 2023: 1-D CNN outputs binary sub-filter selector; "generative fixed-filter" ANC (supervised precursor to GFANC-RL)

*(`DRL-Control-Survey-2507.08196.txt` is intentionally **not** in the catalog — it contains no ANC content and is cited inline in [[deep-rl-anc]] as a general-DRL background reference only.)*

### DRL-ANC ingestion batch (2026-04-15)

*Four new papers: 2 genuine DRL-ANC, 1 metric-learning virtual sensing, 1 comprehensive 2023 review.*

- [paper-luo-gfanc-rl](entities/source-papers.md#paper-luo-gfanc-rl) — Luo et al. *Neural Networks* 2024: SAC over $M{=}15$ binary sub-filter selection; 7–9 dB over FxLMS on real noise; $\gamma{=}0$ so effectively contextual bandit
- [paper-li-rl-secondary-path](entities/source-papers.md#paper-li-rl-secondary-path) — Li, Wu, Bai *AIP Advances* 2025: PPO/DDPG/DQN/GRPO head-to-head on nonlinear $\hat{S}(z)$ ID; closed-loop on real ZSL-92 armored vehicle; GRPO wins
- [paper-wang-metric-vs](entities/source-papers.md#paper-wang-metric-vs) — Wang et al. 2024: cosine-similarity classifier over pre-trained auxiliary filters; 92.6% cross-system transfer without conv-layer retraining
- [paper-shi-anc-review-2023](entities/source-papers.md#paper-shi-anc-review-2023) — Shi, Lam, Gan, Cheer, Elliott *IEEE SPM* 2023: canonical modern classical-ANC review; no DRL/PINN coverage (use as 2023 snapshot only)

### Classical ANC reviews batch (2026-04-16)

*Two foundational review/tutorial papers covering 1999–2020 classical ANC.*

- [paper-kuo-morgan-anc-tutorial-1999](entities/source-papers.md#paper-kuo-morgan-anc-tutorial-1999) — Kuo & Morgan *Proc. IEEE* 1999: **the** canonical ANC tutorial; FxLMS derivation, secondary-path modeling, multichannel, duct/automotive/headphone applications
- [paper-lu-anc-survey-part1-2021](entities/source-papers.md#paper-lu-anc-survey-part1-2021) — Lu et al. *Signal Processing* 2021: decade survey (2009–2020) of linear ANC; FxLMS/FeLMS/FuLMS families, 21 online secondary-path methods, selective ANC precursor to SFANC/GFANC, distributed ANC
- [paper-lu-anc-survey-part2-2021](entities/source-papers.md#paper-lu-anc-survey-part2-2021) — Lu et al. *Signal Processing* 2021: decade survey (2009–2020) of **nonlinear ANC**; Volterra/FLANN/Hammerstein/bilinear/spline/kernel algorithms, GA/PSO/BFO heuristics, fMRI/headphone/vehicle/transformer applications

### Classical ANC & hybrid-absorber batch (2026-04-17)

*Nine free-to-download papers promoting the 2026-04-17 scaffold concept pages.*

#### Tonal / periodic ANC

- [paper-elliott-nelson-spm-1993](entities/source-papers.md#paper-elliott-nelson-spm-1993) — Elliott & Nelson *IEEE SPM* 1993: canonical ANC tutorial; Lueg/Olson-May/Conover history, three acoustic objectives, ±0.6 dB / ±5° precision benchmark for 20 dB tonal reduction
- [paper-ardekani-fxlms-quickreview](entities/source-papers.md#paper-ardekani-fxlms-quickreview) — Ardekani & Abdulla *APSIPA 2011*: FxLMS quick review; **exact** sinusoidal-input convergence analysis

#### Hybrid active-passive absorbers

- [paper-galland-hybrid-flowduct-2005](entities/source-papers.md#paper-galland-hybrid-flowduct-2005) — Galland, Mazeaud & Sellen *Appl. Acoust.* 2005: 5-step flow-duct hybrid-liner design; cell-by-cell feedback FxLMS; piezo + wire-mesh <0.03 m cells
- [paper-betgen-galland-hybrid-liner-2012](entities/source-papers.md#paper-betgen-galland-hybrid-liner-2012) — Betgen, Galland, Piot & Simon *Appl. Acoust.* 2012: basic vs complex hybrid cells; LDV non-intrusive characterization with grazing flow; TL up to 20 dB
- [paper-guicking-patents-overview](entities/source-papers.md#paper-guicking-patents-overview) — Guicking 2009: overview of ~1740 ANVC patent families in 17 sections (incl. §8.2 fan/turbine); patent-landscape reference
- [paper-mei-dark-metamaterial-2012](entities/source-papers.md#paper-mei-dark-metamaterial-2012) — Mei et al. *Nat. Commun.* 2012: dark acoustic metamaterial; near-unity LF absorption with 200 µm membrane, λ/t ≳ 10³
- [paper-wu-ventilated-metamaterial-2018](entities/source-papers.md#paper-wu-ventilated-metamaterial-2018) — Wu et al. arXiv 1801.03613: split-tube ventilated metamaterial; >90% absorption <500 Hz with airflow preserved
- [paper-ma-sheng-metamaterials-review-2016](entities/source-papers.md#paper-ma-sheng-metamaterials-review-2016) — Ma & Sheng *Sci. Adv.* 2016: 15-year acoustic-metamaterials review; bridge to active/tunable variants

#### Psychoacoustic ANC

- [paper-rivera-psychoacoustic-hybrid-anc-2018](entities/source-papers.md#paper-rivera-psychoacoustic-hybrid-anc-2018) — Rivera Benois, Papantoni & Zölzer *ICSV25* 2018: hybrid FeLMS-psy (ITU-R 468) + MVC feedback; FPGA headphone prototype; Zwicker/Aures metric evaluation

### NASA NTRS + classical-ANC batch (2026-04-18)

*Eight papers: NASA NTRS trio (Brooks airfoil self-noise + Sutliff ANC + ANCF 20-year retrospective), Bodson-group adaptive periodic-disturbance pair, Guicking bilingual ANVC overview, and one renamed metamaterials review.*

#### NASA fan-noise literature (promotes [[rooftop-fan-contenders]] from scaffold)

- [paper-brooks-pope-marcolini-airfoil-selfnoise-1989](entities/source-papers.md#paper-brooks-pope-marcolini-airfoil-selfnoise-1989) — Brooks, Pope, Marcolini *NASA RP-1218* 1989: canonical BPM airfoil self-noise; 5 mechanisms on NACA 0012 setting broadband floor for tonal-ANC analyses
- [paper-sutliff-ancf-ge-anc-1997](entities/source-papers.md#paper-sutliff-ancf-ge-anc-1997) — Sutliff, Hu, Pla, Heidelberg *NASA TM-107458 / AIAA-97-1641* 1997: first full modal-control ANC on 48-inch ANCF — (6,0) eliminated at 920 Hz, 9.4 dB 2BPF farfield PWL reduction
- [paper-sutliff-ancf-20yr-retrospective-2019](entities/source-papers.md#paper-sutliff-ancf-20yr-retrospective-2019) — Sutliff *AIAA* 2019: ANCF 1994–2016 history, ~100 publications, Rotating Rake + CFANS, HQ-tubes & Over-the-Rotor Foam Metal Liner path to flight

#### Adaptive periodic-disturbance rejection (extends [[tonal-periodic-anc]] §3)

- [paper-bodson-douglas-sinusoidal-rejection](entities/source-papers.md#paper-bodson-douglas-sinusoidal-rejection) — Bodson & Douglas *Automatica* 1997: indirect vs direct PLL-style adaptive algorithms for unknown-frequency sinusoidal disturbance
- [paper-bodson-jensen-douglas-anc-periodic](entities/source-papers.md#paper-bodson-jensen-douglas-anc-periodic) — Bodson, Jensen, Douglas *IEEE TCST* 2001: multi-harmonic extension with integer-tied frequency estimates; single-mic feedback ANC validated on testbed

#### ANVC overview pair

- [paper-guicking-anvc-overview](entities/source-papers.md#paper-guicking-anvc-overview) — Guicking 2008 bilingual overview of *Active Control of Sound and Vibration*: ANC+AVC+flow-control history, JMC theory, algorithms, active-impedance thread from his own Göttingen group (closest open-access coverage of Guicking & Karcher 1984)

#### Metamaterials (renamed)

- [paper-song-acoustic-metamaterials-review-2021](entities/source-papers.md#paper-song-acoustic-metamaterials-review-2021) — Song, Ding, Cui, Hu *Molecules* 2021: acoustic-metamaterials review by meta-atom / meta-molecule taxonomy (staged as "Fang-2006" by mistake; renamed 2026-04-18 — Fang 2006 primary paper remains pending)

### Community-health / LFN perception batch (2026-04-22)

*Singleton: first community-health / exposure-response paper in the wiki — motivation reference, not ANC methods.*

- [paper-erdelyi-lfn-perceptions-2023](entities/source-papers.md#paper-erdelyi-lfn-perceptions-2023) — Erdélyi et al. *IJERPH* 2023: Dutch survey of $n{=}190$ LFN perceivers; ventilation is the #1 assumed source, impact averages $7.1/10$, passive mitigation unsuccessful for 72–86%. Empirical "why bother" anchor for [[rooftop-fan-contenders]] and [[psychoacoustic-anc]].

## Concepts

### Classical adaptive filtering

- [classical-anc-overview](concepts/classical-anc-overview.md) — **Map of the territory**: all classical (non-AI) ANC methods — linear/nonlinear algorithms, heuristic optimization, control topologies, secondary-path modeling, applications, hardware; companion to ai-anc-overview
- [lms-algorithm](concepts/lms-algorithm.md) — Widrow–Hoff LMS + adaptive noise-cancelling architecture (distilled from Widrow 1975)
- [fxlms-algorithm](concepts/fxlms-algorithm.md) — Filtered-x LMS: LMS with secondary-path compensation for feedforward ANC; includes Latent FxLMS variant

### Rooftop-fan / tonal ANC *(project focus)*

- [tonal-periodic-anc](concepts/tonal-periodic-anc.md) — **BPF-tonal ANC**: tacho-referenced synchronous reference, FxLMS-SF, adaptive notch, RC/ILC, harmonic bank — the narrowband specialization for rotating machinery; sourced from Elliott-Nelson 1993, Ardekani-Abdulla 2011
- [hybrid-active-passive](concepts/hybrid-active-passive.md) — **Hybrid absorbers**: active impedance control, Galland/Betgen active duct liners, Mei/Wu/Ma-Sheng metamaterials (including ventilated), semi-active Helmholtz, tunable piezo
- [psychoacoustic-anc](concepts/psychoacoustic-anc.md) — **Perceptual ANC**: tonality penalty (ISO/DIN), loudness-weighted cost, tonal-to-broadband reshaping, Rivera/Zölzer ITU-R 468 hybrid, differentiable perceptual losses
- [rooftop-fan-contenders](concepts/rooftop-fan-contenders.md) — **Pointer page**: out-of-scope contenders (source mods, staggered RPM, passive absorbers, metamaterials, silencers) mapped to in-wiki active methods; now includes §4.5 NASA fan-noise literature distilled from the Brooks 1989 / Sutliff 1997 / Sutliff 2019 NTRS trio

### AI-based ANC approaches *(project focus)*

- [ai-anc-overview](concepts/ai-anc-overview.md) — **Map of the territory**: 7 categories of AI in ANC; start here
- [deep-anc-crn](concepts/deep-anc-crn.md) — NN *replaces* the adaptive filter: Zhang & Wang 2021 CRN + Dai 2026 speech-preserving reverberant follow-up
- [neural-system-identification](concepts/neural-system-identification.md) — NN *guides* the filter: Helwani 2023 topology-aware VAE + retraction, parent framework of Latent FxLMS
- [meta-learning-anc](concepts/meta-learning-anc.md) — NN *is* the update rule: Feng & So 2024 attention-RNN gradient predictor + Xiao 2025 MAML-SFANC + Yang 2026 co-init
- [neural-secondary-path](concepts/neural-secondary-path.md) — NN *learns the plant*: implicit (Deep ANC) + meta-learned FIR init (Yang 2026) + RL plant-ID (Li/Wu/Bai 2025)
- [pinn-virtual-sensing](concepts/pinn-virtual-sensing.md) — NN *replaces the sensor*: Zhang 2023 canonical PINN-ANC + 5 supporting PINN papers + Wang 2024 metric-learning alternative
- [deep-rl-anc](concepts/deep-rl-anc.md) — NN *replaces the controller*: GFANC-RL (SAC over binary filter selection) + Li/Wu/Bai PPO/DDPG/DQN/GRPO plant-ID benchmark; continuous-drive DRL still open
- [transformer-se-anc](concepts/transformer-se-anc.md) — Transformer / Conformer / Mamba architectures for SE and selective NC — transfer points to neural ANC

## Comparisons

## Queries

## Raw Sources

- `raw/` — text extractions of ANC papers/patents (pdf2txt from `/l/dttd/ANC-Stuff/`); gitignored
- `raw/MANIFEST.md` — text-file ↔ original-PDF mapping; also lists 3 internal project documents excluded from distillation
- `raw/SUMMARIES.md` — working-notes form of the catalog; entities/source-papers.md is the published version

## Pending ingestion

See [pending-sources.md](pending-sources.md) — consolidated wishlist of
paywalled / book / standards / NASA NTRS references we still want to
track down, grouped by the concept page that needs them. Contributors
welcome.

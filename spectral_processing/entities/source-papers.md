---
title: Source Papers -- Distilled Catalog
created: 2026-05-04
updated: 2026-09-08
type: entity
tags: [reference, phase-vocoder, tsm]
sources:
  - spectral_processing/raw/Improved_phase_vocoder_time-scale_modification_of_audio.txt
  - /l/dttd/Improved_phase_vocoder_time-scale_modification_of_audio.pdf
  - https://doi.org/10.1109/89.759041
  - /l/dttd/DAFx26/DAFx26_paper_02.pdf
  - /l/dttd/DAFx26/DAFx26_paper_21.pdf
  - /l/dttd/DAFx26/DAFx26_paper_34.pdf
  - /l/dttd/DAFx26/DAFx26_paper_44.pdf
  - /l/dttd/DAFx26/README_JOS.md
---

# Source Papers -- Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>` ID
used in `index.md`, so inbound links like
`[paper-laroche-dolson-improved-pv-1999](entities/source-papers.md#paper-laroche-dolson-improved-pv-1999)`
resolve inside this page. Blocks are distilled from text extractions in `raw/`
(gitignored); see `raw/MANIFEST.md` for the filename-to-PDF mapping.

When any single paper needs deeper treatment than the bullet summary supports,
promote it to a dedicated `entities/paper-<slug>.md` file and leave the section
here as a cross-link.

---

## Phase-vocoder TSM references

### paper-laroche-dolson-improved-pv-1999

**"Improved Phase Vocoder Time-Scale Modification of Audio"** -- Jean Laroche & Mark Dolson · *IEEE Transactions on Speech and Audio Processing* 7(3):323-332, May 1999 · DOI [10.1109/89.759041](https://doi.org/10.1109/89.759041) · `raw/Improved_phase_vocoder_time-scale_modification_of_audio.txt` · distilled at [[phase-vocoder-and-tsm]]

- Canonical paper explaining why classical phase-vocoder TSM sounds "phasy": standard bin-wise phase propagation preserves **horizontal** coherence over time but can destroy **vertical** coherence across neighboring STFT channels.
- Phase analysis shows that synthesis phases depend on current analysis phase, initial phase, time-scale factor, and accumulated phase-unwrapping integers. Integer factors can avoid the problem with the right initial phases; noninteger factors usually accumulate cross-bin phase errors when sinusoids cross bins or bins are temporarily noise-dominated.
- Introduces an STFT consistency measure adapted from Griffin-Lim. Useful diagnostic, but not a full perceptual predictor: PSOLA can score worse yet sound less reverberant on monophonic speech.
- Reviews two older alternatives: magnitude-only reconstruction avoids phase-unwrapping errors but is too iterative for real-time use; Puckette loose phase locking is cheap but signal-dependent.
- **Identity phase locking:** detect spectral peaks, propagate only peak-bin phases, and rotate the surrounding region of influence so synthesis-bin phase offsets match the analysis-frame offsets.
- **Scaled phase locking:** track corresponding peaks between frames and scale local offsets, improving perceived naturalness over identity locking in the authors' informal listening tests.
- Important implementation payoff: peak-only unwrapping makes 50% overlap practical for Hann/Hamming windows instead of the usual 75%, giving at least a factor-of-two cost reduction.
- Caveats: phase locking does not solve transient smearing, chirp-dependent magnitude reshaping, or harmonic shape-invariance; PSOLA remains better for monophonic pitched speech.
- Tags: phase-vocoder, tsm, stft, phase-unwrap, modifications, reference

---

## DAFx26 (Cambridge MA, 1-4 September 2026)

Pass-1 catalog entries: bullets seeded from the annotated bibliography at
`/l/dttd/DAFx26/README_JOS.md` plus the abstract and opening sections of each
paper. Extractions are in `raw/`; see `raw/MANIFEST.md`.

### paper-caetano-ddm-polynomial-amfm-2026

**"Using the Distribution Derivative Method to Model Acoustic Musical Instrument Sounds with Polynomial AM-FM Sinusoids"** -- Marcelo Caetano (UC San Diego) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_34.txt`

- Problem: quasi-stationary sinusoidal modeling is a solved problem, but **nonstationary** oscillations - above all attack transients - are still modeled poorly, which is exactly where sinusoidal models sound wrong.
- Model: **polynomial modulation sinusoids** (PMS), in which log-amplitude and phase are both polynomials in $t$ within the analysis frame, so amplitude and frequency modulation inside a frame are represented explicitly rather than assumed constant or linear.
- Estimator: the **distribution derivative method** (DDM), which gives accurate parameter estimates for PMS of arbitrary polynomial order - the generalization of the reassignment/derivative family beyond the linear-chirp case handled in [[gaussian-and-chirp-windows]].
- Evaluation: **39 musical instrument sounds**, compared objectively against the standard sinusoidal model (SM+) and the adaptive quasi-harmonic model **eaQHM** using time- and frequency-domain error measures; DDM captures more oscillatory energy than either.
- Perceptual result: a **MUSHRA** listening test on 18 selected sounds finds DDM higher quality than SM+ and eaQHM, and **almost perceptually indistinguishable from the originals**.
- Bears directly on [[sinusoidal-modeling]], [[sinusoidal-parameter-interpolation]] (intra-frame modulation replaces cubic-phase interpolation between frames) and [[sms-sines-plus-noise]] (a better deterministic part leaves a smaller residual).
- Limitation: higher polynomial order means more parameters per partial per frame; the paper does not report a rate/quality trade-off against the extra cost.
- Tags: sinusoidal, qifft, peak-detection, sms, residual, gauss, stft, reference

### paper-apel-giant-fft-group-delay-2026

**"Group Delay Manipulation for Creative Sound Transformation with the Giant FFT"** -- Ted Apel (Boise State University) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_02.txt`

- The **Giant FFT** is a single DFT spanning an entire audio file, so one spectrum encodes the whole temporal evolution of the sound - no windowing, no hop size.
- Problem with existing Giant-FFT effects: manipulating magnitude or phase disrupts the relationships *between* frequency bins, smearing discrete events into sustained textures.
- Framework: work in the **group-delay domain**, $\tau_g(\omega) = -\,d\phi/d\omega$, which makes the temporal center of gravity of spectral energy explicit at every bin.
- Method: identify spectral regions around amplitude peaks, **group them by group-delay similarity**, and displace whole features in time by uniformly modifying the group delay of a group.
- Demonstrations: reordering melodic events in synthetic and acoustic melodies, amplitude-proportional spectral displacement, and group-delay modulation to create temporal copies of spectral features - coherent temporal manipulation **without windowed analysis**.
- Complements the windowed view in [[short-time-fourier-transform]] and [[stft-modifications]]; follows Valimaki et al.'s recent zero-phase Giant-FFT study.
- Limitation: whole-file, non-real-time by construction; grouping heuristics are creative tools rather than a validated event segmentation.
- Tags: fft, dft, phase-unwrap, modifications, applications, stft

### paper-nielsen-keyframe-extrema-tsm-2026

**"Keyframe Time Stretching via Extrema Sampling"** -- Matthew Nielsen (independent, Portland) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_21.txt`

- Target: time-scale modification on **low-power embedded hardware**, where the FFT of a phase vocoder or the cross-correlation of WSOLA is too expensive.
- Idea: reduce a uniformly sampled signal to a set of **timestamped local extrema** - a sparse representation in which the spacing between points directly encodes local information density (roughly, local bandwidth), for free.
- Method: a content-adaptive OLA in which the **crossfade duration is driven by the extrema density**, sample by sample, instead of being a fixed compromise between transients and sustained sounds.
- Cost: about an **order of magnitude cheaper** than PV or WSOLA; dominant artifacts are added saturation and some spectral contrast loss rather than the phasiness of [[phase-vocoder-and-tsm]].
- Evaluated against OLA, WSOLA and PV with objective metrics and a listening test; preserves transients across a wide range of stretch ratios and handles dense layered material coherently.
- Cites the zero-crossing/extrema reconstruction literature; a nice counterpoint to the phase-locking machinery of [[entities/source-papers#paper-laroche-dolson-improved-pv-1999]].
- Limitation: spectral detail is traded away deliberately; no pitch-shifting or formant control is claimed.
- Tags: tsm, ola, modifications, applications, reference

### paper-badia-octave-filter-bank-parallelism-2026

**"Exploring Parallelism and Energy Efficiency in a Multistage Linear-Phase Octave Filter Bank"** -- Jose M. Badia (Universitat Jaume I), Jose A. Belloch (Universidad Carlos III), Vesa Valimaki (Aalto University) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_44.txt`

- Structure: a **multistage linear-phase octave filter bank** built from a cascade of **stretched (IFIR-style) FIR stages** with complementary band splitting, which preserves linear phase across all outputs - see [[multirate-filter-banks]] and the FIR design material in [[window-design-methods]].
- Problem: mapping such cascades onto embedded multicore CPUs raises state management, task synchronization, memory-traffic and energy issues that block-based edge audio makes acute.
- Method: first a **cache-friendly sequential realization** using a blocked streaming schedule and compact circular state; then a parallel design as an **OpenMP task pipeline with explicit dependencies**, which preserves filter-bank semantics without fine-grained synchronization inside the filtering tasks.
- Results on an **NVIDIA Jetson Orin Nano**: the optimized sequential version already sustains more than **1.18 M samples/s**, and the task pipeline reaches speedups above **4.5x** for suitable block sizes.
- Key finding: a clear **throughput-versus-power trade-off** - the most energy-efficient operating point is *not* the maximum-performance one on multicore edge SoCs.
- Limitation: one SoC, one filter-bank structure; no perceptual or filter-design contribution, it is an implementation study.
- Tags: filter-banks, multirate, fir-design, applications, downsampling

### Cross-references to other sub-wikis

- **Alias-Free Oscillator Synchronization via Additive Synthesis** (Roth, Keller, Castaneda, Studer, ETH Zurich) belongs to the sinusoidal/additive family - it maps the Fourier-series coefficients of a bandlimited free-running waveform to those of the synchronized waveform by a linear spectral-resampling transform, and realizes it on a 65 nm ASIC. Catalogued in the virtual analog wiki: [[virtual_analog/entities/source-papers#paper-roth-alias-free-oscillator-sync-2026]]

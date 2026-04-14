---
title: AI-Based Approaches to Active Noise Control (Overview)
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, comparison, tutorial, reference, fxlms, secondary-path]
sources:
  - raw/DeepANC-nihms-1690502.txt
  - raw/LatentFxLMS-2507.03854v1.txt
  - raw/DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt
  - raw/DeepLearningHearingAids-10-1055-s-0041-1735134.txt
---

# AI-Based Approaches to Active Noise Control

This is the **map of the territory** for the research project. Every AI-flavored
method for ANC (or closely adjacent tasks like selective noise cancellation and
acoustic system identification) gets one block here, even if we don't yet have a
primary source in `raw/`. Pages marked "dedicated page" have their own concept
file with deeper treatment; pages marked `[stub]` have a concept file with a
sources-pending marker; pages marked `[in raw/]` are documented only in
`raw/SUMMARIES.md` until we create a dedicated concept page.

The organizing axis is **where the neural network sits in the ANC loop**, not
the architecture family. The same CNN/Transformer/VAE can show up in multiple
rows with very different roles.

## 1. NN *replaces* the adaptive filter (end-to-end mapping)

The network consumes the reference (and possibly the error) and directly outputs
the anti-noise signal — no FxLMS loop, no explicit $\hat{S}(z)$.

- **Deep ANC (CRN-based)** — Zhang & Wang 2021. Convolutional recurrent net
  predicts the real/imag spectrogram of the anti-noise waveform from the
  reference; trained multi-condition; implicitly absorbs loudspeaker
  nonlinearity and secondary-path dynamics. Delay-compensated training
  enforces causality.
  → dedicated page: [[deep-anc-crn]]
- **Early shallow-NN ANC** — Sicuranza & Carini and related 1990s/2000s work
  replacing the FIR adaptive filter with a small MLP to handle mild actuator
  nonlinearity. Historical. See refs [11–13] of Sarkar et al. 2025.
  `[stub-history]`
- **Transformer-based speech enhancement / selective cancellation** —
  attention-based time-frequency masking; dominant paradigm in hearing-aid /
  SE work. Khan et al. 2025 reports ~18.3 dB SI-SDR on reverberant benchmarks.
  Most of this literature is open-loop SE, not closed-loop ANC — but the
  acoustic-scene models transfer.
  → dedicated page: [[transformer-se-anc]]

## 2. NN *guides* the adaptive filter (gradient / weight updates)

The FxLMS (or RLS/Kalman) adaptive loop is kept; a network produces or
constrains the weight updates.

- **Latent FxLMS** — Sarkar et al. 2025. Autoencoder over converged FxLMS
  weight vectors; online gradient step runs in the decoder's *latent space*;
  mixup-trained decoder + latent-normalized updates give faster convergence at
  equal steady-state MSE. Currently documented as a variant on [[fxlms-algorithm]].
  `[in raw/]` (has footnote in fxlms-algorithm.md)
- **Neural network system identification (NNSI) / generative manifold
  learning** — Helwani, Smaragdis, Goodwin (ICASSP 2023) and follow-ups.
  Topologically aware VAE for impulse responses used to accelerate RLS and
  Kalman-filter-based acoustic echo cancellation. Parent framework for
  Latent FxLMS.
  → dedicated page: [[neural-system-identification]]
- **Meta-learning weight-update predictors** — a network is trained to output
  the adaptive filter's weight gradient given current state, so online the
  adaptive filter learns *faster than* ordinary LMS. Referenced as [5] in
  Sarkar et al. 2025.
  → dedicated page: [[meta-learning-anc]]

## 3. NN *learns the secondary path* (plant model)

Instead of the classical offline white-noise $\hat{S}(z)$ identification,
a network continually adapts the secondary-path model from operational data.

- **Online neural secondary-path identification** — MLP/RNN adapts $\hat{S}$ on
  the fly as outdoor conditions drift (temperature, wind, humidity). No probe
  noise needed. Also supported by the CRN approach of Zhang & Wang, which
  implicitly folds $S(z)$ into the learned mapping.
  `[stub]` → [[neural-secondary-path]]

## 4. NN *replaces the sensor* (virtual sensing)

Where you cannot place an error microphone at the "quiet zone" of interest,
a network estimates the pressure field there from sparse available mics.

- **PINN virtual sensing** — physics-informed neural field representing $p(\mathbf{r},t)$
  with a Helmholtz-equation residual in the loss; sparse mics supply boundary
  conditions; the network's evaluation at the target point feeds the virtual
  error signal into an otherwise-classical FxLMS loop.
  → dedicated page: [[pinn-virtual-sensing]]

## 5. NN *replaces the control policy* (reinforcement learning)

Sidesteps the LMS formulation entirely: learn a policy $\pi(\mathbf{a}\mid\mathbf{o})$
mapping sensor observations to actuator drives, with a reward that encodes
reduction at the target *and* any hard constraints (e.g. radiation-shaping,
comfort bounds).

- **Deep RL for constrained ANC arrays** — handles actuator nonlinearity,
  hard directional constraints, and non-differentiable rewards; can discover
  non-obvious strategies (ground reflection, edge diffraction) that FxLMS
  cannot represent. Sample-efficiency and sim-to-real transfer remain open.
  → dedicated page: [[deep-rl-anc]]

## 6. NN *postprocesses* the residual (hybrid spectral suppression)

For hearing-aid / headphone use, a DL postfilter replaces the classical
Wiener/spectral-subtraction stage after an adaptive beamformer or ANC loop.

- **DL postfilter in commercial hearing aids** — Andersen et al. 2021
  (Oticon); the beamformer (MVDR/GSC) is kept, the postfilter is a network
  trained on speech/noise pairs. Clinical intelligibility gains reported.
  `[in raw/]` (see `DeepLearningHearingAids-10-1055-s-0041-1735134.txt`)
- **Gaikwad CNN+attention hearing-aid ANC** — low-power CNN used as the
  single-channel NR stage; claims 12 dB SNR / 45% intelligibility over
  MVDR/MWF baselines.
  `[in raw/]`

## 7. Cross-cutting tooling (not a row but worth tracking)

- **Generative noise-corpus models** for training augmentation (diffusion /
  flow-matching acoustic scene generators).
- **Differentiable DSP layers** that embed a real FxLMS or Wiener update
  inside a neural training graph, so the surrounding network can learn to
  configure a classical ANC loop.
- **Interpretable / uncertainty-aware ANC** — e.g. Bayesian neural nets for
  secondary-path estimation with confidence bounds.

These are not yet represented in `raw/` and will become `[stub]` pages as
soon as we have a primary source.

## Reading map

- For **end-to-end neural ANC** in depth, start at [[deep-anc-crn]].
- For the **classical-loop + neural acceleration** line, read
  [[fxlms-algorithm]] (Latent FxLMS variant) then [[neural-system-identification]]
  and [[meta-learning-anc]].
- For **array / constrained / RL** directions, see [[deep-rl-anc]] and
  [[pinn-virtual-sensing]].
- For **hearing-aid / SE** work, see [[transformer-se-anc]].

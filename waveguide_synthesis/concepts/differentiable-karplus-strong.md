---
title: Differentiable Karplus-Strong
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [string, guitar, delay-line, differentiable, ml, optimization, comparison]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_38.pdf
  - raw/DAFx26_paper_38.txt
---

# Differentiable Karplus-Strong

Event-based sound matching with a differentiable *extended* Karplus-Strong decoder,
and a gradient analysis of what spectral losses can and cannot supervise.[^tablas]

## The decoder

Extended KS in the Jaffe-Smith sense, all blocks differentiable:
- Loop delay $L = f_s/f_0$, split into integer $\lfloor L \rfloor$ and a fractional part.
- Loop filter as a first-order all-pole, re-parameterised so DC gain and cutoff decouple
  decay from damping: $H_L(z) = g\,\dfrac{1+a_1}{1+a_1 z^{-1}}$.
- Fractional delay by order-$N=5$ **Lagrange** interpolation, $h[n] = \prod_{k\ne n}\dfrac{D-k}{n-k}$,
  chosen over allpass interpolation because its fractional delay is far more uniform
  across frequency and it does not ring when the delay changes. It absorbs the
  loop-filter phase delay: $D = L - \lfloor L\rfloor - P_L(f_0)$, $P_L(f_0) = -\angle H_L(e^{j\omega_0})/\omega_0$.
- Excitation: pluck-position comb $H_P(z) = 1 - z^{-p_i}\big((1-p_f) + p_f z^{-1}\big)$ and the
  Jaffe-Smith dynamics filter $H_D(z) = (1-R)/(1-Rz^{-1})$.

Two implementations are compared. **tKSA** closes the loop in the time domain via
parallelised backprop through all-pole filters,
$$H_{t\mathrm{KSA}}(z) = \frac{H_D(z)H_P(z)}{1 - H_L(z)H_I(z)z^{-L_{\text{int}}}} .$$
**fKSA** replaces interpolator and integer delay with the closed-form phase shift
$z_M^{-D} = e^{-j2\pi k M^{-1} D}$ on an $M$-point grid. Because KS is highly resonant
($\mathrm{RT}_{60} = 86.26$ s at $f_0 = 80$ Hz for $g = 0.999$, $a_1 = 0.001$; only 4.5 s at 1280 Hz)
**no** FFT size avoids time-aliasing everywhere; $N_{\text{FFT}} = 2^{14}$ with a 256-sample hop
was the compromise, and aliasing still truncates long decays, making the model
overestimate $g$ and underestimate $a_1$.

## Encoder and losses

A dual front end (log-mel filterbank plus a learnable 1D CNN for phase-sensitive
transients) feeds a 7-block TCN, then a set-prediction Transformer with $N = 10$ learnable
queries matched to ground truth by Hungarian assignment - so plucks are discrete
**events**, not per-frame parameters. Heads emit existence, onset time, $f_0$ (soft-argmax
over 128 log bins), and $g$, $a_1$, pluck position and dynamic level.

Losses: revisited multi-scale spectral $\mathcal{L}_{\text{MSS}}$ over prime window lengths,
spectral optimal transport $\mathcal{L}_{\text{SOT}}$ (per-frame 2-Wasserstein cost along frequency),
and a parameter loss $P_{\text{loss}}$. Rather than supervising the coupled $g$ and $a_1$
separately, $P_{\text{loss}}$ uses their joint analytic decay time
$$\mathrm{RT60}_k = \frac{-3}{f_0 \log_{10}|H_L(e^{j\omega_k})|}$$
under an $L_1$ loss in $\log(1+\mathrm{RT60})$ space. Onsets are differentiable through a
straight-through estimator: forward pass snaps to the nearest sample, backward pass
routes through the continuous phase rotation.

## The gradient result

Coarse/fine gradient accuracy is the fraction of 250 initialisations for which
$\mathrm{sgn}(\partial \mathcal{L}/\partial f) = \mathrm{sgn}(f - f_x)$.

- Time-domain Lagrange interpolation gives gradient accuracy **comparable to frequency
  sampling** - delay length really is differentiable in the time domain, with no
  time-aliasing. This is the paper's main DSP contribution.
- $\mathcal{L}_{\text{MSS}}$ supervises timbre and dynamics well (100% CGA on $g$, $a_1$) but is weak
  on pluck position and unreliable on $f_0$ (68.0% CGA, 54.8% FGA on tKSA).
- **Onsets are the failure mode.** Single-event onset accuracy is near chance for tKSA
  (51.2% with MSS, 14.4% with SOT); SOT on fKSA reaches 88.8% FGA but only, the authors
  argue, because time-aliasing leaks a temporal shift into per-frame spectra - an
  artefact, not a cue. For $K$ simultaneous events, **joint** onset accuracy collapses
  to at most 4.1% at $K = 5$ for every loss.

## Consequences for training

| Regime | Synthetic $F_1$ | $\Delta$ cents | Real-data CLAP KAD |
|---|---|---|---|
| P-Only (parameter loss, synthetic) | 0.92 | 15.14 | 193.78 |
| Audio-Only, time domain (external detectors) | 0.89 | 294.33 | **163.95** |
| P+Audio (time), no detach | 0.01 | 13.86 | 403.83 |
| HpN+ baseline | - | - | 183.11 |

- Joint audio+parameter training **collapses**; detaching the onset head from the audio
  loss always restores performance, exactly as the gradient analysis predicts.
- $P_{\text{loss}}$ on synthetic data learns $f_0$, timbre and onsets best in-domain, but does
  not transfer to NSynth acoustic-guitar recordings (missed onsets, erratic $f_0$),
  plausibly CNN overfitting to synthetic transients. External CREPE + spectral-flux
  detectors with audio losses generalise best on real data, reducing the model's job
  to timbre.
- Harmonics-plus-noise baselines still win most reconstruction metrics - a structural
  ceiling of a single KS loop, which models neither the body, the player's hands, nor
  string-fret collisions. The exception is CLAP perceptual distance, where the
  time-domain KS decoder beats both baselines (no formal listening test).

## See also
- [[string-modeling]] - the extended Karplus-Strong structure being fitted
- [[delay-line-techniques]] - Lagrange versus allpass fractional delay
- [[waveguide-parameter-optimization]] - where this sits in the calibration taxonomy

[^tablas]: P. Tablas de Paula, D. Marttila, R. Diaz, I. Roman, E. Benetos, J. D. Reiss, "Sound Matching with a Differentiable Karplus-Strong Algorithm," DAFx26. See [[entities/source-papers#paper-tablas-differentiable-karplus-strong-2026]].

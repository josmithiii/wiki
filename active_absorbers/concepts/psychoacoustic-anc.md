---
title: Psychoacoustic ANC (tonality, loudness, annoyance)
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [anc, psychoacoustic, tonal, fan-noise, industrial, reference]
sources:
  - raw/Rivera-Zoelzer-PsychoacousticHybridANC-ICSV25-2018.txt
---

# Psychoacoustic ANC

Standard ANC minimises mean-square pressure at the error mic.
Community-noise complaints are not driven by $E[p^2]$ — they are
driven by **tonality, loudness, sharpness, and modulation**. A 5 dB
SPL reduction that leaves a pure tone intact is often
*worse*-received than a 0 dB "reduction" that broadens the tone
into shaped noise.

The canonical validated primary source so far is Rivera Benois,
Papantoni & Zölzer 2018[^rivera-2018], which demonstrates a
psychoacoustic-weighted FeLMS + MVC hybrid structure and evaluates it
using Zwicker / Aures metrics on an FPGA headphone prototype; see
§5 for details.

Directly relevant to data-center rooftop fan hum: the 118 Hz BPF is a
pure tone with a tonality penalty of 3–6 dB under most standards, so a
controller that trades a few dB of level for a dramatic reduction in
tonality can pay off.

## 1. What the standards actually penalize

| Standard | What it measures | Typical fan-hum penalty |
|---|---|---|
| **ISO 1996-2** | $K_T$ tonality adjustment | +3 to +6 dB(A) |
| **DIN 45681** | prominent-tone level above masking threshold | up to +6 dB(A) |
| **ANSI S12.9 Part 3** | prominent discrete tone | +0, +3, or +5 dB |
| **Zwicker loudness** (ISO 532-1/2) | sone, critical-band integration | direct |
| **Aures / DIN 45692 sharpness** | high-frequency concentration | often secondary for fans |
| **Roughness / fluctuation strength** | 20–300 Hz modulation | **relevant for VFD-modulated BPF** |

A community-noise report is effectively a weighted sum of these, not
a raw dB(A) reading. Building a controller whose cost function matches
the complaint metric is the whole point of psychoacoustic ANC.

## 2. Perceptually-weighted cost functions

Replace $J = E[e^2(n)]$ with a perceptual norm $J_\Psi = E[\|\Psi e\|^2]$
where $\Psi$ is:

- **A-weighting** — crude but standard; cheap FIR implementation.
- **Equal-loudness-contour weighting** at an assumed SPL; better than A
  for 60–120 Hz content but level-dependent.
- **Bark-/ERB-band loudness weighting** — closer to Zwicker loudness;
  implemented as a filter-bank before the FxLMS error.
- **Masking-curve weighting** — attenuates error components already
  masked by ambient (wind, traffic); avoids spending actuator authority
  on inaudible residuals. Related to perceptual audio coding.
- **Tonality-aware cost** — penalise tonal residual more than
  equal-energy broadband residual, e.g. $J_T = \alpha J_{\text{tone}} +
  J_{\text{broad}}$ after spectral decomposition.

## 3. Tonal-to-broadband reshaping

If a pure tone cannot be fully cancelled (causality, actuator authority,
or power budget), replace it with shaped broadband noise at equal or
lower loudness but no tonality penalty.

- Controller generates an anti-sound signal that is *partial*
  cancellation of the tone plus an injected shaped-noise pedestal.
- Perceptually equivalent loudness, much lower tonality, often net
  win on the community-noise metric.
- Related to "informed sound masking" in open-plan offices — inject
  HVAC-like noise to mask speech intelligibility.
- Caveat: adding energy (even perceptually-neutral energy) is
  counter-intuitive to the ANC brief and may be politically
  unacceptable depending on the regulator.

## 4. Selective / event-aware ANC

A closely related idea: do not attempt to cancel transients or signals
the listener *wants* to hear.

- [[transformer-se-anc]] and Khan et al. 2025 — "selective" noise
  cancellation distinguishing target from interferer with SOTA SE
  networks.
- Applied to rooftop fans: preserve emergency-vehicle sirens, building
  alarms, speech — cancel only the steady fan component. Unlikely to
  matter for community-noise outdoors, but relevant if the ANC
  radiation pattern leaks indoors.

## 5. Primary source: Rivera Benois, Papantoni & Zölzer 2018

Hybrid ANC headphone architecture combining a **perceptually-weighted
feedforward FeLMS** (Bao & Panahi 2013 layout — ITU-R 468 noise
weighting $H_{nw}(z)$ applied to both the reference and the error
signal driving the adaptation) with a **classical Minimum-Variance
Controller (MVC) feedback** substructure[^rivera-2018]. The two are
coupled via the Foudhaili 2008 connection — the filtered adaptive
control signal $\hat S(z) W_f(z) X(z)$ is subtracted from the
feedback-input summation, isolating the feedback residual.

Design insights transferable to rooftop-fan ANC:

- Perceptual FeLMS alone **underperforms below ~650 Hz** because the
  ITU-R 468 weighting de-emphasises LF — exactly the band that
  matters for 118 Hz BPF community noise. A low-frequency feedback
  substructure is needed.
- The MVC covers <300 Hz; the FeLMS-psy covers 650 Hz upward. The
  spectral **gap between the two bands means the substructures
  barely couple** — each operates near its isolated optimum, avoiding
  the stability coupling that a strongly overlapping hybrid would
  introduce.
- Closed-form transfer function $E(z)/X(z) = [P(z) - S(z) W_f(z)(1 +
  \hat S(z) W_b(z))] / [1 + S(z) W_b(z)]$ — stability tied to
  accurate $\hat S(z) \approx S(z)$. With good $\hat S$, the
  feedforward error reduces to $P(z)/(1 + S(z) W_b(z)) - S(z)
  W_f(z)$.
- FPGA implementation on a Beyerdynamic DT 770 prototype: 48 kHz
  sample rate, 1024-tap adaptive $W_f$, step size $\mu_f = 2 \times
  10^{-12}$, 64-bit fixed-point with 48-bit fractional.
- **Zwicker / Aures metric results** on AM Gaussian white noise
  excitation (70 Hz mod, 30% depth, 82.3 dB SPL): hybrid-psy reduces
  loudness to **11.06 sone** (vs 17.5 passive), roughness to **0.13
  asper** (vs 0.45 passive), and raises Aures pleasantness to
  **0.140** — best among all tested structures.
- Observed artifact: amplification peak at 6300 Hz in both
  FeLMS-psy and hybrid — possibly a $S/\hat S$ mismatch or the
  perceptual-weighting implementation. **Leaky FeLMS + triggered
  online $\hat S$ re-estimation** is the suggested remediation.

## 6. AI-era extensions

- **Differentiable loudness models** — Zwicker-style loudness
  reformulated for autograd; directly pluggable as a training loss
  for [[deep-anc-crn]] or [[meta-learning-anc]].
- **RL with perceptual reward** — natural fit for [[deep-rl-anc]]
  because the reward is non-differentiable / standard-defined
  (tonality penalty, loudness).
- **Perceptual GANs** — adversarial loss against a tonality classifier;
  early-stage research.

## 7. Why this matters for rooftop fans specifically

- Rooftop → community propagation: ground reflection, downward
  refraction, and low-frequency transmission through building
  envelopes all favour the BPF tone over broadband content. The
  *received* spectrum at a residence is more tonal than the source.
- Complaints are reported as "it's a hum", not "it's 52 dB(A)";
  legal thresholds in many jurisdictions (e.g., WHO community-noise
  guidelines, UK BS 4142) include tonality / impulsive penalties.
- An ANC system optimised for dB(A) alone can *increase* complaints
  if it narrows the spectrum further.

## Sources ingested

- **Rivera Benois, Papantoni & Zölzer 2018** (ICSV25) — hybrid
  FeLMS-psy + MVC headphone architecture, FPGA evaluation with
  Zwicker/Aures metrics. See
  `entities/source-papers.md#paper-rivera-psychoacoustic-hybrid-anc-2018`.

## Pending sources

- Zwicker, E. & Fastl, H., *Psychoacoustics: Facts and Models*, Springer (textbook).
- Aures, W., "Berechnungsverfahren für den sensorischen Wohlklang," *Acustica* 59, 1985.
- Kuo & Morgan 1999 ([[classical-anc-overview]]) — brief mention of A-weighted FxLMS variants.
- Zhou, D., DeBrunner, V., *IEEE Trans. Speech Audio Proc.* — perceptual ANC early work.
- Bao, H., Panahi, I. — psychoacoustic ANC publications (the Bao & Panahi 2013 structure that Rivera et al. extend).

See also: [[classical-anc-overview]] §7 ("Psychoacoustic ANC" row),
[[tonal-periodic-anc]] (the tonal component this targets),
[[ai-anc-overview]] (differentiable perceptual losses).

[^rivera-2018]: P. Rivera Benois, V. Papantoni & U. Zölzer, "Psychoacoustic Hybrid Active Noise Control Structure for Application in Headphones," *ICSV25*, Hiroshima, July 2018. Distilled in `entities/source-papers.md#paper-rivera-psychoacoustic-hybrid-anc-2018`.

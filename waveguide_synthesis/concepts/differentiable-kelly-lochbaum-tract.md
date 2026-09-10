---
title: Differentiable Kelly-Lochbaum Tract
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [voice, waveguide, scattering, differentiable, ml, optimization, acoustics]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_39.pdf
  - raw/DAFx26_paper_39.txt
---

# Differentiable Kelly-Lochbaum Tract

Articulatory copy-synthesis of Tuvan *sygyt* overtone singing by gradient descent
through a Kelly-Lochbaum waveguide, extended so a single harmonic in the 1-3 kHz band
can be focused sharply enough.[^camara]

## Target

In sygyt a drone at $f_0$ is sustained while one harmonic $h \in \{2,\dots,10\}$ is selectively
amplified, classically explained by $F_2 \approx F_3$ merging into one narrow peak
(bandwidths reported as low as ~20 Hz under pharyngeal constriction). Standard
low-dimensional articulator parameterisations cannot form resonances that narrow.

## Model

Built on VocalTrax's JAX implementation, at 16 kHz, with three additions.
- **Geometry.** Three coupled waveguide sections: oral tract, 44 cylindrical segments
  glottis to lips; nasal tract, 28 segments velum to nostrils; and a **sublingual tube**,
  15 segments carrying a second source into the oral tract.
- **Scattering.** Standard Kelly-Lochbaum at each boundary,
  $r_i = (A_i - A_{i+1})/(A_i + A_{i+1})$. Two three-way junctions - the sublingual
  junction at oral segment 9 and the velum junction at segment 17 - use
  $$\Sigma = A_L + A_R + A_B, \qquad r_X = \frac{2A_X - \Sigma}{\Sigma},\quad X \in \{L,R,B\}.$$
- **Learnable spatially varying damping.** Uniform damping is replaced by per-segment
  $d_i \in [0.99, 0.9999]$ applied as $R_i \leftarrow R_i d_i$, $L_i \leftarrow L_i d_i$, so the optimizer can
  sharpen $Q$ near the target overtone and broaden it elsewhere.
- **Sources.** Glottal and sublingual Liljencrants-Fant waveforms with learnable
  amplitude, tenseness, open-quotient offset and spectral-tilt offset; the sublingual
  source runs at the detected $f_{ot}$, held fixed during optimization.

## Parameterisation and loss

Two tract controls are compared: a classical **articulator chain** (~13 DOF/frame: tongue
position and diameter, throat constriction, lip rounding, velum, sublingual coupling,
one global damping) and a **cubic B-spline** basis (~70 DOF/frame), $A = B_A\alpha_A$ and
$d = \mathrm{clip}(B_d\alpha_d, 0.99, 0.9999)$ with $K = 20$ control points at uniform knots. The
spline guarantees $C^2$ continuity, so the extra freedom does not produce implausible
per-segment discontinuities.

$f_0$ comes from YIN; the active overtone is the harmonic whose energy exceeds a
6 dB/octave rolloff expectation by more than 6 dB, with 3 dB hysteresis and
Savitzky-Golay smoothing of the harmonic-number track. Both are frozen. Loss:
$$\mathcal{L} = \mathcal{L}_{\text{STFT}} + \lambda_{\text{mel}}\mathcal{L}_{\text{mel}} + \lambda_{\text{harm}}\mathcal{L}_{\text{harm}}
+ \lambda_{\text{energy}}\mathcal{L}_{\text{energy}} + \lambda_{ot}\mathcal{L}_{ot},$$
all weights 1, with the **overtone-salience** term built from
$$S_{ot}(t) = 10\log_{10}\frac{\sum_{f\in B_h}|X(f,t)|^2}{\sum_{f\in B_\pm}|X(f,t)|^2 + \epsilon}$$
($\pm 50$ Hz bands around $h f_0$ and its two neighbours), penalised as
$\|S_{ot}^{\text{target}} - S_{ot}^{\text{synth}}\|_2^2$. Adam, $\eta = 5\times10^{-3}$ after a 100-step warm-up
from $5\times10^{-4}$, gradient clipping at norm 1, 500 iterations, ~30 min per 5 s
segment on CPU (RTF $\approx 360\times$; offline only).

## Results

20 segments from two independent datasets (HFA, 1 singer, 10 pitches F3-E flat 4;
Bergevin et al., 4 Tuvan singers) - 5 singers, 10 pitches in total.

| Method | DOF | LSD HFA (dB) | LSD Bergevin (dB) | SpCorr | Q1 (MUSHRA) |
|---|---|---|---|---|---|
| Articulator chain | 19 | 13.84 | 14.53 | 0.66-0.71 | 11.6-13.6 |
| DDSP harmonic+noise | ~100k | 10.99 | 10.71 | 0.82-0.83 | 35.4-42.4 |
| B-spline waveguide | 86 | **9.64** | **9.04** | **0.86-0.88** | **38.5-44.8** |

- **30% (HFA) and 38% (Bergevin) LSD reduction** over the articulator baseline,
  lowest LSD on all 20 individual segments, Cohen's $d = 2.1$ / $1.9$.
- Beats a DDSP baseline that has direct per-harmonic amplitude control - the paper's
  argument that explicit acoustic structure is a useful inductive bias. DDSP still
  edges it on local overtone spectral correlation (0.12 vs 0.15).
- Overtone band: $|\Delta S_{ot}| = 0.96 \pm 0.70$ dB and $|\Delta\mathrm{HPR}| = 5.5 \pm 2.0$, both
  roughly half the baselines. Cepstral formant-peak error **28 Hz**, against 222 Hz
  (articulator) and 120 Hz (DDSP), with peak prominence 12.0 dB vs 12.4 dB target.
- Learned shapes are interpretable: a pronounced constriction at oral segment 9 (the
  sublingual junction, matching MRI reports of posterior tongue position) in 16 of 20
  segments, with low damping near that junction isolating the proximal tract and high
  damping (high $Q$) in the anterior cavity. None of this is imposed by the loss.
- $2\times2$ ablation: removing the sublingual source costs **+1.0 dB** LSD, removing
  spatially varying damping only **+0.1 dB** - the second source dominates.

Limitations: absolute LSD stays 9-15 dB; the sublingual tube is an acoustic abstraction,
not an anatomical claim; this is copy-synthesis of sustained segments rather than a
controllable singing synthesizer, and fixed pitch tracks limit glissandi.

## See also
- [[waveguide-vocal-models]] - Kelly-Lochbaum tract models generally
- [[scattering-junctions]] - the reflection coefficients and three-way junctions used
- [[differentiable-karplus-strong]] - the sibling DAFx26 differentiable waveguide study
- [[entities/source-papers#paper-camara-articulatory-biphonic-singing-2026]] - catalog entry

[^camara]: M. Camara, M. P. Daza-Llin, F. Marcos-Macias, J. L. Blanco, "Differentiable Articulatory Copy-Synthesis of Biphonic Singing," DAFx26. See [[entities/source-papers#paper-camara-articulatory-biphonic-singing-2026]].

---
title: Modal Analysis Measurement
created: 2026-04-09
updated: 2026-09-08
type: concept
tags: [modal, acoustics, measurement, impulse-response, vibration]
sources:
  - /w/pasp/modal.tex
  - /l/dttd/modal-analysis-of-different-types-of-classical-guitar-bodies.pdf
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
---

# Modal Analysis Measurement

## Overview
Experimental modal analysis (EMA) extracts mode frequencies, damping, and shapes
from measured vibration data. These parameters are then used directly in modal synthesis.

## Basic Measurement Chain
1. Excite the object (impact hammer or shaker)
2. Measure the response (accelerometer, laser vibrometer, or microphone)
3. Compute the Frequency Response Function (FRF) $H(f) = \text{Output}(f) / \text{Input}(f)$
4. Fit a modal model to $H(f)$ → extract $(f_k, d_k, a_k)$

## Excitation Methods
| Method | Pros | Cons |
|--------|------|------|
| Impact hammer | Simple, portable, fast | Limited force amplitude, noise |
| Electrodynamic shaker | Controlled, swept sine or random | Requires attachment fixture |
| Acoustic excitation | Non-contact | Hard to control coupling |
| Laser-induced impulse | Non-contact, precision | Expensive |

## Response Measurement
- **Accelerometer**: contact, mass-loads the object (affects high modes of small objects)
- **Laser Doppler Vibrometer (LDV)**: non-contact, measures velocity; ideal for light objects
- **Microphone**: measures radiated pressure, not structural velocity directly
  (useful for "acoustic modal analysis" — finding radiation modes)

## FRF Estimation
Using averaged measurements to reduce noise:
$$H(f) = S_{xy}(f) / S_{xx}(f) \quad\text{(H1 estimator, minimizes output noise)}$$
$$H(f) = S_{yy}(f) / S_{yx}(f) \quad\text{(H2 estimator, minimizes input noise)}$$

where $S_{xy}$ = cross-power spectrum, $S_{xx}$ = input power spectrum.

## Modal Parameter Extraction Algorithms
### Time domain
- **PRONY**: fits decaying sinusoids to IR; numerically sensitive
- **ERA (Eigensystem Realization Algorithm)**: state-space realization from IR
- **Ibrahim Time Domain (ITD)**: similar to ERA, multi-channel

### Frequency domain
- **Peak picking**: crude; read f_k from peaks, d_k from -3 dB bandwidth
- **Circle fitting**: fit circle in Nyquist plot around each resonance
- **Rational fraction polynomial (RFP)**: global fit of rational polynomial to H(f)
- **PolyMAX**: industry standard; robust, handles closely-spaced modes

### High-resolution spectral methods (signal processing approach)
- **ESPRIT**: eigenspace method, estimates complex poles directly from signal
- **MUSIC**: subspace method, super-resolution frequency estimation
- **MPS (Modal Parameter Synthesis)**: sinusoidal modeling as used in SMS/Serra
- All require estimating number of modes present (model order selection)

## Practical Considerations for Sound Synthesis
- Need only acoustic/radiation modes, not all structural modes
- Modes above ~6-8 kHz often too dense to fit individually; use statistical energy analysis (SEA)
- Damping measurement is harder than frequency measurement (Q-factors of 100-10000)
- Moving the mic/pickup location changes a_k but not f_k or d_k

## Datasets and Libraries
- **FreeSound** has many instrument recordings usable for IR measurement
- **Orchidea** (IRCAM): orchestral sound library with physics annotations
- **RealImpact** (Georg et al., 2022): 150,000 impact recordings from 50 objects,
  synchronized video + audio, used for ML training on modal synthesis

## DAFx26 additions

- **Eigensystem Realization Algorithm (ERA)** applied to measured violin bridge admittance IRs gives a reduced-order state-space model in one algebraic step, beating modal and state-space baselines in time, frequency and energy decay - but without a passivity guarantee: [[entities/source-papers#paper-giampiccolo-era-violin-bridge-2026]]
- Modal parameters of **bridge compliance and bridge-to-air radiation** extracted from measured IRs for all 65 guitars of the Mores dataset, then used to drive per-instrument synthesis: [[entities/source-papers#paper-ducceschi-65-classical-guitars-2026]]
- The **1st DAFx Parameter Estimation Challenge** turned pole-fitting into a scored benchmark on synthetic plate IRs; every entry recovered frequencies and decays far better than gains (no method below 0.83 relative gain error), and a frequency-domain re-evaluation reordered the ranking: [[entities/source-papers#paper-gabrielli-dafx-challenge-overview-2026]]
- Classical competitors that did well there: **matrix-pencil** initialization of a diagonal complex state-space model with closed-form least-squares gains, and **subband autoregressive pole harvesting** on the IR and its first two finite differences: [[entities/source-papers#paper-bittner-matrix-pencil-ssm-taskb-2026]], [[entities/source-papers#paper-franchino-subband-ar-pole-harvesting-2026]]

## Related Concepts
- [[mode-shapes-and-eigenvalues]] — what we are measuring
- [[modal-synthesis-overview]] — how measurements are used in synthesis
- [[fem-bem-for-modal-synthesis]] — computing modes instead of measuring them
- [[realimpact-dataset]] — large-scale measured impact dataset

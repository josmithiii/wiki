---
title: Modal Analysis Measurement
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [modal, acoustics, measurement, impulse-response, vibration]
sources:
  - /w/pasp/modal.tex
  - /l/dttd/modal-analysis-of-different-types-of-classical-guitar-bodies.pdf
---

# Modal Analysis Measurement

## Overview
Experimental modal analysis (EMA) extracts mode frequencies, damping, and shapes
from measured vibration data. These parameters are then used directly in modal synthesis.

## Basic Measurement Chain
1. Excite the object (impact hammer or shaker)
2. Measure the response (accelerometer, laser vibrometer, or microphone)
3. Compute the Frequency Response Function (FRF) H(f) = Output(f) / Input(f)
4. Fit a modal model to H(f) → extract (f_k, d_k, a_k)

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
  H(f) = Sxy(f) / Sxx(f)   [H1 estimator, minimizes output noise]
  H(f) = Syy(f) / Syx(f)   [H2 estimator, minimizes input noise]

where Sxy = cross-power spectrum, Sxx = input power spectrum.

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

## Related Concepts
- [[mode-shapes-and-eigenvalues]] — what we are measuring
- [[modal-synthesis-overview]] — how measurements are used in synthesis
- [[fem-bem-for-modal-synthesis]] — computing modes instead of measuring them
- [[realimpact-dataset]] — large-scale measured impact dataset

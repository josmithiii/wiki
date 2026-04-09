---
title: Resonator Bank Implementation
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [resonator, dsp, modal-synthesis, realtime, filter]
sources: []
---

# Resonator Bank Implementation

## Core Structure
A resonator bank implements modal synthesis as N parallel digital filters.
Each mode k → one 2nd-order IIR section (biquad).

## Biquad Resonator
Transfer function for mode k:
  H_k(z) = a_k * b1_k * z^-1 / (1 - 2*R_k*cos(2*pi*f_k/fs)*z^-1 + R_k^2*z^-2)

Parameters:
- f_k = resonant frequency (Hz)
- R_k = pole radius = exp(-pi * f_k / (Q_k * fs))  [from Q-factor]
       or R_k = exp(-d_k / fs)  [from decay rate d_k in nepers/sample]
- a_k = mode amplitude weight
- fs = sample rate

## Equivalent Forms

### State-space per mode
  s1_k[n] = 2*R_k*cos(theta_k)*s1_k[n-1] - R_k^2*s2_k[n-2] + x[n]
  y_k[n]  = a_k * s1_k[n]

Total output: y[n] = sum_k y_k[n]

### As decaying sinusoid
Impulse response of H_k: h_k(n) = a_k * R_k^n * sin(n * 2*pi*f_k/fs)
This is the sampled version of: a_k * exp(-d_k*t) * sin(2*pi*f_k*t)

## Computational Cost
- N modes: N biquads, each ~5 multiply-adds per sample
- 100 modes at 44.1 kHz = ~22M MACs/sec — trivial on modern CPUs
- 1000 modes = ~220M MACs/sec — still feasible, one core of a modern CPU
- 10,000 modes = ~2.2B MACs/sec — needs GPU parallelism or careful SIMD

## GPU Implementation (Cook / James et al.)
- Each mode mapped to one GPU thread
- All modes updated in parallel per sample
- Reduction sum at output
- Reported ~60,000 modes in real time on 2005-era GPU
- See [[gpu-modal-synthesis]] for details

## SIMD / Vectorization
- Modes are independent → embarrassingly parallel
- Pack 4 or 8 modes per SIMD register (SSE/AVX/NEON)
- Compiler auto-vectorizes if loops are written cleanly
- Coefficient update (pitch shift etc.) can be done between sample blocks

## Mode Pruning
Not all N modes are audible at all times:
- Amplitude thresholding: skip modes where |a_k * R_k^n| < epsilon
- Frequency masking: modes above Nyquist or below ~20 Hz can be dropped
- Perceptual masking: modes masked by louder nearby modes (cf. auditory masking)
- Dynamic pruning reduces CPU load by 5-10x in practice

## Stability
- Biquad stable iff R_k < 1 (pole inside unit circle)
- R_k = exp(-d_k/fs): always stable for d_k > 0 (positive damping)
- Numerical issues: R_k very close to 1 (very long decays) needs double precision
  for coefficient computation, single precision for the filter state is usually OK

## Parameter Mapping
| Physical parameter     | Filter parameter              |
|------------------------|-------------------------------|
| Natural freq f_k       | Pole angle theta_k = 2*pi*f_k/fs |
| Damping d_k (nep/s)    | Pole radius R_k = exp(-d_k/fs) |
| Mode amplitude a_k     | Filter gain coefficient       |
| Excitation location    | Scales all a_k via mode shapes|
| Material density rho   | Scales f_k (f ~ 1/sqrt(rho))  |

## Related Concepts
- [[modal-synthesis-overview]] — top-level context
- [[mode-shapes-and-eigenvalues]] — source of mode parameters
- [[impact-synthesis]] — typical excitation signal
- [[gpu-modal-synthesis]] — massively parallel implementations

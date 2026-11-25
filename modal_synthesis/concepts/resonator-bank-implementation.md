---
title: Resonator Bank Implementation
created: 2026-04-09
updated: 2026-11-25
type: concept
tags: [resonator, dsp, modal-synthesis, realtime]
sources:
  - /w/pasp/modal.tex
  - https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html
---

# Resonator Bank Implementation

## Core Structure
A resonator bank implements modal synthesis as $N$ parallel digital filters.
Each mode $k$ → one 2nd-order IIR section (biquad).

## Biquad Resonator
Transfer function for mode $k$:
$$H_k(z) \;=\; \frac{a_k\, b_{1,k}\, z^{-1}}{1 - 2R_k\cos(2\pi f_k/f_s)\,z^{-1} + R_k^2\,z^{-2}}$$

Parameters:
- $f_k$ = resonant frequency (Hz)
- $R_k = \exp(-\pi f_k / (Q_k f_s))$ (from Q-factor, i.e. bandwidth $B_k = f_k/Q_k$ Hz)
  or $R_k = \exp(-d_k / f_s)$ (from decay rate $d_k = \pi B_k$ in nepers/second)
- $a_k$ = mode amplitude weight; $b_{1,k} = R_k\sin\theta_k$, $\theta_k = 2\pi f_k/f_s$, normalizes the impulse response below
- $f_s$ = sample rate

## Equivalent Forms

### Direct-form recursion per mode
$$\begin{aligned}
s_k[n] &= 2R_k\cos(\theta_k)\,s_k[n-1] - R_k^2\,s_k[n-2] + x[n]\\
y_k[n] &= a_k\, b_{1,k}\, s_k[n-1]
\end{aligned}$$

Total output: $y[n] = \sum_k y_k[n]$

### As decaying sinusoid
Impulse response of $H_k$: $h_k(n) = a_k R_k^n \sin(2\pi f_k n / f_s)$, $n \ge 0$
This is the sampled version of: $a_k e^{-d_k t} \sin(2\pi f_k t)$

## Computational Cost
- N modes: N biquads, each ~5 multiply-adds per sample
- 100 modes at 44.1 kHz = ~22M MACs/sec — trivial on modern CPUs
- 1000 modes = ~220M MACs/sec — still feasible, one core of a modern CPU
- 10,000 modes = ~2.2B MACs/sec — needs GPU parallelism or careful SIMD

## GPU Implementation
- Each mode mapped to one GPU thread
- All modes updated in parallel per sample (or per block)
- Reduction sum at output
- GPU resonator banks date from 2005 (Zhang, Ye & Pan); see [[gpu-modal-synthesis]] for details

## SIMD / Vectorization
- Modes are independent → embarrassingly parallel
- Pack 4 or 8 modes per SIMD register (SSE/AVX/NEON)
- Compiler auto-vectorizes if loops are written cleanly
- Coefficient update (pitch shift etc.) can be done between sample blocks

## Mode Pruning
Not all N modes are audible at all times:
- Amplitude thresholding: skip modes where $|a_k R_k^n| < \epsilon$
- Band limits: modes above Nyquist must be dropped (they would alias); below ~20 Hz they can be
- Perceptual masking: modes masked by louder nearby modes (cf. auditory masking)
- Dynamic pruning reduces CPU load by 5-10x in practice

## Stability
- Biquad stable iff $R_k < 1$ (pole inside unit circle)
- $R_k = \exp(-d_k/f_s)$: always stable for $d_k > 0$ (positive damping)
- Numerical issues: $R_k$ very close to 1 (very long decays) needs double precision
  for coefficient computation, single precision for the filter state is usually OK

## Parameter Mapping
| Physical parameter     | Filter parameter              |
|------------------------|-------------------------------|
| Natural freq $f_k$         | Pole angle $\theta_k = 2\pi f_k/f_s$ |
| Damping $d_k$ (nep/s)      | Pole radius $R_k = \exp(-d_k/f_s)$ |
| Mode amplitude $a_k$       | Filter gain coefficient |
| Excitation location        | Scales all $a_k$ via mode shapes |
| Material density $\rho$    | Scales $f_k$ ($f \propto 1/\sqrt{\rho}$) |

## Related Concepts
- [[modal-synthesis-overview]] — top-level context
- [[mode-shapes-and-eigenvalues]] — source of mode parameters
- [[impact-synthesis]] — typical excitation signal
- [[gpu-modal-synthesis]] — massively parallel implementations
- [[state-space-models-as-modal-resonator-banks]] — a diagonal complex SSM is exactly this filter bank, and is trainable
- [[corpus-driven-parametric-modal-reverb]] — driving thousands of these sections from six perceptual controls

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Modal Expansion](https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html), [State Space to Modal Synthesis](https://ccrma.stanford.edu/~jos/pasp/State_Space_Modal_Synthesis.html)
- [[jos_books/entities/filters-book|Filters]]: [Two-Pole](https://ccrma.stanford.edu/~jos/filters/Two_Pole.html), [Resonator Bandwidth in Terms of Pole Radius](https://ccrma.stanford.edu/~jos/filters/Resonator_Bandwidth_Terms_Pole.html), [Parallel First and/or Second-Order Sections](https://ccrma.stanford.edu/~jos/filters/Parallel_First_and_or_Second_Order.html), [Time-Varying Two-Pole Filters](https://ccrma.stanford.edu/~jos/filters/Time_Varying_Two_Pole_Filters.html)

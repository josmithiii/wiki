---
title: sfFDN and FDN Sandbox
created: 2026-09-10
updated: 2026-09-10
type: entity
tags: [fdn, reverb, dsp, realtime, optimization, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_demo_68.pdf
  - raw/DAFx26_demo_68.txt
---

# sfFDN and FDN Sandbox

Open-source C++ FDN library plus a GUI sandbox, aimed at the gap between MATLAB
research code and shipping real-time reverberators.[^stonge]

- `sfFDN` - <https://github.com/Segfault1602/sfFDN>
- `FDNSandbox` - <https://github.com/Segfault1602/FDNSandbox>

## Library

Modelled on Schlecht's MATLAB FDN Toolbox but built for the audio thread. The
canonical FDN is split into interchangeable blocks - input gains, delay lines,
feedback matrix, loop filters, output gains, tone-correction filter, direct gain -
all deriving from an `AudioProcessor` base class, so a new extension is a new
subclass. Provided variants include constant and time-varying I/O gains, Hadamard,
Householder, random-orthogonal, circulant and nested-allpass feedback matrices,
time-varying delay lines, several IIR loop filters including the Valimaki-Prawda-
Schlecht two-stage attenuation filter, plus **filter feedback matrices** (scattering
FDN) and **velvet-noise decorrelation filters**.

Throughput, microseconds to process 128 samples, Intel Core i9-12900K:

| FDN size | 4 | 6 | 8 | 16 | 32 |
|---|---|---|---|---|---|
| sfFDN | 3.8 | 5.6 | 9.55 | 15.0 | 31.2 |
| RTFDN (Prawda et al. 2020) | 6.02 | 7.3 | 15.0 | 39.2 | 112.0 |

## Sandbox application

Real-time GUI with an audio player, a convolution-reverb module for A/B against a
measured IR, and live plots that update as parameters move: spectrogram and
mel-spectrogram, modal excitation distribution, spectrum and cepstrum, time- and
spectral-domain autocorrelation, attenuation-filter magnitude and phase, EDC and
mel-scale EDR, RT60, and echo density profile.

## Optimization without a differentiable model

Optimization runs directly on the real-time FDN; gradients, where an algorithm
needs them, come from forward or central **finite differences**. Nine ensmallen
algorithms are exposed: gradient descent, Adam, L-BFGS (gradient-based); SPSA,
simulated annealing, CNE, differential evolution, particle swarm, CMA-ES
(gradient-free).

- **Colorless reverberation.** Tunes I/O gains and matrix coefficients, $N^2 + 2N$
  parameters for a random orthogonal matrix, dropping to $2N + N$ for Householder
  or circulant. Loss $\mathcal{L}_{\text{color}} = \alpha_1\mathcal{L}_{\text{flatness}} + \alpha_2\mathcal{L}_{\text{sparsity}}$ with
  $\mathcal{L}_{\text{flatness}} = |\mathrm{Flatness}(X) - 0.56|$ (0.56 being the empirical spectral
  flatness of a 48000-sample noise signal) and $\mathcal{L}_{\text{sparsity}} = \|x\|_2/\|x\|_1$ to stop
  the flatness term collapsing echo density. Result on a 6-channel FDN: faster
  echo-density buildup and a narrower modal-excitation distribution.
- **RIR matching.** 21 parameters - 10 band $\mathrm{RT}_{60}(\omega)$ values, 10 tone-correction
  gains and a global gain - against normalised mel-EDR and EDC errors. Matches a
  pyroomacoustics target EDR more closely than the RIR2FDN analysis-synthesis
  route, which tracks the EDR slope but misses its initial level.

Limitation: a demo paper - no comparison against other FDN libraries beyond RTFDN,
and the optimizers are wrappers rather than a differentiable FDN.

## See also
- [[differentiable-fdn-design]] - the gradient-based alternative
- [[artificial-reverberation]] - FDN background
- [[entities/source-papers#paper-stonge-fdn-sandbox-sffdn-2026]] - catalog entry

[^stonge]: A. St-Onge & G. Scavone, "FDN Sandbox: Real-Time Experimentation and Analysis of FDNs," DAFx26 demo. See [[entities/source-papers#paper-stonge-fdn-sandbox-sffdn-2026]].

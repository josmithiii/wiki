---
title: Virtual Analog Overview
created: 2026-09-08
updated: 2026-09-08
type: concept
tags: [va-filters, circuit-modeling, antialiasing, neural-va, real-time, tutorial]
sources:
  - /l/dttd/DAFx26/README_JOS.md
  - virtual_analog/entities/source-papers.md
---

# Virtual Analog Overview

Virtual analog (VA) modeling means reproducing, in digital audio, the behavior
of analog hardware: synthesizer filters and oscillators, guitar pedals and
amplifiers, compressors, tape and spring devices. What makes it its own field
rather than "just filter design" is that the interesting behavior is
**nonlinear**, **time-varying**, and judged by ear.

## The classical taxonomy

- **White box** - write the circuit equations and discretize them. Accurate and
  interpretable; needs the schematic and component values.
- **Grey box** - keep a physically meaningful structure (a gain-reduction
  detector, a ladder topology, a modal bank) and fit its parameters to data.
- **Black box** - learn the input/output map with a neural network from
  measurements alone. Fastest to build, opaque, and hardest to make behave under
  knob motion.

## Method families

### Trapezoidal / TPT / ZDF filters
Discretize a continuous-time state-space filter prototype with the trapezoidal
rule (bilinear transform), resolving the resulting delay-free loops
algebraically. This "topology-preserving transform" / "zero-delay feedback"
family covers the state-variable, Sallen-Key, Moog ladder and diode ladder
filters. The open questions are stability under audio-rate parameter modulation
and where to put the saturating nonlinearities:

- [[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]] - common quadratic Lyapunov functions survive trapezoidal discretization, giving genuine BIBO proofs for time-varying VA filters.
- [[entities/source-papers#paper-oyama-moog-ladder-nonlinearity-2026]] - SPICE-referenced comparison of five digital ladders, and which stage's nonlinearity actually matters.
- [[entities/source-papers#paper-fontana-allpass-clipping-prevention-2026]] - keeping modulated allpass sections from overshooting unity.

### State-space and DAE circuit solvers
Nodal or state-space formulations (MNA, DAE) solved per sample with Newton
iteration or a surrogate. SPICE is the reference; the cost is the nonlinear
solve.

- [[entities/source-papers#paper-zea-adaptive-multirate-qp-2026]] - a quadratic program with a linear surrogate constraint replaces the Newton loop, with the residual driving adaptive step size.

### Wave digital filters
The scattering/wave-variable route to modular circuit emulation. WDFs are
covered canonically in the waveguide wiki - see [[wave-digital-filters]],
[[wdf-adaptors]], [[wdf-elements]] and [[wdf-applications]] - and the three
DAFx26 WDF papers are catalogued there and cross-linked from
[[entities/source-papers#wave-digital-filter-papers-catalogued-in-waveguide_synthesis]].

### Antialiasing
Any static nonlinearity applied at the audio rate generates harmonics above
Nyquist that fold back. The three standard answers are oversampling, bandlimited
correction functions (BLEP/BLAMP/polyBLEP) and **antiderivative antialiasing**
(ADAA), which convolves the nonlinearity with a reconstruction kernel
analytically.

- [[entities/source-papers#paper-gabrielli-polyadaa-2026]] - ADAA beyond linear reconstruction, via Chebyshev approximation of the nonlinearity.
- [[entities/source-papers#paper-roth-alias-free-oscillator-sync-2026]] - oscillator sync made alias-free by construction in the Fourier-series domain.
- [[entities/source-papers#paper-argentieri-arbitrary-polygon-oscillator-2026]] - polyBLAMP from runtime geometry plus adaptive oversampling.

### Black-box neural VA
Recurrent (LSTM/GRU) and convolutional (WaveNet-style) models trained on
input/output recordings, conditioned on the device's controls. Open problems:
artifacts under time-varying conditioning, sample-rate dependence, and cost.

- [[entities/source-papers#paper-kallinen-deep-regularized-rnn-va-2026]] - stability-regularized deep conditioned LSTMs with a gammatone-filterbank loss.
- [[entities/source-papers#paper-massi-fno-sample-rate-independent-va-2026]] - Fourier neural operators for sample-rate-independent inference.

### Grey-box hybrids
Neural components embedded in a physical structure: an MLP or KAN solving the
nonlinear junction inside a WDF, a differentiable circuit or synthesizer fitted
by gradient descent, a compressor whose detector is measured rather than
guessed.

- [[entities/source-papers#paper-thompson-compressor-control-voltage-2026]] - train and evaluate against the measured gain-reduction control voltage, not proxy audio metrics.
- [[entities/source-papers#paper-braun-fm-shared-embeddings-2026]] and [[entities/source-papers#paper-tabata-fm-parameter-estimation-2026]] - inverse problems for FM synthesizers.

### Deployment constraints
A VA algorithm ships inside an audio callback. What decides feasibility is not
average throughput but worst-case time per block, and whether the inference path
is callback-safe at all.

- [[entities/source-papers#paper-balasubramaniam-apple-silicon-neural-audio-2026]] - inference backends benchmarked under real DAW contention, by tail latency and deadline misses.
- [[entities/source-papers#paper-huang-snapdragon-gpu-neural-audio-2026]] - when a mobile integrated GPU helps and when per-call overhead eats the gain.
- [[entities/source-papers#paper-sato-wavenet-pruning-ios-2026]] - 90% magnitude pruning plus a sparse engine puts a WaveNet amp model on an iPhone CPU.

## See also

- [[entities/source-papers]] - the full DAFx26 pass-1 catalog for this wiki.
- [[wave-digital-filters]] - the WDF formalism, in the waveguide wiki.

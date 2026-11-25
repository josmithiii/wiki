---
title: Virtual Analog Overview
created: 2026-09-08
updated: 2026-11-25
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
rule ([bilinear transform](https://ccrma.stanford.edu/~jos/filters/Bilinear_Transformation.html)), resolving
the resulting delay-free loops algebraically - [[tpt-zdf-filters]]. This "topology-preserving transform" /
"zero-delay feedback" family covers the state-variable, Sallen-Key, Moog ladder
and diode ladder filters. The open questions are stability under audio-rate
parameter modulation and where to put the saturating nonlinearities:

- [[time-varying-filter-stability]] - common quadratic Lyapunov functions survive trapezoidal discretization, giving genuine BIBO proofs for time-varying VA filters.
- [[moog-ladder-filter-models]] and [[ladder-nonlinearity-ablation]] - SPICE-referenced comparison of five digital ladders, and which stage's nonlinearity actually matters.
- [[allpass-clipping-prevention]] - keeping modulated allpass sections from overshooting unity.

### State-space and DAE circuit solvers
Nodal or state-space formulations (MNA, DAE) solved per sample with Newton
iteration or a surrogate. SPICE is the reference; the cost is the nonlinear
solve.

- [[state-space-circuit-solvers]] - a quadratic program with a linear surrogate constraint replaces the Newton loop, with the residual driving adaptive step size.

### Wave digital filters
The scattering/wave-variable route to modular circuit emulation. WDFs are
covered canonically in the waveguide wiki - see [[wave-digital-filters]],
[[wdf-adaptors]], [[wdf-elements]], [[wdf-applications]] and
[[wdf-code-generation]] - and the three
DAFx26 WDF papers are catalogued there and cross-linked from
[[entities/source-papers#wave-digital-filter-papers-catalogued-in-waveguide_synthesis]].

### Antialiasing
Any static nonlinearity applied at the audio rate generates harmonics above
Nyquist that fold back. The three standard answers are oversampling, bandlimited
correction functions (BLEP/BLAMP/polyBLEP) and **antiderivative antialiasing**
(ADAA), which convolves the nonlinearity with a reconstruction kernel
analytically.

- [[antiderivative-antialiasing]] and [[polyadaa]] - ADAA fundamentals, then ADAA beyond linear reconstruction via Chebyshev approximation of the nonlinearity.
- [[alias-free-oscillator-sync]] and [[hasy-asic]] - oscillator sync made alias-free by construction in the Fourier-series domain, and the 65 nm chip that runs it.
- [[entities/source-papers#paper-argentieri-arbitrary-polygon-oscillator-2026]] - polyBLAMP from runtime geometry plus adaptive oversampling.
- [[entities/source-papers#paper-dittmar-pulsetable-synthesis-2026]] - pulsetable (pulse-forming) synthesis of wind tones, an oscillator model outside the alias-correction family.

### Black-box neural VA
Recurrent (LSTM/GRU) and convolutional (WaveNet-style) models trained on
input/output recordings, conditioned on the device's controls. Open problems:
artifacts under time-varying conditioning, sample-rate dependence, and cost.

- [[neural-va-architectures]] - stability-regularized deep conditioned LSTMs with a gammatone-filterbank loss.
- [[fourier-neural-operators-va]] - Fourier neural operators for sample-rate-independent inference.

### Grey-box hybrids
Neural components embedded in a physical structure: an MLP or KAN solving the
nonlinear junction inside a WDF
([[waveguide_synthesis/entities/source-papers#paper-giampiccolo-kan-vs-mlp-wdf-2026|KANs vs MLPs]]),
a differentiable circuit or synthesizer fitted
by gradient descent, a compressor whose detector is measured rather than
guessed.

- [[entities/source-papers#paper-thompson-compressor-control-voltage-2026]] - train and evaluate against the measured gain-reduction control voltage, not proxy audio metrics (background: [why compression is nonlinear](https://ccrma.stanford.edu/~jos/filters/Why_Dynamic_Range_Compression.html)).
- [[entities/source-papers#paper-braun-fm-shared-embeddings-2026]] and [[entities/source-papers#paper-tabata-fm-parameter-estimation-2026]] - inverse problems for FM synthesizers (background: [FM synthesis](https://ccrma.stanford.edu/~jos/sasp/Frequency_Modulation_FM_Synthesis.html); see also [[waveguide_synthesis/concepts/loopback-fm-time-varying-delay|loopback FM]]).

### Deployment constraints
A VA algorithm ships inside an audio callback. What decides feasibility is not
average throughput but worst-case time per block, and whether the inference path
is callback-safe at all.

- [[real-time-neural-inference-deployment]] - inference backends benchmarked under real DAW contention, by tail latency and deadline misses.
- [[mobile-gpu-neural-audio]] - when a mobile integrated GPU helps and when per-call overhead eats the gain.
- [[neural-model-compression]] - 90% magnitude pruning plus a sparse engine puts a WaveNet amp model on an iPhone CPU.

## See also

- [[entities/source-papers]] - the full DAFx26 catalog for this wiki.

## JOS online books
- [[jos_books/entities/filters-book|Filters]]: [Bilinear A/D Transformation](https://ccrma.stanford.edu/~jos/filters/Digitizing_Analog_Filters_Bilinear.html), [Analog Filters](https://ccrma.stanford.edu/~jos/filters/Analog_Filters.html)
- [[jos_books/entities/pasp-book|PASP]]: [Virtual Analog](https://ccrma.stanford.edu/~jos/pasp/Virtual_Analog.html), [Lumped Models](https://ccrma.stanford.edu/~jos/pasp/Lumped_Models.html), [Nonlinear Elements](https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Elements.html), [Wave Digital Filters](https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Filters_I.html)

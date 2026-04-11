# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-04-10 | Total pages: 19

## Entities
- [[realimpact-dataset]] — 150k calibrated impact recordings from 50 objects; ML training resource

## Concepts
- [[damping-models]] — viscous, thermoelastic, and frequency-dependent damping; per-mode decay rates and DSP pole placement
- [[excitation-signals]] — impulse, noise burst, and continuous excitation; modal coupling via mode shapes at drive point
- [[fem-bem-for-modal-synthesis]] — computing mode shapes and frequencies numerically from CAD + material data
- [[friction-synthesis]] — continuous rubbing/bowing sounds via nonlinear feedback loop on resonator bank
- [[gpu-modal-synthesis]] — massively parallel resonator bank on GPU; enables ~100k+ modes in real time
- [[impact-synthesis]] — impact sound from Hertz contact model + modal response; core use case of modal synth
- [[material-properties-and-modes]] — how E, rho, eta affect mode frequencies, damping, and perceptual character
- [[modal-analysis-measurement]] — experimental extraction of mode parameters via FRF + pole-fitting algorithms
- [[modal-synthesis-overview]] — top-level: physics-based synthesis by summing N decaying sinusoidal modes
- [[mode-shapes-and-eigenvalues]] — math of eigenmodes: K*phi = omega^2*M*phi; modal superposition; orthogonality
- [[realtime-modal-synthesis]] — CPU/GPU strategies, perceptual mode reduction, LOD, latency budget for interactive synthesis
- [[resonator-bank-implementation]] — N parallel biquad IIR filters implementing modal coordinates; cost and GPU SIMD
- [[rigid-body-sound-synthesis]] — real-time physics-engine + modal synth pipeline for games/VR
- [[nonlinear-modal-synthesis]] — mode coupling, collisions, tension modulation; energy-conserving numerical methods
- [[coupled-structures]] — string-bridge-body coupling, commuted synthesis, state-space multi-I/O approach
- [[ml-modal-parameter-estimation]] — neural mode prediction, differentiable modal synthesizers, audio-domain training
- [[radiation-and-directivity]] — radiation efficiency vs. mode shape, acoustic transfer, directivity patterns
- [[stochastic-modal-synthesis]] — SEA, high-frequency mode density, noise-band synthesis above mode resolution limit

## Comparisons
- [[waveguide-vs-modal]] — delay-line waveguide vs. eigenmode resonator bank: equivalence, tradeoffs, hybrid use

## Queries

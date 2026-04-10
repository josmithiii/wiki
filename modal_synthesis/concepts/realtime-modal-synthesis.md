---
title: Real-Time Modal Synthesis
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [realtime, modal-synthesis, dsp, gpu, physical-modeling, resonator, impact]
sources:
  - https://ccrma.stanford.edu/~jos/pasp/
  - https://dl.acm.org/doi/10.1145/1276377.1276416
---

# Real-Time Modal Synthesis

Running modal synthesis at audio rates (44.1-96 kHz) with low latency (<10 ms)
requires careful management of mode count, CPU/GPU budget, and parameter update strategies.

## The Core Bottleneck

Each mode = 1 biquad IIR (6 multiply-adds per sample at 44.1 kHz):
- 100 modes: 600 MFLOPS — trivially real-time on CPU
- 10,000 modes: 60 GFLOPS — needs GPU or SIMD
- 100,000 modes: 600 GFLOPS — GPU only, carefully optimized

Practical objects: ~100-500 modes audible to humans above noise floor.
Full physics (FEM): thousands of modes, but perceptually only ~50-200 matter.

## Perceptual Mode Reduction

Critical optimization: discard inaudible modes before synthesis.

### Frequency Masking
- Modes above ~16 kHz inaudible; above ~10 kHz, low-amplitude modes masked
- Remove modes with omega_n > 2*pi*16000

### Amplitude Thresholding
- Modal amplitude a_n = |phi_n(x_out)| * |phi_n(x_in)| / (m_n * omega_n)
- Modes with a_n < threshold (e.g., -60 dB relative to peak) removed
- Tyically cuts 60-80% of FEM modes for perceptual transparency

### Temporal Decay Pruning
- Highly damped modes (T60 < ~5 ms): pre-compute as single sample
- Retain only modes with T60 > audio-buffer-length for run-time integration

Result: 1000-mode FEM object often reduces to 50-200 run-time modes.

## CPU Real-Time Strategies

### SIMD Parallelism
- Pack 4 (SSE) or 8 (AVX) mode states into single vector register
- All 8 modes advance in lockstep per sample — no branching
- Throughput: ~8x over scalar code for resonator loop

### Resonator Scheduling
- Process resonators in batches matching cache line size
- Sort modes by frequency — improves cache locality for mode parameters
- Interleave left/right ear coupling for binaural output

### Parameter Update Rate
- Mode parameters (omega_n, sigma_n) rarely change during synthesis
- Update at control rate (e.g., every 64 samples) not audio rate
- Exception: Doppler shifts, material morphing — needs smooth interpolation

## GPU Real-Time Strategies

See [[gpu-modal-synthesis]] for full treatment. Key points:

- Each thread handles 1 mode; blocks of 256 threads cover 256 modes
- Memory layout: structure-of-arrays (SoA) for coalesced reads
- Latency: kernel launch overhead ~20-50 us — fine for 64-sample buffers at 48 kHz
- Excitation broadcast: single value written to all threads simultaneously
- Output: parallel reduction (sum) of all mode outputs

## Dynamic Mode Management

For interactive/game contexts, objects appear and disappear:

### Active Mode Budget
- Set hard cap N_max (e.g., 256 CPU, 16384 GPU)
- Scheduler assigns modes to active objects based on proximity/importance
- Low-importance objects get fewer modes (level-of-detail)

### Level-of-Detail (LOD) for Modes
- LOD 0 (close/prominent): full 200-mode model
- LOD 1 (medium): 50 modes (top by amplitude)
- LOD 2 (distant): 10 modes (fundamentals only)
- LOD 3 (very far): simple bandpass filter (no individual modes)
- Smooth LOD transitions: crossfade between mode counts over ~50 ms

### Mode Onset/Offset
- New impact: activate mode set, initialize with contact force initial conditions
- Natural mute: remove modes when amplitude < -80 dB (inaudible)
- Forced mute (budget exceeded): fade over 10-20 ms then zero

## Latency Budget

| Component | Typical Budget |
|---|---|
| Input device (ADC) | 1-5 ms |
| Audio buffer size | 64-256 samples (1.3-5.8 ms @ 44.1kHz) |
| Modal computation | <1 ms (CPU), <0.5 ms (GPU) |
| DAC output | 1-5 ms |
| Total target | <10 ms for interactive feel |

- 256-sample buffer = 5.8 ms — acceptable for most games/VR
- 64-sample buffer = 1.5 ms — needed for instrument response

## Parameter Modulation

Real-time parameters that can be modulated:

- Strike position: changes phi_n(x_in) — different modes excited
- Listen position: changes phi_n(x_out) — different timbral balance
- Material morphing: interpolate omega_n, sigma_n between presets
- Contact stiffness (Hertz): controls spectral content via contact duration
- Geometry deformation: re-map mode frequencies (requires pre-computed morphs)

## Relevant Implementations

- Modal: Cycling '74 Max object; ~200 modes on CPU (2000s vintage)
- PhysX Audio: NVIDIA GPU modal synth for game audio (~2009, unreleased)
- Resonance Audio: Google's spatial audio uses simplified modal room model
- Modus: research system (Cook & Scavone) for real-time impact synthesis
- See [[rigid-body-sound-synthesis]] for game-engine integration patterns
- See [[gpu-modal-synthesis]] for GPU architecture details

## Cross-References

- Resonator bank: [[resonator-bank-implementation]]
- GPU scaling: [[gpu-modal-synthesis]]
- Mode count after FEM: [[fem-bem-for-modal-synthesis]]
- Game physics integration: [[rigid-body-sound-synthesis]]

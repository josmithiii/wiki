---
title: GPU Modal Synthesis
created: 2026-04-09
updated: 2026-11-25
type: concept
tags: [gpu, modal-synthesis, realtime, dsp, resonator]
sources:
  - https://graphics.cs.cmu.edu/projects/pat/
  - /l/dttd/NonlinearModalSynthModeCoupling-Poirot-Bilbao-EURASIP-2024.pdf
---

# GPU Modal Synthesis

## Motivation
Modal synthesis is embarrassingly parallel: each of $N$ modes is an independent
2nd-order oscillator. GPUs with thousands of cores are a natural fit.
A CPU handles a few thousand modes in real time (more with SIMD, see
[[realtime-modal-synthesis]]); a GPU pushes to $10^5$ and beyond.

## Parallelization Strategy
Per audio sample:
1. Each GPU thread computes one mode: state update + output contribution
2. Parallel reduction: sum all mode outputs → single sample
3. Transfer result to CPU → DAC

Per audio block (more efficient):
1. Compute block of 64-256 samples for all modes
2. Prefix-sum or tree reduction per sample in the block
3. Single DMA transfer to CPU per block

## Historical Milestones
- Cook (1997): PhISM/PhISEM percussive synthesis; Cook & Scavone (1999): the STK toolkit (CPU, not GPU)
- Zhang, Ye & Pan (2005): "Physically-Based Sound Synthesis on GPUs" (ICEC) - modal synthesis on a pre-CUDA programmable GPU
- James, Barbič & Pai (2006): Precomputed Acoustic Transfer - cheap per-mode radiation at run time
  (not GPU-specific; see [[radiation-and-directivity]])
- Bonneel et al. (2008): "Fast Modal Sounds with Scalable Frequency-Domain Synthesis" - an STFT-domain alternative
- Skare & Abel (DAFx 2019): real-time crash cymbals from a GPU-accelerated modal filterbank

## GPU Implementation
Before CUDA (2007), GPU sound synthesis meant shader programs (e.g. Zhang et al. 2005).
In compute-kernel terms the structure is:
- Map $N$ modes → $N$ threads (formerly fragment-shader instances)
- Mode state: $(s_1, s_2)$ per thread in global memory
- Coefficients: $(R, \theta, a)$ in constant or texture memory (fast cache)
- Per-sample: each thread does one biquad iteration, writes output to shared mem
- Tree reduction: $O(\log N)$ depth to sum $N$ outputs
- Bottleneck: reduction, not the filter computation itself

## Modern GPU Considerations
- Warp divergence: avoid conditional branching per mode (use amplitude culling at block level)
- Memory: 100k modes × 2 floats state = 800 KB - small enough that memory bandwidth is not the bottleneck
- Mixed precision: float32 for state update, accumulation in float64 if needed
- CUDA vs Metal vs Vulkan Compute: all viable; CUDA most mature for this

## Latency Challenge
Real-time audio requires low latency (typically 5-15 ms / 256-512 samples at 44.1 kHz).
GPU adds overhead:
- CPU→GPU data transfer (contact events, parameter updates): 0.1-1 ms
- Kernel launch overhead: ~10 microseconds
- GPU→CPU audio readback: 0.1-0.5 ms
Total added GPU latency: 0.5-2 ms — acceptable for most applications.

## Comparison with CPU
| Metric | CPU (optimized SIMD) | GPU (CUDA) |
|--------|---------------------|------------|
| Max real-time modes (2023) | ~5,000-10,000 | ~500,000-1,000,000 |
| Latency | < 1 ms | 1-5 ms |
| Power | Low | Higher |
| Complexity | Medium | High |

## Practical Limits
Even with GPU, there are synthesis limits:
- Physics engine contact event rate: 10k-100k events/sec typical
- Each new impact re-excites that object's modes; all active modes must be summed
- With 1000 objects × 200 modes each, summing 200k oscillators per sample
- Amplitude culling essential: 95%+ of oscillators below audible threshold at any time

## Related Concepts
- [[resonator-bank-implementation]] — CPU-side biquad bank (baseline)
- [[rigid-body-sound-synthesis]] — main use case for GPU synthesis
- [[impact-synthesis]] — typical workload driving GPU synthesis
- [[realtime-modal-synthesis]] — CPU/GPU budgets, mode pruning and level of detail

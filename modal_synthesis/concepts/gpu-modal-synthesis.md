---
title: GPU Modal Synthesis
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [gpu, modal-synthesis, realtime, dsp, resonator]
sources: []
---

# GPU Modal Synthesis

## Motivation
Modal synthesis is embarrassingly parallel: each of N modes is an independent
2nd-order oscillator. GPUs with thousands of cores are a natural fit.
CPU synthesis is limited to ~1000-2000 modes in real time; GPU pushes to ~100,000.

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
- Cook & Scavone (1999): early GPU sound synthesis exploration
- James, Barbic & Pai (2006): 60,000 modes in real time on NVIDIA GeForce 7800
- Nikunen & Virtanen (2013): GPU-accelerated synthesis of room impulse responses
  using modal superposition

## CUDA Implementation (2006-era)
Rath & Rocchesso (2005) and James (2006) approaches:
- Map N modes → N CUDA threads
- Mode state: (s1, s2) per thread in global memory
- Coefficients: (R, theta, a) in constant or texture memory (fast cache)
- Per-sample: each thread does one biquad iteration, writes output to shared mem
- Tree reduction: O(log N) to sum N outputs
- Bottleneck: reduction, not the filter computation itself

## Modern GPU Considerations
- Warp divergence: avoid conditional branching per mode (use amplitude culling at block level)
- Memory bandwidth: 100k modes × 2 floats state = 800 KB → fits in L2 cache
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
- Each new impact starts N_modes new oscillators; they must be summed
- With 1000 objects × 200 modes each, summing 200k oscillators per sample
- Amplitude culling essential: 95%+ of oscillators below audible threshold at any time

## Related Concepts
- [[resonator-bank-implementation]] — CPU-side biquad bank (baseline)
- [[rigid-body-sound-synthesis]] — main use case for GPU synthesis
- [[impact-synthesis]] — typical workload driving GPU synthesis

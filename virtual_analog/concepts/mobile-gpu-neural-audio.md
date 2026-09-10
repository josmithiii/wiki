---
title: Mobile GPU Neural Audio
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [gpu, real-time, embedded, benchmark, neural-va]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_18.pdf
  - raw/DAFx26_paper_18.txt
---

# Mobile GPU Neural Audio

Can the **integrated GPU** of a mobile SoC accelerate streaming neural audio under
per-callback deadlines? Sometimes - and the deciding factor is architectural
parallelism, not parameter count. Companion to
[[real-time-neural-inference-deployment]], which sets out the deadline model.[^1]

## Setup

Five models from 769 parameters (a dense neural oscillator) to ~6 M (BRAVE, a causal
convolutional VAE), in a custom C++ AudioReach engine on a Qualcomm QCS6490 (Kryo 670
CPU, Adreno 643 iGPU, unified memory), via the QNN backend of the QAIRT SDK, sweeping
batch/block size against the 20.83 us sample period. Where the iGPU helps:

| Model | Regime | Best CPU | QNN GPU | Verdict |
|---|---|---|---|---|
| Neural oscillator (769) | sample-by-sample | RTNeural 0.2 us | 126 us at batch 1, 1.6 us at 1024 | CPU wins |
| AutoGuitarAmp LSTM (1,861) | sample-by-sample | RTNeural 0.43 us | 167.6 us | CPU wins decisively |
| NAM WaveNet (13,802) | block-based | NAMcore 6.3 us | 53 us at 64, 6.1 us at 1024 | parity only at large blocks |
| MS-Wavehax (~500 K) | block-based, 2D depthwise sep. conv | ONNX RT 12.2 us at 1440 (underruns) | 6.1 us at 480, 2.9 us at 1440 | **GPU wins outright** |
| BRAVE (~6 M) | block-based, strided 1D conv | ONNX RT 7.9 us at 1024, 25 underruns | 10.7 us, **0 underruns** | GPU preferable |

- Recurrent models are the worst case: no temporal parallelism, so per-call overhead
  dominates with nothing to amortize it against.
- Parameter count alone does not predict suitability - *architectural parallelism*
  does. 2D depthwise separable convolutions win at the smallest tested block; 1D
  dilated or strided convolutions need large blocks.
- **Borrowed parallelism** is the trap: inflating the buffer to feed the GPU buys
  throughput with interaction latency, and above ~10 ms that is unusable musically.
- QNN pre-compiles the graph and pre-allocates memory, so GPU execution is a
  deterministic kernel-dispatch sequence - more predictable than ONNX Runtime on CPU,
  which can allocate during inference. BRAVE shows this directly: similar mean times,
  dozens of CPU underruns versus zero on GPU.
- Caveat: GPU runs settle into one of two performance modes at initialization (NAM at
  block 256: ~13 us versus ~19 us, about 45 % apart), which no QNN setting fixed.
- Extrapolating up the Snapdragon line, CPU cores roughly double while per-call GPU
  overhead does not shrink proportionally, so the GPU-advantage threshold likely moves
  to still larger and more parallel models.

**Limitations:** one vendor SDK and one mid-range board, no host-contention scenario,
and the Hexagon NPU (12 TOPS, requiring INT8/INT16 quantization of unknown audio
impact) is left for future work. No thermal throttling was observed (peak ~81 C), but
phones may throttle earlier under skin-temperature limits.

## See also

[[real-time-neural-inference-deployment]] - [[neural-model-compression]] -
[[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-huang-snapdragon-gpu-neural-audio-2026]] - Huang, Srinivasan, van Troyer, Zappi, "Benchmarking Integrated GPU Acceleration of Real-Time Neural Audio Inference on Snapdragon", DAFx26.

---
title: Real-Time Neural Inference Deployment
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [real-time, benchmark, neural-va, plugin, apple-silicon]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_16.pdf
  - raw/DAFx26_paper_16.txt
---

# Real-Time Neural Inference Deployment

Whether a neural VA model ships is decided by the audio callback, not by average
throughput. This page gives the deadline model and the Apple Silicon benchmark under
realistic DAW contention;[^1] [[mobile-gpu-neural-audio]] covers the mobile iGPU.

## The callback-deadline model versus real-time factor

- The driver invokes the callback every $B/f_s$ seconds; the DAW traverses its whole
  plugin graph *synchronously* inside that window. Miss it and the output buffer
  underruns - an audible glitch, counted as a hardware **xrun**. Typical low-latency
  budgets: $B = 64$-$128$ at 48 kHz is 1.3-2.7 ms; 64-1024 samples spans 1.3-21.3 ms.
- **Real-time factor** (RTF = compute time / audio duration, or / deadline) is the
  usual ML-community metric and is *not sufficient*: it is a mean over a long buffer,
  while feasibility depends on the worst case of every single callback under cache,
  memory-bandwidth and scheduling pressure. Report **tail percentiles** (p95, p99,
  p99.9), xruns, and - for asynchronous wrappers - inference underruns.
- GPU and NPU paths are usually not callback-safe: kernel launch, transfer and
  synchronization overhead can exceed the deadline itself at small buffers, and
  consumer NPU APIs expose no low-latency callback path.

## Backends compared (Apple Silicon study)

Models: LSTM, TCN and WaveNet at three sizes (841 to 93,745 parameters), all
stateful, mono, 48 kHz. Machine: MacBook Air M3, macOS Tahoe 26.4.[^1]

| Backend | RT-safe | AMX | Added latency |
|---|---|---|---|
| BNNSGraph (Core ML AOT graph compiler) | yes | native | 0 |
| RTNeural (Eigen / XSIMD) | yes | no | 0 |
| LibTorch | no | via Accelerate BLAS | 0 |
| ONNX Runtime (MLAS, NEON only) | no | no | 0 |
| anira wrapping LibTorch / ONNX RT | audio thread only | inherited | +1 buffer |

- **BNNSGraph** compiles the whole model graph ahead of time - operation fusion, weight
  repacking, memory-copy elimination - and reaches the on-chip matrix co-processor
  (AMX), which unlike a GPU has no launch, transfer or sync cost. Audio models sit in
  the sweet spot: an LSTM hidden state of 20-96, or 8-48 conv channels, is too small
  for a GPU to amortize dispatch but big enough for AMX to beat NEON. RealtimeSanitizer
  reported zero violations over 100 invocations, matching Apple's no-alloc/no-lock claim.
- **anira** moves inference to worker threads behind a lock-free ring buffer: the
  audio thread never blocks, at the cost of one buffer of latency and a different
  failure mode (zeroed output = inference underrun).

## Under DAW contention

The contention harness builds real mix sessions in **Tracktion Engine** driven through
the BlackHole virtual driver: Dimension A is one neural plugin plus conventional Audio
Unit chains on 0/8/24/36 of 36 tracks; B scales neural instances 1-16 in parallel; C
varies serial insert depth 1-7 on one track. Large models, buffer 128 (2.67 ms):

| Backend / model | isolated RTF | p99 utilization, $c=0$ | xruns | p99 at $c=36$ |
|---|---|---|---|---|
| BNNSGraph TCN-L | 0.022 | 13.7 % | 0 | 14.3 % |
| RTNeural-XSIMD TCN-L | 0.211 | **158.5 %** | **355** | 88.0 % |
| RTNeural-XSIMD LSTM-L | 0.089 | 79.9 % | 0 | 81.7 % |
| anira (either backend) | - | $\le 0.9$ % (audio thread only) | 0 | $\le 0.7$ % |

- The central finding: a model that looks like 5x real time in isolation produced
  **355 xruns** under an actual Core Audio callback with *zero* contention tracks.
  Isolated RTF is not a proxy for real-time robustness.
- BNNSGraph never exceeded 20 % p99 for large models at buffer 128 and stayed flat
  across contention levels; isolated throughput advantage grows with buffer size
  (TCN-Large: 3x RTNeural at buffer 32, 25x at 1024) and with model size.
- For LSTM, RTNeural-Eigen beats BNNSGraph at small/medium hidden sizes (154x vs 149x
  RT small; 64x vs 21x medium) because recurrence is inherently sequential; at
  $H = 96$ the per-sample matrices are wide enough for AMX to win (19x vs 13x).
- Scaling (Dimension B, TCN-L): BNNSGraph 4.0 % p99 at 1 instance rising to 27.1 % at
  16, 1 xrun; RTNeural produces xruns from 4 instances (3) up to 312 at 16;
  anira-LibTorch keeps zero xruns but accumulates 14,022 TCN-L inference underruns at 16
  instances (44,324 for LSTM-L), while anira-ONNX RT has zero - its lower per-inference
  cost, not anira's scheduling, decides that failure mode.
- Serial insert depth (Dimension C) barely matters: neural p99 moves under one
  percentage point from depth 1 to 7. Parallel instance count is the real pressure.

**Limitations:** one M3 machine, mono audio, a flat mix topology, a virtual audio
driver, anira's default shared worker pool, and ONNX TCN/WaveNet effectively stateless
across calls; memory footprint not measured.

## See also

[[mobile-gpu-neural-audio]] (the same argument on a mobile iGPU) -
[[neural-model-compression]] (attack the model, not the runtime) -
[[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-balasubramaniam-apple-silicon-neural-audio-2026]] - Balasubramaniam, Ramachandran, Timoney, "Real-Time Neural Audio on Apple Silicon: Benchmarking Inference Frameworks Under Realistic DAW Contention", DAFx26.

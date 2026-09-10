---
title: Linear-Phase Octave Filter Bank Implementation
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [filter-banks, multirate, fir-design, applications, downsampling]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_44.pdf
  - spectral_processing/raw/DAFx26_paper_44.txt
---

# Linear-Phase Octave Filter Bank Implementation

An implementation study, not a filter-design one: how to map the
multistage linear-phase octave filter bank of Bruschi et al. (2022)
onto a multicore edge SoC so that memory traffic, task synchronization
and *energy* are handled, not just multiply-accumulates.[^badia-2026]

## The structure

Cascade of **stretched (IFIR-style) FIR stages** with complementary
band splitting - see [[multirate-filter-banks]] and
[[window-design-methods]]. With a prototype half-band FIR of
$n_\mathrm{coef}$ taps and group delay $D=(n_\mathrm{coef}-1)/2$,
$N_f$ cascaded stages produce $N_f+1$ bands (the paper's figure uses
$N_f=9$, 10 bands):

- Stage $f$ applies $H_\mathrm{LP}(z^{s})$ with stretch $s=2^{f}$, evaluated as
$$x^{(f)}_\mathrm{LP}[n]=\sum_{k=0}^{n_\mathrm{coef}-1} b[k]\,x^{(f)}[n-ks],$$
so the MAC count per output sample is $n_\mathrm{coef}$ **independent of the stretched support** - the stretch only changes which past samples are read, and the zero-inserted coefficients are never materialized.
- The complementary (high) band is a subtraction from the delayed stage input, $x^{(f)}_\mathrm{band}[n]=x^{(f)}[n-D_f]-x^{(f)}_\mathrm{LP}[n]$ with $D_f=2^{f}D$. Linear phase is preserved across all outputs.
- Bands are time-aligned at the summation node by the shift $\Delta_f=\big(2^{N_f}-2^{f+1}\big)D$, applied not by storing delayed subbands but by accumulating at a shifted output index $p=n+\Delta_f$:
$$y[p] \mathrel{+}= \big(x_\mathrm{del}-x_\mathrm{LP}\big)\,g[N_f-f].$$

## Sequential realization

- **Blocked streaming schedule**: loop blocks, then stages, then samples in the block; two length-$B$ ping-pong buffers hold the current stage input and the low-pass output passed downstream, keeping intermediate data contiguous.
- **Compact circular state** per stage instead of full-length intermediate signals: a write pointer advances modulo the state length, so the delay line is never shifted. Cache locality up, spatial cost down.
- Ordering matters for correctness: `ReadDelay` **before** the low-pass update, then the aligned accumulation. The blocked traversal changes execution order and locality but not the mathematics.

## OpenMP task pipeline

One block at one stage is the unit of concurrent work, so the pipeline
depth is $N_f$ and several blocks are in flight at different stages.
Three task types, with dependencies carrying the semantics:

| Task | Dependencies | Role |
|---|---|---|
| `LoadBlock` | `depend(out: X0,b)` | inject input block |
| `StageBlockTask` | `depend(in: Xf,b, out: Xf+1,b, inout: Sf)` | one stage on one block |
| `ReduceOutputSegment` | `depend(in: XNf,b)` | merge thread-local output |

- The `in`/`out` pair encodes the **inter-stage** cascade order per block; the `inout: Sf` token serializes tasks of the *same* stage across consecutive blocks, preserving per-stage streaming state. No fine-grained locking inside the filtering hot path.
- Direct updates of the global $y$ would race (aligned indices overlap between tasks), so each thread accumulates into a private $y_\mathrm{local}[t]$ and a reduction task flushes $y[p]\mathrel{+}=\sum_t y_\mathrm{local}[t][p]$ over $[i_\mathrm{start},i_\mathrm{end})$, zeroing as it goes. Correct because all alignment shifts are nonnegative and the dependency closure guarantees the segment is complete.
- Intermediate block signals live in per-stage **sliding windows** of $W$ samples, $W$ a power of two for bitmask modulo, sized to hold all in-flight blocks.
- Stage tasks are nearly equal in cost (same MAC count), so the pipeline is well balanced; the reduction task's cost grows linearly with thread count.
- A "fused-load" variant folds `LoadBlock` into stage 0, removing one task, one copy and one dependency per block. It helps only at small/intermediate block sizes.

## Jetson Orin Nano numbers

Six-core Arm Cortex-A78AE, 8 GB LPDDR5, JetPack 5.1.1, GCC 9.4.0
`-O3 -march=native`, OpenMP 4.5, power sampled at 10 Hz with `pmlib`
(dynamic power = measured minus idle baseline at the same frequency).

- Sequential: 0.81 s per million samples at block size 1, 0.84 s at 16384, i.e. **> 1.18 M samples/s** at every tested block size.
- Parallel: below 32 samples per block, task overhead sinks the pipeline (worse with 6 threads than 3). With 3 threads the speedup approaches the ideal 3; with 6 threads it exceeds **4.5x**. Best balance at blocks of 1024-2048.
- Frequency scaling, 2048-sample block, one core: 23.5 ms at 115.2 MHz down to 1.8 ms at 1510.4 MHz (13x); minimum 0.3 ms with six cores at maximum frequency.
- Dynamic CPU power ranges from 0.52 W (one core, minimum frequency) to 2.39 W (six cores, maximum).
- **Energy is minimized at neither extreme**: 0.43 mJ per 2048-sample block with one core at 1036.8 MHz, about 0.5 mJ with six cores in the same frequency range, and a non-monotonic surface peaking at 3.60 mJ for two cores at the minimum frequency - the classic DVFS effect where time grows faster than power falls.

## Limits

- One SoC, one filter-bank structure, and a block-based kernel on preallocated buffers rather than a real audio callback (no host scheduling, wake-up cost or deadline enforcement).
- Optimal block size, thread count and frequency are platform-specific; SIMD, coefficient symmetry and alternative state layouts are untried.
- The fully linear-phase structure has a fixed group delay, so it suits phase-coherent equalization and crossovers rather than ultra-low-latency monitoring.
- C/OpenMP source published at `github.com/josembadia/hp-multistage-filter`.

## Related Concepts
- [[multirate-filter-banks]] - tree-structured and complementary band splitting
- [[window-design-methods]] - prototype FIR design
- [[spectral-audio-applications]] - equalization and crossover use cases
- [[entities/source-papers#paper-badia-octave-filter-bank-parallelism-2026]] - catalog entry

[^badia-2026]: Jose M. Badia, Jose A. Belloch and Vesa Valimaki, "Exploring Parallelism and Energy Efficiency in a Multistage Linear-Phase Octave Filter Bank," *Proc. DAFx26*, Cambridge MA, Sept. 2026, pp. 356-363. Distilled in [[entities/source-papers#paper-badia-octave-filter-bank-parallelism-2026]].

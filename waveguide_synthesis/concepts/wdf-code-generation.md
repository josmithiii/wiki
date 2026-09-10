---
title: WDF Code Generation
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [waveguide, scattering, dsp, realtime, faust, comparison, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_23.pdf
  - raw/DAFx26_paper_23.txt
---

# WDF Code Generation

Treating wave digital circuit modelling as a **compilation** problem rather than a
library problem: a declarative circuit language, a static compiler and a minimal
runtime, reaching near the theoretical execution bound.[^chowdhury]

## Why libraries pay

Object-oriented WDF libraries encapsulate each element and adaptor as an object. Two
costs follow: much per-object data need not persist between samples yet is stored
anyway, and values are duplicated across elements of the same circuit. Both inflate
per-sample memory traffic, hurt cache locality and block compiler optimisation. RT-WDF
adds virtual dispatch and pointer chasing on top; FAUST `wdmodels` fixes topology at
translation time but leaves no control over memory layout; `chowdsp_wdf`'s
template-metaprogramming path removes most dispatch but still encodes the circuit as a
type hierarchy, which constrains layout. The ideal stores only minimal persistent state.

## The toolchain

`wdf_compiler` (MIT-licensed, written in Jai, emitting Jai, C++, C or Rust) has three parts.
- **A declarative DSL** with four sections: `circuit` is the WDF connection tree written
  as declarations with children, `inputs` and `outputs` name the source and probe
  elements, and `meta` carries the namespace, extra sources for custom elements, and
  which specialised `calc_impedances` variants to emit. Values take metric prefixes.
- **A static compiler** emitting three data types and two method families: `Params`
  (component values, `constexpr` when static), `Impedances` (read-only
  per-parameter-change data - port impedances, adaptor coefficients), `State` (the only
  genuinely persistent data, e.g. a capacitor's $z^{-1}$), plus `calc_impedances` and
  `process`. Extra `calc_impedances` variants update only the components whose
  parameters change often. Voltage waves throughout; storage elements discretised by
  the trapezoid rule by default, with an alpha-transform capacitor available.
- **A minimal runtime** for elements that resist generation: diodes and antiparallel
  diode pairs via the Werner et al. model with D'Angelo's Lambert-$W$ approximation, a
  quadric-surface triode, and SIMD helpers (SSE, NEON) for R-type adaptors.

For an RC lowpass the generated code carries **one** state variable and one
impedance variable; the equivalent `chowdsp_wdf` model carries about 20.

Two further tricks. **Circuit reduction** merges elements where possible (series
resistors, an R+C pair), skipping any element whose voltage or current is a declared
output; on a purpose-built test circuit this cuts instructions per sample below 25% and
cycles below 50% of the unreduced model. And the 3-port series adaptor is emitted in a
**2-multiply** form
$$b_1 = a_1 - \tfrac{R_1}{R_p}(a_0 - b_0), \qquad b_2 = -a_0 - a_1 + \tfrac{R_1}{R_p}(a_0-b_0),$$
so $b_1$ and $b_2$ have no mutual dependency and issue in parallel on a superscalar CPU -
faster than the classic 1-multiply form (15.09 vs 19.53 cycles/sample) even though it
does more multiplies.

## The performance score

Given a circuit topology and the target CPU's instruction tables, estimate cycles per
sample under a latency bound $L$ and a throughput bound $T$; for measured $M$,
$$S = \frac{L - M}{L - T},$$
so $S = 0\%$ is ideal latency-bound and $S = 100\%$ ideal throughput-bound. Negative means
worse than latency-bound; above 100% means circuit reduction removed work the bound
assumed.

## Measurements

Apple M1 Pro and AMD Zen 4, Clang 20.1.6, `-std=c++20 -O3`; four circuits (RC lowpass,
diode clipper, pre-amp EQ, Baxandall EQ, the last needing an R-type adaptor).
`wdf_compiler` was fastest on all four circuits on both CPUs.

| Circuit (Apple M1, cycles/sample) | RT-WDF | wdmodels | chowdsp_wdf | wdf_compiler |
|---|---|---|---|---|
| RC lowpass | 72.07 | 19.04 | 22.09 | **4.42** |
| Pre-amp EQ | 346.18 | 73.30 | 66.33 | **59.18** |
| Diode clipper | - | 374.53 | 131.78 | **112.79** |
| Baxandall EQ | 588.16 | 59.23 | 65.55 | **36.56** |

Performance scores: RT-WDF is negative throughout (-82% to -190%); the others mostly
exceed 50%; `wdf_compiler` reaches 99.9% (M1) and **103.6%** (Zen 4) on the RC lowpass and
about 70-80% on the pre-amp EQ. Max error against `chowdsp_wdf` across the test suite is
$7.12\times10^{-5}$, within single-precision tolerance. Under XSIMD `batch<float>` the
generated code is more than **6x** faster than `chowdsp_wdf`. Generated C++ is usually
fastest of the four output languages; Rust is consistently slowest.

Topology is fixed at compile time, but a prototype plug-in recovers dynamic construction
by watching the description file, re-running the compiler and hot-reloading a dynamic
library in well under a second - not practical with FAUST or heavily templated C++.

## See also
- [[wave-digital-filters]] - the underlying theory
- [[wdf-applications]] - where these models get deployed
- [[wdf-adaptors]] - the series/parallel adaptors being specialised
- [[entities/source-papers#paper-chowdhury-performance-oriented-wdf-2026]] - catalog entry

[^chowdhury]: J. Chowdhury & M. Rau, "Performance-Oriented Wave Digital Circuit Emulation," DAFx26. See [[entities/source-papers#paper-chowdhury-performance-oriented-wdf-2026]].

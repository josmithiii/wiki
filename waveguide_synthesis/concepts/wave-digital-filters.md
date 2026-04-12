---
title: Wave Digital Filters
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [waveguide, scattering, dsp, physical-modeling, impedance]
sources:
  - /l/l420/WaveDigitalFiltersIntro/wdfi-content.tex
  - /l/l420/WaveDigitalFilters/WDFIntro.tex
  - /w/pasp/adaptors.tex
---

# Wave Digital Filters

A wave digital filter (WDF) digitizes lumped physical elements (masses, springs,
resistors) using the bilinear transform and wave variables. Unlike digital
waveguides (distributed 1D propagation), WDFs model lumped systems — but both
use traveling-wave scattering as the interconnection mechanism.

## The Modularity Problem

Goal: digitize each physical element separately, then connect them.

Bilinear-transform digitization of individual elements produces instantaneous
feedthrough (current input appears in current output). Connecting two such
elements creates a **delay-free loop** — each needs the other's output to
compute its own.

Resolving by substitution destroys modularity: coefficients of one element
leak into the other's update equation. Changing the spring constant forces
recomputation of the mass update.

## Wave Variables to the Rescue

Decompose force f and velocity v into traveling-wave components:
  f(t) = f^+(t) + f^-(t)
  v(t) = [f^+(t) - f^-(t)] / R_0

where R_0 > 0 is a free **port wave impedance** parameter per element.

### Element Reflectance
Given driving-point impedance R(s), the force-wave reflectance from port R_0:
  rho(s) = [R(s) - R_0] / [R(s) + R_0]

This is the impedance step over the impedance sum — same formula as
[[scattering-junctions]] but now in the Laplace domain.

## Key Insight: Choosing R_0 to Kill Delay-Free Paths

After bilinear transform, each element reflectance has a delay-free path
proportional to its "instantaneous reflectance." By choosing R_0 to match:

| Element | R(s) | Choose R_0 = | rho(z) |
|---------|------|-------------|--------|
| Mass m | ms | mc | -z^{-1} (pure delay + sign flip) |
| Spring k | k/s | k/c | +z^{-1} (pure delay) |
| Dashpot mu | mu | mu | 0 (matched termination) |

where c = 2/T is the bilinear transform constant.

Each reactive element becomes a **unit delay** — no delay-free path.
Element parameters (k, m) are encoded entirely in the port impedances.

## Connecting Elements: Adaptors

Elements with different port impedances connect via **adaptors** —
memoryless scattering junctions:

- **Parallel adaptor**: common force, velocities sum to zero
  - rho = (R_2 - R_1) / (R_2 + R_1)
- **Series adaptor**: common velocity, forces sum to zero

Since each element is a pure delay and each adaptor is memoryless,
there are **no delay-free loops** in the complete system.

See [[wdf-adaptors]] for full derivation and N-port generalization.

## Properties

- **Energy conservation**: bilinear transform maps lossless elements
  to unit-circle poles; reactive reflectances are allpass
- **Stability**: guaranteed by passivity (element reflectance gain <= 1)
- **Modularity**: changing one element only changes its R_0 and the
  adaptor coefficient — other elements untouched
- **Frequency warping**: omega_d = (2/T) * arctan(omega_0 * T/2)
  — slight pitch error, correctable

## Comparison: Forward/Backward Euler vs. Bilinear Transform

| Method | Explicit? | |lambda| | Modular? |
|--------|-----------|---------|----------|
| Forward Euler | Yes | > 1 (unstable) | Yes |
| Backward Euler | No (implicit) | < 1 (overdamped) | No |
| Bilinear transform | No (implicit) | = 1 (perfect) | No |
| **WDF (bilinear + waves)** | **Yes** | **= 1 (perfect)** | **Yes** |

WDFs achieve the best of all worlds: explicit, stable, energy-conserving,
and modular.

## Related Concepts
- [[wdf-adaptors]] — parallel/series adaptors, N-port, one-multiply form
- [[wdf-elements]] — mass, spring, dashpot, transformer, gyrator, nonlinear
- [[wdf-applications]] — audio circuits, piano hammer, tonehole, nonlinear FX
- [[scattering-junctions]] — same math, different domain (DWG vs. WDF)
- [[waveguide-overview]] — distributed vs. lumped: DWG vs. WDF

## References
[^1]: Fettweis, A. (1986). "Wave Digital Filters: Theory and Practice." Proc. IEEE 74(2).
[^2]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford, Appendix on WDFs.
[^3]: Smith, J.O. III. MUS420 Lectures: "Introduction to Wave Digital Filters" and "Wave Digital Filters."

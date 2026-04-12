---
title: Digital Waveguide Overview
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [waveguide, physical-modeling, delay-line, traveling-wave, dsp]
sources:
  - /w/pasp/delay-waveguide.tex
  - /w/pasp/strings.tex
  - https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguides.html
---

# Digital Waveguide Overview

A digital waveguide (DWG) is a bidirectional delay line at some wave impedance R.
It efficiently simulates 1D acoustic wave propagation — strings, bores, horns —
by directly implementing d'Alembert's traveling-wave solution.

## Core Principle

Any 1D linear acoustic vibration = sum of two opposing traveling waves (d'Alembert, 1747):
- $y(t,x) = y_{\text{right}}(t - x/c) + y_{\text{left}}(t + x/c)$
- A bidirectional delay line holds sampled versions of both components
- Physical variables (force, pressure, velocity) = sum of left + right components

## Physical Outputs and Inputs

**Output** (observation): sum the two delay-line taps at the observation point
- $y_{\text{physical}}(n) = y_{\text{right}}(n) + y_{\text{left}}(n)$ at the tap position

**Superimposing input** (ideal pluck): add equal disturbance to both delay lines
- Graph-theoretic transpose of the output (transposed taps)

**Interacting input** (reed, bow): input depends on incoming wave state
- Incoming amplitude = sum of approaching traveling-wave components
- Outgoing disturbance computed from nonlinear interaction function
- Models guitar plectra, violin bows, woodwind reeds

## From Delay Loop to Instrument

1. **Infinite string**: single bidirectional delay line
2. **Finite string** (rigid terminations): delay-line loop (sign inversion at each end)
3. **Damped string**: insert loop filter $G(z)$ with $|G(e^{j\omega})| \le 1$
4. **Stiff string**: add allpass dispersion filter in the loop
5. **Excited string**: pluck/strike/bow via input junction

This progression yields the Karplus-Strong / Extended Karplus-Strong family.

## Wave Variables

Two common choices:
- **Displacement/velocity waves**: $y^+(n)$, $y^-(n)$ — sum gives displacement
- **Force/pressure waves**: $f^+(n)$, $f^-(n)$ — sum gives force; difference gives velocity
- Choice affects sign conventions at scattering junctions

## Wave Impedance

- String: $R = \sqrt{K \epsilon}$ where $K$ = tension, $\epsilon$ = mass density
- Acoustic tube: $R = \rho c / A$ where $A$ = cross-sectional area
- Needed for connecting waveguides to each other or to lumped elements
- See [[scattering-junctions]] for how impedance mismatches create reflections

## Computational Efficiency

A digital waveguide loop of length $N$ replaces:
- $N$ second-order resonators (modal synthesis) for a quasi-harmonic series
- $N^2$ multiply-adds per sample (finite-difference grid)
with just $N$ delay samples + 1 filter evaluation per sample period.

## Relation to Other Methods

| Method | Represents | Cost | Strengths |
|--------|-----------|------|-----------|
| Digital waveguide | Traveling waves | $O(N)$ per string | Exact for 1D; commutes losses |
| Finite difference | Grid samples | $O(N)$ but higher constant | Handles 2D/3D, nonlinear |
| Modal synthesis | Eigenmodes | $O(M)$ per mode | Any geometry; independent modes |

See [[waveguide-vs-modal]] in the modal_synthesis wiki for detailed comparison.

## Related Concepts
- [[scattering-junctions]] — connecting waveguides at impedance discontinuities
- [[delay-line-techniques]] — interpolation, variable delay, allpass tuning
- [[string-modeling]] — application to plucked/struck/bowed strings
- [[bore-modeling]] — application to wind instrument tubes

## References
[^1]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.
[^2]: d'Alembert, J. (1747). Recherches sur la courbe que forme une corde tendue.

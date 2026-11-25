---
title: Digital Waveguide Overview
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [waveguide, physical-modeling, delay-line, traveling-wave, dsp]
sources:
  - /w/pasp/delay-waveguide.tex
  - /w/pasp/strings.tex
  - https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguides.html
  - https://ccrma.stanford.edu/~jos/pasp/Ideal_Vibrating_String.html
---

# Digital Waveguide Overview

A digital waveguide (DWG) is a bidirectional delay line at some wave impedance $R$.[^1]
It efficiently simulates 1D acoustic wave propagation — strings, bores, horns —
by directly implementing d'Alembert's traveling-wave solution.

## Core Principle

Any 1D linear acoustic vibration = sum of two opposing traveling waves (d'Alembert, 1747[^2]):
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
- **Force/pressure waves**: $f^+(n)$, $f^-(n)$ — sum gives force; difference gives $R$ times velocity
- Choice affects sign conventions at scattering junctions

## Wave Impedance

- String: $R = \sqrt{K \epsilon}$ where $K$ = tension, $\epsilon$ = mass density
- Acoustic tube: $R = \rho c / A$ where $A$ = cross-sectional area
- Needed for connecting waveguides to each other or to lumped elements
- See [[scattering-junctions]] for how impedance mismatches create reflections

## Computational Efficiency

A lossless waveguide costs $O(1)$ per sample (a fetch, a store and a pointer
update), independent of its length. A string loop of $N$ delay samples replaces:
- about $N/2$ second-order resonators (modal synthesis), one per partial below Nyquist
- $O(N)$ multiply-adds per sample on a finite-difference grid
with $N$ samples of memory + 1 loop-filter evaluation per sample - for $N = 500$,
[three orders of magnitude](https://ccrma.stanford.edu/~jos/pasp/Computational_Savings.html) less work.

## Relation to Other Methods

| Method | Represents | Cost | Strengths |
|--------|-----------|------|-----------|
| Digital waveguide | Traveling waves | $O(1)$ per sample ($O(N)$ memory) | Exact for 1D; commutes losses |
| Finite difference | Grid samples | $O(N)$ per sample | Handles 2D/3D, nonlinear |
| Modal synthesis | Eigenmodes | $O(M)$ per sample for $M$ modes | Any geometry; independent modes |

See [[modal_synthesis/comparisons/waveguide-vs-modal|waveguide vs. modal]] for a detailed comparison.

## Related Concepts
- [[scattering-junctions]] — connecting waveguides at impedance discontinuities
- [[delay-line-techniques]] — interpolation, variable delay, allpass tuning
- [[string-modeling]] — application to plucked/struck/bowed strings
- [[bore-modeling]] — application to wind instrument tubes
- [[circular-buffer-topology-monodromy]] — the delay loop as a line bundle; why mixed boundaries halve $f_0$
- [[wave-digital-filters]] — the lumped-element counterpart using the same wave variables

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Digital Waveguides](https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguides.html), [Ideal Vibrating String](https://ccrma.stanford.edu/~jos/pasp/Ideal_Vibrating_String.html), [Traveling-Wave Solution](https://ccrma.stanford.edu/~jos/pasp/Traveling_Wave_Solution_I.html), [Alternative Wave Variables](https://ccrma.stanford.edu/~jos/pasp/Alternative_Wave_Variables.html), [Waveguide and FDTD Equivalence](https://ccrma.stanford.edu/~jos/pasp/Equivalence_Digital_Waveguide_Finite.html)

## References
[^1]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010; online at <https://ccrma.stanford.edu/~jos/pasp/>.
[^2]: d'Alembert, J. (1747). Recherches sur la courbe que forme une corde tendue.

---
title: Scattering Junctions
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [scattering, waveguide, impedance, dsp, physical-modeling]
sources:
  - /w/pasp/delay-allpass-waveguide.tex
  - /w/pasp/adaptors.tex
  - /w/pasp/idealtubesummary.tex
  - https://ccrma.stanford.edu/~jos/pasp/Signal_Scattering.html
  - https://ccrma.stanford.edu/~jos/pasp/Scattering_Impedance_Changes.html
---

# Scattering Junctions

When two waveguides of different impedance meet, incoming waves partially
reflect and partially transmit.[^2] This is scattering — the fundamental
mechanism for modeling area changes in tubes, bridge coupling in strings,
and multi-waveguide interconnections.

## Two-Port Scattering (Kelly-Lochbaum)

Two waveguides with impedances $R_1$ and $R_2$ joined end-to-end:[^1]

**Reflection coefficient** (pressure/force waves):
$$k \;=\; \frac{R_2 - R_1}{R_2 + R_1}$$

**Scattering relations** (pressure):
- Reflected: $p_1^- = k\, p_1^+$
- Transmitted: $p_2^+ = (1 + k)\, p_1^+$

For velocity waves: reflection = $-k$, transmission = $1 - k$.

### Kelly-Lochbaum Form (4 multiplies, 2 adds)
$$\begin{aligned}
p_1^- &= k\, p_1^+ + (1-k)\, p_2^-\\
p_2^+ &= (1+k)\, p_1^+ - k\, p_2^-
\end{aligned}$$

### One-Multiply Form (1 multiply, 3 adds)
$$\begin{aligned}
t    &= k\,(p_1^+ - p_2^-)\\
p_1^- &= p_2^- + t\\
p_2^+ &= p_1^+ + t
\end{aligned}$$

The one-multiply form is preferred in practice — same result, fewer ops.

## Multiport Scattering (N Waveguides)

$N$ waveguides meeting at a single series junction (common velocity):
- Junction velocity: $v_J = \dfrac{2\sum_k R_k v_k^+}{\sum_k R_k}$, which is $\dfrac{2}{N} \sum_{k=1}^{N} v_k^+$ for equal impedances
- Outgoing: $v_k^- = v_J - v_k^+$ (continuity)
- When $N$ is a power of 2 and impedances are equal: **multiply-free** scattering
  ($2/N$ is a bit shift) - a Householder reflection $\frac{2}{N}\mathbf{1}\mathbf{1}^T - I$
- Used in [[waveguide-meshes]] and FDN reverberators

For a parallel junction (common pressure), junction pressure is the admittance-weighted sum:
$$p_J \;=\; \frac{2\sum_k \Gamma_k\, p_k^+}{\sum_k \Gamma_k}, \qquad \Gamma_k = 1/R_k$$

## Wave Digital Filter Adaptors

WDF adaptors compute the same scattering as DWN junctions but operate
on bilinear-transform-warped wave variables. Key types:

- **Parallel adaptor**: forces equal, velocities sum to zero
- **Series adaptor**: velocities equal, forces sum to zero
- Both reduce to the same reflection coefficient $k = (R_2 - R_1)/(R_2 + R_1)$

See [[wdf-adaptors]] and the PASP appendix [Wave Digital Filters](https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Filters_I.html) for the full theory.

## Applications

| Structure | Scattering Models |
|-----------|------------------|
| Vocal tract | Area changes between cylindrical tube sections |
| Clarinet bore | Tone holes, register hole, bell |
| Guitar bridge | String-body impedance mismatch |
| Waveguide mesh | 4-port (2D) or 6-port (3D) junctions |
| FDN reverb | Feedback matrix = scattering at virtual junction |

## Lossless Property

Scattering is power-conserving by construction (signal power is $p^2/R$, so
each wave is weighted by its own admittance):
- $\dfrac{(p_1^-)^2}{R_1} + \dfrac{(p_2^+)^2}{R_2} = \dfrac{(p_1^+)^2}{R_1}$ for a wave incident from side 1
- A network of lossless junctions + pure delays = lossless allpass system
- This is the basis for digital waveguide network (DWN) design

## Related Concepts
- [[waveguide-overview]] — the bidirectional delay lines being connected
- [[delay-line-techniques]] — fractional delay at junctions
- [[bore-modeling]] — piecewise cylindrical tubes with scattering junctions
- [[artificial-reverberation]] — FDN feedback matrices as scattering
- [[differentiable-kelly-lochbaum-tract]] — learnable three-way junctions and damping in a vocal tract

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Scattering at Impedance Changes](https://ccrma.stanford.edu/~jos/pasp/Scattering_Impedance_Changes.html), [Kelly-Lochbaum Scattering Junctions](https://ccrma.stanford.edu/~jos/pasp/Kelly_Lochbaum_Scattering_Junctions.html), [One-Multiply Scattering Junctions](https://ccrma.stanford.edu/~jos/pasp/One_Multiply_Scattering_Junctions.html), [Loaded Waveguide Junctions](https://ccrma.stanford.edu/~jos/pasp/Loaded_Waveguide_Junctions.html), [Signal Scattering](https://ccrma.stanford.edu/~jos/pasp/Signal_Scattering.html)

## References
[^1]: Kelly, J. & Lochbaum, C. (1962). "Speech synthesis." 4th ICA, Copenhagen.
[^2]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010; online at <https://ccrma.stanford.edu/~jos/pasp/>.

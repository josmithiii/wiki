---
title: Scattering Junctions
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [scattering, waveguide, impedance, dsp, physical-modeling]
sources:
  - /w/pasp/delay-allpass-waveguide.tex
  - /w/pasp/adaptors.tex
  - /w/pasp/idealtubesummary.tex
  - https://ccrma.stanford.edu/~jos/pasp/Signal_Scattering.html
---

# Scattering Junctions

When two waveguides of different impedance meet, incoming waves partially
reflect and partially transmit. This is scattering — the fundamental
mechanism for modeling area changes in tubes, bridge coupling in strings,
and multi-waveguide interconnections.

## Two-Port Scattering (Kelly-Lochbaum)

Two waveguides with impedances $R_1$ and $R_2$ joined end-to-end:

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

$N$ waveguides meeting at a single junction (all wave impedances equal):
- Junction velocity: $v_J = \dfrac{1}{N} \sum_{k=1}^{N} v_k^+$ (for equal impedances)
- Outgoing: $v_k^- = v_J - v_k^+$ (continuity)
- When $N$ is a power of 2: **multiply-free** scattering (Hadamard structure)
- Used in waveguide meshes and FDN reverberators

For unequal impedances, junction pressure is the impedance-weighted sum:
$$p_J \;=\; \frac{2\sum_k \Gamma_k\, p_k^+}{\sum_k \Gamma_k}, \qquad \Gamma_k = 1/R_k$$

## Wave Digital Filter Adaptors

WDF adaptors compute the same scattering as DWN junctions but operate
on bilinear-transform-warped wave variables. Key types:

- **Parallel adaptor**: forces equal, velocities sum to zero
- **Series adaptor**: velocities equal, forces sum to zero
- Both reduce to the same reflection coefficient $k = (R_2 - R_1)/(R_2 + R_1)$

See PASP Appendix on Wave Digital Filters for the full theory.

## Applications

| Structure | Scattering Models |
|-----------|------------------|
| Vocal tract | Area changes between cylindrical tube sections |
| Clarinet bore | Tone holes, register hole, bell |
| Guitar bridge | String-body impedance mismatch |
| Waveguide mesh | 4-port (2D) or 6-port (3D) junctions |
| FDN reverb | Feedback matrix = scattering at virtual junction |

## Lossless Property

Scattering is energy-conserving by construction:
- $|\text{reflected}|^2 + |\text{transmitted}|^2 = |\text{incident}|^2$
- A network of lossless junctions + pure delays = lossless allpass system
- This is the basis for digital waveguide network (DWN) design

## Related Concepts
- [[waveguide-overview]] — the bidirectional delay lines being connected
- [[delay-line-techniques]] — fractional delay at junctions
- [[bore-modeling]] — piecewise cylindrical tubes with scattering junctions
- [[artificial-reverberation]] — FDN feedback matrices as scattering

## References
[^1]: Kelly, J. & Lochbaum, C. (1962). "Speech synthesis." 4th ICA, Copenhagen.
[^2]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.

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

Two waveguides with impedances R_1 and R_2 joined end-to-end:

**Reflection coefficient** (pressure/force waves):
  k = (R_2 - R_1) / (R_2 + R_1)

**Scattering relations** (pressure):
- Reflected: p_1^- = k * p_1^+
- Transmitted: p_2^+ = (1 + k) * p_1^+

For velocity waves: reflection = -k, transmission = 1 - k.

### Kelly-Lochbaum Form (4 multiplies, 2 adds)
  p_1^- =  k * p_1^+ + (1-k) * p_2^-
  p_2^+ = (1+k) * p_1^+ - k * p_2^-

### One-Multiply Form (1 multiply, 3 adds)
  temp = k * (p_1^+ - p_2^-)
  p_1^- = p_2^- + temp
  p_2^+ = p_1^+ + temp

The one-multiply form is preferred in practice — same result, fewer ops.

## Multiport Scattering (N Waveguides)

N waveguides meeting at a single junction (all wave impedances equal):
- Junction velocity: v_J = (1/N) * sum(v_in_k, k=1..N)  [for equal impedances]
- Outgoing: v_out_k = v_J - v_in_k  (continuity)
- When N is a power of 2: **multiply-free** scattering (Hadamard structure)
- Used in waveguide meshes and FDN reverberators

For unequal impedances, junction pressure is the impedance-weighted sum:
  p_J = 2 * sum(Gamma_k * p_k^+) / sum(Gamma_k)  where Gamma_k = 1/R_k

## Wave Digital Filter Adaptors

WDF adaptors compute the same scattering as DWN junctions but operate
on bilinear-transform-warped wave variables. Key types:

- **Parallel adaptor**: forces equal, velocities sum to zero
- **Series adaptor**: velocities equal, forces sum to zero
- Both reduce to the same reflection coefficient k = (R_2 - R_1)/(R_2 + R_1)

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
- |reflected|^2 + |transmitted|^2 = |incident|^2
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

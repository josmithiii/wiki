---
title: Waveguide Meshes
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [mesh, waveguide, wave-equation, dsp, room, acoustics]
sources:
  - /w/pasp/mesh.tex
  - https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Mesh.html
---

# Waveguide Meshes

A digital waveguide mesh extends 1D waveguide modeling to 2D and 3D by
connecting waveguides at multiport scattering junctions arranged on a
regular grid. Think of a tennis racket: 1D strings crossing at nodes.

## 2D Rectilinear Mesh

At each node, four incoming traveling-wave components scatter:
  v_node = (v_N^+ + v_E^+ + v_S^+ + v_W^+) / 2
  v_k^- = v_node - v_k^+,  k = N, E, S, W

- Lossless by construction (energy-conserving scattering)
- Linear and time-invariant → only error is dispersion
- Multiply-free when N (ports per junction) is a power of 2

### Faust Implementation (4-port junction)
```
process = bus(4) <: par(i,4,*(-1)), (bus(4) :> *(.5) <: bus(4)) :> bus(4);
```

## Dispersion

The only error in a lossless mesh: propagation speed varies with
frequency and direction. Quantified by von Neumann analysis.

| Geometry | Isotropy | Cost | Notes |
|----------|----------|------|-------|
| Rectilinear | Poor (diagonal faster) | Lowest | Simplest to implement |
| Triangular | Best known elementary | Medium | Least dispersion variation |
| Interpolated | Configurable | Higher | Frequency-warping can compensate |
| Tetrahedral (3D) | Good | High | Used for room acoustics |

- **Frequency warping** (Savioja et al.): compensates frequency-dependent
  dispersion but not angle-dependent; best combined with isotropic mesh

## Applications

- **Room acoustics**: 3D mesh simulates sound propagation in enclosures
  - Requires quarter-inch spatial sampling for 20 kHz bandwidth
  - Feasible for small rooms; concert halls still too expensive
- **Violin body**: statistical modeling of reverberant body response
  (Huang, Serafin & Smith) — mesh captures "reverberant" tail,
  separate EQ handles low-frequency body/air modes
- **Membrane/plate simulation**: 2D mesh for drums, gongs
- **Diffusion modeling**: mesh boundaries can model surface diffusion
  (quadratic residue sequences for maximally diffusing boundaries)

## Mesh vs. Finite Differences

The waveguide mesh is equivalent to a specific class of finite-difference
schemes (Bilbao). Key advantage: energy invariance is built in by
construction (lossless scattering), rather than needing separate stability
analysis. Disadvantage: less flexibility for non-uniform media.

## Related Concepts
- [[scattering-junctions]] — the multiport junctions connecting the mesh
- [[artificial-reverberation]] — meshes as brute-force room models
- [[waveguide-overview]] — the 1D building blocks

## References
[^1]: Van Duyne, S. & Smith, J.O. (1993). "Physical Modeling with the 2-D Digital Waveguide Mesh." ICMC.
[^2]: Savioja, L. et al. (2000). "Interpolated rectangular 3-D digital waveguide mesh algorithms." IEEE TSA.
[^3]: Bilbao, S. (2004). "Wave and Scattering Methods for Numerical Simulation." Wiley.

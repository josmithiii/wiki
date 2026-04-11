---
title: Banded Waveguides
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [banded, waveguide, percussion, physical-modeling, dsp]
sources:
  - /l/wgr/Sections/Advancements/InstrumentModelling.tex
---

# Banded Waveguides

Banded waveguides model 2D/3D vibrating objects (bars, plates, bells, cymbals)
using a small set of 1D waveguide loops, each representing a "closed wavetrain"
— a quasi-1D path of wave propagation on the object's surface.

## Motivation

Objects like cymbals, gongs, and bells have complex 2D vibration patterns.
A full waveguide mesh is expensive. But many of the perceptually important
modes travel along identifiable closed paths on the surface (nodal circles,
radial lines). Each such path can be modeled as a 1D filtered delay loop.

## Principle

1. Identify closed wavetrains on the object (from mode analysis or measurement)
2. Model each wavetrain as a 1D waveguide loop with appropriate:
   - Delay length (sets the pitch of that wavetrain's partial series)
   - Loop filter (damping, dispersion along the path)
   - Coupling to excitation point
3. Sum contributions from all wavetrains for the output

## Advantages

- Much cheaper than a full 2D/3D mesh
- Each wavetrain captures a quasi-harmonic series of partials
- Natural for objects with strong azimuthal or radial symmetry
- Excitation position affects which wavetrains are driven

## Applications

- **Cymbals**: closed wavetrains along circular paths (Essl 2004, Serafin 2001)
- **Glockenspiel/triangle**: 1D bar modes (tonal percussion)
- **Bells**: combined radial and azimuthal wavetrains
- **Timpani**: membrane wavetrains + 3D air cavity mesh

## Relation to Modal Synthesis

Banded waveguides are a hybrid approach:
- Like modal synthesis: each loop produces a series of partials
- Like waveguide synthesis: uses delay loops with physical parameters
- Unlike modal synthesis: partials within each band are automatically
  quasi-harmonic (set by loop length), not independently specified
- Complementary to [[modal_synthesis/concepts/modal-synthesis-overview]]

## Related Concepts
- [[waveguide-meshes]] — the brute-force alternative for 2D/3D
- [[waveguide-overview]] — 1D waveguide loop foundation
- [[string-modeling]] — similar delay-loop structure, different geometry

## References
[^1]: Essl, G. & Cook, P. (2004). "Banded Waveguides on Circular Topologies." DAFx.
[^2]: Serafin, S. et al. (2001). "Banded Waveguides." ICMC.

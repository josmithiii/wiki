---
title: Banded Waveguides
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [banded, waveguide, percussion, physical-modeling, dsp]
sources:
  - /l/wgr/Sections/Advancements/InstrumentModelling.tex
---

# Banded Waveguides

Banded waveguides model stiff or 2D/3D vibrating objects (bars, bowls, cymbals)
using a small set of band-limited 1D waveguide loops, each representing a
"closed wavetrain" — a path along which a traveling wave closes on itself in
phase at one modal frequency.[^1]

## Motivation

Stiff bars are strongly dispersive, so one delay loop cannot place all their
inharmonic partials; cymbals, gongs, and bowls add 2D vibration patterns, and a
full waveguide mesh is expensive. But each perceptually important mode can be
seen as a wave that returns in phase after one trip round a closed path. Each
such closed wavetrain gets its own bandpass-filtered delay loop.

## Principle

1. Identify the modes / closed wavetrains (from mode analysis or measurement)
2. Split the spectrum into bands, one per mode; in each band run a 1D loop with:
   - Bandpass filter selecting that mode's frequency region
   - Delay length = round-trip time of the wavetrain at that frequency
     (dispersion is absorbed by giving each band its own length)
   - Loop gain (damping) and coupling to the excitation point
3. Sum contributions from all bands for the output

## Advantages

- Much cheaper than a full 2D/3D mesh
- Keeps traveling-wave (spatial) state, so nonlinear excitations such as bowing
  can be attached as in [[reed-and-bow-models]] - awkward in pure modal synthesis
- Natural for objects with strong azimuthal or radial symmetry
- Excitation position affects which bands are driven

## Applications

- **Bars**: struck and bowed marimba/vibraphone bars - the original application
- **Cymbals and gongs**: the banded waveguide mesh (Serafin, Huang & Smith 2001)[^2]
- **Bowls and glasses**: circular wavetrains with beating mode pairs (singing bowls, glass harmonica)
- Contrast: membranes with an air cavity (timpani) are usually done with a 2D mesh
  plus a 3D mesh ([[waveguide-meshes]])

## Relation to Modal Synthesis

Banded waveguides are a hybrid approach:
- Like modal synthesis: one resonance per band, tuned and damped independently
- Like waveguide synthesis: delay loops whose lengths are physical round-trip times
- Unlike a resonator bank: each band holds a propagating wave, not just a mode amplitude
- Complementary to [[modal_synthesis/concepts/modal-synthesis-overview|modal synthesis]];
  see also [[modal_synthesis/comparisons/waveguide-vs-modal|waveguide vs. modal]]

## Related Concepts
- [[waveguide-meshes]] — the brute-force alternative for 2D/3D
- [[waveguide-overview]] — 1D waveguide loop foundation
- [[string-modeling]] — similar delay-loop structure, different geometry

## JOS online books
- [[jos_books/entities/pasp-book|PASP]] has no banded-waveguide section yet; background: [Percussion Instruments](https://ccrma.stanford.edu/~jos/pasp/Percussion_Instruments.html), [The Dispersive 1D Wave Equation](https://ccrma.stanford.edu/~jos/pasp/Dispersive_1D_Wave_Equation.html)

## References
[^1]: Essl, G., Serafin, S., Cook, P.R. & Smith, J.O. (2004). "Theory of Banded Waveguides" and "Musical Applications of Banded Waveguides." CMJ 28(1).
[^2]: Serafin, S., Huang, P. & Smith, J.O. (2001). "The Banded Digital Waveguide Mesh." Workshop on Future Directions of Computer Music, Barcelona.

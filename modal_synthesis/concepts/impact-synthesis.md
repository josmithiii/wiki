---
title: Impact Synthesis
created: 2026-04-09
updated: 2026-11-25
type: concept
tags: [impact, modal-synthesis, physical-modeling, acoustics, rigid-body]
sources:
  - /l/dttd/CollisionsBilbao2015.pdf
---

# Impact Synthesis

## Overview
Impact synthesis models the sound produced when two objects collide.
Most common excitation model for modal synthesis — a struck or dropped object.
Early work: Gaver (1993), Cook (1997), van den Doel & Pai (1998); real-time interactive
contact sounds in FoleyAutomatic (van den Doel, Kry & Pai 2001).

## Physics of Impact
Two contact phases:
1. Contact phase: objects deform at contact point; contact force builds and decays
2. Post-contact: each object rings freely (its modal response to the impulse)

Key insight: for rigid-body impact, contact force ~ a half-sine pulse of duration $T_c$.
$T_c$ depends on object stiffnesses (Hertz contact model):
$$T_c \;\sim\; 1/f_{\text{contact}} \;\propto\; (m^2 / k_h^2 v_0)^{1/5}$$
(Hertz: effective mass $m$, contact stiffness $k_h$, impact speed $v_0$ - stiffer or faster means shorter).

## Hertz Contact Model
Force during contact:
$$F(t) \;=\; k_h\, \delta(t)^{3/2}$$

where:
- $\delta(t)$ = mutual indentation (overlap) of objects at contact point
- $k_h$ = Hertz contact stiffness = $f(E_1, E_2, R_1, R_2)$ (elastic moduli, radii)

Resulting force pulse ~ smooth bump; spectral content up to ~$1/T_c$ Hz.

## Modal Response
Object's acoustic output after impact:
$$y(t) \;=\; \sum_k a_k\, \phi_k(r_{\text{impact}}) \int_0^t F(\tau)\, h_k(t-\tau)\, d\tau$$

For an ideal impulse $F(t) = \delta(t)$:
$$y(t) \;=\; \sum_k a_k\, \phi_k(r_{\text{impact}})\, e^{-d_k t}\, \sin(2\pi f_k t)$$

For real contact pulse $F(t)$: each mode is convolved with $F(t)$,
which attenuates high-frequency modes (the pulse is a low-pass filter).
Hard materials → short $T_c$ → more HF modes excited.
Soft materials (rubber) → long $T_c$ → only LF modes excited.

## Precomputed Impact Sounds
The standard pipeline (van den Doel, Kry & Pai 2001; O'Brien, Shen & Gatchalian 2002):
- Precompute mode parameters offline (FEM)
- Store per-vertex mode shape values
- At runtime: look up $\phi_k(r_{\text{impact}})$ and trigger the resonator bank
- Enables real-time rigid-body impact sound synthesis for games/VR
- James, Barbič & Pai (2006), "Precomputed Acoustic Transfer", adds each mode's precomputed
  radiation to the listener (see [[radiation-and-directivity]])

## Contact Models for Different Material Types
| Material | Hertz model? | $T_c$ | Modes excited |
|----------|--------------|-----|---------------|
| Metal-metal | Yes | very short | broad spectrum |
| Wood-wood | Yes (approx) | short | mid-high freq |
| Rubber-hard | Nonlinear | long | low freq only |
| Cloth | Complex | N/A | not modal |

## Perceptual Factors
- Decay rate (internal damping) → the main cue to material (Klatzky, Pai & Krotkov 2000)
- Frequency → size (lower = larger), and a secondary material cue
- Mode spacing → shape perception
- Spectral centroid → brightness / hardness
- Inharmonicity → "metallic" vs "wooden" timbre

## Multiple Simultaneous Impacts
- Sum independent resonator bank responses
- Same object hit twice: superpose two sets of initial conditions
- Each impact adds a new "excitation event" to each modal oscillator
- No nonlinear coupling between modes (linear assumption)

## Related Concepts
- [[modal-synthesis-overview]] — parent concept
- [[resonator-bank-implementation]] — how the response is synthesized
- [[friction-synthesis]] — continuous excitation (bowing, scraping)
- [[rigid-body-sound-synthesis]] — full simulation pipeline
- [[material-properties-and-modes]] — how material affects mode parameters
- [[nonlinear-modal-synthesis]] — power-law collisions with energy-stable numerical schemes

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Piano Hammer Modeling](https://ccrma.stanford.edu/~jos/pasp/Piano_Hammer_Modeling.html), [Nonlinear Spring Model](https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Spring_Model.html), [Including Hysteresis](https://ccrma.stanford.edu/~jos/pasp/Including_Hysteresis.html), [Ideal String Struck by a Mass](https://ccrma.stanford.edu/~jos/pasp/Ideal_String_Struck_Mass.html)

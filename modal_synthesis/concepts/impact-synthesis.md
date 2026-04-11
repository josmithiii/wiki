---
title: Impact Synthesis
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [impact, modal-synthesis, physical-modeling, acoustics, rigid-body]
sources:
  - /l/dttd/CollisionsBilbao2015.pdf
---

# Impact Synthesis

## Overview
Impact synthesis models the sound produced when two objects collide.
Most common excitation model for modal synthesis — a struck or dropped object.
Pioneered by Perry Cook (1995) and later made real-time by James, Barbic, Pai (2006).

## Physics of Impact
Two contact phases:
1. Contact phase: objects deform at contact point; contact force builds and decays
2. Post-contact: each object rings freely (its modal response to the impulse)

Key insight: for rigid-body impact, contact force ~ a half-sine pulse of duration T_c.
  T_c depends on object stiffnesses (Hertz contact model):
    T_c ~ (1/f_contact) ~ material stiffness^{-2/5}

## Hertz Contact Model
Force during contact:
  F(t) = k_h * delta(t)^{3/2}

where:
- delta(t) = mutual indentation (overlap) of objects at contact point
- k_h = Hertz contact stiffness = f(E1, E2, R1, R2)  [elastic moduli, radii]

Resulting force pulse ~ smooth bump; spectral content up to ~1/T_c Hz.

## Modal Response
Object's acoustic output after impact:
  y(t) = sum_k [ a_k * phi_k(r_impact) * integral_0^t F(tau)*h_k(t-tau) dtau ]

For an ideal impulse F(t) = delta(t):
  y(t) = sum_k [ a_k * phi_k(r_impact) * exp(-d_k*t) * sin(2*pi*f_k*t) ]

For real contact pulse F(t): each mode is convolved with F(t),
which attenuates high-frequency modes (the pulse is a low-pass filter).
Hard materials → short T_c → more HF modes excited.
Soft materials (rubber) → long T_c → only LF modes excited.

## Precomputed Impact Sounds
James, Barbic & Pai (2006) "Precomputed Acoustic Transfer":
- Precompute mode parameters offline (FEM)
- Store per-vertex mode shape values
- At runtime: look up phi_k(r_impact) and trigger resonator bank
- Enables real-time rigid-body impact sound synthesis for games/VR

## Contact Models for Different Material Types
| Material | Hertz model? | T_c | Modes excited |
|----------|--------------|-----|---------------|
| Metal-metal | Yes | very short | broad spectrum |
| Wood-wood | Yes (approx) | short | mid-high freq |
| Rubber-hard | Nonlinear | long | low freq only |
| Cloth | Complex | N/A | not modal |

## Perceptual Factors (Cook 2002)
- Fundamental frequency most salient cue for material (hardness)
- Decay rate → hardness/damping perception
- Mode spacing → size and shape perception
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

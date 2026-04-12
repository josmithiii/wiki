---
title: Coupled Structures
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [modal-synthesis, physical-modeling, vibration, string, acoustics, dsp]
sources:
  - /l/dttd/RealTimeGuitarSynthesisBilbao-DAFx24.pdf
  - /w/pasp/modal.tex
---

# Coupled Structures

Musical instruments are rarely single vibrating bodies. A guitar is a string
coupled to a bridge coupled to a soundboard coupled to an air cavity.
Modeling these couplings is essential for realistic synthesis.

## Physics of Coupling

Two subsystems share energy at a junction point (or region):
- Force continuity: F_string = F_bridge at the coupling point
- Velocity continuity: v_string = v_bridge at the coupling point
- Energy flows bidirectionally: string excites body, body loads string

### Modal Coupling Formulation
Given two systems with modes $\phi_i^A$ and $\phi_j^B$ coupled at point $x_c$:
- Coupling force projects onto each system's modal basis
- $g_i^A(t) = \phi_i^A(x_c)\, F_c(t)$ (modal excitation of system A)
- $g_j^B(t) = \phi_j^B(x_c)\, F_c(t)$ (modal excitation of system B)
- The coupling point acts as both excitation and observation point

## Guitar: String + Bridge + Body (Bilbao DAFx24)[^1]

Full real-time guitar model combining:
- Nonlinear stiff string (Kirchhoff-Carrier tension modulation)
- Collision with frets, fingerboard, and stopping finger
- Body modeled as a set of modes driven at bridge point

### Key Design Choices
- Modal expansion for string — avoids large spatial grid
- Energy quadratisation (IEQ/SAV) for all nonlinearities — no Newton-Raphson
- Explicit or small-linear-system updates — real-time viable
- String-body coupling: force at bridge, velocity matching
- Includes pitch glide, fret buzz, harmonics, and stopped-string effects

## Delay Loop Expansion (PASP)[^2]

When modes are quasi-harmonic (strings, tubes), a filtered delay loop
is far more efficient than N separate biquads:
- $H(z) = \sum_k a_k / (1 - H_k(z)\, z^{-N_k})$
- $N_k$ = delay length (sets fundamental pitch)
- $H_k(z)$ = low-order filter (fine-tunes mode frequencies and damping)
- One delay loop replaces an entire harmonic series of biquads
- Basis of digital waveguide synthesis

### When to Use Delay Loops vs. Modal Biquads
- Quasi-harmonic partials (strings, tubes): delay loop wins
- Inharmonic partials (plates, bells, bars): biquad bank required
- Hybrid: delay loop for string + biquad bank for body (commuted synthesis)

## Commuted Synthesis[^2]

If excitation and pickup positions are fixed, coupling simplifies:
- Precompute combined impulse response h(t) = string * bridge * body
- Synthesize: y(t) = excitation(t) * h(t)  [convolution]
- Often cheaper than running all resonators in real time
- Tradeoff: loses ability to change pickup position or individual modes
- Used extensively in commercial samplers and early physical models

## State-Space Approach[^2]

For multiple inputs/outputs, the state-space formulation is more systematic:
- Form $(A, B^{(i)}, C^{(o)})$ where $B$ depends on input location, $C$ on output
- Diagonalize → $(\Lambda, \beta^{(i)}, \gamma^{(o)})$ — modal representation
- Similarity transform preserves input-output behavior exactly
- Each mode gets proper excitation weight beta and observation weight gamma
- Generalizes naturally to multi-point coupling

## Multi-Object Coupling

Beyond instrument subcomponents:
- Object-on-object contact: modes of both objects excited at impact point
- Rolling/sliding: continuous contact force modulated by surface texture
- Sympathetic resonance: nearby objects excited by radiated sound
- See [[nonlinear-modal-synthesis]] for collision coupling details

## Related Concepts
- [[modal-synthesis-overview]] — foundation
- [[nonlinear-modal-synthesis]] — collision and tension nonlinearities
- [[resonator-bank-implementation]] — biquad bank DSP
- [[friction-synthesis]] — continuous excitation coupling
- [[impact-synthesis]] — impulsive excitation at coupling point

## References
[^1]: Bilbao, Russo, Webb & Ducceschi (2024). "Real-Time Guitar Synthesis." DAFx24.
[^2]: Smith, J.O. III. "Physical Audio Signal Processing," online book, CCRMA/Stanford.

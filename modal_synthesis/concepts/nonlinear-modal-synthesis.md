---
title: Nonlinear Modal Synthesis
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [modal-synthesis, physical-modeling, vibration, impact, dsp]
sources:
  - /l/dttd/NonlinearModalSynthModeCoupling-Poirot-Bilbao-EURASIP-2024.pdf
  - /l/dttd/CollisionsBilbao2015.pdf
  - /l/dttd/BilbaoCollisions-ISMA-2024.pdf
  - /l/dttd/TunableCollisionsPianoHammerDAFx23.pdf
  - /l/dttd/QuadraticSplineCollisions-DAFx24.pdf
---

# Nonlinear Modal Synthesis

Standard [[modal-synthesis-overview]] assumes linear superposition — modes evolve
independently. Real instruments violate this: collisions, tension modulation,
and geometric nonlinearities couple modes and transfer energy between them.

## Mode Coupling

When vibration amplitudes are large enough, modes exchange energy:
- Thin plates/shells: Föppl-von Kármán equations govern nonlinear plate dynamics
- Energy cascades from driven modes to higher/lower modes over time
- Perceptual effect: delayed tonal components, spectral enrichment, "shimmer"

### Poirot-Bilbao Coupled Filter Model (EURASIP 2024)[^1]
- Departs from strict PDE simulation for perceptual/procedural goals
- Coupled Mathews-Smith resonant filters with inter-modal energy transfer
- Coupling matrix C_ij encodes energy flow between mode pairs
- Power transfer: P_i(n+1) = [P_i(n) + T_i(n)] * exp(-2*alpha_i/fs)
- Equivalence between filter signal power and modal mechanical energy
- Randomization of coupling improves realism
- Achievable in real time (no iterative solver needed)

## Collision Nonlinearities

Collisions are one-sided nonlinearities: force is zero until contact, then large.

### Power-Law Contact Model[^2]
- F = K * [eta]_+^alpha, where eta = penetration depth
- K = stiffness, alpha > 1 (typically 1.5–3 for Hertzian contact)
- Potential: Phi = K * [eta]_+^(alpha+1) / (alpha+1)
- Energy-conserving finite difference schemes guarantee numerical stability

### Bilbao's Hamiltonian Framework[^2][^3]
- Cast collision as additional potential energy term in Hamiltonian
- Discrete energy balance: delta_t- h = -q (h = total energy, q = dissipated power)
- Stability follows from h >= 0
- Bounds on spurious penetration: max(eta) <= [(2(alpha+1)*h) / (K*h_spatial)]^(1/(alpha+1))
- Applies to lumped (hammer-string) and distributed (string-barrier) collisions

### Applications in Musical Instruments
- Piano hammer-string: lumped collision, power-law deformable hammer[^4]
- Guitar string-fret: distributed collision with rigid barrier[^3]
- Sitar/tambura: string against curved bridge (pitch bending, buzzing)
- Snare drum: wire-membrane distributed collision
- Reed beating: clarinet/oboe reed against mouthpiece lay

## Tension Modulation (Kirchhoff-Carrier)

At large amplitudes, string stretching increases effective tension:
- K[u] = (EA/2L) * integral[(du/dx)^2 dx] * d^2u/dx^2
- Causes pitch glide upward at high amplitudes
- Couples all modes through shared tension term

## Energy Quadratisation Methods[^4][^5]

Modern approach avoiding iterative Newton-Raphson solvers:
- Invariant Energy Quadratisation (IEQ) / Scalar Auxiliary Variable (SAV)
- Introduce auxiliary variable to make nonlinear energy term quadratic
- Yields explicit or small-linear-system update — real-time viable
- Van Walstijn et al. (DAFx23): tunable collision parameters at runtime[^4]
- Bhanuprakash et al. (DAFx24): quadratic spline approximation of contact potential[^5]

## Computational Cost

| Method | Real-time? | Solver | Accuracy |
|--------|-----------|--------|----------|
| Full Föppl-von Kármán | ~8x real-time (CPU) | Iterative | High |
| Coupled filter bank | Yes | None (explicit) | Perceptual |
| Energy quadratisation | Yes | Small linear system | High |
| Power-law alpha=1 exact | Yes | Analytic closed-form | Medium |

## Related Concepts
- [[modal-synthesis-overview]] — linear modal synthesis foundation
- [[impact-synthesis]] — excitation models for collisions
- [[coupled-structures]] — multi-object energy transfer
- [[resonator-bank-implementation]] — DSP realization of mode filters

## References
[^1]: Poirot, Bilbao & Kronland-Martinet (2024). "A simplified and controllable model of mode coupling." EURASIP JASM.
[^2]: Bilbao, Torin & Chatziioannou (2015). "Numerical Modeling of Collisions in Musical Instruments." Acta Acustica.
[^3]: Bilbao (2024). "Numerical Modeling of String/Barrier Collisions." ISMA.
[^4]: van Walstijn, Bhanuprakash & Chatziioannou (2023). "Tunable Collisions." DAFx23.
[^5]: Bhanuprakash, van Walstijn & Chatziioannou (2024). "Quadratic Spline Approximation of the Contact Potential." DAFx24.

---
title: Coupled Structures
created: 2026-04-10
updated: 2026-11-25
type: concept
tags: [modal-synthesis, physical-modeling, vibration, string, acoustics, dsp]
sources:
  - /l/dttd/RealTimeGuitarSynthesisBilbao-DAFx24.pdf
  - /w/pasp/modal.tex
  - https://ccrma.stanford.edu/~jos/pasp/Delay_Loop_Expansion.html
  - https://ccrma.stanford.edu/~jos/pasp/State_Space_Approach_Modal.html
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
---

# Coupled Structures

Musical instruments are rarely single vibrating bodies. A guitar is a string
coupled to a bridge coupled to a soundboard coupled to an air cavity.
Modeling these couplings is essential for realistic synthesis.

## Physics of Coupling

Two subsystems share energy at a junction point (or region):
- Force balance: $F_{\text{string}} = F_{\text{bridge}}$ (equal and opposite) at the coupling point
- Velocity continuity: $v_{\text{string}} = v_{\text{bridge}}$ at the coupling point
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
is far more efficient than $N$ separate biquads:
- $H(z) = \sum_k a_k / (1 - H_k(z)\, z^{-N_k})$
- $N_k$ = delay length (sets fundamental pitch)
- $H_k(z)$ = low-order filter (fine-tunes mode frequencies and damping)
- One delay loop replaces an entire harmonic series of biquads
- Basis of digital waveguide synthesis ([[waveguide_synthesis/concepts/waveguide-overview|waveguide overview]])

### When to Use Delay Loops vs. Modal Biquads
- Quasi-harmonic partials (strings, tubes): delay loop wins
- Inharmonic partials (plates, bells, bars): biquad bank required
- Hybrid: delay loop for string + biquad bank for body (commuted synthesis)

## Commuted Synthesis[^3]

If string and body are linear and time-invariant, their order can be swapped
(see [[waveguide_synthesis/concepts/commuted-synthesis|commuted synthesis]]):
- Commute the body ahead of the string: excitation → body → string
- Precompute the aggregate excitation $a(t) = e(t) * h_{\text{body}}(t)$ and store it as a table
- Synthesize by playing $a(t)$ into the string loop - no body filter runs at all
- Far cheaper than hundreds of body resonators per voice
- Tradeoff: the body is frozen into the table (no run-time mode or pickup changes), and
  bridge feedback from body to string must be folded into the string loop filter

## State-Space Approach[^2]

For multiple inputs/outputs, the state-space formulation is more systematic:
- Form $(A, B^{(i)}, C^{(o)})$ where $B$ depends on input location, $C$ on output
- Diagonalize → $(\Lambda, \beta^{(i)}, \gamma^{(o)})$ — modal representation
- Similarity transform preserves input-output behavior exactly
- Each mode gets proper excitation weight $\beta$ and observation weight $\gamma$
- Generalizes naturally to multi-point coupling
- See [[state-space-models-as-modal-resonator-banks]] and [[era-bridge-admittance-identification]]

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
- **DAFx26 additions (Sept 2026):** measured bridge compliance and radiation coupled to a nonlinear string for 65 classical guitars, and reduced-order state-space realization of measured violin bridge admittances - see [[entities/source-papers#paper-ducceschi-65-classical-guitars-2026]] and [[entities/source-papers#paper-giampiccolo-era-violin-bridge-2026]]
- Distilled in full: [[sav-nonlinear-string-with-measured-body]] (guitar bridge coupling) and [[era-bridge-admittance-identification]] (violin bridge admittance)

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Delay Loop Expansion](https://ccrma.stanford.edu/~jos/pasp/Delay_Loop_Expansion.html), [State Space Approach to Modal Expansions](https://ccrma.stanford.edu/~jos/pasp/State_Space_Approach_Modal.html), [Commuted Synthesis](https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html), [Bridge Modeling](https://ccrma.stanford.edu/~jos/pasp/Bridge_Modeling.html), [String Coupling Effects](https://ccrma.stanford.edu/~jos/pasp/String_Coupling_Effects.html)
- [[jos_books/entities/filters-book|Filters]]: [Modal Representation](https://ccrma.stanford.edu/~jos/filters/Modal_Representation.html), [Similarity Transformations](https://ccrma.stanford.edu/~jos/filters/Similarity_Transformations.html)

## References
[^1]: Bilbao, Russo, Webb & Ducceschi (2024). "Real-Time Guitar Synthesis." DAFx24.
[^2]: Smith, J.O. III. *Physical Audio Signal Processing*, [Modal Expansion](https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html) (delay loop and state-space subsections).
[^3]: Smith, J.O. III. *Physical Audio Signal Processing*, [Commuted Synthesis](https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html).

---
title: Rigid-Body Sound Synthesis
created: 2026-04-09
updated: 2026-11-25
type: concept
tags: [rigid-body, modal-synthesis, impact, physical-modeling, realtime]
sources:
  - /l/dttd/CollisionsBilbao2015.pdf
  - /l/dttd/SynthMatch-DDSP-Diaz-Hayes-RigidBodyModal-ICASSP23.pdf
---

# Rigid-Body Sound Synthesis

## Overview
Rigid-body sound synthesis couples a physics simulation (rigid-body dynamics)
with modal synthesis to generate realistic impact and rolling sounds in real time.
Standard approach in game audio and VR since ~2005.

## System Architecture

```
Physics Engine (rigid-body dynamics)
    |
    | contact events: (object A, object B, contact point, force magnitude)
    v
Sound Engine (modal synthesis)
    |
    | for each contact event:
    |   look up mode parameters for A and B
    |   look up mode shapes at contact point
    |   trigger resonator bank with scaled impulse
    v
Audio Output
```

## Contact Detection → Sound Trigger
Physics engine reports contacts with:
- Contact point $r_c$ in world coordinates
- Contact normal force $F(t)$ (force profile over contact duration)
- Relative velocity at contact $v_{\text{rel}}$

Sound trigger:
- Estimate $T_c$ from Hertz model (depends on material stiffness, mass; see [[impact-synthesis]])
- Excitation spectrum = Fourier transform of $F(t)$ ≈ low-pass up to $1/T_c$
- Scale mode amplitudes by $\phi_k(r_c)$ times the force magnitude
- Start all resonators with these initial conditions

## Precomputed Mode Data
For each object in the scene:
- Offline: compute modes via FEM + BEM (or measure experimentally)
- Store: $\{f_k, d_k, a_k[\text{per vertex}]\}$ for ~100-500 modes
- At runtime: look up $a_k$ for the contact vertex

## Precomputed Acoustic Transfer (James, Barbič, Pai 2006)
Key paper: "Precomputed Acoustic Transfer: Output-Sensitive, Accurate Sound Generation
for Geometrically Complex Vibration Sources" (SIGGRAPH 2006).

Contributions:
- Precompute each mode's radiated field offline (BEM), then approximate it by a few
  equivalent multipole sources
- Runtime: evaluate each mode's transfer at the listener position - cost independent of
  mesh complexity ("output-sensitive"), no BEM at runtime
- Captures direction- and distance-dependent radiation; see [[radiation-and-directivity]]

## Scalability
Problem: (number of objects) × (modes per object) resonators → too many for large scenes.
Solutions:
1. **Amplitude culling**: only run resonators above perceptual threshold
2. **Distance culling**: skip objects too far from listener
3. **Level-of-detail modes**: fewer modes for distant objects
4. **GPU parallelism**: all resonators on GPU, reduce to CPU for output
5. **Stochastic synthesis**: for very large counts, model statistically ([[stochastic-modal-synthesis]])

## Rolling Sounds
Rolling = continuous sequence of micro-impacts from surface roughness.
Model:
- Surface texture profile $h(x)$
- As object rolls at speed $v$: contact height variation = $h(vt)$
- Band-pass filtered noise (bandwidth ~ $v$ / texture correlation length)
- Modulates amplitude of resonator bank continuously

## Scraping
Similar to rolling but different statistics:
- Object edge scraping along surface
- Texture profile along scrape path
- Often richer in harmonics (regular texture → tonal components)

## Key Papers / Implementations
- van den Doel & Pai (1998): "The Sounds of Physical Shapes" (Presence) — early system
- van den Doel, Kry & Pai (2001): FoleyAutomatic — interactive impact, rolling and sliding sounds
- O'Brien, Shen & Gatchalian (2002): "Synthesizing Sounds from Rigid-Body Simulations" — FEM modes + rigid-body sound
- James, Barbič & Pai (2006): Precomputed acoustic transfer
- Zheng & James (2010): "Rigid-Body Fracture Sound with Precomputed Soundbanks"; (2011): "Toward High-Quality Modal Contact Sound"

## Related Concepts
- [[impact-synthesis]] — core sound generation model
- [[fem-bem-for-modal-synthesis]] — offline mode computation
- [[resonator-bank-implementation]] — DSP realization
- [[gpu-modal-synthesis]] — GPU acceleration for many objects
- [[ml-modal-parameter-estimation]] — differentiable rigid-body modal models

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Rigid-Body Dynamics](https://ccrma.stanford.edu/~jos/pasp/Rigid_Body_Dynamics.html), [Equations of Motion for Rigid Bodies](https://ccrma.stanford.edu/~jos/pasp/Equations_Motion_Rigid_Bodies.html)

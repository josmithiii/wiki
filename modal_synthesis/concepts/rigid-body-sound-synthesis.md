---
title: Rigid-Body Sound Synthesis
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [rigid-body, modal-synthesis, impact, physical-modeling, realtime]
sources: []
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
- Contact point r_c in world coordinates
- Contact normal force F(t) (force profile over contact duration)
- Relative velocity at contact v_rel

Sound trigger:
- Estimate T_c from Hertz model (depends on material stiffness, mass)
- Excitation spectrum = Fourier transform of F(t) ≈ low-pass up to 1/T_c
- Scale mode amplitudes by phi_k(r_c) * F_magnitude
- Start all resonators with these initial conditions

## Precomputed Mode Data
For each object in the scene:
- Offline: compute modes via FEM + BEM (or measure experimentally)
- Store: {f_k, d_k, a_k[per vertex]} for ~100-500 modes
- At runtime: look up a_k for the contact vertex

## Precomputed Acoustic Transfer (James, Barbic, Pai 2006)
Key paper: "Precomputed Acoustic Transfer: Output-Sensitive, Accurate Sound Generation
for Geometrically Complex Vibration Sources" (SIGGRAPH 2006).

Contributions:
- Precompute BEM acoustic transfer per mode per vertex → stored table
- Runtime: O(N_modes) per sample, no BEM at runtime
- Handles directional radiation (HRTF-compatible)
- Demo: 100+ objects, all with physically accurate sound, real-time

## Scalability
Problem: N objects × N_modes resonators → too many for large scenes.
Solutions:
1. **Amplitude culling**: only run resonators above perceptual threshold
2. **Distance culling**: skip objects too far from listener
3. **Level-of-detail modes**: fewer modes for distant objects
4. **GPU parallelism**: all resonators on GPU, reduce to CPU for output
5. **Stochastic synthesis**: for very large N, model statistically

## Rolling Sounds
Rolling = continuous sequence of micro-impacts from surface roughness.
Model:
- Surface texture profile h(x)
- As object rolls at speed v: contact height variation = h(v*t)
- Band-pass filtered noise (bandwidth ~ v / texture_correlation_length)
- Modulates amplitude of resonator bank continuously

## Scraping
Similar to rolling but different statistics:
- Object edge scraping along surface
- Texture profile along scrape path
- Often richer in harmonics (regular texture → tonal components)

## Key Papers / Implementations
- van den Doel & Pai (1996): "The sounds of physical shapes" — early system
- O'Brien, Shen & Gatchalian (2002): FEM + rigid-body sound
- James, Barbic & Pai (2006): Precomputed acoustic transfer
- Zheng & James (2011): Rigid-body fracture sound with precomputed transfer

## Related Concepts
- [[impact-synthesis]] — core sound generation model
- [[fem-bem-for-modal-synthesis]] — offline mode computation
- [[resonator-bank-implementation]] — DSP realization
- [[gpu-modal-synthesis]] — GPU acceleration for many objects

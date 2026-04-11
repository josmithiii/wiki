---
title: Friction Synthesis
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [friction, modal-synthesis, physical-modeling, acoustics, vibration]
sources:
  - /w/pasp/modal.tex
---

# Friction Synthesis

## Overview
Friction synthesis models continuous rubbing, bowing, and scraping sounds.
Unlike impact (a single impulse), friction creates ongoing, velocity-dependent forces
that couple back into the resonator bank — this requires a feedback loop.

## Friction Force Model
The classic Coulomb friction force is discontinuous (stick-slip).
For synthesis, smooth models are used:

### Stribeck curve approximation
  F_friction(v_rel) = mu_k * F_normal * tanh(v_rel / v_s) - b * v_rel

where:
- v_rel = relative velocity between object and bow/finger
- mu_k = kinetic friction coefficient
- F_normal = normal contact force
- v_s = Stribeck velocity (smoothing parameter)
- b * v_rel = viscous term

### Physical insight
- v_rel ~ 0: high static friction → "stick" phase, object moves with bow
- v_rel large: kinetic friction → "slip" phase, object slides under bow

## Feedback Structure
Unlike impact, friction creates a closed loop:
  x[n] → compute v_rel[n] → F_friction[n] → resonator bank → x[n+1]

This nonlinear feedback can produce self-sustained oscillations (violin bow!).

## Bowed String / Bowed Bar
For a bowed string at contact point x_b:
  v_bow - v_string(x_b, t) = v_rel(t)
  F_bow(t) = F_friction(v_rel(t))
  v_string(x_b, t) = sum_k [ phi_k(x_b) * q_k'(t) ]

Combine with modal ODE for each mode → nonlinear feedback system.
At correct bow speed and force: self-sustaining steady-state oscillation.

## Stability and Practical Challenges
- Stick-slip instabilities can cause numerical chaos
- Requires implicit or semi-implicit integration per time step
- Alternatively: use precomputed tables of steady-state solutions
  (Serafin, S. "Modeling Piano Hammers and Other Nonlinear Force-Driven Systems,"
  PhD thesis, Stanford University / CCRMA, 2004)

## Scraping and Rolling
- Scraping: friction force modulated by surface texture → band-limited noise
  Model: F_friction(t) = F0 * (1 + n(x_bow(t))) where n(x) = surface texture profile
- Rolling: continuous contact, no true stick-slip; sounds differ from bowing

## Applications
- Violin/cello/bass bowing
- Finger on wine glass (glass harmonica)
- Brake squeal, chalk on blackboard
- Rubber ball rolling on surface

## Cook's Physically-Based Models (Physis)
Perry Cook (2002, "Real Sound Synthesis"):
- "Bowed Rod" model: 1D bar modes + Stribeck feedback
- Demonstrates sustained tones with realistic bow-pressure / bow-speed interaction
- Playable via MIDI: bow force ↔ velocity, bow speed ↔ pitch control

## Related Concepts
- [[modal-synthesis-overview]] — parent concept
- [[impact-synthesis]] — impulsive excitation (simpler, no feedback)
- [[resonator-bank-implementation]] — the resonator bank used in feedback loop
- [[mode-shapes-and-eigenvalues]] — mode shapes needed at contact point

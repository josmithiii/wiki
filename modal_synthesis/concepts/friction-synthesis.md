---
title: Friction Synthesis
created: 2026-04-09
updated: 2026-11-25
type: concept
tags: [friction, modal-synthesis, physical-modeling, acoustics, vibration]
sources:
  - /w/pasp/modal.tex
  - https://ccrma.stanford.edu/~jos/pasp/Bowed_Strings.html
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
$$F_{\text{friction}}(v_{\text{rel}}) \;=\; F_{\text{normal}}\left[\mu_k + (\mu_s-\mu_k)\,e^{-(v_{\text{rel}}/v_s)^2}\right]\tanh(v_{\text{rel}} / v_0) + b\, v_{\text{rel}}$$

where:
- $v_{\text{rel}}$ = relative velocity between object and bow/finger
- $\mu_s > \mu_k$ = static and kinetic friction coefficients
- $F_{\text{normal}}$ = normal contact force
- $v_s$ = Stribeck velocity (how fast friction falls from $\mu_s$ to $\mu_k$)
- $v_0 \ll v_s$ = smoothing of the sign discontinuity at $v_{\text{rel}}=0$; $b\, v_{\text{rel}}$ = viscous term

The falling (negative-slope) part of this curve is what sustains stick-slip oscillation.

### Physical insight
- $v_{\text{rel}} \approx 0$: high static friction → "stick" phase, object moves with bow
- $v_{\text{rel}}$ large: kinetic friction → "slip" phase, object slides under bow

## Feedback Structure
Unlike impact, friction creates a closed loop:
$$x[n] \;\to\; v_{\text{rel}}[n] \;\to\; F_{\text{friction}}[n] \;\to\; \text{resonator bank} \;\to\; x[n+1]$$

This nonlinear feedback can produce self-sustained oscillations (violin bow!).

## Bowed String / Bowed Bar
For a bowed string at contact point $x_b$:
$$\begin{aligned}
v_{\text{bow}} - v_{\text{string}}(x_b, t) &= v_{\text{rel}}(t)\\
F_{\text{bow}}(t) &= F_{\text{friction}}(v_{\text{rel}}(t))\\
v_{\text{string}}(x_b, t) &= \sum_k \phi_k(x_b)\, \dot{q}_k(t)
\end{aligned}$$

Combine with modal ODE for each mode → nonlinear feedback system.
At correct bow speed and force: self-sustaining steady-state oscillation.

## Stability and Practical Challenges
- Stick-slip instabilities can cause numerical chaos
- Requires implicit or semi-implicit integration per time step
- Alternatively: precompute the friction-curve/junction solution as a lookup table, as in
  waveguide bowed strings ([[waveguide_synthesis/concepts/reed-and-bow-models|reed and bow models]];
  Serafin, S., "The Sound of Friction: Real-Time Models, Playability and Musical Applications,"
  PhD thesis, Stanford University / CCRMA, 2004)

## Scraping and Rolling
- Scraping: friction force modulated by surface texture → band-limited noise
  Model: $F_{\text{friction}}(t) = F_0\,(1 + n(x_{\text{bow}}(t)))$ where $n(x)$ = surface texture profile
- Rolling: continuous contact, no true stick-slip; sounds differ from bowing

## Applications
- Violin/cello/bass bowing
- Finger on wine glass (glass harmonica)
- Brake squeal, chalk on blackboard
- Rubber ball rolling on surface

## Key Work
- Avanzini, Serafin & Rocchesso (2005): elasto-plastic friction model driving modal resonators
  (IEEE Trans. Speech and Audio Processing)
- Essl & Cook (1999) and Essl, Serafin, Cook & Smith (2004): bowed bars, bowls and glasses with
  [[waveguide_synthesis/concepts/banded-waveguides|banded waveguides]] - one band-limited delay loop per mode
- Cook (2002), *Real Sound Synthesis for Interactive Applications*: modal and friction models for games/VR
- Finite-difference bowed strings with a modal bridge: [[waveguide_synthesis/concepts/bowed-string-finite-difference-models|yehu model]]

## Related Concepts
- [[modal-synthesis-overview]] — parent concept
- [[impact-synthesis]] — impulsive excitation (simpler, no feedback)
- [[resonator-bank-implementation]] — the resonator bank used in feedback loop
- [[mode-shapes-and-eigenvalues]] — mode shapes needed at contact point

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Bowed Strings](https://ccrma.stanford.edu/~jos/pasp/Bowed_Strings.html), [The Bow-String Scattering Junction](https://ccrma.stanford.edu/~jos/pasp/Bow_String_Scattering_Junction.html), [Digital Waveguide Bowed-String](https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Bowed_String.html), [Linear Commuted Bowed Strings](https://ccrma.stanford.edu/~jos/pasp/Linear_Commuted_Bowed_Strings.html)

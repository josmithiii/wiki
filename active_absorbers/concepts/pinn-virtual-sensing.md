---
title: PINN Virtual Sensing for Active Noise Control
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, wave-equation, acoustics, microphone, array, comparison]
sources: []  # primary sources pending ingestion
---

# Physics-Informed Neural Networks for Virtual Sensing in ANC

**Status: stub.** Primary sources not yet in `raw/`. This page fixes the
framing for the research project so it can be expanded in place.

## The virtual-sensing problem

Classical ANC minimizes residual power **at the error microphone**, which is
only a proxy for the actual target — usually an ear position, a listener
zone, or a compliance location that cannot be instrumented. Virtual sensing
is the practice of estimating the pressure at the *real* target from a set
of auxiliary mics placed where they are physically allowed.

Classical virtual sensing (Moreau, Cazzolato, Kestell) uses offline
transfer-function identification and a fixed mapping. Its failure modes are
**non-stationarity** (temperature drift, occupancy changes) and
**sparse sensor coverage** (the fixed mapping has no capacity to infer the
wave field elsewhere).

## The PINN idea

Represent the pressure field $p(\mathbf{r},t)$ directly as a neural network
with spatiotemporal inputs and a scalar output:
$$
p_\theta:\,(\mathbf{r},\,t)\,\mapsto\,p_\theta(\mathbf{r},t).
$$
Train with two loss terms:

1. **Data loss** — match the measured pressures at the physical mic
   locations $\mathbf{r}_k$, $p_\theta(\mathbf{r}_k,t) \approx y_k(t)$.
2. **Physics residual** — enforce the (homogeneous or forced) **Helmholtz**
   or wave equation on a batch of collocation points inside the domain:
$$
\mathcal{R}(\mathbf{r},t) = \nabla^2 p_\theta - \frac{1}{c^2}\frac{\partial^2 p_\theta}{\partial t^2} + s(\mathbf{r},t),
\quad
\mathcal{L}_{\text{phys}} = \|\mathcal{R}\|^2.
$$

The network is trained online on a sliding window of sensor data. Once
converged, $p_\theta$ can be **evaluated at the virtual target** $\mathbf{r}_v$
to produce a virtual error signal $e_v(n) = p_\theta(\mathbf{r}_v,n)$,
which is then fed into an otherwise classical [[fxlms-algorithm]] loop.

## Why this is attractive for ANC

- **Sensor sparsity.** Only a few mics are needed; the PDE constraint
  extrapolates the field.
- **Physical consistency.** Unlike a black-box regressor, the output obeys
  reciprocity, radiation conditions (if encoded in the loss), and the wave
  equation's speed limit.
- **Non-stationary environments.** The online version re-trains the network
  continually as conditions drift, so the virtual sensor tracks.
- **Composable with any controller.** PINN virtual sensing does not replace
  the controller — it replaces the sensor. FxLMS, Deep ANC, DRL-ANC can all
  benefit.

## Why this is hard

- **Training cost.** Online PINN training is expensive; the Helmholtz
  residual needs many collocation points and differentiation through the
  network at each step.
- **Conditioning.** The wave equation is a second-order PDE; small phase
  errors near sources cause large residuals and numerical instability.
- **Boundary conditions.** Room reflections, absorbing surfaces, and sources
  themselves all need to be modeled or flagged as unknowns.
- **Frequency range.** PINNs struggle at high frequencies where spatial
  oscillations are rapid; multi-scale architectures (Fourier features,
  SIREN) are typically required.

## Alternatives worth benchmarking against

- **Gaussian-process virtual sensing** with a Matérn or wave-equation
  kernel — closed-form posterior, no training.
- **Kirchhoff–Helmholtz integral** with measured boundary pressures.
- **Equivalent-source methods** (ESM) using spherical or plane-wave bases.
- **Black-box neural regression** without the physics loss — baseline for
  ablating the PDE term.

## Role in the AI-ANC project

Virtual sensing is a **controller-agnostic sensor upgrade**. The project
should benchmark it specifically against classical Moreau-style virtual
sensing on the rooftop-fan geometry, with an FxLMS controller as the fixed
reference, then re-run the comparison with Latent FxLMS
(see [[fxlms-algorithm]]) and Deep ANC (see [[deep-anc-crn]]) as controllers
to see whether the virtual-sensing win is additive.

See [[ai-anc-overview]] category 4 for the surrounding taxonomy.

## Candidate primary sources to ingest

Not yet in `raw/`. When available:

- Post-2020 PINN-for-acoustics survey(s).
- PINN virtual-sensing demonstrators for room acoustics / ANC.
- Comparisons of PINN, Gaussian-process, and ESM virtual sensing on a
  shared benchmark.
- Fourier-feature / SIREN adaptations that extend PINNs to audio-band
  frequencies.

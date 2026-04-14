---
title: Neural Secondary-Path Modeling for ANC
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, secondary-path, fxlms, stability, loudspeaker, comparison]
sources:
  - raw/DeepANC-nihms-1690502.txt
---

# Neural Secondary-Path Modeling

**Status: stub** (one primary source so far — Deep ANC — which *implicitly*
learns $S(z)$; explicit online neural identification papers not yet in
`raw/`).

## The problem

Every feedforward ANC system needs a model of the secondary path
$\hat{S}(z)$ — the transfer function from the control signal through the
DAC, amplifier, loudspeaker, acoustic propagation, and error microphone.
Classical FxLMS requires this estimate to have **phase error below 90°**
across the adaptation bandwidth (see [[fxlms-algorithm]]). In real
deployments $S(z)$ drifts:

- **Temperature and humidity** change the speed of sound and the driver's
  mechanical parameters.
- **Wind and airflow** modulate the acoustic path, especially outdoors
  (rooftop fans, HVAC outlets).
- **Fit and placement** (active [[headphones]], in-ear) change with every
  wear.
- **Nonlinear effects** (voice-coil heating, cone excursion, port
  compression) break the LTI assumption at high drive.

Classical practice: identify $\hat{S}(z)$ offline with white-noise probe
signals, or re-identify online with injected perturbation noise. Both are
unsatisfying — offline identification fails to track drift, and online
probe injection adds residual noise that degrades the ANC result.

## Neural alternatives

### 1. Implicit — subsumed in a Deep ANC controller

In [[deep-anc-crn]] the loss function includes the physical secondary path
during training, so the controller network implicitly learns to
pre-compensate $S(z)$. No explicit $\hat{S}(z)$ is maintained at runtime.
Upside: simple, nothing to identify online. Downside: the network freezes
the (training distribution of) $S(z)$, so large deployment drift forces
retraining.

### 2. Explicit online neural identification

A small MLP or RNN is trained online to map the control-signal history
to the observed error-mic signal, tracking $\hat{S}$ as the plant changes.
This can be done with or without probe injection:

- **With probe:** same as classical online ID, but with a nonlinear
  (hence more capacity) identifier; handles driver nonlinearity.
- **Probe-free:** exploit the natural excitation provided by the control
  signal itself; well-defined only when the control signal is sufficiently
  rich (broadband residuals during adaptation).

### 3. Generative secondary-path priors (NNSI-style)

Train an autoencoder on a dataset of secondary paths collected across the
expected operating envelope (temperatures, positions, fit conditions).
Online, identify $\hat{S}$ by latent-space adaptation over the decoder —
the same NNSI trick that [[neural-system-identification]] applies to the
*controller* filter, here applied to the *plant* filter.

### 4. Physics-informed plant models

Encode the loudspeaker's Thiele–Small small-signal model and the acoustic
path's Helmholtz propagation as differentiable blocks, and learn only the
residual. Much higher sample efficiency than a black-box identifier when
the physics is partially known.

## Open questions for the project

- **Latent drift identification.** Can we identify the secondary path in
  the latent space of a pre-trained autoencoder faster than FxLMS
  adapts the controller? If yes, we get a clean separation of timescales:
  fast controller adaptation (Latent FxLMS) on top of a slowly drifting
  latent plant model.
- **Probe-free bounds.** Under what excitation conditions is probe-free
  online identification well-posed?
- **Joint vs decoupled identification.** Is it better to identify
  controller and plant jointly (end-to-end Deep ANC) or to keep them
  decoupled with explicit $\hat{S}$? The answer likely depends on the
  drift rate.

## Relation to other pages

- [[fxlms-algorithm]] — classical secondary-path requirement and the 90°
  phase-error bound.
- [[deep-anc-crn]] — the implicit / end-to-end alternative.
- [[neural-system-identification]] — the manifold-constrained ID framework
  that this page's item 3 instantiates.
- [[ai-anc-overview]] category 3 — where this page sits in the taxonomy.

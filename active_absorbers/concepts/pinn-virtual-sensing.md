---
title: PINN Virtual Sensing for Active Noise Control
created: 2026-04-14
updated: 2026-04-15
type: concept
tags: [anc, fxlms, wave-equation, acoustics, microphone, array, comparison]
sources:
  - raw/PINN-ANC-Zhang-2309.10605.txt
  - raw/PINN-SoundField-Survey-2408.14731.txt
  - raw/PINN-PointNeuron-2408.16969.txt
  - raw/PINN-PermutationInvariant-2601.19491.txt
  - raw/PINN-Volumetric-2403.09524.txt
  - raw/PINN-1D-ParamSources-2109.11313.txt
---

# Physics-Informed Neural Networks for Virtual Sensing in ANC

Virtual sensing replaces an *uninstrumentable* error microphone (inside an
ear canal, at a compliance point in a room) with an *estimate* of the
pressure there, derived from auxiliary microphones placed where they are
physically allowed. A PINN makes this estimate by training a neural network
to represent the pressure field $p(\mathbf{r},t)$ subject to both data
matching and a wave-equation residual. The controller — typically
[[fxlms-algorithm]] — runs unchanged on the virtual error signal.

Classical virtual sensing (Moreau, Cazzolato, Kestell) is a fixed linear
mapping identified offline. Its failure modes are **non-stationarity**
(temperature drift, occupancy changes) and **sparse sensor coverage** (a
fixed mapping has no capacity to infer the wave field elsewhere). PINN
virtual sensing aims to fix both by re-estimating the field continually with
a physically-consistent parametric surrogate.

## The PINN idea

Represent the pressure field $p(\mathbf{r},t)$ directly as a neural network
$p_\theta\!:\,(\mathbf{r},t)\to p_\theta(\mathbf{r},t)$. Train with two loss
terms:

1. **Data loss** — match the measured pressures at the physical mic
   locations $\mathbf{r}_k$: $p_\theta(\mathbf{r}_k,t) \approx y_k(t)$.
2. **Physics residual** — enforce the wave equation on a batch of
   collocation points inside the domain:
$$
\mathcal{R}(\mathbf{r},t) = \nabla^2 p_\theta - \frac{1}{c^2}\frac{\partial^2 p_\theta}{\partial t^2},
\qquad
\mathcal{L}_{\text{phys}} = \|\mathcal{R}\|^2.
$$

Once $p_\theta$ is fit, evaluate it at the virtual target $\mathbf{r}_v$ to
produce a virtual error signal $e_v(n) = p_\theta(\mathbf{r}_v,n)$ which is
fed into an otherwise-standard FxLMS loop.

## Zhang et al. 2023 — the canonical PINN-for-ANC demonstration

Zhang, Ma, Abhayapala, Samarasinghe, Bastine[^zhang23] provide the
reference implementation and the first clean benchmark of PINN virtual
sensing inside an actual ANC loop.

**Architecture and training.** A small fully-connected MLP — one hidden
layer, 16 neurons, $\tanh$ activation — maps $(n, x, y, z) \to p(n,x,y,z)$.
The loss is $\mathcal{L}_{\text{data}} + \lambda\,\mathcal{L}_{\text{phys}}$
with the wave-equation residual above. Training uses TensorFlow autodiff,
$5\times 10^5$ epochs, learning rate $10^{-3}$.

**Geometry.**

- **8 monitoring microphones** on a sphere of radius $r = 0.26$ m *outside*
  the region of interest (the head).
- **Virtual error microphones** at $\pm 0.1$ m along the $y$-axis (ear
  positions).
- **2 secondary sources** and **1 primary source**; tonal primaries at
  $\{300, 400, 500\}$ Hz; sample rate 24 kHz, $c = 343$ m/s.

**Controller integration.** The ANC loop is a standard multichannel FxLMS
(they call it MCFxLMS) with two substitutions: the primary-path signal at
the virtual locations is PINN-interpolated, and the residual signal for the
FxLMS error is likewise read off the PINN. Zhang et al. compare the
*PINN-assisted* ANC system against (a) a conventional multiple-point ANC
system using only the monitoring mics as error references, and (b) a
spherical-harmonic (SH) interpolation baseline.

**Reported results.**

- $\sim 8$ dB lower interpolation error vs the SH baseline at the virtual
  positions.
- **$\sim -13$ dB additional steady-state noise reduction** at the ear
  virtual mics vs multiple-point ANC.
- $\sim -10$ dB lower residual in the controlled region around the ears.

The critical fact for the AI-ANC project: **the controller is unchanged**.
All the improvement comes from a better error signal, not a better
adaptation rule. This is what makes virtual sensing a *controller-agnostic
sensor upgrade* — see the "Role in the AI-ANC project" section below.

## The wider PINN-for-acoustics family

Zhang et al. 2023 is a small MLP with a generic Helmholtz loss. Several
more sophisticated architectures have appeared since and are candidates for
upgrading the basic PINN virtual sensor:

### Point Neuron Learning (Bi & Abhayapala 2024)[^bi24]

Every neuron embeds the **free-space Green's function** — the 0-th order
spherical Hankel function $h_0^{(1)}$ — as its activation, so the forward
pass **strictly satisfies the Helmholtz equation by construction**. No PDE
loss term is needed; training reduces to observation-MSE plus $\ell_1$
regularization. Neuron parameters are interpretable: weights encode source
amplitudes, biases encode source locations. Outperforms vanilla PINN and
kernel ridge regression on 2-D / 3-D reverberant sound-field reconstruction,
especially in extrapolation regimes where vanilla PINNs drift.

### Permutation-invariant deep-set PINN (Chen et al. 2025)[^chen25]

Architecture: $\hat{P}(\mathbf{r},\mathbf{s},f) = \rho(\phi(\mathbf{r}) + \phi(\mathbf{s}))$
with two MLPs $\phi, \rho$ (2 hidden layers × 128, $\tanh$). The summation
in the latent space guarantees permutation invariance, which in turn
*automatically* enforces **acoustic reciprocity**
$P(\mathbf{r},\mathbf{s}) = P(\mathbf{s},\mathbf{r})$ — no loss term needed.
Supports region-to-region ATF interpolation (both source and receiver
varying), beats kernel ridge regression by $>5$ dB NMSE above 1 kHz on the
UTS 60-speaker / 64-mic anechoic dataset. One limitation: one model per
frequency bin.

### Volumetric time-domain PINN for speech (Olivieri et al. 2024)[^olivieri24]

Time-domain wave-equation PINN for volumetric RIR reconstruction from sparse
mics, tested on the real-measured **MeshRIR** dataset. Handles *broadband*
speech inputs — crucial for ANC, since most PINN-acoustics work has been
monochromatic. Derived quantities like particle velocity and intensity can
be read off the network via autodiff. Beats frequency-domain equivalent-
source and time-domain RIR-ESM baselines.

### Historical / background

- **Borrel-Jensen et al. 2021**[^borrel21]: the first parametric PINN for
  1-D sound fields with *moving* Gaussian sources and frequency-dependent
  impedance boundaries. Useful as context, not for ANC directly — 1-D only,
  targeted at VR/games surrogate modeling.
- **Koyama et al. 2024 survey**[^koyama24]: IEEE Signal Processing Magazine
  invited survey. Five-category taxonomy of physics-informed ML for
  sound-field estimation (basis expansion, PDE-kernel KRR, PDE-regularized
  regression, vanilla PINN, physics-embedded architectures). The umbrella
  reference for this page.

## Why this is attractive for ANC

- **Sensor sparsity.** Only a few mics are needed — Zhang et al. use 8.
  The PDE constraint extrapolates the field.
- **Physical consistency.** Outputs obey reciprocity, radiation conditions
  (if encoded in the loss), and the wave equation's speed limit. A
  black-box regressor has no such guarantees.
- **Non-stationary environments.** The online version re-trains the network
  continually as conditions drift, so the virtual sensor tracks — though
  Zhang et al. 2023 only demonstrated stationary tonal sources.
- **Controller-agnostic.** FxLMS, Latent FxLMS ([[fxlms-algorithm]]), or
  Deep ANC ([[deep-anc-crn]]) all benefit from a better virtual error
  signal. The virtual sensor is a drop-in upgrade, not an architectural
  replacement.

## Why this is hard

- **Training cost.** PINN training is expensive; the Helmholtz residual
  needs many collocation points and differentiation through the network at
  each step. Zhang et al.'s $5\times 10^5$ epochs are offline; a real-time
  online variant is an open problem.
- **Conditioning.** The wave equation is a stiff second-order PDE; small
  phase errors near sources produce large residuals and numerical
  instability. Point Neuron Learning sidesteps this by making satisfaction
  exact at the architectural level.
- **Boundary conditions.** Room reflections, absorbing surfaces, and sources
  themselves all need to be modeled or flagged as unknowns. Zhang et al.
  2023 tests in a simulated room; outdoor rooftop-fan geometry adds
  ground reflection and edge diffraction that are harder to encode.
- **Frequency range.** Vanilla PINNs struggle at high frequencies where
  spatial oscillations are rapid. Fourier-feature / SIREN / point-neuron
  architectures are the standard remedies.

## Alternatives worth benchmarking against

- **Gaussian-process virtual sensing** with a Matérn or wave-equation
  kernel — closed-form posterior, no training.
- **Kirchhoff–Helmholtz integral** with measured boundary pressures.
- **Equivalent-source methods** (ESM) with spherical or plane-wave bases.
- **Black-box neural regression** without the physics loss — the ablation
  baseline that isolates the value of the PDE term.
- **Classical Moreau / Cazzolato / Kestell virtual sensing** — the
  established transfer-function-based method; critical comparison point.

## Role in the AI-ANC project

Virtual sensing is a **controller-agnostic sensor upgrade**, which makes it
compositional with every other row of [[ai-anc-overview]]. The natural
benchmark sequence on the rooftop-fan geometry:

1. Classical FxLMS with classical Moreau virtual sensing — baseline.
2. Same controller, Zhang-style PINN virtual sensing — measures the
   virtual-sensor win in isolation.
3. Latent FxLMS ([[fxlms-algorithm]]) with PINN virtual sensing — measures
   whether the two improvements stack.
4. Deep ANC ([[deep-anc-crn]]) with PINN virtual sensing — same, for the
   end-to-end neural controller.

If the PINN virtual-sensor win is additive across controllers, it's a
cheap-to-deploy enhancement for any ANC system. If the win saturates once
the controller is neural, the extra PINN complexity isn't worth it.

See [[ai-anc-overview]] category 4 for the surrounding taxonomy.

[^zhang23]: Zhang, Y. A., Ma, F., Abhayapala, T., Samarasinghe, P., Bastine, A., "An Active Noise Control System Based on Soundfield Interpolation Using a Physics-informed Neural Network," arXiv:2309.10605, 2023. See `raw/PINN-ANC-Zhang-2309.10605.txt`.
[^bi24]: Bi, Y., Abhayapala, T., "Point Neuron Learning: A New Physics-Informed Neural Network Architecture," arXiv:2408.16969, 2024. See `raw/PINN-PointNeuron-2408.16969.txt`.
[^chen25]: Chen, Z., Zhao, S., Ma, F., Cheng, X., Burnett, I., "Permutation-Invariant Physics-Informed Neural Network for Region-to-Region Sound Field Reconstruction," arXiv:2601.19491, 2025. See `raw/PINN-PermutationInvariant-2601.19491.txt`.
[^olivieri24]: Olivieri, M., Karakonstantis, X., Pezzoli, M., Antonacci, F., Sarti, A., Fernandez-Grande, E., "Physics-Informed Neural Network for Volumetric Sound Field Reconstruction of Speech Signals," arXiv:2403.09524, 2024. See `raw/PINN-Volumetric-2403.09524.txt`.
[^borrel21]: Borrel-Jensen, N., Engsig-Karup, A. P., Jeong, C.-H., "Physics-Informed Neural Networks for One-Dimensional Sound Field Predictions with Parameterized Sources and Impedance Boundaries," arXiv:2109.11313, 2021. See `raw/PINN-1D-ParamSources-2109.11313.txt`.
[^koyama24]: Koyama, S. et al. (attribution tentative), "Physics-Informed Machine Learning for Sound Field Estimation," *IEEE Signal Processing Magazine* invited paper, arXiv:2408.14731, 2024. See `raw/PINN-SoundField-Survey-2408.14731.txt`.

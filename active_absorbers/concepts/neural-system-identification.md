---
title: Neural Network System Identification (NNSI) for Adaptive Filtering
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, fxlms, rls, secondary-path, comparison, tutorial]
sources:
  - raw/NNSI-Helwani-ICASSP2023.txt
  - raw/LatentFxLMS-2507.03854v1.txt
---

# Neural Network System Identification (NNSI)

**NNSI** is a framework for adaptive acoustic filtering in which the FIR
coefficient vector $\mathbf{w}$ is constrained to lie on the **image of a
pre-trained decoder** $D\!:\mathbb{R}^d\!\to\!\mathbb{R}^L$, with $d \ll L$.
Online adaptation then happens in the decoder's latent space rather than in
the full $L$-dimensional filter space. NNSI is not a specific algorithm but a
recipe that can wrap LMS, NLMS, RLS, Kalman filtering, or FxLMS.

The parent reference is Helwani, Smaragdis, and Goodwin, *"Generative Modeling
Based Manifold Learning for Adaptive Filtering Guidance,"* ICASSP 2023[^helwani23],
cited as [3] in Sarkar et al. 2025[^sarkar25].

## The core idea

If the physical situation driving the adaptive filter (source position, room
geometry, ear-cup fit, cable state) is constrained to a bounded region, then
the set of *converged* filter weights lies on a low-dimensional manifold
$\mathcal{M}\subset\mathbb{R}^L$. An autoencoder trained on a dataset of
converged filters learns an approximation of $\mathcal{M}$ via the image of
its decoder:
$$
\mathcal{M} \approx \{\,D(\mathbf{z})\,:\,\mathbf{z}\in\mathbb{R}^d\,\}.
$$
During online operation, the adaptive filter is re-parameterized as
$\mathbf{w}(n) = D(\mathbf{z}(n))$. Updates apply a standard adaptive rule to
$\mathbf{z}$, not $\mathbf{w}$. The decoder then projects the latent step
back onto $\mathcal{M}$. The reduction in effective parameter count improves
convergence speed and steady-state error, at the cost of losing any weight
configurations outside $\mathcal{M}$.

## Generic NNSI update

Let $g(n)$ be the gradient produced by any classical adaptive rule acting on
the current $\mathbf{w}(n)$ — e.g., the FxLMS gradient $-e(n)\mathbf{x}'(n)$.
The NNSI update is
$$
\mathbf{z}(n+1) = \mathbf{z}(n) - \mu\,J_D^{T}(\mathbf{z}(n))\,g(n),
\qquad
\mathbf{w}(n+1) = D(\mathbf{z}(n+1)),
$$
where $J_D$ is the decoder Jacobian. In practice the Jacobian-vector product
is computed by automatic differentiation, so only a backward pass through the
decoder is needed per sample (or per block).

## Helwani 2023: the original NNSI paper

Helwani et al.[^helwani23] frame the manifold as a **topological space**
rather than a mere point cloud, and insist that the decoder preserve that
topology. The core construction:

1. **Topology-aware VAE.** Ordinary VAEs have no reason to preserve the
   topological structure of the input space in their latent space. Helwani
   et al. use a **DIP-VAE-II** disentanglement term to decorrelate the
   latent coordinates and add a *simplicial-complex constraint*: if a set
   of training impulse responses $\{h_{\sigma_0},\ldots,h_{\sigma_k}\}$
   forms a simplex $\sigma$ in input space, the corresponding latent codes
   must form a simplex in latent space. This forces convex combinations
   of IRs to map to convex combinations of codes.
2. **Kirchhoff–Helmholtz topology.** The choice of which IR tuples span a
   simplex is driven by the **Kirchhoff–Helmholtz integral**: pressure
   within a volume is determined by boundary pressure and its normal
   derivative, so topology in the acoustic IR space is determined by the
   monitoring microphone arrangement. The learned manifold therefore
   encodes the array geometry directly.
3. **Retraction-based adaptation.** Instead of a vanilla
   Jacobian-vector-product latent step, Helwani et al. use a **retraction**
   $\psi$ — a smooth mapping from the tangent space $T_{\mathbf{z}}\mathcal{M}$
   back onto the manifold. One gradient step becomes "step in the tangent
   space, then retract." Both a first-order (Euler) retraction and a
   second-order (Newton-style) retraction are derived.

Experiments demonstrate the method on **acoustic impulse-response tracking**
with baselines of plain RLS and $\ell_1$-regularized RLS (forgetting factor
$0.95$). Training set: 200 synthetic RIRs generated in a $6\times 6 \times 2$ m
shoebox via Pyroomacoustics. Test: unseen RIRs at 20 dB SNR. The
retraction-based method reaches lower early-stage error than both RLS
baselines due to the latent-space dimensionality reduction.

Notable gaps in the 2023 paper — filled by follow-ups rather than this one:

- **FxLMS is not tested**, only RLS-style IR tracking. The FxLMS extension is
  Sarkar et al. 2025 (*Latent FxLMS*, see [[fxlms-algorithm]]).
- **No secondary-path modeling** — the adaptive filter here *is* the acoustic
  channel estimate, not a controller with a plant in the loop.
- **No online retraining** of the VAE — the learned manifold is frozen at
  deployment.

## Instantiations in the literature

| Base algorithm | Application | Reference |
| --- | --- | --- |
| RLS / $\ell_1$-reg RLS | Acoustic IR tracking (shoebox sim) | Helwani et al. ICASSP 2023[^helwani23] |
| FxLMS | Spatially constrained feedforward ANC | Latent FxLMS, Sarkar et al. 2025[^sarkar25] (see [[fxlms-algorithm]]) |

## Training the autoencoder

The decoder is trained offline on a dataset of converged filters (or, in
Helwani 2023, measured impulse responses) $\{\mathbf{w}^*_k\}$, one per
sampled configuration of the underlying physical constraint. The choice of
regularization determines how the latent space is shaped:

- **Plain autoencoder.** Minimum reconstruction error; no latent-space
  structure.
- **DIP-VAE-II + simplicial-complex constraint.** Helwani 2023's choice.
  Enforces both disentanglement and topology preservation via
  Kirchhoff–Helmholtz-derived simplices.
- **Plain variational autoencoder (VAE).** A generic KL-regularized VAE
  without the topology constraint; in *Latent FxLMS* this turns out to
  *hurt* convergence compared to plain AE + mixup.
- **Mixup constraint.** Convex combinations of training filters must
  round-trip correctly through the AE; empirically the most useful
  constraint for FxLMS adaptive-filter guidance per Sarkar et al. 2025.
- **Physics-based constraints.** Directly impose Helmholtz, image-source,
  or reciprocity structure on the reconstructed impulse responses — open
  direction, closest in spirit to the PINN architectures catalogued on
  [[pinn-virtual-sensing]].

## Relation to Latent FxLMS

Latent FxLMS is exactly the FxLMS instantiation of NNSI. The Latent FxLMS
bullet on [[fxlms-algorithm]] gives the concrete update and the empirical
findings (latent-normalized updates + mixup beats VAE).

## Why this matters for the AI-ANC project

NNSI gives a **principled way to inject prior knowledge** into a classical
adaptive loop without throwing the loop away. It preserves the stability,
adaptivity, and real-time guarantees of FxLMS / RLS / Kalman, but exploits
the fact that the deployment scenario is usually constrained. For rooftop-fan
ANC with a bounded source region, this is a near-perfect fit — and it
composes with the other entries in [[ai-anc-overview]].

## Open questions

- **Generalization off the manifold.** What happens when the true converged
  filter lies outside $D(\mathbb{R}^d)$?
- **Autoencoder retraining.** When is it worth refreshing the decoder with
  newly observed converged filters — and can that be done online?
- **Manifold discovery without labels.** Can we learn the decoder from
  *operational* data without a pre-collected set of converged filters?

[^helwani23]: Helwani, K., Smaragdis, P., Goodwin, M. M., "Generative Modeling Based Manifold Learning for Adaptive Filtering Guidance," *ICASSP 2023*, pp. 1–5. See `raw/NNSI-Helwani-ICASSP2023.txt`.
[^sarkar25]: Sarkar, K. et al., "Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters," arXiv:2507.03854, 2025. See `raw/LatentFxLMS-2507.03854v1.txt`.

---
title: Neural Network System Identification (NNSI) for Adaptive Filtering
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, fxlms, rls, secondary-path, comparison, tutorial]
sources:
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
cited as [3] in Sarkar et al. 2025[^sarkar25]. A follow-up applies the same
idea to an extended Kalman filter for acoustic echo cancellation[^nnsi-aec].

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

## Instantiations in the literature

| Base algorithm | Application | Reference |
| --- | --- | --- |
| RLS | Acoustic impulse-response tracking | Helwani et al. ICASSP 2023[^helwani23] |
| Extended Kalman filter | Acoustic echo cancellation | NNSI-AEC follow-up[^nnsi-aec] |
| FxLMS | Spatially constrained ANC | Latent FxLMS, Sarkar et al. 2025[^sarkar25] (see [[fxlms-algorithm]]) |

## Training the autoencoder

The decoder is trained offline on a dataset of converged filters
$\{\mathbf{w}^*_k\}$, one per sampled configuration of the underlying physical
constraint (e.g. source position on a grid). The choice of regularization
determines how the latent space is shaped:

- **Plain autoencoder.** Minimum reconstruction error; no latent-space
  structure.
- **Variational autoencoder (VAE).** Latent-space prior encourages
  disentangled codes; in Latent FxLMS this turns out to *hurt* convergence
  compared to plain AE + mixup.
- **Mixup constraint.** Convex combinations of training filters must
  round-trip correctly through the AE; empirically the most useful
  constraint for adaptive-filter guidance.
- **Physics-based constraints.** Impose Helmholtz / image-source / reciprocity
  structure on the reconstructed impulse responses (open direction).

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

[^helwani23]: Helwani, K., Smaragdis, P., Goodwin, M. M., "Generative Modeling Based Manifold Learning for Adaptive Filtering Guidance," *ICASSP 2023*, pp. 1–5. `[pending ingestion]`
[^nnsi-aec]: Follow-up NNSI-for-Kalman paper referenced as [4] in Sarkar et al. 2025. `[pending full citation + ingestion]`
[^sarkar25]: Sarkar, K. et al., "Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters," arXiv:2507.03854, 2025. See `raw/LatentFxLMS-2507.03854v1.txt`.

---
title: Meta-Learning Weight Updates for Adaptive ANC
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, fxlms, lms, comparison, stability]
sources:
  - raw/LatentFxLMS-2507.03854v1.txt
---

# Meta-Learning Weight Updates

A complementary line to [[neural-system-identification]]: instead of
constraining the filter to a manifold, **learn the *update rule* itself** with
a neural network. The classical gradient step
$\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\,e(n)\mathbf{x}'(n)$ (see
[[fxlms-algorithm]]) is replaced by
$$
\mathbf{w}(n+1) = \mathbf{w}(n) + f_\theta\!\big(\mathbf{w}(n),\,\mathbf{x}(n),\,e(n),\,\text{state}\big),
$$
where $f_\theta$ is a small neural network trained offline across many
instances of the adaptation problem. The network is a **learned optimizer**
for FxLMS, in the meta-learning sense of Andrychowicz et al. 2016 and
"learning to learn by gradient descent by gradient descent."

This approach is referenced as [5] in Sarkar et al. 2025[^sarkar25], and is
explicitly contrasted there with NNSI: meta-learning outputs **weight-space
updates**, while NNSI outputs **latent-space updates** that are then decoded.
Both try to beat vanilla FxLMS convergence, but through different
parameterizations.

## Training protocol (typical)

1. Collect a distribution over ANC scenarios — different reference
   statistics, different primary and secondary paths, different SNRs.
2. For each scenario, simulate a short adaptation trajectory of length $T$
   starting from $\mathbf{w}(0)$.
3. Differentiate through the whole trajectory with the network $f_\theta$
   *in* the update rule, and minimize a meta-loss such as the mean residual
   power over $T$ or the time to reach a threshold MSE.
4. Typical parameterizations of $f_\theta$: small LSTM over per-tap state
   (à la L2L), 1-D convolution across the filter, or a coordinate-wise MLP.

## What the network sees

The input state passed to $f_\theta$ varies across the literature:

- **Current filter weights** $\mathbf{w}(n)$
- **Filtered reference** $\mathbf{x}'(n)$
- **Error** $e(n)$ and a short window of past errors
- **Running second-moment statistics** (for NLMS-style normalization)
- Sometimes the **reference signal spectrum** for narrowband vs broadband
  discrimination

## Strengths

- Can outperform FxLMS on the training distribution: faster convergence,
  lower steady-state error, implicit step-size tuning.
- Amortizes hyperparameter selection — the network learns effective $\mu$,
  leak factor, and regularization across scenarios.
- Can produce **stable** updates in regimes where classical FxLMS diverges,
  by learning to shrink the update near instability.

## Weaknesses

- **Distribution shift.** A meta-learner overfits its training distribution;
  deployment on a different plant or noise statistics degrades.
- **No stability guarantees.** Classical FxLMS has closed-form sufficient
  conditions on $\mu$ (see [[fxlms-algorithm]] stability section); a learned
  optimizer does not.
- **Training cost.** Differentiating through long trajectories is expensive
  and numerically delicate (exploding/vanishing meta-gradients).

## Relation to the research project

Meta-learning and NNSI target the same pain point — slow FxLMS convergence —
but from opposite directions. A compelling experiment for our setting: train
a single meta-learner across a distribution of primary-source positions on
the rooftop geometry, and compare against Latent FxLMS on the same
distribution. If Latent FxLMS wins, the manifold structure is the dominant
effect; if the meta-learner wins, the update-rule freedom matters more; if
they tie, a hybrid ("learned update on a learned manifold") is worth trying.

## Sources pending

We do not yet have the specific meta-learning-for-ANC paper referenced by
Sarkar et al. in `raw/`. When ingested, the reference should replace this
section and the footnote below.

[^sarkar25]: Sarkar, K. et al., "Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters," arXiv:2507.03854, 2025. Reference [5] of that paper is the meta-learning-for-ANC work discussed here. See `raw/LatentFxLMS-2507.03854v1.txt` for the exact citation context. `[primary source pending ingestion]`

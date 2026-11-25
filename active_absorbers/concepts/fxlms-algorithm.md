---
title: Filtered-x LMS (FxLMS) Algorithm
created: 2026-04-14
updated: 2026-11-25
type: concept
tags: [fxlms, lms, anc, feedforward, secondary-path, stability, reference]
sources:
  - raw/Morgan-1980-multiple-correlation-cancellation-loops.txt  # to ingest
  - raw/Burgess-1981-active-adaptive-sound-control-duct.txt       # to ingest
  - raw/LatentFxLMS-2507.03854v1.txt
  - raw/ANC-Tutorial-Review-1999-2010913102917710.txt
---

# Filtered-x LMS (FxLMS)

FxLMS is the standard adaptive algorithm for feedforward active noise control. It extends the Widrow–Hoff [[lms-algorithm]] to the case where a linear **secondary path** $S(z)$ (DAC, amplifier, loudspeaker, acoustic propagation, microphone, ADC) sits between the adaptive filter output and the error sensor. Without the "filtered-x" correction, the ordinary LMS update is biased by $S(z)$ and can diverge. The extension is attributed to Morgan (1980)[^morgan80] and Burgess (1981)[^burgess81], not the Widrow 1975 paper — see [[lms-algorithm]] for the underlying LMS machinery, and [[classical-anc-overview]] for the wider family of FxLMS variants.

## Setup

- Reference signal: $x(n)$ (correlated with the noise at the error mic)
- Adaptive FIR filter: $\mathbf{w}(n) = [w_0, w_1, \ldots, w_{L-1}]^T$
- Control (anti-noise) output: $y(n) = \mathbf{w}^T(n)\,\mathbf{x}(n)$
- Secondary path: $S(z)$, with estimate $\hat{S}(z)$ (see [[neural-secondary-path]])
- Primary-path noise at error mic: $d(n)$
- Error signal: $e(n) = d(n) - \big(s * y\big)(n)$

## Why plain LMS fails with a plant in the loop

The ordinary Widrow–Hoff update (see [[lms-algorithm]]) assumes the adaptive filter output goes directly to the error subtractor. When the error is measured *after* $S(z)$, the instantaneous gradient estimate $-e(n)\,\mathbf{x}(n)$ no longer points along the true MSE gradient — convergence slows, the stable $\mu$ range shrinks, and the loop goes unstable if $\angle S(e^{j\omega})$ exceeds $\pm 90^\circ$ at any frequency where the loop gain is non-negligible.

## The FxLMS fix

Filter the reference through $\hat{S}(z)$ before using it in the weight update:
$$
\mathbf{x}'(n) = \hat{s} * \mathbf{x}\,(n),
\qquad
\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\, e(n)\, \mathbf{x}'(n).
$$
This restores an (approximately) unbiased stochastic-gradient update with respect to the true $\mathrm{MSE} = E[e^2(n)]$.

## Stability and step size

For slow adaptation, $\mathbf{w}$ and $S(z)$ can be commuted and ordinary LMS analysis applies with $x'$ as the reference. The maximum usable step size is then approximately[^kuo99]
$$
\mu_{\max} \approx \frac{1}{2\,(L + \Delta)\,P_{x'}},
$$
where $P_{x'} = E[x'^2(n)]$ is the filtered-reference power and $\Delta$ is the overall delay of the secondary path in samples. (Kuo & Morgan write the update as $\mathbf{w}(n+1)=\mathbf{w}(n)+\mu\,\mathbf{x}'(n)e(n)$, for which the bound reads $1/[(L+\Delta)P_{x'}]$; the factor of 2 above is this page's $2\mu$ convention.) Secondary-path delay therefore slows FxLMS directly, by shrinking the usable step size. Robustness to phase error in $\hat{S}(z)$ requires
$$
\big|\angle S(e^{j\omega}) - \angle \hat{S}(e^{j\omega})\big| < 90^\circ
$$
across the adaptation bandwidth (Morgan 1980). Beyond $90^\circ$ the update has a positive projection on the error and the loop diverges.

## Variants

- **Normalized FxLMS (FxNLMS):** divide $\mu$ by $P_{x'}(n)$ for signal-power independence.
- **Leaky FxLMS:** add a leak factor $\gamma$: $\mathbf{w}(n+1) = (1-\mu\gamma)\mathbf{w}(n) + 2\mu e(n)\mathbf{x}'(n)$, for robustness to bias and finite-precision drift.
- **Modified FxLMS (Bjarnason 1995):** reconstructs the disturbance estimate $\hat d(n) = e(n) + (\hat s * y)(n)$ and adapts on the internal error $\hat d(n) - \mathbf{w}^T(n)\mathbf{x}'(n)$ formed with the *current* weights. This takes the secondary-path delay out of the adaptation loop, so the step size is no longer limited by $\Delta$ (ordinary-LMS bound), at the cost of extra filtering and more reliance on $\hat S$.
- **Multichannel FxLMS (MEFxLMS):** matrix of secondary paths $S_{mk}(z)$ from $K$ actuators to $M$ error mics ($J$ references, $K$ secondary sources, $M$ error sensors in the Kuo–Morgan convention used on [[classical-anc-overview]]); used for zone/room control.
- **Frequency-domain / partitioned-block FxLMS:** FFT-based for long $\mathbf{w}$ and/or long $\hat{S}$.
- **Latent FxLMS (Sarkar et al. 2025)[^latent]:** when the primary source position is constrained to a bounded spatial region, converged FxLMS weights $\mathbf{w}^*$ lie on a low-dimensional manifold in $\mathbb{R}^L$. Train a (shallow) autoencoder offline on a dataset of converged filters, one per sampled source location. Online, perform the FxLMS gradient step on the **latent code** $\mathbf{z}$ rather than on $\mathbf{w}$, and reconstruct the cancellation filter via the decoder $\mathbf{w}(n) = D(\mathbf{z}(n))$. A *latent-normalized* update plays the same role as NLMS in $\mathbf{z}$-space. With a **mixup**-trained decoder this converges significantly faster than standard FxLMS at comparable steady-state MSE; a plain-VAE decoder is markedly worse, so disentanglement is not the active ingredient. The paper only demonstrates bounded-region primaries — generalization / interpolation is flagged as future work.

## Causality constraint

For feedforward cancellation to work, the electrical path (reference mic → $\mathbf{w}$ → $S(z)$ → error mic) must be *faster* than the acoustic path (reference mic → error mic). If it is not, the adaptive filter would need to be non-causal. This is why FxLMS is typically applied to duct and headphone geometries where a reference can be taken upstream of the error sensor with adequate acoustic delay. When causality cannot be met, only narrowband or periodic noise remains controllable[^kuo99] — the case treated on [[tonal-periodic-anc]].

## JOS online books
- [[jos_books/entities/filters-book|Filters]]: [Phase and Group Delay](https://ccrma.stanford.edu/~jos/filters/Phase_Group_Delay.html) (the $90^\circ$ phase condition and the delay $\Delta$), [FIR Digital Filters](https://ccrma.stanford.edu/~jos/filters/Finite_Impulse_Response_Digital.html), [Filter Stability](https://ccrma.stanford.edu/~jos/filters/Filter_Stability.html)
- [[jos_books/entities/pasp-book|PASP]]: [Converting Propagation Distance to Delay Length](https://ccrma.stanford.edu/~jos/pasp/Converting_Propagation_Distance_Delay.html) (acoustic delay budget for the causality constraint)
- [[jos_books/entities/mdft-book|MDFT]]: [FIR System Identification](https://ccrma.stanford.edu/~jos/mdft/FIR_System_Identification.html) (offline estimation of $\hat S$)

[^morgan80]: Morgan, D. R., "An Analysis of Multiple Correlation Cancellation Loops with a Filter in the Auxiliary Path," *IEEE Trans. Acoustics, Speech, Signal Processing*, vol. 28, no. 4, pp. 454–467, Aug. 1980. *(pending ingestion into `raw/`)*
[^burgess81]: Burgess, J. C., "Active Adaptive Sound Control in a Duct: A Computer Simulation," *J. Acoust. Soc. Am.*, vol. 70, no. 3, pp. 715–726, Sep. 1981. *(pending ingestion into `raw/`)*
[^kuo99]: Kuo, S. M., Morgan, D. R., "Active Noise Control: A Tutorial Review," *Proc. IEEE*, vol. 87, no. 6, pp. 943–973, June 1999 (Eq. 10 and the causality discussion of Sec. II). See [[entities/source-papers#paper-kuo-morgan-anc-tutorial-1999|paper-kuo-morgan-anc-tutorial-1999]].
[^latent]: Sarkar, K., Zhuang, Y., Lu, A., Corey, R. M., Singer, A. C., Mittal, M., "Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters," arXiv:2507.03854, 2025. See `raw/LatentFxLMS-2507.03854v1.txt`.

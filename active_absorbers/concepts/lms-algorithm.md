---
title: LMS Adaptive Filter and Adaptive Noise Cancelling (Widrow 1975)
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [lms, anc, feedforward, stability, reference, history, tutorial]
sources:
  - raw/ANC-Widrow-j1975adaptivenoise.txt
---

# LMS Adaptive Filter and Adaptive Noise Cancelling

This page distills what is actually *in* Widrow et al. 1975[^widrow75] — the Widrow–Hoff LMS algorithm, the tapped-delay-line adaptive filter, and the "adaptive noise cancelling" architecture that motivated it. For the acoustic-control extension with a plant in the loop, see [[fxlms-algorithm]].

## Adaptive noise cancelling architecture

Two inputs:
- **Primary** $d(n) = s(n) + n_0(n)$ — signal of interest plus noise
- **Reference** $x(n) = n_1(n)$ — correlated with $n_0$ but (ideally) uncorrelated with $s$

An adaptive FIR filter $\mathbf{w}(n)$ transforms $x(n)$ into an estimate of $n_0(n)$; the output is
$$
e(n) = d(n) - \mathbf{w}^T(n)\,\mathbf{x}(n).
$$
When the filter has converged, $e(n)$ is the minimum-MSE estimate of $s(n)$. Unlike fixed Wiener filtering, no prior spectral knowledge is required — the filter learns online from $e(n)$ alone.

## The Widrow–Hoff LMS update

Minimize $\xi(n) = E[e^2(n)]$ by stochastic gradient descent on the instantaneous squared error. With the true gradient $\nabla\xi = -2\mathbf{P} + 2\mathbf{R}\mathbf{w}$ replaced by the one-sample estimate $\hat{\nabla} = -2 e(n)\,\mathbf{x}(n)$:
$$
\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\, e(n)\, \mathbf{x}(n).
$$
No squaring, averaging, or differentiation is required — just a multiply–accumulate per tap per sample. The expected weight vector converges to the Wiener solution $\mathbf{w}^* = \mathbf{R}^{-1}\mathbf{P}$ provided
$$
0 < \mu < \frac{1}{\lambda_{\max}},
$$
where $\lambda_{\max}$ is the largest eigenvalue of the reference autocorrelation matrix $\mathbf{R}$.

## Convergence time constants

The learning curve is a sum of exponentials, one per mode. The $p$-th mode has time constant $\tau_p = 1/(4\mu\lambda_p)$. A single-exponential approximation using $\mathrm{tr}(\mathbf{R})$ gives
$$
\tau_{\mathrm{mse}} \approx \frac{L+1}{4\mu\,\mathrm{tr}(\mathbf{R})} = \frac{\text{(number of weights)}}{(4\mu)\cdot\text{(total input power)}}.
$$
This is the fundamental speed-vs-misadjustment trade-off of LMS: small $\mu$ means slow adaptation; large $\mu$ means noisy weights and residual MSE above the Wiener floor.

## Tapped-delay-line FIR realization

The adaptive linear combiner operates on a delay-line state $\mathbf{x}(n) = [x(n), x(n-1), \ldots, x(n-L+1)]^T$. Design rules from the paper:
- **Tap spacing:** $\le 1/(2B)$ (Nyquist for signal bandwidth $B$)
- **Total delay length:** $\ge 1/\Delta f$ for frequency resolution $\Delta f$
- **Number of weights:** $L \approx 2B/\Delta f$
- Non-uniform (e.g. log-periodic) tap spacing can reduce $L$ without changing the adaptation law.

## Example applications in the paper

Widrow 1975 demonstrates adaptive cancelling across a spectrum of application domains, none of which involve an acoustic plant in the control path:
- **ECG interference cancelling** — remove 60 Hz power-line hum from electrocardiograms using a reference taken from a wall outlet; the filter learns the small magnitude/phase mismatch between the two paths.
- **Speech with noise** — cancel noise in a cockpit/factory environment given a reference mic in the noise field.
- **Antenna sidelobe cancelling** — suppress jammers using an auxiliary antenna and a two-weight combiner (one of the earliest known adaptive-array applications).
- **Echo/reverberation suppression**, **maternal ECG removal from fetal ECG**, and **plant-noise reduction in speech**.

## Why this is not yet FxLMS

In all of the 1975 examples, the adaptive filter output goes *directly* to the subtractor — there is no dynamic system between $\mathbf{w}^T\mathbf{x}$ and the error sensor. The moment you drop a loudspeaker, acoustic path, and error microphone into that position, the instantaneous gradient $-e(n)\mathbf{x}(n)$ is no longer unbiased, stability is lost at phase errors exceeding $90^\circ$, and the filtered-reference correction of [[fxlms-algorithm]] becomes necessary. Morgan (1980) and Burgess (1981) made that extension; Widrow's 1975 paper does not anticipate it.

## Causality caveat (already visible in 1975)

Widrow notes in Appendix B that an ideal noise-cancelling filter may be non-causal when the reference path has more delay than the primary path, and gives the finite-length causal approximation. This same causality constraint re-appears in acoustic ANC, where the reference-mic-to-error-mic electrical path must be faster than the acoustic path — see the causality note on [[fxlms-algorithm]].

[^widrow75]: Widrow, B., Glover, J. R., McCool, J. M., Kaunitz, J., Williams, C. S., Hearn, R. H., Zeidler, J. R., Dong, E., Goodlin, R. C., "Adaptive Noise Cancelling: Principles and Applications," *Proc. IEEE*, vol. 63, no. 12, pp. 1692–1716, Dec. 1975. See `raw/ANC-Widrow-j1975adaptivenoise.txt`.

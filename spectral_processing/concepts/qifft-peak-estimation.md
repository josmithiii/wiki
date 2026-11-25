---
title: QIFFT Peak Estimation
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [qifft, peak-detection, sinusoidal]
sources:
  - /w/sasp/qifft.tex
  - /w/sasp/qint.tex
  - /w/sasp/peaks.tex
  - /w/sasp/findpeaks.tex
  - /w/sasp/maxr.tex
  - https://ccrma.stanford.edu/~jos/sasp/Optimal_Peak_Finding_Spectrum.html
  - https://ccrma.stanford.edu/~jos/sasp/Sinusoidal_Peak_Interpolation.html
---

# QIFFT Peak Estimation

The **Quadratically-Interpolated FFT** (QIFFT) method estimates the
amplitude, frequency, and phase of each spectral peak by fitting a
parabola to the three log-magnitude samples around a local maximum.
A fast, approximate maximum-likelihood estimator for sinusoids in
noise.

## Algorithm

Given the **dB** magnitudes $\alpha$, $\beta$, $\gamma$ of bins $k-1$, $k$
(the local maximum) and $k+1$ of a zero-padded FFT, fit
$$y(p) \;=\; a(p - p_0)^2 + b$$
to the three samples. The parabolic vertex is:
$$p_0 \;=\; \frac{1}{2}\,\frac{\alpha - \gamma}{\alpha - 2\beta + \gamma}$$
$$y_{\max} \;=\; \beta - \tfrac{1}{4}(\alpha - \gamma)\, p_0$$

Estimates:
- **Frequency**: $\hat{f} = (k + p_0)\, f_s / N$
- **Amplitude (dB)**: $y_{\max}$
- **Phase**: linear (or quadratic) interpolation of the **unwrapped** phase at $k + p_0$

## Why Log Magnitude

A **Gaussian window transform** is exactly a parabola in
log magnitude (see [[gaussian-and-chirp-windows]]):
$$\log |W_G(\omega)| \;=\; -\tfrac{1}{2}\sigma^2 \omega^2$$
So QIFFT is **exact** for a Gaussian window. Other windows have
approximately parabolic main-lobe tops — flatter tops give lower bias.

## Bias vs Window Type

Approximate peak-frequency bias (% of $f_s/M$) versus zero-padding
factor $L = N/M$, from the Abe-Smith fits behind SASP's
minimum-zero-padding tables (`zpfmin.m`):

| Window | Bias at $L=2$ | Bias at $L=5$ |
|--------|--------------:|--------------:|
| Rectangular | ~1% | $<0.1$% |
| Hann/Hamming | ~0.2% | $<0.05$% |
| Blackman | ~0.1% | $<0.01$% |
| Blackman-Harris | $<0.1$% | negligible |

**Rule**: zero-padding factor $L \ge 5$ makes the bias inaudible for
any standard window (a 0.1% frequency error is about 2 cents). Windows
with flatter main-lobe tops need less: see the minimum-$L$ table in
[[zero-padding-and-interpolation]].

## Optimality

QIFFT is:
- Extremely close to the **maximum-likelihood** estimator for a **single**
  sinusoid in white noise (the ML estimate is the peak of the
  rectangular-window DTFT magnitude)
- Near-ML for multiple **well-separated** sinusoids
- **Perceptually optimal** for $L \ge 5$: errors below JND

Breakdown cases:
- Overlapping main lobes → side-lobe interaction biases both peaks
- Very short windows → parabolic fit is a poor match for the main lobe
- Chirps → use chirplet / reassigned spectrogram

## Implementation Notes

- Always use dB magnitude, not linear.
- Always use **zero-phase zero padding** for clean phase interpolation.
- Pick peaks as local maxima with a minimum amplitude threshold and a
  minimum separation (≥ 1 main-lobe width) — see [`findpeaks.m`](https://ccrma.stanford.edu/~jos/sasp/Matlab_listing_findpeaks_m.html).
- Unwrap phase before interpolating (see [[phase-vocoder-and-tsm]]).

## Reassignment (brief)

Time-frequency **reassignment** improves peak localization by moving
each STFT sample to its instantaneous frequency and group delay
(computed from derivatives of $X_m(k)$ wrt window). Sharper than
QIFFT but more expensive; complementary.

## Related Concepts
- [[sinusoidal-modeling]] — QIFFT is the estimator
- [[spectrum-analysis-windows]] — window choice determines bias
- [[zero-padding-and-interpolation]] — required for accurate peaks
- [[gaussian-and-chirp-windows]] — QIFFT is exact for Gaussian
- [[nonstationary-sinusoidal-estimation-ddm]] - DDM/PMS estimator for nonstationary partials

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Quadratic Interpolation of Spectral Peaks](https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html), [Bias of Parabolic Peak Interpolation](https://ccrma.stanford.edu/~jos/sasp/Bias_Parabolic_Peak_Interpolation.html), [Optimal Peak-Finding in the Spectrum](https://ccrma.stanford.edu/~jos/sasp/Optimal_Peak_Finding_Spectrum.html), [Maximum Likelihood Sinusoid Estimation](https://ccrma.stanford.edu/~jos/sasp/Maximum_Likelihood_Sinusoid_Estimation.html), [Matlab listing: qint.m](https://ccrma.stanford.edu/~jos/sasp/Matlab_listing_qint_m.html), [Time-Frequency Reassignment](https://ccrma.stanford.edu/~jos/sasp/Time_Frequency_Reassignment.html)

---
title: QIFFT Peak Estimation
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [qifft, peak-detection, sinusoidal]
sources:
  - /w/sasp/qifft.tex
  - /w/sasp/qint.tex
  - /w/sasp/peaks.tex
  - /w/sasp/findpeaks.tex
  - /w/sasp/maxr.tex
---

# QIFFT Peak Estimation

The **Quadratically-Interpolated FFT** (QIFFT) method estimates the
amplitude, frequency, and phase of each spectral peak by fitting a
parabola to the three log-magnitude samples around a local maximum.
A fast, approximate maximum-likelihood estimator for sinusoids in
noise.

## Algorithm

Given FFT magnitudes $\alpha = |X(k-1)|$, $\beta = |X(k)|$,
$\gamma = |X(k+1)|$ in **dB** (log magnitude), fit
$$y(p) \;=\; a(p - p_0)^2 + b$$
to the three samples. The parabolic vertex is:
$$p_0 \;=\; \frac{1}{2}\,\frac{\alpha - \gamma}{\alpha - 2\beta + \gamma}$$
$$y_{\max} \;=\; \beta - \tfrac{1}{4}(\alpha - \gamma)\, p_0$$

Estimates:
- **Frequency**: $\hat{f} = (k + p_0)\, f_s / N$
- **Amplitude (dB)**: $y_{\max}$
- **Phase**: linear interpolation of **unwrapped** phase at $k + p_0$

## Why Log Magnitude

A **Gaussian window transform** is exactly a parabola in
log magnitude (see [[gaussian-and-chirp-windows]]):
$$\log |W_G(\omega)| \;=\; -\tfrac{1}{2}\sigma^2 \omega^2$$
So QIFFT is **exact** for a Gaussian window. Other windows have
approximately parabolic main-lobe tops — flatter tops give lower bias.

## Bias vs Window Type

Peak-frequency bias (% of $f_s/M$) for minimum zero-padding factors:

| Window | Bias at $L=2$ | Bias at $L=5$ |
|--------|--------------:|--------------:|
| Rectangular | ~1% | $<0.1$% |
| Hann/Hamming | ~0.3% | $<0.05$% |
| Blackman | ~0.1% | $<0.01$% |
| Blackman-Harris | $<0.1$% | negligible |

**Rule**: zero-padding factor $L \ge 5$ makes bias perceptually
inaudible for any standard window (~2 cents).

## Optimality

QIFFT is:
- **ML-optimal** for a **single** sinusoid in white noise, asymptotically
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
  minimum separation (≥ 1 main-lobe width) — see `findpeaks.m`.
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

---
title: Noise Spectrum Analysis
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [noise, statistical-dsp, bbt, windows]
sources:
  - /w/sasp/noisespecanal.tex
  - /w/sasp/bbt.tex
  - /w/sasp/statdsp.tex
  - /w/sasp/estimator-variance.tex
---

# Noise Spectrum Analysis

The periodogram $|X_m(k)|^2$ is an **unbiased but inconsistent**
estimate of the power spectral density (PSD): its variance does
**not** decrease with longer windows. To get smooth PSD estimates
you must **average**.

## The Problem

For a WSS random signal,
$$\hat{S}_x(\omega) \;=\; \frac{1}{M}|X(\omega)|^2$$
has:
- **Mean**: smoothed true PSD (convolved with $|W|^2$).
- **Variance**: roughly $|S_x(\omega)|^2$ — constant in $M$.

More data gives higher frequency resolution, **not** lower variance.

## Bartlett's Method

Split signal into $K$ **non-overlapping** rectangular-windowed
segments, compute periodograms, average:
$$\hat{S}^{(B)}_x(\omega) \;=\; \frac{1}{K}\sum_{k=0}^{K-1}\hat{S}^{(k)}_x(\omega)$$
Variance reduces by factor $K$; frequency resolution drops by $K$.

## Welch's Method

Generalization of Bartlett with:
- **Windowing** (Hann, Hamming, etc.) to reduce leakage
- **Overlapping** segments (typically 50%) to use data more efficiently

$$\hat{S}^{(W)}_x(\omega) \;=\; \frac{1}{K U}\sum_{m=0}^{K-1}|X_m(\omega)|^2$$
where $U = \frac{1}{M}\sum w^2(n)$ normalizes window energy. Standard
choice for practical PSD estimation; much lower variance than a
single periodogram.

## Blackman-Tukey Method

Smooth the **sample autocorrelation** before transforming:
$$\hat{S}^{(BT)}_x(\omega) \;=\; \sum_{l=-L}^{L} w_{\text{lag}}(l)\,\hat{r}_{xx}(l)\, e^{-j\omega l}$$
Lag window $w_{\text{lag}}$ (e.g., Bartlett, Parzen) controls
resolution/variance. Equivalent to convolving the periodogram with
$W_{\text{lag}}(\omega)$.

Relation to Welch: both trade resolution for variance; Welch uses
frequency-domain averaging, BT uses lag-domain windowing. In
practice they give similar results.

## Bias-Variance Trade-off

| Knob | Effect |
|------|--------|
| Longer segments | better resolution, more variance |
| More segments | less variance, worse resolution |
| Larger overlap | more effective segments, more variance reduction |
| Wider lag window | less variance (BT), more bias |

**Rule of thumb**: pick segment length from desired resolution; pick
number of segments from desired variance; overlap 50% with Hann.

## Processing Gain

A window reduces noise variance by its **equivalent noise
bandwidth** (ENBW):
$$\text{ENBW} \;=\; \frac{M\sum w^2(n)}{\left[\sum w(n)\right]^2}$$
- Rectangular: 1.0
- Hann: 1.5
- Hamming: 1.36
- Blackman: 1.73
Windows trade flatness for slightly worse noise averaging.

## Estimator Variance

For a smoothed periodogram with $K$ independent averages:
$$\text{Var}[\hat{S}_x(\omega)] \;\approx\; \frac{S_x^2(\omega)}{K}$$
Use Chi-squared confidence intervals with $2K$ degrees of freedom.

## Practical Recipe

1. Choose segment length $M$ for desired $\Delta f$.
2. Pick a low-leakage window (Hann default; Kaiser for sharp spectra).
3. 50% overlap, Welch averaging.
4. Log-magnitude display in dB.
5. For short signals, use multitaper (DPSS) — multiple orthogonal
   windows averaged; lowest variance for fixed resolution.

## Related Concepts
- [[spectrum-analysis-windows]] — window choice here, too
- [[short-time-fourier-transform]] — Welch = windowed STFT with $|\cdot|^2$
- [[sms-sines-plus-noise]] — noise-model consumer of these estimates

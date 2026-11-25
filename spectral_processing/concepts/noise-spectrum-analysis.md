---
title: Noise Spectrum Analysis
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [noise, statistical-dsp, blackman-tukey, windows]
sources:
  - /w/sasp/noisespecanal.tex
  - /w/sasp/statdsp.tex
  - /w/sasp/estimator-variance.tex
  - https://ccrma.stanford.edu/~jos/sasp/Beginning_Statistical_Signal_Processing.html
  - https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Noise.html
---

# Noise Spectrum Analysis

The periodogram $\tfrac{1}{M}|X_m(k)|^2$ is an **asymptotically unbiased
but inconsistent** estimate of the power spectral density (PSD): its
variance does **not** decrease with longer windows. To get smooth PSD
estimates you must **average**.

## The Problem

For a WSS random signal,
$$\hat{S}_x(\omega) \;=\; \frac{1}{M}|X(\omega)|^2$$
has:
- **Mean**: the true PSD smoothed by $\tfrac{1}{M}|W(\omega)|^2$ (for a
  rectangular window, the transform of the Bartlett-window bias on the
  sample autocorrelation).
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

$$\hat{S}^{(W)}_x(\omega) \;=\; \frac{1}{K M U}\sum_{m=0}^{K-1}|X_m(\omega)|^2$$
where $U = \frac{1}{M}\sum w^2(n)$ normalizes window energy ($U=1$ for
the rectangular window, giving SASP's average of periodograms). Standard
choice for practical PSD estimation; much lower variance than a
single periodogram.

## Blackman-Tukey Method

Smooth the **sample autocorrelation** before transforming:
$$\hat{S}^{(BT)}_x(\omega) \;=\; \sum_{l=-L}^{L} w_{\text{lag}}(l)\,\hat{r}_{xx}(l)\, e^{-j\omega l}$$
Lag window $w_{\text{lag}}$ (e.g., Bartlett, Parzen) controls
resolution/variance. Equivalent to convolving the periodogram with
$W_{\text{lag}}(\omega)$. (SASP does not treat this method by name; its
"smoothed PSD" discussion of the Bartlett-windowed sample
autocorrelation is the same idea.)

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

## Processing Gain

Sinusoids add coherently in the DFT sum, noise adds on a power basis,
so a length-$N$ DFT gives a sinusoid in white noise a **processing gain**
of $N$ in its bin: $\text{SNR} = N A^2/\sigma_v^2$, i.e. $+3$ dB per
doubling of $N$. A tapered window gives up part of that gain, by its
**equivalent noise bandwidth** in bins,
$$\text{ENBW} \;=\; \frac{M\sum w^2(n)}{\left[\sum w(n)\right]^2}$$
(rectangular 1.0, Hamming 1.36, Hann 1.5, Blackman 1.73).

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

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [The Periodogram](https://ccrma.stanford.edu/~jos/sasp/Periodogram.html), [Welch's Method](https://ccrma.stanford.edu/~jos/sasp/Welch_s_Method.html), [Smoothed Power Spectral Density](https://ccrma.stanford.edu/~jos/sasp/Smoothed_Power_Spectral_Density.html), [Processing Gain](https://ccrma.stanford.edu/~jos/sasp/Processing_Gain.html), [Statistical Signal Processing](https://ccrma.stanford.edu/~jos/sasp/Beginning_Statistical_Signal_Processing.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Power Spectral Density](https://ccrma.stanford.edu/~jos/mdft/Power_Spectral_Density_Estimation.html)

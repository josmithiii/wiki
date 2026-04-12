---
title: Short-Time Fourier Transform
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [stft, dft, windows]
sources:
  - /w/sasp/stft.tex
  - /w/sasp/sinespecanal.tex
---

# Short-Time Fourier Transform

The STFT slides a window over the signal and computes a DTFT per
frame, producing a 2D time-frequency representation.

## Definition

$$X_m(\omega) \;=\; \sum_{n=-\infty}^{\infty} x(n)\, w(n - mR)\, e^{-j\omega n}$$

where
- $x(n)$ — input signal
- $w(n)$ — analysis window of length $M$
- $R$ — hop size in samples
- $m$ — frame index

In practice $\omega \to \omega_k = 2\pi k/N$ and the inner sum is an
$N$-point FFT with $N \ge M$ (zero-padded). This yields the
**discrete STFT** $X_m(k)$.

## Two Dual Interpretations

**OLA (transform) view** — fix $m$, vary $\omega$: a sequence of
windowed DFTs that tile time. See [[overlap-add-stft]].

**FBS (filter-bank) view** — fix $\omega_k$, vary $m$: the time series
$X_m(k)$ is the output of a bandpass filter at center frequency
$\omega_k$. See [[filter-bank-summation-stft]].

Both are rearrangements of the same double sum — Fourier duals.

## Key Parameters

| Parameter | Controls | Typical |
|-----------|----------|---------|
| Window length $M$ | frequency resolution ($\propto 1/M$) | 20–100 ms |
| Hop size $R$ | time resolution; $R \le M$ | $M/4$ (75% overlap) |
| FFT size $N$ | bin spacing ($2\pi/N$) | $\ge M$, power of 2 |
| Window shape $w$ | side-lobe leakage | Hann, Kaiser, BH |

## Frame vs Bin Rate

- Analysis frame rate: $f_s / R$
- Bin spacing in Hz: $f_s / N$
- Main-lobe width in Hz: $\sim k_w\, f_s / M$, $k_w$ = window constant

## Uncertainty Principle

Time-frequency resolution is bounded:
$$\Delta t \cdot \Delta f \;\ge\; \text{const}$$
Long windows = good frequency resolution, bad time resolution, and
vice versa. Gaussian window attains the lower bound (see
[[gaussian-and-chirp-windows]]).

## Invertibility

The STFT is highly redundant (oversampled in time when $R<M$ and in
frequency when $N>M$). Inversion uses either:
- **Inverse OLA**: sum windowed inverse DFTs of each frame.
- **FBS synthesis**: remodulate bin signals and sum.

Perfect reconstruction requires conditions on $(w, R, N)$ — see the
two view-specific pages.

## STFT Matrix Picture

For real-time audio $x(n)$, typical display:

```
time  →
freq  ┌──────────────────┐
  ↑   │    |X_m(k)| dB   │  ← spectrogram
      └──────────────────┘
```

A spectrogram is $|X_m(k)|$ on a dB scale. See
[[noise-spectrum-analysis]] for statistical smoothing.

## Related Concepts
- [[overlap-add-stft]] — transform view, COLA
- [[filter-bank-summation-stft]] — filter-bank view
- [[stft-modifications]] — safe spectral edits
- [[spectrum-analysis-windows]] — window choice

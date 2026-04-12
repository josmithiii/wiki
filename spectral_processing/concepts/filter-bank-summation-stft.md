---
title: Filter Bank Summation STFT (FBS)
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [stft, fbs, dft-filter-bank, perfect-reconstruction, portnoff]
sources:
  - /w/sasp/fbs.tex
  - /w/sasp/dftfilterbank.tex
  - /w/sasp/stftfilterbank.tex
  - /w/sasp/fftfb.tex
  - /w/sasp/portnoffwin.tex
  - /w/sasp/downsampling.tex
---

# Filter Bank Summation STFT (FBS)

The **filter-bank view** of the STFT: each DFT bin $X_m(k)$ is the
output of a bandpass filter centered at $\omega_k = 2\pi k/N$.

## Derivation

Rewrite the STFT, fixing $k$ and letting $n = mR$:
$$X_n(k) \;=\; e^{-j\omega_k n}\sum_{l} h(n-l)\, x(l), \qquad h(n) = w(-n)$$

So $X_n(k) = e^{-j\omega_k n}\, (h\ast x)(n)$ — a **demodulation**
(multiply by $e^{-j\omega_k n}$) followed by a lowpass filter with
impulse response $h(n) = w(-n)$, equivalent to a bandpass filter at
$\omega_k$ with prototype $w$.

## DFT Filter Bank

The length-$N$ DFT is a **critically sampled uniform filter bank** of
$N$ bandpass filters with identical prototype $W(\omega)$, evenly
spaced at $\omega_k = 2\pi k/N$. Adding $R>1$ decimation (hop) gives
an **under-sampled STFT filter bank** with $N$ channels downsampled by
$R$.

## Synthesis (Summation)

Reconstruct $x$ by remodulating each bin and summing:
$$\hat{x}(n) \;=\; \sum_{k=0}^{N-1} f(n)\, X_n(k)\, e^{j\omega_k n}$$
with synthesis window $f$ (often equal to $w$ or its dual).

## FBS Perfect Reconstruction Condition

Reconstruction is exact iff the **window samples at multiples of the
hop frequency** satisfy:
$$\sum_{k=0}^{N-1} w(n + kN) \;=\; c\quad \text{(Nyquist-}N\text{ window)}$$
Equivalently, $w$ is a **Nyquist-$N$** sequence:
$W(e^{j\omega}) + W(e^{j(\omega - 2\pi/N)}) + \cdots$ integrates to $c$.

Contrast with OLA's condition (COLA in time). The two conditions are
**Fourier duals**.

## Aliasing Cancellation

When $R > 1$, each channel is aliased. FBS perfect reconstruction
requires **aliasing cancellation** across channels upon resynthesis:
the imaging from remodulation cancels the aliasing from decimation.
This is the defining trick of maximally decimated filter banks.

## Portnoff Windows

For large hops $R > M$ (window shorter than hop), reconstruction
requires **Portnoff windows** — window functions longer than the FFT
size that satisfy FBS conditions. Built by time-aliasing a long
prototype into the FFT buffer. Enables efficient DFT filter banks
with narrow channels and long effective impulse responses.

## Complexity

- Direct filter bank: $N \cdot M$ mults/sample.
- FFT filter bank: $\sim\frac{N\log_2 N}{R}$ mults/sample via
  polyphase decomposition — same output, much cheaper.
- Polyphase view: rearrange $w$ into $R$ sub-filters, one per
  decimation phase $\Rightarrow$ FFT over phases.

## When to Use FBS

- Bin signals interpreted as time series: **phase vocoder**,
  [[f0-and-spectral-envelope]] tracking, instantaneous frequency.
- Audio coding filter banks (MPEG, AAC): polyphase modulated DFT banks.
- When the application wants per-channel processing rather than
  per-frame block processing.

## Related Concepts
- [[overlap-add-stft]] — dual OLA view
- [[short-time-fourier-transform]] — the common STFT
- [[multirate-filter-banks]] — generalization beyond uniform DFT
- [[phase-vocoder-and-tsm]] — canonical FBS application

---
title: SASP Overview
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [stft, dft, windows, sinusoidal, sms, phase-vocoder, applications]
sources:
  - /w/sasp/intro.tex
  - /w/sasp/contents.tex
  - /w/sasp/conclusions.tex
---

# SASP Overview

*Spectral Audio Signal Processing* (SASP) by Julius O. Smith III develops
the theory and practice of FFT-based analysis, modification, and
resynthesis of music and audio signals. Web edition:
`https://ccrma.stanford.edu/~jos/sasp/`.

## Big Picture

The book builds three interlocking views of the same math:

1. **Transform view** — the signal is a sum of windowed blocks, each
   analyzed by a DFT. This leads to the overlap-add (OLA) interpretation
   of the STFT and to fast FFT convolution.
2. **Filter-bank view** — each DFT bin is the output of a modulated
   bandpass filter. This is the filter-bank summation (FBS) interpretation
   and generalizes to multirate / wavelet filter banks.
3. **Sinusoidal-model view** — spectral peaks are tracked across frames
   and resynthesized as additive sinusoids, possibly with a noise
   residual (SMS).

All three converge on the Short-Time Fourier Transform
$$X_m(\omega) \;=\; \sum_{n=-\infty}^{\infty} x(n)\, w(n-mR)\, e^{-j\omega n}$$
with window $w$, hop size $R$, and frame index $m$.

## Chapter Map

| Part | Topic | Pages |
|------|-------|-------|
| Foundations | DFT/DTFT, four Fourier cases, theorems | [[dtft-and-fourier-theorems]], [[zero-padding-and-interpolation]] |
| Windows & FIR | Window zoo, FIR design | [[spectrum-analysis-windows]], [[window-design-methods]] |
| STFT | Two dual views | [[short-time-fourier-transform]], [[overlap-add-stft]], [[filter-bank-summation-stft]], [[stft-modifications]] |
| Sinusoidal | Peaks, tracking, SMS | [[sinusoidal-modeling]], [[qifft-peak-estimation]], [[sinusoidal-parameter-interpolation]], [[sms-sines-plus-noise]] |
| Modification | Phase vocoder, cross-synth | [[phase-vocoder-and-tsm]], [[cross-synthesis-and-morphing]] |
| Spectral models | f0, envelope, noise | [[f0-and-spectral-envelope]], [[noise-spectrum-analysis]] |
| Filter banks | Multirate, wavelets | [[multirate-filter-banks]] |
| Appendices | Gaussian, applications | [[gaussian-and-chirp-windows]], [[spectral-audio-applications]] |

## How the Views Connect

- OLA and FBS are **Fourier duals** — the same STFT, different
  scheduling of the sums. OLA groups by frame; FBS groups by bin.
- Sinusoidal modeling reads the STFT as a time-varying list of peaks.
- Phase vocoder is STFT modification that respects phase consistency
  across frames.
- Multirate filter banks generalize the uniform DFT filter bank to
  non-uniform (auditory, wavelet) partitions.

## Related Wikis
- [waveguide_synthesis](../../waveguide_synthesis/index.md) — physical modeling companion volume (PASP)
- [modal_synthesis](../../modal_synthesis/index.md) — modal / resonator view of the same signals

## References
[^1]: Smith, J.O. III. *Spectral Audio Signal Processing*, W3K, 2011.

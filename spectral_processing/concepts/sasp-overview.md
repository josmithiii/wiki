---
title: SASP Overview
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [stft, dft, windows, sinusoidal, sms, phase-vocoder, applications]
sources:
  - /w/sasp/intro.tex
  - /w/sasp/contents.tex
  - /w/sasp/conclusions.tex
---

# SASP Overview

*Spectral Audio Signal Processing* (SASP) by Julius O. Smith III[^1] develops
the theory and practice of FFT-based analysis, modification, and
resynthesis of music and audio signals. Free online at
<https://ccrma.stanford.edu/~jos/sasp/>; the chapter-by-chapter hub is
the [[jos_books/entities/sasp-book|SASP hub page]]. SASP is book 4 of a
series: its prerequisites are [[jos_books/entities/mdft-book|MDFT]] (the
DFT and its theorems) and [[jos_books/entities/filters-book|Filters]]
(LTI filters, phase, FIR), and its physical-modeling companion is
[[jos_books/entities/pasp-book|PASP]].

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

| Part | SASP chapter (online) | Wiki pages |
|------|-----------------------|------------|
| Foundations | 2. [Fourier Transforms and Theorems](https://ccrma.stanford.edu/~jos/sasp/Fourier_Transforms_Continuous_Discrete_Time_Frequency.html) | [[dtft-and-fourier-theorems]], [[zero-padding-and-interpolation]] |
| Windows | 3. [Spectrum Analysis Windows](https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Windows.html) | [[spectrum-analysis-windows]] |
| FIR design | 4. [FIR Digital Filter Design](https://ccrma.stanford.edu/~jos/sasp/FIR_Digital_Filter_Design.html) | [[window-design-methods]] |
| Sinusoids | 5. [Spectrum Analysis of Sinusoids](https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Sinusoids.html) | [[qifft-peak-estimation]], [[sinusoidal-modeling]] |
| Noise | 6. [Spectrum Analysis of Noise](https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Noise.html) | [[noise-spectrum-analysis]] |
| STFT | 7. [Time-Frequency Displays](https://ccrma.stanford.edu/~jos/sasp/Time_Frequency_Displays.html) | [[short-time-fourier-transform]] |
| OLA view | 8. [Overlap-Add STFT Processing](https://ccrma.stanford.edu/~jos/sasp/Overlap_Add_OLA_STFT_Processing.html) | [[overlap-add-stft]] |
| FBS view | 9. [Filter Bank View of the STFT](https://ccrma.stanford.edu/~jos/sasp/Filter_Bank_Summation_FBS.html) | [[filter-bank-summation-stft]], [[stft-modifications]] |
| Applications | 10. [Applications of the STFT](https://ccrma.stanford.edu/~jos/sasp/Applications_STFT.html) | [[sms-sines-plus-noise]], [[sinusoidal-parameter-interpolation]], [[phase-vocoder-and-tsm]], [[cross-synthesis-and-morphing]], [[f0-and-spectral-envelope]], [[spectral-audio-applications]] |
| Filter banks | 11. [Multirate Filter Banks](https://ccrma.stanford.edu/~jos/sasp/Multirate_Filter_Banks.html) | [[multirate-filter-banks]] |
| Appendices | D. [Gaussian Function Properties](https://ccrma.stanford.edu/~jos/sasp/Gaussian_Function_Properties.html), G. [Spectral Audio Modeling History](https://ccrma.stanford.edu/~jos/sasp/History_Spectral_Audio_Signal.html), H. [The PARSHL Program](https://ccrma.stanford.edu/~jos/sasp/PARSHL_Program.html) | [[gaussian-and-chirp-windows]], [[spectral-audio-applications]], [[sinusoidal-modeling]] |

## How the Views Connect

- OLA and FBS are **Fourier duals** — the same STFT, different
  scheduling of the sums. OLA groups by frame; FBS groups by bin.
- Sinusoidal modeling reads the STFT as a time-varying list of peaks.
- Phase vocoder is STFT modification that respects phase consistency
  across frames.
- Multirate filter banks generalize the uniform DFT filter bank to
  non-uniform (auditory, wavelet) partitions.

## Related Wikis
- [[waveguide_synthesis/index|waveguide_synthesis]] — physical modeling companion volume (PASP)
- [[modal_synthesis/index|modal_synthesis]] — modal / resonator view of the same signals
- [[jos_books/index|JOS online books]] — hub pages for all four books

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Introduction and Overview](https://ccrma.stanford.edu/~jos/sasp/Introduction_Overview.html), [Book Series Overview](https://ccrma.stanford.edu/~jos/sasp/Book_Series_Overview.html), [Summary and Conclusions](https://ccrma.stanford.edu/~jos/sasp/Summary_Conclusions.html)

## References
[^1]: Smith, J.O. III. *Spectral Audio Signal Processing*, W3K Publishing, 2011, ISBN 978-0-9745607-3-1. <https://ccrma.stanford.edu/~jos/sasp/>

---
title: Multirate Filter Banks
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [multirate, filter-banks, wavelets, perfect-reconstruction]
sources:
  - /w/sasp/mfb.tex
  - /w/sasp/wavelets.tex
  - /w/sasp/downsampling.tex
  - https://ccrma.stanford.edu/~jos/sasp/Multirate_Filter_Banks.html
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
---

# Multirate Filter Banks

Filter banks that decompose a signal into frequency bands **at
different sample rates** — the foundation of audio coding, wavelets,
and efficient subband processing.

## Basic Operators

- **Downsampling by $M$**: $y(n) = x(Mn)$. Frequency:
  $Y(\omega) = \tfrac{1}{M}\sum_{k=0}^{M-1}X\!\left(\tfrac{\omega - 2\pi k}{M}\right)$ — aliased sum.
- **Upsampling by $L$**: $y(n) = x(n/L)$ at multiples of $L$, else 0.
  Frequency: $Y(\omega) = X(L\omega)$ — spectral images.

A filter + decimation = **analysis**; expansion + filter = **synthesis**.

## Noble Identities

Reading each side left to right in signal-flow order:
$$\downarrow M \to H(z) \;\equiv\; H(z^M) \to \downarrow M \qquad\qquad
\uparrow L \to H(z^L) \;\equiv\; H(z) \to \uparrow L$$
They let filtering be moved to the low-rate side of a rate change,
which is where polyphase efficiency comes from.

## Polyphase Decomposition

$$H(z) \;=\; \sum_{k=0}^{M-1} z^{-k}\, E_k(z^M)$$
An $M$-channel filter splits into $M$ sub-filters running at $1/M$
rate. Combined with an $M$-point DFT gives the efficient
**polyphase DFT filter bank** underlying [[filter-bank-summation-stft]].

## Perfect Reconstruction (PR) Condition

For an $M$-channel analysis/synthesis bank with analysis filters
$H_k(z)$ and synthesis filters $F_k(z)$, PR requires:
$$\sum_{k=0}^{M-1} H_k(z)\, F_k(z) \;=\; c\, z^{-n_0}$$
$$\sum_{k=0}^{M-1} H_k(zW_M^l)\, F_k(z) \;=\; 0,\quad l=1,\dots,M-1$$
(no aliasing). The second condition is the **aliasing cancellation**
constraint.

## Two-Channel PR Filter Banks

### Quadrature Mirror Filters (QMF)
$H_1(z) = H_0(-z)$, $F_0(z) = H_0(z)$, $F_1(z) = -H_0(-z)$.
Aliasing cancels, and PR reduces to $H_0^2(z) - H_0^2(-z) = g\,z^{-d}$.
The only exact FIR solutions are two-tap (Haar-like) filters, so
practical QMF banks are approximate ("pseudo-QMF") or IIR. For
linear-phase $H_0$ the condition becomes power complementarity,
$|H_0(\omega)|^2 + |H_0(\pi - \omega)|^2 = \text{const}$.

### CQF and Biorthogonal Banks
- **Conjugate quadrature filters**: $h_1(n) = -(-1)^n h_0(L-1-n)$ with a
  power-symmetric $H_0$ - exact FIR PR (orthogonal), but not linear phase.
- **Biorthogonal**: let analysis and synthesis filters differ, which
  allows linear-phase FIR PR banks (JPEG 2000, many wavelet codecs).

## Cosine-Modulated Filter Banks

Whole bank derived from a single prototype $p(n)$ via cosine
modulation:
$$h_k(n) \;=\; p(n)\cos\!\left[\tfrac{(2k+1)\pi}{2M}(n - \tfrac{M-1}{2}) + \phi_k\right]$$
Very efficient: the 32-band pseudo-QMF bank of MPEG-1 Layers I-III and
the MDCT of Layer III and AAC are of this type. PR conditions reduce to
conditions on $p(n)$ alone.

## Wavelets as Dyadic Filter Banks

Iterate a two-channel PR filter bank on the **lowpass** output
$\Rightarrow$ octave-spaced frequency resolution, **constant-Q** in
the log sense:

```
x ─┬→ [H0,↓2] ─┬→ [H0,↓2] ─┬→ [H0,↓2] → ...
   └→ [H1,↓2]  └→ [H1,↓2]  └→ [H1,↓2]      (octave-band outputs)
```

This tree *is* the **discrete wavelet transform**. The continuous-time
wavelet and scaling function arise as the limit of the iterated
filters' impulse responses (Daubechies, biorthogonal spline, etc.).

## Non-Uniform / Auditory Banks

Goal: match critical bands (Bark, ERB, mel scales) — 24ish bands,
log-spaced above ~500 Hz. Built from tree-structured banks
(wavelet-style), summed FFT bins, bilinear frequency warping, or
gammatone (auditory-model) filters.

## Related Concepts
- [[filter-bank-summation-stft]] — uniform DFT bank is a special case
- [[spectral-audio-applications]] — audio coding uses these banks
- [[window-design-methods]] — prototype filter design
- [[linear-phase-octave-filter-bank-implementation]] - blocked/parallel edge-SoC realization of a multistage linear-phase octave bank (DAFx26; catalog entry [[entities/source-papers#paper-badia-octave-filter-bank-parallelism-2026|Badia et al. 2026]])

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Polyphase Decomposition](https://ccrma.stanford.edu/~jos/sasp/Polyphase_Decomposition.html), [Perfect Reconstruction Filter Banks](https://ccrma.stanford.edu/~jos/sasp/Perfect_Reconstruction_Filter_Banks.html), [Critically Sampled PR Filter Banks](https://ccrma.stanford.edu/~jos/sasp/Critically_Sampled_Perfect_Reconstruction.html), [MPEG Filter Banks](https://ccrma.stanford.edu/~jos/sasp/MPEG_Filter_Banks.html), [Wavelet Filter Banks](https://ccrma.stanford.edu/~jos/sasp/Wavelet_Filter_Banks.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Downsampling Theorem (Aliasing Theorem)](https://ccrma.stanford.edu/~jos/mdft/Downsampling_Theorem_Aliasing_Theorem.html)

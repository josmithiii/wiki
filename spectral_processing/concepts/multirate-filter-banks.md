---
title: Multirate Filter Banks
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [multirate, filter-banks, wavelets, perfect-reconstruction]
sources:
  - /w/sasp/mfb.tex
  - /w/sasp/wavelets.tex
  - /w/sasp/downsampling.tex
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

$$\downarrow M \cdot H(z) \;\equiv\; H(z^M) \cdot \downarrow M$$
$$\uparrow L \cdot H(z^L) \;\equiv\; H(z) \cdot \uparrow L$$
Let filtering be moved across rate changes to exploit polyphase
efficiency.

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
Eliminates aliasing but PR requires $|H_0(\omega)|^2 + |H_0(\omega - \pi)|^2 = 1$
which is hard to satisfy exactly with linear-phase FIRs.

### Conjugate Quadrature Filters (CQF)
Use the **power-complementary** property; FIR PR possible but not
linear phase.

### Biorthogonal / Linear-Phase PR
Relax orthogonality so analysis and synthesis filter differ. Allows
linear-phase FIR PR filter banks (used in JPEG and many wavelet
codecs).

## Cosine-Modulated Filter Banks

Whole bank derived from a single prototype $p(n)$ via cosine
modulation:
$$H_k(n) \;=\; p(n)\cos\!\left[\tfrac{(2k+1)\pi}{2M}(n - \tfrac{M-1}{2}) + \phi_k\right]$$
Very efficient, form the basis of MPEG-1 Layer 1/2/3 and AAC subband
filter banks. PR conditions reduce to conditions on $p(n)$ alone.

## Wavelets as Dyadic Filter Banks

Iterate a two-channel PR filter bank on the **lowpass** output
$\Rightarrow$ octave-spaced frequency resolution, **constant-Q** in
the log sense:

```
x → [H0,↓2] → [H0,↓2] → [H0,↓2] → ...
         ↓          ↓          ↓
        [H1,↓2]   [H1,↓2]   [H1,↓2]
```

Continuous-time limit = **discrete wavelet transform**. Wavelet
bases arise from the iterated filter's impulse response (Daubechies,
biorthogonal spline, etc.).

## Non-Uniform / Auditory Banks

Goal: match critical bands (Bark, ERB, mel scales) — 24ish bands,
log-spaced above ~500 Hz. Built by:
- Tree-structured uniform banks (wavelet-style)
- Warped-frequency filters (bilinear transform)
- Gammatone banks (auditory model)

## Related Concepts
- [[filter-bank-summation-stft]] — uniform DFT bank is a special case
- [[spectral-audio-applications]] — audio coding uses these banks
- [[window-design-methods]] — prototype filter design

---
title: Overlap-Add STFT (OLA)
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [stft, ola, cola, perfect-reconstruction]
sources:
  - /w/sasp/ola.tex
  - /w/sasp/cola.tex
  - /w/sasp/poisson.tex
  - /w/sasp/fftconv.tex
  - https://ccrma.stanford.edu/~jos/sasp/Overlap_Add_OLA_STFT_Processing.html
---

# Overlap-Add STFT (OLA)

The **transform view** of the STFT: decompose $x$ into windowed frames,
process each frame as a whole DFT, inverse-DFT, and add back with
overlap.

## Decomposition Identity

If the analysis window satisfies the **Constant Overlap-Add (COLA)**
condition at hop $R$,
$$\sum_{m=-\infty}^{\infty} w(n - mR) \;=\; c, \quad \forall n$$
then
$$\sum_{m} X_m(\omega) \;=\; c\, X(\omega)$$
and the signal reconstructs as
$$x(n) \;=\; \frac{1}{c}\sum_m \operatorname{IDTFT}\!\left\{X_m\right\}(n)$$

By the Poisson summation formula the constant is $c = W(0)/R$ (the
window's dc gain divided by the hop); scale $w$ so that $c=1$.

## COLA Examples

| Window | COLA at $R$ |
|--------|-------------|
| Rectangular | any $R$ dividing $M$ |
| Bartlett (triangular) | $R = M/2$ |
| Hann, Hamming (periodic), any generalized Hamming | $R = M/k$, integer $k\ge 2$ (e.g. $M/2$, $M/4$) |
| Blackman family (3-term) | $R = M/k$, integer $k\ge 3$ (e.g. $M/3$, $M/4$) |
| $L$-term Blackman-Harris | $R = M/k$, integer $k\ge L$ |
| any window | $R = 1$ (sliding FFT) |

**75% overlap** ($R = M/4$) is the ubiquitous default for
Hann/Hamming/Blackman-family windows when spectra are modified.

## Poisson Summation View

COLA in time $\Leftrightarrow$ spectral Nyquist condition:
$$W\!\left(\tfrac{2\pi k}{R}\right) = 0, \quad k = 1,2,\dots,R-1$$
The window transform $W$ must be zero at all nonzero harmonics of the
frame rate $2\pi/R$ ("weak COLA"; necessary and sufficient when the
spectrum is not modified). The periodic Hann transform is zero at every
multiple of $2\pi/M$ from $\pm 4\pi/M$ outward, which covers the
frame-rate harmonics for $R = M/2$ ($4\pi k/M$) and $R = M/4$
($8\pi k/M$). "Strong COLA" - $W(\omega)=0$ for $|\omega|\ge\pi/R$ - is
the safer target when frames are modified, and can only be approximated
by a finite window.

## FFT-Convolution via OLA

For frequency-domain filtering by $H(\omega)$:
$$y \;=\; \sum_m \operatorname{shift}_{mR}\!\left\{\operatorname{IFFT}\left[H_m \cdot \operatorname{FFT}(\operatorname{shift}_{-mR}(x)\cdot w_M)\right]\right\}$$

Practical rules:
- FFT length $N \ge M + L_h - 1$ to avoid time-aliasing from the filter.
- If $h$ has length $L_h$ and $w$ is rectangular of length $M$, pad to
  $N = M + L_h - 1$ — the classic overlap-add FFT convolution.
- For arbitrary analysis window $w$, increase oversampling so that
  time-varying $H_m$ doesn't alias across frames.

## Time-Varying Filtering (Safe Modifications)

OLA supports slowly varying $H_m(\omega)$ as long as:
1. $H_m$ changes slowly vs. the frame rate $f_s/R$.
2. The implied impulse response $h_m$ is shorter than the zero-padding
   headroom.

Fast modifications alias and produce artifacts. See [[stft-modifications]].

## OLA Block Algorithm

```
for each frame m:
    buf = x[mR - M/2 : mR + M/2] * w
    X   = FFT(zero-pad(buf, N))
    Y   = H_m * X
    y_m = IFFT(Y)
    output[mR - N/2 : mR + N/2] += y_m
```

## Related Concepts
- [[filter-bank-summation-stft]] — dual FBS view
- [[short-time-fourier-transform]] — the common STFT
- [[stft-modifications]] — what modifications preserve reconstruction
- [[phase-vocoder-and-tsm]] — OLA with phase management

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Overlap-Add Decomposition](https://ccrma.stanford.edu/~jos/sasp/Overlap_Add_Decomposition.html), [COLA Examples](https://ccrma.stanford.edu/~jos/sasp/COLA_Examples.html), [Frequency-Domain COLA Constraints](https://ccrma.stanford.edu/~jos/sasp/Frequency_Domain_COLA_Constraints.html), [Convolving with Long Signals](https://ccrma.stanford.edu/~jos/sasp/Convolving_Long_Signals.html), [Weighted Overlap Add](https://ccrma.stanford.edu/~jos/sasp/Weighted_Overlap_Add.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Convolution Theorem](https://ccrma.stanford.edu/~jos/mdft/Convolution_Theorem.html)

---
title: Overlap-Add STFT (OLA)
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [stft, ola, cola, perfect-reconstruction]
sources:
  - /w/sasp/ola.tex
  - /w/sasp/cola.tex
  - /w/sasp/poisson.tex
  - /w/sasp/fftconv.tex
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

$c=1$ with unity-gain COLA is the convention.

## COLA Examples

| Window | COLA at $R$ |
|--------|-------------|
| Rectangular | any $R$ dividing $M$ |
| Hann, Hamming (periodic) | $R = M/2,\, M/4,\, M/8,\dots$ |
| Blackman | $R = M/3,\, M/6,\dots$ (3-term) |
| Bartlett (triangular) | $R = M/2$ |

Hop size **75% overlap** ($R = M/4$) is the ubiquitous default for
Hann/Hamming/Blackman-family windows.

## Poisson Summation View

COLA in time $\Leftrightarrow$ spectral Nyquist condition:
$$W\!\left(\tfrac{2\pi k}{R}\right) = 0, \quad k = 1,2,\dots,R-1$$
The window transform $W$ must have zeros at all non-zero harmonics of
$2\pi/R$. This is why Hann (zeros at $\pm 2\pi/M$) and $R = M/4$ work.

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

---
title: Zero Padding and Spectral Interpolation
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [dft, fft, ft-theorems]
sources:
  - /w/sasp/specinterp.tex
  - /w/sasp/zpblackman.tex
  - /w/sasp/zpfmin.tex
---

# Zero Padding and Spectral Interpolation

## Fundamental Theorem

> **Zero-padding in the time domain = ideal bandlimited interpolation
> of the spectrum in the frequency domain.**

Let $x$ be length $M$ and let $x_{\text{zp}}$ be $x$ followed by $N-M$
zeros. Then the length-$N$ DFT of $x_{\text{zp}}$ samples the DTFT of
$x$ on a finer grid:
$$X_{\text{zp}}(k) \;=\; X\!\left(\tfrac{2\pi k}{N}\right),\quad k=0,\dots,N-1$$
where $X(\omega)$ is the DTFT of the original $M$ samples.

No information is added — the DFT is merely **interpolated**.

## Why Zero-Pad

1. **Visualize the true DTFT** — avoid the "picket fence" of coarse
   DFT bins. Peaks and side lobes appear where they actually are.
2. **Peak localization** — makes [[qifft-peak-estimation]] accurate by
   densely sampling the main lobe.
3. **Next power of two** — let an FFT implementation handle arbitrary
   $M$.
4. **Acyclic (linear) convolution** — pad two length-$M$ sequences to
   length $\ge 2M-1$ before FFT-multiplying to avoid time-aliasing.
5. **Frame "ringing" headroom** in overlap-add FFT filtering.

## Zero-Phase Zero Padding

To preserve phase symmetry, zero-pad by splitting the window about
$n=0$ (negative-time half at the end of the buffer):
$$x_{\text{zp}} \;=\; [\,x(0), x(1),\dots,x(M/2{-}1),\;0,\dots,0,\;x(-M/2),\dots,x(-1)\,]$$
A real even window then produces a real even DFT — no linear-phase
slope from buffer offset. Essential for clean peak finding and
additive resynthesis.

## Spectral Interpolation as Sinc Sum

The interpolated spectrum between DFT bins is an exact **aliased-sinc**
sum (periodic sinc or Dirichlet kernel):
$$X(\omega) \;=\; \sum_{k=0}^{N-1} X(k)\, \operatorname{asinc}_N\!\!\left(\omega - \tfrac{2\pi k}{N}\right)$$

## Minimum Zero-Padding for Peak-Finding

For QIFFT bias below a spec $\Delta$ (% of $f_s/M$):

| Window | $\Delta=1\%$ | $\Delta=0.1\%$ |
|--------|-------------:|---------------:|
| Rectangular | 2.1 | 4.1 |
| Hamming/Hann | 1.2 | 2.4 |
| Blackman | 1.0 | 1.8 |

Flatter-topped main lobes need less padding because parabolic
interpolation fits better (see [[qifft-peak-estimation]]).

## Caveats

- Zero padding does **not** improve **resolution** — that is set by
  the window length $M$ (main-lobe width). See [[spectrum-analysis-windows]].
- Padding after windowing is the usual order; padding before
  windowing is almost never wanted.

## Related Concepts
- [[dtft-and-fourier-theorems]] — DFT samples the DTFT
- [[qifft-peak-estimation]] — primary beneficiary
- [[spectrum-analysis-windows]] — resolution vs interpolation distinction

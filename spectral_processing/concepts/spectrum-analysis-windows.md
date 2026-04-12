---
title: Spectrum Analysis Windows
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [windows, main-lobe, dtft]
sources:
  - /w/sasp/windows.tex
  - /w/sasp/dpssw.tex
  - /w/sasp/zpblackman.tex
---

# Spectrum Analysis Windows

A window $w(n)$, $n=0,\dots,M-1$, tapers a signal block before DFT
analysis. Windowing = multiplication in time = convolution by the
**window transform** $W(\omega)$ in frequency. Every spectrum seen
through a window is the true spectrum convolved with $W(\omega)$.

## Core Trade-off

All windows trade **main-lobe width** (resolution) against **side-lobe
level** (dynamic range / leakage):

| Window | Main lobe width (bins) | Peak side lobe (dB) | Roll-off (dB/oct) |
|--------|------------------------:|--------------------:|------------------:|
| Rectangular | 2 | $-13$ | $-6$ |
| Hann (raised cosine) | 4 | $-32$ | $-18$ |
| Hamming | 4 | $-43$ | $-6$ |
| Blackman (classic) | 6 | $-58$ | $-18$ |
| Blackman-Harris 4-term | 8 | $-92$ | $-6$ |
| Kaiser ($\beta=10$) | $\approx 6$ | $\approx -74$ | $-6$ |
| Dolph-Chebyshev | parametric | **equi-ripple** | $0$ |
| DPSS (Slepian) | parametric | minimum leakage | varies |

Main-lobe width is measured in frequency bins of width $2\pi/M$.

## Generalized Hamming Family

$$w(n) \;=\; \alpha - (1-\alpha)\cos\!\left(\tfrac{2\pi n}{M-1}\right)$$

- $\alpha=1$: rectangular
- $\alpha=0.5$: Hann (nulls at $\pm 2\pi/M$ cancel first side lobe)
- $\alpha=0.54$: Hamming (cancels peak of first side lobe)

## Blackman-Harris Family

$$w(n) \;=\; \sum_{k=0}^{K-1} a_k \cos\!\left(\tfrac{2\pi k n}{M-1}\right)$$

Add more cosine terms $\Rightarrow$ more adjustable side lobes
$\Rightarrow$ wider main lobe. Minimum side-lobe variants:
3-term ($-71$ dB), 4-term ($-92$ dB).

## Kaiser Window

$$w(n) \;=\; \frac{I_0\!\left(\beta\sqrt{1-(2n/(M-1)-1)^2}\right)}{I_0(\beta)}$$

Near-optimal time-frequency concentration via modified Bessel $I_0$.
Parameter $\beta$ continuously trades resolution for side-lobe
suppression. Defining feature: user picks $(\beta, M)$ from a spec.

## Dolph-Chebyshev

Equi-ripple side lobes; main lobe is **narrowest** possible for a
given side-lobe level $\alpha$ (in dB). Defined via Chebyshev
polynomials:
$$W(\omega) \;=\; \frac{\cos\!\left[M\cos^{-1}(\beta\cos(\omega/2))\right]}{\cosh[M\cosh^{-1}\beta]}$$
Drawback: tiny impulses at window endpoints.

## DPSS (Slepian, Prolate)

Eigenvectors of the sinc kernel — concentrate maximum energy in a
main lobe of specified width. Asymptotically optimal; Kaiser is a
close, closed-form approximation.

## Practical Choice

- **General-purpose display**: Hann or Blackman.
- **Sinusoidal peak estimation**: Blackman-Harris family or Kaiser
  ($\beta\approx 9$) — flat tops, low leakage.
- **Audio coding / low-leakage**: Kaiser ($\beta\approx 12$), DPSS.
- **Max resolution at fixed side-lobe spec**: Dolph-Chebyshev.

## Related Concepts
- [[zero-padding-and-interpolation]] — resolution vs interpolation
- [[qifft-peak-estimation]] — window choice affects peak bias
- [[window-design-methods]] — designing custom windows
- [[gaussian-and-chirp-windows]] — theoretically optimal (Gaussian)

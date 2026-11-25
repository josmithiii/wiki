---
title: Spectrum Analysis Windows
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [windows, main-lobe, dtft]
sources:
  - /w/sasp/windows.tex
  - /w/sasp/dpssw.tex
  - /w/sasp/zpblackman.tex
  - https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Windows.html
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
| Hann (raised cosine) | 4 | $-31.5$ | $-18$ |
| Hamming | 4 | $-43$ | $-6$ |
| Blackman (classic) | 6 | $-58$ | $-18$ |
| Blackman-Harris 4-term | 8 | $-92$ | $-6$ |
| Kaiser ($\beta=10$) | $\approx 6.7$ | $\approx -74$ | $-6$ |
| Dolph-Chebyshev | parametric | **equi-ripple** | $0$ |
| DPSS (Slepian) | parametric | minimum leakage | varies |

Main-lobe width is measured zero-to-zero in bins of width $\Omega_M = 2\pi/M$
(so the rectangular main lobe is $4\pi/M$ rad/sample). The Hamming figure is the
large-$M$ limit ($-42.76$ dB); short windows give about $-41$ dB. The Kaiser
main lobe is $2\sqrt{1+(\beta/\pi)^2}$ bins wide.

## Generalized Hamming Family

$$w(n) \;=\; \alpha - (1-\alpha)\cos\!\left(\tfrac{2\pi n}{M-1}\right)$$

- $\alpha=1$: rectangular
- $\alpha=0.5$: Hann - value and slope go to zero at the endpoints, which
  maximizes the roll-off rate (18 dB/octave)
- $\alpha=25/46\approx 0.54$: Hamming - cancels the largest side lobe, at the
  price of an endpoint discontinuity (6 dB/octave roll-off)

## Blackman-Harris Family

$$w(n) \;=\; \sum_{k=0}^{K-1} (-1)^k a_k \cos\!\left(\tfrac{2\pi k n}{M-1}\right),\qquad a_k>0$$
(causal form; the $(-1)^k$ disappears in SASP's zero-phase form, $n$ centered on 0).

Each added cosine term buys one more degree of freedom (lower side
lobes or faster roll-off) and widens the main lobe by 2 bins ($K$ terms
$\Rightarrow$ $2K$ bins). $K=2$ is the generalized Hamming family; the
classic Blackman ($a = 0.42, 0.5, 0.08$) spends one degree of freedom on
roll-off and one on side lobes. Minimum side-lobe variants: 3-term
($-71$ dB), 4-term ($-92$ dB).

## Kaiser Window

$$w(n) \;=\; \frac{I_0\!\left(\beta\sqrt{1-(2n/(M-1)-1)^2}\right)}{I_0(\beta)}$$

Near-optimal time-frequency concentration via modified Bessel $I_0$.
Parameter $\beta$ continuously trades resolution for side-lobe
suppression. Defining feature: user picks $(\beta, M)$ from a spec.

## Dolph-Chebyshev

Equi-ripple side lobes; main lobe is **narrowest** possible for a
given side-lobe level of $-20\alpha$ dB. Defined via Chebyshev
polynomials, sampled at $\omega_k = 2\pi k/M$:
$$W(\omega_k) \;=\; \frac{\cos\!\left[M\cos^{-1}(\beta\cos(\omega_k/2))\right]}{\cosh[M\cosh^{-1}\beta]},
\qquad \beta = \cosh\!\left[\tfrac{1}{M}\cosh^{-1}(10^{\alpha})\right]$$
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

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Generalized Hamming Window Family](https://ccrma.stanford.edu/~jos/sasp/Generalized_Hamming_Window_Family.html), [Blackman-Harris Window Family](https://ccrma.stanford.edu/~jos/sasp/Blackman_Harris_Window_Family.html), [Kaiser Window](https://ccrma.stanford.edu/~jos/sasp/Kaiser_Window.html), [Dolph-Chebyshev Window](https://ccrma.stanford.edu/~jos/sasp/Dolph_Chebyshev_Window.html), [Slepian or DPSS Window](https://ccrma.stanford.edu/~jos/sasp/Slepian_DPSS_Window.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Spectrum Analysis of a Sinusoid](https://ccrma.stanford.edu/~jos/mdft/Spectrum_Analysis_Sinusoid_Windowing.html)

---
title: DTFT and Fourier Theorems
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [dft, dtft, ft-theorems]
sources:
  - /w/sasp/fourcases.tex
  - /w/sasp/case-dtft.tex
  - /w/sasp/case-ft.tex
  - /w/sasp/dtft-thms.tex
  - /w/sasp/thms-ct.tex
  - https://ccrma.stanford.edu/~jos/sasp/Selected_Continuous_Fourier_Theorems.html
  - https://ccrma.stanford.edu/~jos/sasp/Fourier_Transforms_Continuous_Discrete_Time_Frequency.html
---

# DTFT and Fourier Theorems

## Four Fourier Cases

Time/frequency can independently be continuous or discrete, giving four
transforms. When time is discrete, frequency is periodic (finite);
when time is finite, frequency is discrete.

| Time | Frequency | Transform |
|------|-----------|-----------|
| continuous, infinite | continuous, infinite | FT |
| continuous, periodic | discrete, infinite | FS |
| discrete, infinite | continuous, periodic | DTFT |
| discrete, finite | discrete, finite | DFT |

SASP uses the **DTFT** for theory and the **DFT** (via FFT) in practice.

## Definitions

**DTFT:**
$$X(\omega) \;=\; \sum_{n=-\infty}^{\infty} x(n)\, e^{-j\omega n}, \qquad \omega \in (-\pi,\pi]$$

**Inverse DTFT:**
$$x(n) \;=\; \frac{1}{2\pi}\int_{-\pi}^{\pi} X(\omega)\, e^{j\omega n}\, d\omega$$

**DFT** (length $N$, $\omega_k = 2\pi k/N$):
$$X(k) \;=\; \sum_{n=0}^{N-1} x(n)\, e^{-j 2\pi n k/N}$$

All transforms are inner products $X(\omega) = \langle x, s_\omega\rangle$
with a complex sinusoid basis $s_\omega(n) = e^{j\omega n}$.

## Key Theorems (DTFT)

| Theorem | Identity |
|---------|----------|
| Linearity | $\alpha x + \beta y \;\leftrightarrow\; \alpha X + \beta Y$ |
| Shift | $x(n-n_0) \;\leftrightarrow\; e^{-j\omega n_0}\, X(\omega)$ |
| Modulation | $e^{j\omega_0 n}\, x(n) \;\leftrightarrow\; X(\omega-\omega_0)$ |
| Convolution | $x\ast y \;\leftrightarrow\; X\cdot Y$ |
| Multiplication | $x\cdot y \;\leftrightarrow\; \tfrac{1}{2\pi} X \circledast Y$ |
| Parseval | $\sum_n \lvert x(n)\rvert^2 \;=\; \tfrac{1}{2\pi}\int_{-\pi}^{\pi} \lvert X(\omega)\rvert^2 d\omega$ |
| Correlation | $(x\star y)(l) \triangleq \sum_m \overline{x(m)}\,y(m+l) \;\leftrightarrow\; \overline{X(\omega)}\,Y(\omega)$ |
| Flip/conj | $\overline{x(-n)} \;\leftrightarrow\; \overline{X(\omega)}$ |

## Poisson Summation (the bridge)

Sampling in one domain $\Leftrightarrow$ periodization (aliasing) in
the other. In the form SASP uses for windows (hop $R$, $\omega_k = 2\pi k/R$):
$$\sum_{m} w(n-mR) \;=\; \frac{1}{R}\sum_{k=0}^{R-1} W(\omega_k)\, e^{j\omega_k n}$$
Its Fourier dual is the sampling (aliasing) theorem,
$\sum_n x(nT)e^{-j\omega nT} = \tfrac{1}{T}\sum_k X(\omega - 2\pi k/T)$.

This is the foundation of the COLA window condition in
[[overlap-add-stft]], of the Nyquist($N$) window condition in
[[filter-bank-summation-stft]], and of aliasing under downsampling
([[multirate-filter-banks]]).

## Why These Matter

- **Shift/modulation** duality is why the STFT is both a hopping
  transform and a modulated filter bank.
- **Convolution theorem** justifies FFT-based filtering (OLA).
- **Parseval** connects time-domain and spectral energies — used in
  window design and in [[noise-spectrum-analysis]].

## Related Concepts
- [[zero-padding-and-interpolation]] — sampling the DTFT via DFT
- [[short-time-fourier-transform]] — DTFT + windowing
- [[spectrum-analysis-windows]] — windowing = multiplication = convolution in $\omega$

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Fourier Theorems for the DTFT](https://ccrma.stanford.edu/~jos/sasp/Fourier_Theorems_DTFT.html), [Discrete Time Fourier Transform](https://ccrma.stanford.edu/~jos/sasp/Discrete_Time_Fourier_Transform.html), [Continuous Fourier Theorems](https://ccrma.stanford.edu/~jos/sasp/Selected_Continuous_Fourier_Theorems.html), [Poisson Summation Formula](https://ccrma.stanford.edu/~jos/sasp/Poisson_Summation_Formula.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Fourier Theorems for the DFT](https://ccrma.stanford.edu/~jos/mdft/Fourier_Theorems_DFT.html), [Discrete Time Fourier Transform (DTFT)](https://ccrma.stanford.edu/~jos/mdft/Discrete_Time_Fourier_Transform.html)

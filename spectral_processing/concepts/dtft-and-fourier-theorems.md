---
title: DTFT and Fourier Theorems
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [dft, dtft, ft-theorems]
sources:
  - /w/sasp/fourcases.tex
  - /w/sasp/case-dtft.tex
  - /w/sasp/case-ft.tex
  - /w/sasp/dtft-thms.tex
  - /w/sasp/thms-ct.tex
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
| Parseval | $\sum |x(n)|^2 \;=\; \tfrac{1}{2\pi}\int |X(\omega)|^2 d\omega$ |
| Correlation | $r_{xy}(l) \;\leftrightarrow\; X(\omega)\overline{Y(\omega)}$ |
| Flip/conj | $\overline{x(-n)} \;\leftrightarrow\; \overline{X(\omega)}$ |

## Poisson Summation (the bridge)

Sampling in one domain $\Leftrightarrow$ periodization in the other:
$$\sum_{n} x(nT)\, e^{-j\omega nT} \;=\; \frac{1}{T}\sum_{k} X\!\left(\omega - \tfrac{2\pi k}{T}\right)$$

This is the foundation of the **aliasing theorem**, the COLA window
condition in [[overlap-add-stft]], and the Nyquist view of bin decimation
in [[filter-bank-summation-stft]].

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

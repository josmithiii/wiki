---
title: PolyADAA
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [adaa, antialiasing, nonlinear, oversampling, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_47.pdf
  - raw/DAFx26_paper_47.txt
---

# PolyADAA

ADAA with **higher-order Lagrange reconstruction** in place of the usual linear one,
made tractable by approximating the nonlinearity with Chebyshev polynomials. Read
[[antiderivative-antialiasing]] first for the ADAA formulation and notation.[^1]

## Higher-order reconstruction

Linear interpolation is Lagrange interpolation of order $N = 1$. Raising $N$ gives
$\tilde{x}(\tau) = \sum_{k=0}^{N} x[n{+}k{-}1] L_k(\tau)$ with
$L_k(\tau) = \prod_{j \ne k} \frac{\tau - \tau_j}{\tau_k - \tau_j}$, expanded into
monomial (Horner) form $\tilde{x}(\tau) = b_0 + b_1\tau + \dots + b_N\tau^N$,
$b_i = \sum_k \alpha_{k,i}\,x[n{+}k{-}1]$ - $N$ multiplies and $N$ adds, division-free
and branch-free (SIMD-friendly).

**Why no closed form.** For $N > 1$ the derivative $d\tilde{x}/d\tau$ is no longer
constant, so $u = \tilde{x}(\tau)$ requires inverting a polynomial (multiple roots),
and the integrand has no closed form for generic $f$.

**Chebyshev fix.** Approximate $g(\tau) = f(\tilde{x}(\tau))$ on $\tau \in [0,1]$ by
Chebyshev polynomials of the first kind, $t = 2\tau - 1$:

$$g(\tau) \approx \sum_{k=0}^{K} c_k\,T_k(2\tau-1), \quad
y[n] \approx \sum_{k=0}^{K} c_k M_k, \quad
M_k = \int_{-1}^{1} T_k(t)\,W(t)\,dt$$

- $g$ is evaluated at the $K{+}1$ Chebyshev nodes; the $c_k$ are **DCT-I**
  coefficients, from a length-$2K$ real FFT of the symmetric vector
  $[g(\tau_0),\dots,g(\tau_K),g(\tau_{K-1}),\dots,g(\tau_1)]$.
- The **moments** $M_k$ depend only on the kernel and are precomputed offline.
  Rectangular: $M_0 = 1$; $M_k = 0$ for odd $k$; $M_k = (-1)^{k/2}/(1-k^2)$ for even
  $k \ge 2$. Triangular ($W(t) = 2(1-|t|)$): evaluated numerically once.
- Consequences: switching kernel changes a table, not the code; **no antiderivatives
  of $f$ are needed**, so a new nonlinearity costs no analysis; and the $0/0$
  ill-conditioning is gone.

**Runtime:** gather $N{+}1$ samples, build $L_k(\tau)$, evaluate $\tilde{x}(\tau_m)$ at
the Chebyshev nodes by Horner, apply $f$, form the symmetric vector, take a
length-$2K$ FFT, sum $c_k M_k$. Cost is dominated by the $K$ transcendental calls;
Lagrange work is about $(K{+}1)(2N{+}1)$ flops, DCT about $K\log_2 K$. For $N=3$,
$K=16$: 17 $\tanh$ calls, 119 flops, one length-32 FFT.

## Reported results

$\Delta\mathrm{SNR}$ over the trivial (no antialiasing) method, averaged over MIDI
notes 69-108, $f(x) = \tanh(x)$ driven hard at $A = 9$. Baselines: ADAA-R 5.7 dB,
ADAA-T 10.6 dB.[^1]

| PolyADAA variant | $N = 2$ | $N = 3$ |
|---|---|---|
| rect. kernel, $K = 8$ | 19.33 dB | 15.99 dB |
| rect. kernel, $K = 16$ / 32 | 19.34 dB | 16.16 dB |
| tri. kernel, $K = 8$ | 10.39 dB | 24.54 dB |
| tri. kernel, $K = 32$ | 10.40 dB | **27.09 dB** |
| tri. kernel, $K = 32$ + LUT | 10.38 dB | 27.08 dB |

- Even the *worst* PolyADAA variant roughly ties ADAA-T, so the method dominates
  ADAA-R outright. $K$ saturates early: $K = 8$ or 16 already reaches the ceiling for
  $\tanh$. PolyADAA-R $N=2$, $K=8$ wins below MIDI note 70, PolyADAA-T $N=3$, $K=8$
  above it.
- Cost for 48k samples in blocks of 64 (C++, i7-1360P): ADAA-R 0.9 ms, ADAA-T 6.9 ms;
  PolyADAA $K=8$ 11.7 ms ($N{=}2$) / 14.1 ms ($N{=}3$); $K=32$ 65.2 / 71.1 ms; $K=32$
  with an 8192-point interpolated **LUT** for $f$, 5.5 / 13.4 ms - an 81-91 % saving
  with no SNR loss above A4. Kernel type does not affect runtime (only the moments).
- Hard clip $f(x) = \tfrac12(|x{+}1| - |x{-}1|)$: PolyADAA-R ($N{=}2, K{=}8$) slightly
  beats ADAA-T; PolyADAA-T ($N{=}3, K{=}32$) beats ADAA-T by nearly 20 dB.

**Limitations:** memoryless nonlinearities only; finite-support (rectangular,
triangular) kernels only - combining PolyADAA with IIR kernels is open; a Chebyshev
fit is needed per nonlinearity and amplitude range; cost exceeds plain ADAA unless a
LUT or fast approximation replaces $f$.

## See also

[[antiderivative-antialiasing]] - [[alias-free-oscillator-sync]] -
[[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-gabrielli-polyadaa-2026]] - Gabrielli & Squartini, "PolyADAA: Improving Aliasing Reduction in Memoryless Nonlinearities Using Lagrange Interpolation and Polynomial Approximation", DAFx26.

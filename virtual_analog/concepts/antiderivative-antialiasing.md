---
title: Antiderivative Antialiasing (ADAA)
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [adaa, antialiasing, nonlinear, oversampling, va-filters, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_47.pdf
  - raw/DAFx26_paper_47.txt
---

# Antiderivative Antialiasing (ADAA)

Applying a memoryless nonlinearity $f(\cdot)$ at the audio rate broadens the bandwidth
and everything above Nyquist folds back. ADAA (Parker, Zavalishin and Le Bivic, 2016)
suppresses that fold-back analytically instead of by raising the sample rate.[^1]

## ADAA fundamentals

Four conceptual steps: (a) reconstruct a continuous-time $\tilde{x}(t)$ from the
samples, (b) apply $f$ in continuous time, (c) convolve with an antialiasing kernel
$h$, (d) resample. Only (c) needs a closed form,
$y[n] = \int h(u)\, f(\tilde{x}(n-u))\, du$. With **linear** reconstruction and a
rectangular kernel on $[0,1]$, the substitution $u = \tilde{x}(\tau)$ works because
$d\tilde{x}/d\tau = x_n - x_{n-1}$ is constant, giving first-order ADAA:

$$y[n] = \frac{F_1(x_n) - F_1(x_{n-1})}{x_n - x_{n-1}},
\qquad F_1(x) = \int f(x)\,dx$$

- **Ill-conditioning branch.** As $x_n \to x_{n-1}$ the quotient becomes $0/0$, so
  implementations must branch below a threshold (e.g. to $f((x_n+x_{n-1})/2)$). This
  is why ADAA loses SNR at low frequencies and low input levels: with the triangular
  kernel it is *worse than no antialiasing* below MIDI note 60 (see [[polyadaa]]).
- **Second order** convolves two rectangles into a triangular kernel on $[0,2]$ and
  needs the second antiderivative $F_2 = \int F_1$, giving a two-term difference
  quotient in $(x_n - x_{n-1})^2$ and $(x_{n-2}-x_{n-1})^2$: one more sample of delay
  and worse low-frequency conditioning.
- **Higher orders and IIR-ADAA.** Subsequent work improved the *kernel* - higher-order
  FIR kernels (FIR-ADAA) and kernels designed in the Laplace domain (IIR-ADAA) - with
  extensions to stateful systems and to WDF circuit simulation
  ([[wave-digital-filters]]). But carrying IIR-ADAA over to wavetable synthesis, whose
  input *is* a linear ramp, gave a much larger SNR gain per kernel order, identifying
  the **linear reconstruction**, not the kernel, as the remaining bottleneck.

## Beyond linear reconstruction

Raising the *reconstruction* order rather than the kernel order is the PolyADAA
method, which uses Lagrange interpolation plus a Chebyshev approximation of $f$ to
keep the integral tractable: [[polyadaa]].

## See also

[[virtual-analog-overview]] - [[alias-free-oscillator-sync]] (alias-free by
construction rather than by correction) - [[moog-ladder-filter-models]]

## References

[^1]: [[entities/source-papers#paper-gabrielli-polyadaa-2026]] - Gabrielli & Squartini, "PolyADAA: Improving Aliasing Reduction in Memoryless Nonlinearities Using Lagrange Interpolation and Polynomial Approximation", DAFx26.

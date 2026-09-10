---
title: Loopback FM via a Time-Varying Delay Line
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [delay-line, waveguide, dsp, nonlinear, tutorial]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_36.pdf
  - raw/DAFx26_paper_36.txt
---

# Loopback FM via a Time-Varying Delay Line

How to implement loopback FM - an oscillator that modulates its own frequency -
with a time-varying delay line, so that arbitrary audio can be fed through it.[^smyth]

## Time-varying delay lines warp time

A TVDL output is $y(n) = x(n - D(n))$, so for input $e^{j\omega_c nT}$ the phase is
$\theta_c(n) = \omega_c(n - D(n))T$ and the instantaneous frequency is
$$\omega_i(n) = \omega_c\left(1 - \frac{d}{dn}D(n)\right)
\;\;\Longrightarrow\;\;
\frac{d}{dn}D(n) = 1 - m_t(n), \quad m_t(n) = \frac{\omega_i(n)}{\omega_c},$$
with $m_t$ the momentary transposition. Integrating,
$D(n) = n - (\theta_c/\omega_c) f_s$. A circular buffer requires
$d_0 \le D(n) \le D_M$.

- **Oscillatory modulation is easy.** For $\omega_i(n) = \omega_c - d\cos(\omega_m nT)$,
  $D_m(n) = \frac{I}{\omega_c}\sin(\omega_m nT) f_s + \frac{I}{\omega_c}f_s$, where the DC term (a constant
  of integration equal to the sinusoid's amplitude) is exactly what keeps $D$
  positive. This is vibrato and flanging.
- **A sustained pitch shift is not.** A constant target $\omega_i$ gives
  $D_l(n) = n\left(1 - \omega_i/\omega_c\right)$, growing linearly and bounded only by the
  input length. Crossfading between two arbitrarily wrapped TVDLs is the usual
  workaround; the paper reports limited success with coherent signals.

## The loopback FM oscillator

LBFM has $\omega_b(t) = \omega_c + B\omega_c\,\Re\{z_b(t)\}$, $-1 < B < 1$, implemented sample by
sample as a rotation $z_b(n) = e^{j(\omega_c + B\omega_c\Re\{z_b(n-1)\})T}z_b(n-1)$. A PM
implementation by cumulative summation is shown to be *algebraically identical*,
so it buys no accuracy. The closed form does:
$$z_0(t) = \frac{b_0 + e^{j\omega_0 t}}{1 + b_0 e^{j\omega_0 t}},\qquad
\angle z_0(t) = \omega_0 t - 2\phi(t),\qquad
\phi(t) = \tan^{-1}\!\frac{b_0\sin(\omega_0 t)}{1 + b_0\cos(\omega_0 t)} .$$
This is an allpass-shaped expression. Matching linear and oscillating terms of the
analytically integrated phase gives the parameter map
$$b_0 = \frac{\pm\sqrt{1-B^2}-1}{B}\ (B \ne 0), \qquad
\omega_0 = \pm\,\omega_c\sqrt{1-B^2},$$
so the **sounding** frequency $\omega_0$ - not the carrier - is a directly available
parameter, and the phase is analytic rather than numerically integrated.

## Wrapping the delay function

The LBFM phase has both a linear and an oscillating part, so the delay function is
unbounded. Substituting $\angle z_0$ into the TVDL relation and wrapping only the
linear term, $\hat{n} = n \bmod \tilde{N}$:
$$\hat{D}_b(n) = \hat{n}\left(1 - \frac{\omega_0}{\omega_c}\right) + \frac{f_s}{\omega_c}\,2\phi(n).$$
The $\phi$ term is itself oscillatory and needs no wrapping. The wrap period is
chosen so input and output coincide *and* have the same slope,
$$\omega_c \tilde{N}T \bmod 2\pi = \omega_i \tilde{N}T \bmod 2\pi
\;\;\Longrightarrow\;\;
\tilde{N} = \frac{f_s}{f_c - f_i},$$
rounded to $N = \lfloor \tilde{N}\rfloor$ or $\lceil \tilde{N}\rceil$. Intersections that satisfy the phase
condition but not the slope condition are disqualified; that is why naive
wrapping produces artefacts.

Finally $\hat{D}_b$ can still go negative. Adding an offset $d_0$ multiplies the output
by $e^{-jd_0\omega_c T}$, so unless $d_0\omega_c T$ is a multiple of $2\pi$ the waveform *shape*
changes. Choosing
$$d_0 = k\,\frac{2\pi}{\omega_c T} = k\,\frac{f_s}{f_c},\qquad k = 1 \text{ usually suffices}$$
makes the delay positive with no phase distortion; the minimum offset that merely
makes $D$ positive visibly distorts the waveform.

## Reading

Three incremental cases: (i) FM via TVDL is ideal, the delay function is naturally
bounded; (ii) LBFM sustains a pitch shift, so the delay grows linearly; (iii) the
closed form supplies the sounding frequency and analytic phase needed to wrap and
offset it correctly. Limitations: a single-oscillator treatment, with no cost
comparison against direct closed-form synthesis of the same signal.

## See also
- [[delay-line-techniques]] - variable delay lines, interpolation, pitch shifting
- [[nonlinear-and-time-varying-fdn-effects]] - other nonlinear operations inside delay loops
- [[entities/source-papers#paper-smyth-loopback-fm-tvdl-2026]] - catalog entry

[^smyth]: T. Smyth, "Loopback Frequency Modulation Using a Time-Varying Delay Line," DAFx26. See [[entities/source-papers#paper-smyth-loopback-fm-tvdl-2026]].

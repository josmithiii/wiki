---
title: TPT / ZDF Filters (Trapezoidal Integration)
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [tpt-zdf, va-filters, state-space, time-varying, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_28.pdf
  - raw/DAFx26_paper_28.txt
---

# TPT / ZDF Filters (Trapezoidal Integration)

The dominant discretization route for virtual analog filters: take a
continuous-time state-space prototype of the analog circuit and integrate it
with the trapezoidal rule. Also called the (state-space) bilinear or Tustin
transform; "topology-preserving transform" (TPT) and "zero-delay feedback"
(ZDF) are the audio-DSP names for the same construction, because the analog
block diagram survives intact and the delay-free loops it creates are resolved
algebraically rather than broken with a unit delay.[^1]

## Continuous-time prototype

$$\dot{x}(t) = A_C x(t) + B_C u(t), \qquad y(t) = C_C x(t) + D_C u(t)$$

with transfer function $H(s) = C_C (sI - A_C)^{-1} B_C + D_C$.

## Trapezoidal (bilinear) discretization

Applying $x[n+1] - x[n] = g\big( (A_C x[n{+}1] + B_C u[n{+}1]) + (A_C x[n] + B_C u[n]) \big)$
and the state change of variable $\tilde{x}[n] = (I - gA_C)x[n] - gB_C u[n]$
that absorbs the implicit $u[n{+}1]$ term gives[^1]

$$\begin{aligned}
A &= (I - gA_C)^{-1}(I + gA_C), &\quad B &= 2g\,(I - gA_C)^{-1} B_C,\\
C &= C_C (I - gA_C)^{-1}, &\quad D &= D_C + g\,C_C (I - gA_C)^{-1} B_C .
\end{aligned}$$

- $g > 0$ is the discretization parameter. Without pre-warping $g = T/2$ with
  $T$ the sampling period.
- With the prototype normalized to $\omega_C = 1$ rad/s, pre-warping a target
  discrete cutoff $\omega_D$ uses $g = \tan(\omega_D T / 2)$.
- The matrix inverse $(I - gA_C)^{-1}$ *is* the zero-delay-feedback solve: in
  block-diagram form it is the closed-form solution of the instantaneous
  feedback loop around each integrator.

## Worked example: one-pole lowpass

Normalized RC section $\dot{x} = -x + u$, $y = x$ (so $A_C = -1$, $B_C = 1$,
$C_C = 1$, $D_C = 0$) discretizes to[^1]

$$x[n{+}1] = \frac{1-g}{1+g}x[n] + \frac{2g}{1+g}u[n], \qquad
y[n] = \frac{1}{1+g}x[n] + \frac{g}{1+g}u[n].$$

This one-pole section is the building block of the cascade-plus-feedback
ladder structures in [[moog-ladder-filter-models]].

## Time variation

Modulating cutoff or resonance means a *sequence of frozen LTI prototypes*
$A_C[n], B_C[n], C_C[n], D_C[n]$ each discretized with a possibly varying
$g[n]$. The result is treated as a switched discrete-time system, not as the
discretization of one time-varying continuous system.[^1] Frozen-coefficient
pole analysis then proves nothing - see
[[time-varying-filter-stability]].

## Where it is used

- State-variable and Sallen-Key filters, Moog and diode ladders.
- Zavalishin's *The Art of VA Filter Design* is the standard practitioner
  reference; the nonlinear TPT/ZDF ladder core used as the ablation platform in
  [[moog-ladder-filter-models]] solves its implicit equation by
  Newton-Raphson.
- The passivity-based alternative is the scattering formulation of
  [[wave-digital-filters]] in the waveguide wiki, which also uses the bilinear
  transform but gets stability from energy arguments instead of a Lyapunov
  certificate.

## See also

- [[virtual-analog-overview]] - where TPT/ZDF sits among the method families.
- [[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]]

## References

[^1]: [[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]] - McClellan, "Stability Analysis of Time-Varying Virtual Analog Filters", DAFx26.

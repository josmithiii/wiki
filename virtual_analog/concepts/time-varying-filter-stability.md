---
title: Time-Varying VA Filter Stability
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [stability, time-varying, va-filters, tpt-zdf, state-variable, ladder-filter, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_28.pdf
  - raw/DAFx26_paper_28.txt
---

# Time-Varying VA Filter Stability

Musical VA filters modulate cutoff and resonance continuously, so the running
system is linear *time-varying* and can blow up even when the frozen-coefficient
system is stable at every instant - pole placement proves nothing. This page
gives the common quadratic Lyapunov function (CQLF) machinery and the results it
yields.[^1] Setting: a SISO state-space filter
$x[n{+}1] = A[n]x[n] + B[n]u[n]$, $y[n] = C[n]x[n] + D[n]u[n]$, $x[n] \in
\mathbb{R}^N$, from trapezoidal discretization of frozen continuous prototypes
(see [[tpt-zdf-filters]]). **BIBO stable** means there is $G \ge 0$ with
$|y[n]| \le GM$ whenever $|u[n]| \le M$ for all $n$.

## Common quadratic Lyapunov functions

A symmetric positive definite $P \in \mathbb{R}^{N\times N}$ (i.e. the quadratic
form $V(x) = x^T P x$) is a **CQLF** if, for all $x$ and $n$,

$$(A[n]x)^T P (A[n]x) \le \rho\, x^T P x, \ \ \rho \in [0,1) \tag{D}$$
$$x^T\!\big(A_C[n]^T P + P A_C[n]\big)x \le -\alpha\, x^T P x, \ \ \alpha > 0
\tag{C}$$

in the discrete (D) and continuous (C) cases; (C) says
$A_C[n]^T P + P A_C[n] + \alpha P$ is negative semi-definite for all $n$.

**Equivalence with matrix norms.** (D) holds iff Laroche's criterion 2 holds -
an invertible $T$ and $\gamma \in [0,1)$ with $\|T A[n] T^{-1}\| \le \gamma$
(induced Euclidean norm): take $T$ from the Cholesky factor $P = T^T T$, then
$\gamma = \sqrt{\rho}$. The Lyapunov and matrix-norm routes of earlier audio work
are thus one criterion. With bounded $B, C, D$, a CQLF gives BIBO stability.

## The key theorem: CQLFs survive trapezoidal discretization

**Theorem.** Let $\|A_C[n]\| < M$ and $g[n] \in [g_\min, g_\max)$, $g_\min > 0$.
If $P$ satisfies (C) for the family $A_C[n]$, it also satisfies (D) for the
trapezoidally discretized $A[n]$:[^1]

$$x^T A[n]^T P A[n] x \le \left(1 - \frac{2 g_\min \alpha \lambda_\min(P)}
{\lambda_\max(P)\,(1 + g_\max M)^2}\right) x^T P x .$$

*Sketch:* invert to $A_C[n] = \frac{1}{g[n]}(A[n]-I)(A[n]+I)^{-1}$, substitute
into (C), use $A[n] + I = 2(I - g[n]A_C[n])^{-1}$ to get
$x^T(A^T P A - P)x \le -2g[n]\alpha\, z^T P z$ with $z = (I-g[n]A_C[n])^{-1}x$,
then bound $\|x\| \le (1 + g_\max M)\|z\|$ and use
$\lambda_\min(P)\|z\|^2 \le z^T P z \le \lambda_\max(P)\|z\|^2$. Payoff: prove
stability in the *continuous* domain, where the matrices are far simpler, and
inherit it - with both $A_C[n]$ and $g[n]$ varying, one $P$ serving all $A_C[n]$.

**Corollary (filter sweeps).** Any filter from trapezoidally discretizing a
stable minimal LTI prototype is BIBO stable under *arbitrary* cutoff modulation
$g[n] \in [g_\min, g_\max)$: sweeping cutoff alone is always safe.

## Case studies

| Filter | Result under time-varying $g[n]$ | Counterexample |
|---|---|---|
| State-variable (SVF) | stable, all $R[n] \in [R_\min, R_\max]$, $R_\min > 0$ | - |
| Sallen-Key | stable for all $k[n] \in [0, k_\max]$, $k_\max < 2$ | - |
| Moog ladder | stable for fixed $k \in [0,4)$; time-varying $k[n] \in [0, 2.88]$ | unstable for $k[n]$ alternating $0, 2.89$ at $g = 1.3764$ |
| Diode ladder | stable for fixed $k \in [0, 901/49 \approx 18.4)$; time-varying $k[n] \in [0, 8.90]$ | unstable for $k[n]$ alternating $0, 8.91$ at $g = 1.8161$ |

- **SVF** (rows of $A_C$: $(-2R, -1)$, $(1, 0)$; lower $R$ = more resonance):
  take $P$ with unit diagonal and off-diagonal $\varepsilon < 2R/(1+R^2)$ at
  both endpoints; Sylvester's criterion on $A_C^T P + P A_C$ (leading entry
  $-4R + 2\varepsilon < 0$, determinant $4\varepsilon(2R - \varepsilon(1+R^2))
  > 0$) gives negative definiteness - simpler than earlier CAS-based proofs.
- **Sallen-Key** maps to the SVF by a similarity $T$ with $R = 1 - k/2$: if $P$
  is a CQLF for $A_{C1} = T A_{C2} T^{-1}$ then $T^T P T$ is one for $A_{C2}$
  (outputs still differ, since $T B_C$ does not match).
- **Ladders**: $P$ found by numerical search - Moog uses
  $P = \mathrm{diag}(1.14397715, 1.71579237, 2.69245163, 4)$,
  $\alpha = 6.8\times10^{-6}$; since $A_C^T P + P A_C + \alpha P$ is affine in
  $k$, checking the endpoints suffices ($k \in [0,2.88]$ improves on Helie's
  earlier $[0, 5/3)$). Counterexamples alternate $k[n]$ every sample; the
  two-period product $F = A_1 A_0$ has $|\lambda_1| \approx 1.001$ (Moog),
  $\approx 1.0008$ (diode), excited by an impulse and visible at the output, so
  the bounds are close to tight.

## Limitations and relations

- A CQLF is sufficient, not necessary: failing to find one proves nothing.
- Counterexamples switch per sample; slowly varying parameters are likely safe
  over wider ranges, but there is no precise musical-rate statement yet.
- [[wave-digital-filters]] get time-varying stability from passivity instead;
  [[allpass-clipping-prevention]] enforces $|y| \le M$ directly at runtime.

## References

[^1]: [[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]] - McClellan, "Stability Analysis of Time-Varying Virtual Analog Filters", DAFx26.

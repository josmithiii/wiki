---
title: State-Space Circuit Solvers (Adaptive QP)
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [state-space, circuit-modeling, nonlinear, spice, real-time, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_31.pdf
  - raw/DAFx26_paper_31.txt
---

# State-Space Circuit Solvers (Adaptive QP)

White-box VA solves the circuit's DAE per sample. The classical state-space route (Yeh;
Holters and Zolzer) needs *two* numerical procedures per step - a Newton-type iteration
for the nonlinear algebraic constraint, then a discretization to propagate the state -
hence two error sources. This reformulation replaces both with one convex **quadratic
program** plus residual-driven adaptive step size.[^1]

## Formulation

Circuit in state-space DAE form, $q$ collecting the nonlinear-device voltages and currents
and $\eta$ their current-voltage relations: $\dot{x} = Ax + Bu + Gq$, $Hq = Dx + Eu$,
$\eta(q) = 0$. Instead of solving $\eta(q_k) = 0$ each step, replace it with a **first-order
surrogate** - integrate $\dot{\eta}(q) = J(q)\dot{q} = K\eta(q)$ with Forward Euler while
integrating the linear dynamics with Backward Euler - giving three linear equalities in
$z_k = [x_k^\top\ q_k^\top]^\top$:

$$\begin{aligned}
(I - h_k A)x_k - h_k G q_k &= x_{k-1} + h_k B u_k\\
-D x_k + H q_k &= E u_k\\
J_{k-1} q_k &= h_k K_k \eta(q_{k-1}) + J_{k-1} q_{k-1}
\end{aligned}$$

with $J_{k-1} = d\eta(q_{k-1})/dq$ and $K_k$ Hurwitz (borrowed from constraint stabilization
in rigid-body dynamics). The step is $z_k = \arg\min_z \tfrac12 z^\top Q z + c^\top z$
subject to $A^{(k)}_\text{eq} z = b^{(k)}_\text{eq}$, optionally with inequality constraints
for state or device bounds; output $y_k = Mx_k + Lu_k + Nq_k$ as usual.

**Why a QP.** It is the general form, admitting cost metrics, regularization and bounds.
But with $Q = I$, $c = 0$ and no active inequalities it collapses to the minimum-norm
solution $z_k = (A^{(k)}_\text{eq})^\dagger b^{(k)}_\text{eq}$, a Moore-Penrose
pseudo-inverse solve - numerically indistinguishable here, and far cheaper.

## Residual as defect indicator

Choosing $K_k = -I/h_k$ annihilates the linearized constraint over the step, so the
**post-step nonlinear residual** $\nu_k := \eta(q_k) - \hat{\eta}(q_k) = \eta(q_k)$,
$\delta_k^\text{QP} := \|\nu_k\|$, is exactly the Taylor remainder left by linearizing $\eta$. Under boundedness, a band-limited
input ($\|u_k - u_{k-1}\| \le U_\text{BL}h_k$), uniform regularity of $A^{(k)}_\text{eq}$, a
Lipschitz Jacobian and a bounded step ratio, the induced mismatch is $O(h_k)$, hence
$\|q_k - q_{k-1}\| = O(h_k)$ and $\|\nu_k\| \le M\|q_k - q_{k-1}\|^2 = O(h_k^2)$ - the correct
local order ($p = 1$) for step-size control. Accept the step when $\delta_k^\text{QP} \le$ tol;
otherwise shrink $h_k$ and redo it, using a deadbeat, PID (H321) or predictive (H0211)
Soderlind controller with order $\kappa = 2$, clipped to $[h_\text{min}, h_\text{max}]$. After
acceptance the step resets to some $\bar h_0 \le h_0$ so it does not stay needlessly small.

## Results against SPICE

Three circuits: diode clipper (baseline), BJT common-emitter amplifier, and a Colpitts
oscillator as a stress test (self-oscillating circuits are sensitive to discretization error).
MATLAB on a Ryzen 7 5800H, $h_0 = 1/44100$ s.

| Circuit | SPICE | best proposed | note |
|---|---|---|---|
| Diode clipper (2.205 kHz, 5 V) | 80.70 ms | 1.38 ms fixed-$h$ pseudo-inverse; 5.26 ms deadbeat adaptive | ECQP 43.14 ms, output indistinguishable |
| CE amplifier (220 Hz, 0.5 V) | 210.80 ms | 99.01 ms (predictive), 100.90 ms (deadbeat) | PID rule slower than SPICE (238 ms) |
| Colpitts oscillator (12 V step) | 215.60 ms | 85.65 ms (predictive) | min step ~200 ns = 128x oversampling |

- **Adaptive step size matters more than a fixed high rate.** With fixed $h$, Backward
  Euler beats the trapezoidal rule on the clipper (it is L-stable and damps the fast
  modes clipping excites); with adaptive stepping the two become indistinguishable and
  squared error against SPICE drops sharply.
- The QP residual is a *more interpretable* defect indicator than a step-doubling
  baseline: it spikes narrowly exactly where the diodes start clipping and the step size
  drops there, whereas step-doubling stays flat with wide drops around the events.
- The controller (deadbeat / PID / predictive) barely matters for the clipper; best
  accuracy/time trade-offs came at $\bar h_0 = h_0/4$ (clipper), $h_0$ (amplifier),
  $h_0/8$ (oscillator).
- Colpitts: build-up, steady-state waveform and spectrum all match, resonance at 11.35 kHz
  versus SPICE's 11.3 kHz (a small lag that becomes a small lead over 20 ms).
- Preliminary real-time evidence: MATLAB Audio Toolbox exported the clipper and amplifier
  as VST `.dll` plugins that ran in REAPER with no perceptible dropouts, circuit and device
  parameters exposed as live controls.

**Limitations:** MATLAB implementation, short simulations, synthetic inputs; no
latency-oriented benchmark, sparse or embedded solver; the choice of $\bar h_0$ and of the
QP metric $Q$ (energy- or passivity-motivated metrics being the obvious direction) remain
open; matrices are hand-derived per circuit, no netlist pipeline. Code and demos at
`https://mezea-uvg.github.io/RAMA/`.

## See also

[[virtual-analog-overview]] - [[tpt-zdf-filters]] - [[wave-digital-filters]] (the
scattering route to the same problem)

## References

[^1]: [[entities/source-papers#paper-zea-adaptive-multirate-qp-2026]] - Zea & Rivera, "Residual-Driven Adaptive Multi-Rate Quadratic Programming Framework for Nonlinear Analog Audio Circuit Emulation", DAFx26.

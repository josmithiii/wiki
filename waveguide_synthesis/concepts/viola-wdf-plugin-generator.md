---
title: VIOLA — Automatic WDF Audio Plug-in Generator
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [dsp, faust, realtime, nonlinear, reference]
sources:
  - raw/papers/automatic-generation-va-plugins-wdf.txt
  - https://github.com/polimi-ispl/viola
  - https://polimi-ispl.github.io/viola/
---

# VIOLA — Automatic Plug-in Generation from SPICE Netlists

**VIOLA** (waVe dIgital audiO pLug-in generAtor) is a MATLAB framework
by Giampiccolo, Ravasi & Bernardini (Politecnico di Milano, JAES 2025)
for automatically generating Virtual Analog (VA) audio plug-ins from
SPICE netlists via [[wave-digital-filters]]. Target output: VST / AU /
EXE / DLL usable in any DAW.[^1]

## Pipeline

1. **SPICE parser** — reads `.net`/`.txt`, extracts element types, values,
   and the incidence matrix $A \in \{-1,0,1\}^{O\times N}$.
2. **Topology derivation** — computes fundamental loop $B$ and cut-set
   $Q$ matrices directly from $A$:
   $$F = (\Lambda^T\Lambda)^{-1}\Lambda^T\Theta, \quad
     B = [I\ {-}F^T],\ Q = [F\ I]$$
   where $\Lambda,\Theta$ come from a tree/cotree split of $A$.
   For op-amp (nullor) circuits, a double-digraph decomposition yields
   separate $F_V, F_I$.
3. **Scattering matrix** — $S$ from Eq. (9)/(10) of [^1]; with nullors
   from Eq. (11)/(12).
4. **Adaptation** — see below; adapts one junction port to the single
   nonlinear element.
5. **Solver instantiation** — explicit tree if one nonlinearity (after
   consolidation); otherwise SIM (see below).
6. **MATLAB Audio Toolbox** — wraps the WDF as a plug-in with auto-laid-out
   knob GUI and compiles to C++.

## Arbitrary Port Adaptation (new result)

Werner et al. (2015) solved the linear scattering problem for arbitrary
topologies via MNA stamps (see [[wdf-r-type-adaptors]]), noting that
adaptation requires "solving for $R_n$" such that $S_{nn}=0$ without
specifying a method (symbolic algebra or numerical root-finding would
both work). VIOLA contributes a **direct closed-form formula** — the
Thévenin equivalent resistance — that gives $Z_n$ in one shot without
iteration or symbolic manipulation. Using MNA, let $\check{A},\check{Z}$
be the reduced incidence and port-resistance matrices (remove port $n$'s
column and node $\alpha$'s row). Then

$$\check{R}_\alpha = \check{Y}^{-1}\left(I + \check{U}\check{\Psi}^{-1}\check{O}\check{Y}^{-1}\right),
  \quad Z_n = e_\beta^T \check{R}_\alpha e_\beta$$

where $\check{Y}=\check{A}\check{Z}^{-1}\check{A}^T$ and
$\check{\Psi} = H - \check{O}\check{Y}^{-1}\check{U}$ is the Schur
complement. This is the Thévenin equivalent resistance seen from port
$n$ — exactly the reflection-free choice. For a detailed derivation
with a worked delta-network example, see
[[wdf-arbitrary-port-adaptation]].

## Diodes and Consolidation

Diodes use the Extended Shockley model (series $R_s$, shunt $R_p$)
solved in closed form via the Wright $\omega$ function[^1]:
$$b = \sigma(a) - \phi\,\omega\!\left(\ln\chi + \psi(a) + \sigma(a)/\phi\right).$$
Following standard practice (Yeh & Smith 2008, Paiva et al. 2012,
Werner et al. 2015), series of $D$ identical diodes collapse by scaling
$\eta,R_s,R_p$ by $D$; antiparallel identical pairs collapse via
$b=\operatorname{sgn}(a)f(|a|)$. VIOLA automates this detection during
netlist parsing.

## Scattering Iterative Method (SIM)

For circuits with multiple irreducible nonlinearities, VIOLA runs SIM[^1]
— a fixed-point iteration updating nonlinear port resistances
$Z_p[k] = v'_p(i_p[k-1])$ to match the tangent of the $i$–$v$ curve.
Convergence check $\|v^{(\gamma)} - v^{(\gamma-1)}\|_2 \le \varepsilon_{\text{SIM}}$
(typically $10^{-5}$ V). **Dynamic Scattering Recomputation (DSR)**
only rebuilds $S$ when $\sum_p |v'_p - Z_p[k-1]| \ge \xi_{\text{DSR}}$
(e.g. 1 kΩ), amortizing the matrix inversion.

## Validation (JAES 2025)

| Circuit | Nonlinearities | Method | MSE | RTR @ 48 kHz |
|---|---|---|---|---|
| EHX Op Amp Big Muff Pi | 6 × 1N4148 (consolidatable) | Explicit tree | $1.42\times10^{-6}$ | **0.039** |
| Digitech Overdrive 250 | 3 × 1N4148 (asymmetric) | SIM + DSR | $3.9\times10^{-10}$ | **0.166** |

Both RTRs $\ll 1$ on an Intel i7-11800H — real-time with wide headroom.

## Significance

- **First end-to-end SPICE → VA plug-in pipeline** based on WDFs —
  builds on Werner et al.'s MNA-based scattering (2015) and Bernardini
  et al.'s reciprocal connection networks (2019), adding SPICE parsing,
  automatic solver selection, and plug-in compilation.
- **Direct port adaptation formula** — computes $Z_n$ in closed form as
  the Thévenin resistance, more elegant than numerical root-finding
  (which also works) but not strictly required for automation.
- **Automatic diode consolidation** — the technique of collapsing
  series/antiparallel diodes into a single element is well established
  (Yeh & Smith 2008, Paiva et al. 2012, Werner et al. 2015). VIOLA
  automates this as part of the SPICE parsing pipeline, often reducing
  multi-NL circuits to explicit single-NL solutions (e.g. Big Muff Pi:
  6 diodes → 1 element, RTR 0.039).
- **SIM + DSR** as a table-free alternative to K-method for circuits
  with irreducible multiple nonlinearities.
- Constrained class: R, L, C, potentiometers, resistive sources, ideal
  op-amps, diodes. Future work: multi-port nonlinearities, JUCE backend,
  better iterative solvers.

## Related

- [[wdf-r-type-adaptors]] — MNA-based scattering that VIOLA builds on
- [[wdf-multiple-nonlinearities]] — K-method framework; SIM is an alternative
- [[wave-digital-filters]] — theory
- [[wdf-adaptors]] — scattering junctions
- [[wdf-elements]] — one-port models including diode
- [[wdf-applications]] — broader VA emulation context

## References
[^1]: Giampiccolo, R.; Ravasi, S.; Bernardini, A. "Automatic Generation
    of Virtual Analog Audio Plug-ins based on Wave Digital Filters."
    *J. Audio Eng. Soc.*, vol. 73, no. 6, pp. 376–387, 2025.
    doi:10.17743/jaes.2022.0208. Code: https://github.com/polimi-ispl/viola

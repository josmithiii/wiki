---
title: "WDF Arbitrary Port Adaptation"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [scattering, impedance, dsp, reference]
sources:
  - raw/papers/automatic-generation-va-plugins-wdf.txt
---

# WDF Arbitrary Port Adaptation

## What Is Adaptation?

In a WDF with one nonlinear element, the entire structure can be solved
**explicitly** (no iterative solver) — provided the junction port
connected to that element is **adapted**: its free parameter $Z_n$ is
chosen so that the diagonal entry $S_{nn} = 0$, eliminating the
delay-free loop at that port. For simple series or parallel junctions,
adaptation formulas are textbook. For a **general N-port topological
junction** — any circuit topology that doesn't decompose into a tree
of 2-port series/parallel adaptors — no closed-form adaptation formula
existed until Giampiccolo et al. (2025).

## The Gap: Why This Was Hard

To adapt port $n$ of a general junction, one had to:

1. Form the scattering matrix $S$ **symbolically**, leaving $Z_n$ as a
   free variable — this requires inverting an $(l\times l)$ or
   $(q\times q)$ matrix symbolically (Eqs. 9–12 in [[viola-wdf-plugin-generator]]).
2. Expand $S_{nn}$ into a rational expression in $Z_n$.
3. Set $S_{nn} = 0$ and solve for $Z_n$ with a symbolic algebra system.

For a 3-port delta this is manageable; for a 25-port circuit like the
Big Muff Pi, the symbolic expression is enormous. This manual,
tool-dependent step blocked any fully automatic SPICE-to-WDF pipeline.

## The New Result: Adaptation via Thévenin Resistance

The key insight: **the port resistance that makes $S_{nn}=0$ is the
Thévenin equivalent resistance seen looking into the network from port
$n$'s terminals.** This can be computed purely numerically via Modified
Nodal Analysis (MNA).

Let port $n$ have terminal nodes $\alpha$ (reference) and $\beta$.
Remove port $n$'s column from the incidence matrix $A$ and node
$\alpha$'s row → reduced matrices $\check{A}$, $\check{Z}$. Then:

$$\check{Y} = \check{A}\,\check{Z}^{-1}\check{A}^T, \qquad
  \check{R}_\alpha = \check{Y}^{-1}, \qquad
  Z_n = e_\beta^T\,\check{R}_\alpha\,e_\beta$$

(With op-amps/nullors, $\check{R}_\alpha$ gains a Schur-complement
correction — see [[viola-wdf-plugin-generator#arbitrary-port-adaptation-new-result]].)

No symbolic algebra. The matrix $\check{Y}$ is $(O{-}1)\times(O{-}1)$
where $O$ is the number of nodes — typically much smaller than $N$ —
and is inverted **numerically** with known element values.

## Worked Example: Delta (Triangle) Network

Three resistors in a delta — the simplest topology requiring a general
3-port scattering junction (it cannot be represented as a WDF tree of
2-port series/parallel adaptors).

```
       R₂
    1 ----- 2           Nodes: 0, 1, 2
    |     /              R₁: 0 — 1
 R₁ |   / R₃             R₂: 1 — 2
    | /                  R₃: 0 — 2
    0
```

Port 1 ($R_1$, nodes $\alpha{=}0$, $\beta{=}1$) is the root of the
connection tree — the one port we need to adapt. (In practice this is
where the nonlinear element sits, since it's the only element that
can't self-adapt.) We want the adaptation resistance $Z_1$.

### Old Method — Symbolic

The 3-port scattering matrix (via loop analysis with
$B = [1,\ {-}1,\ {-}1]$) gives:

$$S_{11} = \frac{Z_2 + Z_3 - Z_1}{Z_1 + Z_2 + Z_3}$$

Setting $S_{11}=0$ yields $Z_1 = Z_2 + Z_3$. Easy here — but only
because we could form and manipulate $S$ symbolically for a 3-port.

### New Method — MNA (Numerical)

**Step 1.** Full incidence matrix and reduction:

$$A = \begin{pmatrix} -1 & 0 & -1 \\ +1 & -1 & 0 \\ 0 & +1 & +1 \end{pmatrix}
\xrightarrow{\text{drop col 1, row 0}}
\check{A} = \begin{pmatrix} -1 & 0 \\ +1 & +1 \end{pmatrix},\quad
\check{Z} = \operatorname{diag}(Z_2,\, Z_3)$$

**Step 2.** Reduced nodal admittance:

$$\check{Y} = \check{A}\,\check{Z}^{-1}\check{A}^T
= \begin{pmatrix} 1/Z_2 & -1/Z_2 \\ -1/Z_2 & 1/Z_2+1/Z_3 \end{pmatrix}$$

**Step 3.** Invert ($\det\check{Y} = 1/(Z_2 Z_3)$):

$$\check{R}_0 = \check{Y}^{-1}
= \begin{pmatrix} Z_2+Z_3 & Z_3 \\ Z_3 & Z_3 \end{pmatrix}$$

**Step 4.** Read off the $(\beta,\beta)=(1,1)$ entry:

$$Z_1 = e_1^T\,\check{R}_0\,e_1 = Z_2 + Z_3 \quad\checkmark$$

The result matches — it is simply the Thévenin resistance seen from
port 1's terminals: with $R_1$ removed, current flows from node 1
through $R_2$ to node 2, then through $R_3$ back to node 0, i.e.
$R_2$ and $R_3$ in series.

### Why the Delta Still Illustrates the Point

The delta **cannot** be built from WDF 2-port series/parallel adaptors
— it requires a general 3-port junction with its own scattering matrix.
The adaptation result $Z_1=Z_2+Z_3$ happens to equal a series formula,
but that's a consequence of the circuit (one loop), not of the topology
being "series" in the WDF-tree sense. For larger non-decomposable
topologies — Wheatstone bridges, op-amp feedback networks — the
Thévenin resistance has no simple closed form, and the MNA formula
becomes the only practical path.

## Related

- [[viola-wdf-plugin-generator]] — the VIOLA framework that uses this result
- [[wdf-adaptors]] — standard 2-port series/parallel adaptation
- [[wave-digital-filters]] — WDF fundamentals
- [[scattering-junctions]] — scattering matrices

## References
[^1]: Giampiccolo, R.; Ravasi, S.; Bernardini, A. "Automatic Generation
    of Virtual Analog Audio Plug-ins based on Wave Digital Filters."
    *JAES*, vol. 73, no. 6, pp. 376–387, 2025. Sec. 3.2.

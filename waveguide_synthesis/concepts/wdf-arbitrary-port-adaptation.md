---
title: "WDF Arbitrary Port Adaptation"
created: 2026-04-15
updated: 2026-11-25
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
adaptation formulas are textbook. For **R-type topological junctions**
— those that can't decompose into series/parallel adaptors —
Werner et al. (2015) solved the scattering matrix derivation via MNA
(see [[wdf-r-type-adaptors]]), but adaptation was left to symbolic
algebra or root-finding until Giampiccolo et al. (2025).[^1]

## Prior Approaches to Adaptation

Werner's MNA stamp method (2015) computes $S$ numerically for any given
set of port resistances, and notes that adaptation requires "solving for
$R_n$" such that $S_{nn}=0$, without specifying a method. This could be
done by:

1. **Symbolic algebra** — keep $Z_n$ as a free variable, invert
   symbolically, expand $S_{nn}$, solve. Works but doesn't scale well
   to large circuits.
2. **Numerical root-finding** — evaluate $S_{nn}(Z_n)$ for trial values,
   bisect or Newton. Automatable but iterative.

Both are viable. Giampiccolo et al. (2025) contribute a third option:

## Direct Formula: Adaptation via Thévenin Resistance

The key insight: **the port resistance that makes $S_{nn}=0$ is the
Thévenin equivalent resistance seen looking into the network from port
$n$'s terminals.** This can be computed in closed form via Modified
Nodal Analysis (MNA) — no iteration, no symbolic manipulation.

Let port $n$ have terminal nodes $\alpha$ (reference) and $\beta$.
Remove port $n$'s column from the incidence matrix $A$ and node
$\alpha$'s row → reduced matrices $\check{A}$, $\check{Z}$. Then:

$$\check{Y} = \check{A}\,\check{Z}^{-1}\check{A}^T, \qquad
  \check{R}_\alpha = \check{Y}^{-1}, \qquad
  Z_n = e_\beta^T\,\check{R}_\alpha\,e_\beta$$

(With op-amps/nullors, $\check{R}_\alpha$ gains a Schur-complement
correction — see [[viola-wdf-plugin-generator]].)

No symbolic algebra. The matrix $\check{Y}$ is $(O{-}1)\times(O{-}1)$
where $O$ is the number of nodes — typically much smaller than $N$ —
and is inverted **numerically** with known element values.

## Worked Example: Delta (Triangle) Network

Three one-ports in a delta form a single loop, i.e. a plain three-port
**series** junction - not an R-type topology, but the smallest case on
which the formula can be checked by hand against the textbook
reflection-free series port ([[wdf-adaptors]]).

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

### Via Scattering Matrix (symbolic or root-finding)

The 3-port series scattering matrix (via loop analysis with
$B = [1,\ {-}1,\ {-}1]$) gives:

$$S_{11} = \frac{Z_2 + Z_3 - Z_1}{Z_1 + Z_2 + Z_3}$$

Setting $S_{11}=0$ yields $Z_1 = Z_2 + Z_3$. Easy here — for larger
circuits one would use symbolic algebra or numerical root-finding.

### Via Thévenin Resistance (direct formula)

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

### What the Delta Does and Does Not Show

The result $Z_1=Z_2+Z_3$ is exactly the classical series reflection-free
port, as it must be: the delta *is* a series adaptor, so the example only
verifies the mechanics. The formula earns its keep on genuinely
non-decomposable (R-type) junctions, the smallest of which has six ports
(bridged-T, Wheatstone bridge), and on op-amp feedback networks. There
the Thévenin resistance has no convenient closed form, and one numerical
inversion of $\check{Y}$ replaces symbolic algebra or root-finding.

## Related

- [[wdf-r-type-adaptors]] — MNA-derived scattering for R-type junctions
  (solves the linear problem; this page addresses the remaining
  adaptation step)
- [[viola-wdf-plugin-generator]] — the VIOLA framework that uses this result
- [[wdf-adaptors]] — standard 2-port series/parallel adaptation
- [[wave-digital-filters]] — WDF fundamentals
- [[scattering-junctions]] — scattering matrices

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Reflection Free Port](https://ccrma.stanford.edu/~jos/pasp/Reflection_Free_Port.html), [Series Reflection Free Port](https://ccrma.stanford.edu/~jos/pasp/Series_Reflection_Free_Port.html), [Binary Connection Tree Series Adaptor](https://ccrma.stanford.edu/~jos/pasp/Binary_Connection_Tree_Series.html)

## References
[^1]: Giampiccolo, R.; Ravasi, S.; Bernardini, A. "Automatic Generation
    of Virtual Analog Audio Plug-ins based on Wave Digital Filters."
    *JAES*, vol. 73, no. 6, pp. 376–387, 2025. Sec. 3.2.

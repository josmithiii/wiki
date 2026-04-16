---
title: "WDF R-Type Adaptors for Arbitrary Topologies"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [scattering, impedance, dsp, reference]
sources:
  - raw/papers/werner-wdf-adaptors-arbitrary-topologies-dafx15.txt
  - raw/papers/werner-dissertation-2016.txt
---

# WDF R-Type Adaptors for Arbitrary Topologies

Classical WDF adaptors handle only series and parallel connections.
Werner, Smith & Abel (DAFx-15)[^1] present two methods for deriving
scattering matrices for **R-type** (rigid / non-decomposable) topologies
that may include multiport linear elements (transformers, controlled
sources, op-amps). This is the companion paper to
[[wdf-multiple-nonlinearities]], which builds on these linear techniques
to handle nonlinear circuits.

## The Problem

Many real audio circuits contain topologies that **cannot be decomposed**
into series/parallel connections:

- **Bridged-T networks** — guitar tone stacks (Bassman, Tube Screamer),
  analog drum machines (TR-808)
- **Op-amp feedback paths** — output fed back through a network to the
  inverting input
- **Transformer-coupled stages** — controlled sources in tube amplifiers

Before this work, such circuits were simply intractable as WDFs.

## Method 1: MNA-Derived Scattering (the main result)

### SPQR Decomposition

Apply the graph-theoretic method of Fränken et al.[^2] to find the
circuit's SPQR tree. Multiport linear elements (op-amps, transformers)
are kept intact via replacement graphs. The result: a tree of S (series),
P (parallel), and **R-type** (rigid) nodes, plus Q (single-component)
leaves.

### Instantaneous Thévenin Port Equivalent

Each port of the R-type adaptor is replaced by its instantaneous
Thévenin equivalent: a voltage source $e_n = a_n$ in series with a
resistance $R_n$ (the port resistance). This produces a Kirchhoff-domain
equivalent circuit that can be analyzed with standard MNA.

### MNA Stamp Procedure

Assemble the MNA system matrix $X$ using element stamps — resistors,
voltage sources, and controlled sources (VCVS for op-amps, etc.):

$$\begin{pmatrix} Y & A \\ B & D \end{pmatrix}
  \begin{pmatrix} v_n \\ j \end{pmatrix}
  = \begin{pmatrix} i_s \\ e \end{pmatrix}$$

For simple R-type adaptors (no multiport elements): $i_s=0$, $B=A^T$,
$D=0$. One node is chosen as the datum (dropped from the system).

### Scattering Matrix

From the wave variable definition $b = a - 2R_p i$ and the MNA solution
$j = [0\ I]X^{-1}[0\ I]^T e$, with $i = -j$ and $e = a$:

$$S = I + 2\begin{bmatrix}0 & R\end{bmatrix}X^{-1}\begin{bmatrix}0 \\ I\end{bmatrix}$$

where $R = \operatorname{diag}(R_1,\ldots,R_N)$. **Adaptation** (making
one port reflection-free for inclusion in a WDF tree) is done as usual:
solve $S_{nn} = 0$ for $R_n$. See
[[wdf-arbitrary-port-adaptation]] for the general adaptation formula.

## Method 2: Ring Resolution (wave-domain algebraic)

When a non-tree-like arrangement of standard 3-port series/parallel
adaptors is found by inspection (a "ring"), it can be collapsed:

1. Partition the ring's scattering into internal ($a_i, b_i$) and
   external ($a, b$) waves
2. Impose port compatibility: $a_i = Cb_i$ (permutation with possible
   sign flips)
3. Eliminate internal waves:
   $$S = S_{21}(C^{-1} - S_{11})^{-1}S_{12} + S_{22}$$

Advantage: no graph theory needed. Disadvantage: the ring must be found
by inspection (no systematic procedure); no multiport element support.

## Case Studies

### Fender Bassman Tone Stack
- Bridged-T topology → 6-port R-type adaptor + 4 series adaptors
- Both methods applied; results match SPICE except for expected
  bilinear-transform frequency warping at high frequencies

### Tube Screamer Tone/Volume Stage
- Op-amp (VCVS with gain $A_{OL}$) absorbed into R-type adaptor via
  replacement graph
- Demonstrates general op-amp modeling beyond the differential-amplifier
  special case of Paiva et al.

## Key Contributions

- **First general method** for deriving R-type adaptor scattering
  matrices, including absorbed multiport linear elements
- **Stamp-based** (automatable) — same MNA stamp philosophy used in
  SPICE simulators
- **Connection Tree** (CT) replaces Binary Connection Tree (BCT) — R-type
  adaptors have $\ge 6$ ports, so the tree is no longer binary
- Direct enabler of [[wdf-multiple-nonlinearities]] — the R-type adaptor
  at the root hosts all nonlinear ports in the companion framework

## Related

- [[wdf-multiple-nonlinearities]] — companion paper; uses R-type
  adaptors to host multiple nonlinear elements
- [[wdf-adaptors]] — classical series/parallel adaptors
- [[wdf-arbitrary-port-adaptation]] — general port adaptation (later
  generalization by Giampiccolo et al.)
- [[viola-wdf-plugin-generator]] — VIOLA automates the full pipeline
  from SPICE netlist through R-type adaptor derivation to plug-in
- [[wave-digital-filters]] — WDF fundamentals

## References
[^1]: Werner, K.J.; Smith, J.O.; Abel, J.S. "Wave Digital Filter
    Adaptors for Arbitrary Topologies and Multiport Linear Elements."
    *Proc. DAFx-15*, Trondheim, 2015.
[^2]: Fränken, D. et al. "Generation of Wave Digital Structures for
    Networks Containing Multiport Elements." *IEEE TCAS-I*, 2005.
[^3]: Werner, K.J. *Virtual Analog Modeling of Audio Circuitry Using
    Wave Digital Filters.* Ph.D. diss., Stanford, 2016. Ch. 2 gives
    the comprehensive treatment with TR-808 bridged-T case studies.

---
title: "WDF Multiple/Multiport Nonlinearities"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [scattering, nonlinear, dsp, impedance]
sources:
  - raw/papers/resolving-wdf-multiple-multiport-nonlinearities.txt
  - raw/papers/werner-dissertation-2016.txt
---

# WDF Multiple/Multiport Nonlinearities

Classical WDFs support only **one nonlinear one-port element**,
placed at the root of a binary connection tree where its junction port
is adapted (see [[wdf-arbitrary-port-adaptation]]). Werner, Nangia,
Smith & Abel (DAFx 2015)[^1] introduced a general framework that
removes this limitation, accommodating **any number** of nonlinear
elements with **any number of ports** each, in **arbitrary topologies**.

## The Problem

Real audio circuits (tube amps, distortion pedals) contain multiple
nonlinear devices — diodes, BJTs, triodes — often in topologies with
feedback between them. The standard WDF tree can only adapt one port,
so the root can host only one nonlinearity. Previous workarounds:

- **Combine into one port** — e.g. antiparallel diode pair as a single
  element (works only when devices are topologically adjacent)[^2]
- **Cross-control models** — e.g. triode with zero grid current, so the
  plate-cathode acts as a one-port with grid voltage as parameter[^3]
- **Ad-hoc unit delays** — decouple nonlinearities at the cost of
  accuracy

None of these handle the general case.

## Framework Overview

### Step 1: SPQR Decomposition → R-Type Root

Extend the graph-theoretic method of Fränken et al.[^4] to nonlinear
circuits: replace all nonlinear elements with a single replacement
graph, then search for split components (SPQR tree). The result:

- A **root R-type adaptor** containing all nonlinear ports — the
  topology that cannot be decomposed further into series/parallel
- **Standard WDF subtrees** hanging below, handled with classical
  techniques

### Step 2: Separate Scattering from Nonlinearity

Pull the nonlinear elements out of the R-type adaptor and place them
above it. The system becomes (Fig. 1 of [^1]):

$$a_I = f(b_I), \quad b_I = S_{11}a_I + S_{12}a_E, \quad
  b_E = S_{21}a_I + S_{22}a_E$$

where $a_I, b_I$ are internal (nonlinear) port waves, $a_E, b_E$ are
external port waves from the subtrees below, and $f(\cdot)$ is the
vector nonlinearity. This has a **delay-free loop** through $f$ and
$S_{11}$ — not yet computable.

### Step 3: Move to the Kirchhoff Domain (w–K Converter)

Replace the wave-domain nonlinearity $f(\cdot)$ with a Kirchhoff-domain
relationship $i_C = h(v_C)$, connected to the scattering via a wave–
Kirchhoff converter $C$:

$$C = \begin{pmatrix} -R_I & I \\ -2R_I & I \end{pmatrix}$$

where $R_I = \operatorname{diag}(R_1,\ldots,R_P)$ is the matrix of
internal port resistances. Advantage: $h(\cdot)$ is usually explicit
and easy to tabulate (Shockley diode law, Ebers–Moll BJT model, etc.).

### Step 4: Consolidate into NLSS Form

Combine the eight $S$ and $C$ partitions into four matrices $E, F, M, N$:

$$v_C = Ea_E + Fi_C, \quad b_E = Ma_E + Ni_C, \quad i_C = h(v_C)$$

with $H = (I - C_{22}S_{11})^{-1}$ and

$$E = C_{12}(I + S_{11}HC_{22})S_{12}, \quad
  F = C_{12}S_{11}HC_{21} + C_{11}$$
$$M = S_{21}HC_{22}S_{12} + S_{22}, \quad N = S_{21}HC_{21}$$

One delay-free loop remains: $v_C \to i_C \to v_C$ through $h$ and $F$.

### Step 5: Resolve via K-Method

The K-method (Borin, De Poli & Rocchesso, 2000) transforms the
Kirchhoff nonlinearity $i_C = h(v_C)$ into a **transformed
nonlinearity** $i_C = g(p)$ where $p = Ea_E$ is a pseudo-wave
variable with no delay-free loop:

$$\begin{pmatrix} p \\ i_C \end{pmatrix}
  = \begin{pmatrix} I & -K \\ I & 0 \end{pmatrix}
  \begin{pmatrix} v_C \\ i_C \end{pmatrix},
  \quad K = F$$

Since $h(\cdot)$ is explicit in the Kirchhoff domain, it can be
pre-tabulated on a grid, then transformed to $g(\cdot)$ via the
K-method. At runtime: $p = Ea_E$ (matrix-vector multiply),
$i_C = g(p)$ (scattered interpolation), $b_E = Ma_E + Ni_C$.

## Deriving the Scattering Matrix S

The R-type adaptor's $S$ is derived from Modified Nodal Analysis:
replace each port with its instantaneous Thévenin equivalent (voltage
source $a_n$, resistance $R_n$), form the MNA system $Xv = s$, then

$$S = I + 2\begin{bmatrix}0 & R\end{bmatrix}X^{-1}\begin{bmatrix}0 \\ I\end{bmatrix}$$

(detailed in companion paper Werner et al., DAFx-15[^5]).

## Case Study: Big Muff Pi Clipping Stage

Three nonlinear ports: antiparallel 1N914 diode pair + BJT (2N5089)
$V_{BE}$ and $V_{CE}$ junctions. The R-type adaptor has 8 ports
(3 internal + 5 external). A $201^3$ lookup table for $h(\cdot)$ is
transformed to $g(\cdot)$. WDF output matches SPICE to within a few mV.

## Relationship to Later Work

- **SIM** (Bernardini et al., 2018+; used in [[viola-wdf-plugin-generator]])
  — an alternative iterative solver for the same class of problems;
  avoids tabulation but requires iterating at each sample
- **Neural K-method** (Bernardini et al., 2025) — replaces the lookup
  table with a neural network
- **Olsen et al. (DAFx 2016)** — iterative techniques for resolving
  grouped nonlinearities in the same framework

## Related

- [[wdf-arbitrary-port-adaptation]] — adapting a single port (the
  single-nonlinearity case this framework generalizes)
- [[wave-digital-filters]] — WDF fundamentals
- [[wdf-elements]] — nonlinear element models (diode, K-method)
- [[wdf-applications]] — VA circuit emulation context
- [[viola-wdf-plugin-generator]] — VIOLA uses SIM as an alternative
  to the K-method for this problem class

## References
[^1]: Werner, K.J.; Nangia, V.; Smith, J.O.; Abel, J.S. "Resolving
    Wave Digital Filters with Multiple/Multiport Nonlinearities."
    *Proc. DAFx-15*, Trondheim, 2015.
[^2]: Werner, K.J. et al. "An Improved and General Diode Clipper Model
    for Wave Digital Filters." *AES Conv. 139*, 2015.
[^3]: Karjalainen, M.; Pakarinen, J. "Wave Digital Simulation of a
    Vacuum-Tube Amplifier." *ICASSP*, 2006.
[^4]: Fränken, D. et al. "Generation of Wave Digital Structures for
    Networks Containing Multiport Elements." *IEEE TCAS-I*, 2005.
[^5]: Werner, K.J. et al. "Wave Digital Filter Adaptors for Arbitrary
    Topologies and Multiport Linear Elements." *DAFx-15*, 2015.
[^6]: Werner, K.J. *Virtual Analog Modeling of Audio Circuitry Using
    Wave Digital Filters.* Ph.D. diss., Stanford, 2016. Ch. 4 gives
    the comprehensive treatment; also adds Newton-Raphson as an
    alternative to lookup-table resolution.

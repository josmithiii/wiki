---
title: WDF Adaptors
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [waveguide, scattering, dsp, impedance, physical-modeling]
sources:
  - /w/pasp/adaptors.tex
  - /w/pasp/paralleladaptor.tex
  - /w/pasp/seriesadaptor.tex
  - https://ccrma.stanford.edu/~jos/pasp/Adaptors_Wave_Digital_Elements.html
  - /l/l420/WaveDigitalFiltersIntro/wdfi-content.tex
---

# WDF Adaptors

An adaptor is a memoryless N-port interface that interconnects wave digital
elements by implementing scattering appropriate for the physical connection
type (parallel or series).[^1][^2] It computes exactly the same as a scattering
junction in a digital waveguide network.

## Two-Port Parallel Adaptor (Force Waves)

Parallel connection: common force, velocities sum to zero.

Junction force from incoming waves:
$$
f_J \;=\; \frac{2\,(\Gamma_1\, f_1^+ + \Gamma_2\, f_2^+)}{\Gamma_1 + \Gamma_2},
\qquad \Gamma_i \;\triangleq\; 1/R_i.
$$

Reflection coefficient:
$$
\rho \;=\; \frac{R_2 - R_1}{R_2 + R_1}.
$$

### Kelly-Lochbaum Form (4 multiplies, 2 adds)
$$
\begin{aligned}
f_1^- &= \rho\, f_1^+ + (1-\rho)\, f_2^+\\
f_2^- &= (1+\rho)\, f_1^+ - \rho\, f_2^+
\end{aligned}
$$

### One-Multiply Form (1 multiply, 3 adds)
$$
\begin{aligned}
t    &= \rho\,(f_1^+ - f_2^+)\\
f_1^- &= f_2^+ + t\\
f_2^- &= f_1^+ + t
\end{aligned}
$$

The one-multiply form is most efficient in custom VLSI. The Kelly-Lochbaum form
may be more efficient in software and slightly faster in parallel hardware.

## Two-Port Series Adaptor

Series connection: common velocity, forces sum to zero.

Same $\rho$; the result is the dual of the parallel case ($f \leftrightarrow v$,
$R \leftrightarrow \Gamma$). In velocity waves, then converted to force waves
via $f_i^+ = R_i v_i^+$, $f_i^- = -R_i v_i^-$:
$$
\begin{aligned}
v_1^- &= -\rho\, v_1^+ + (1+\rho)\, v_2^+ & \qquad f_1^- &= \rho\, f_1^+ - (1-\rho)\, f_2^+\\
v_2^- &= (1-\rho)\, v_1^+ + \rho\, v_2^+ & \qquad f_2^- &= -(1+\rho)\, f_1^+ - \rho\, f_2^+
\end{aligned}
$$
One-multiply force-wave form: $t = \rho\,(f_1^+ + f_2^+)$, $f_1^- = t - f_2^+$, $f_2^- = -f_1^+ - t$.

## N-Port Adaptors

For $N$ elements connected at a junction:

### N-Port Parallel (force waves)
Junction force and outgoing waves:
$$
f_J \;=\; \frac{2 \sum_{i=1}^{N} \Gamma_i\, f_i^+}{\sum_{i=1}^{N} \Gamma_i},
\qquad
f_i^- \;=\; f_J - f_i^+.
$$

When all impedances are equal ($\Gamma_i = \Gamma$ for all $i$):
$$
f_J \;=\; \frac{2}{N} \sum_{i=1}^{N} f_i^+
$$
— multiply-free when $N$ is a power of 2.

### N-Port Series (velocity waves)
Junction velocity:
$$
v_J \;=\; \frac{2 \sum_{i=1}^{N} R_i\, v_i^+}{\sum_{i=1}^{N} R_i},
\qquad
v_i^- \;=\; v_J - v_i^+.
$$

## Compatible Port Connections

When connecting a WDF element to adaptor port $i$:
- Signal $f^-$ leaving the element becomes $f_i^+$ at the adaptor port
- Signal $f_i^-$ leaving the adaptor port becomes $f^+$ entering the element
- Both sides must use the same port impedance $R_i$ (arrows align in the wave flow diagram)

## Dependent Port and Reflection-Free Port

Two distinct devices, often confused:

- **Dependent port** — the junction coefficients $\alpha_i = 2\Gamma_i/\sum_j\Gamma_j$
  (parallel) or $\beta_i = 2R_i/\sum_j R_j$ (series) sum to 2, so one of them
  follows from the others and its multiply can be eliminated.
- **Reflection-free port** — choose port $i$'s impedance so its own reflection
  coefficient is zero (no instantaneous path from $f_i^+$ to $f_i^-$):
$$
\text{parallel: } R_i = \frac{1}{\sum_{j\neq i}\Gamma_j},
\qquad
\text{series: } R_i = \sum_{j\neq i} R_j .
$$

Joining two adaptors at a reflection-free port avoids a delay-free loop, so
adaptors chain into a (binary) connection tree with every reflection-free port
facing the root. The root element must then accept an imposed port impedance -
see [[wdf-arbitrary-port-adaptation]] for the same idea at R-type junctions.

## Relation to DWG Scattering Junctions

WDF adaptors and DWG scattering junctions compute the same scattering.
The difference:
- WDF wave variables have bilinear-transform-compressed spectra
- DWG signals have bandlimited (unwarped) spectra
- Both use the same reflection coefficient formula

## Related Concepts
- [[wave-digital-filters]] — the framework these adaptors serve
- [[wdf-elements]] — the elements being connected
- [[scattering-junctions]] — DWG equivalent of WDF adaptors
- [[wdf-r-type-adaptors]] — R-type (non-series/parallel) adaptors via MNA
- [[wdf-arbitrary-port-adaptation]] — general port adaptation formula
- [[wdf-code-generation]] — the 3-port series adaptor specialised for superscalar CPUs

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Adaptors for Wave Digital Elements](https://ccrma.stanford.edu/~jos/pasp/Adaptors_Wave_Digital_Elements.html), [Two-Port Parallel Adaptor for Force Waves](https://ccrma.stanford.edu/~jos/pasp/Two_Port_Parallel_Adaptor_Force.html), [Two-Port Series Adaptor for Force Waves](https://ccrma.stanford.edu/~jos/pasp/Two_Port_Series_Adaptor_Force.html), [General Parallel Adaptor for Force Waves](https://ccrma.stanford.edu/~jos/pasp/General_Parallel_Adaptor_Force.html), [Reflection Free Port](https://ccrma.stanford.edu/~jos/pasp/Reflection_Free_Port.html), [Compatible Port Connections](https://ccrma.stanford.edu/~jos/pasp/Compatible_Port_Connections.html)

## References
[^1]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010, Appendix F, "Adaptors for Wave Digital Elements"; online at <https://ccrma.stanford.edu/~jos/pasp/>.
[^2]: Fettweis, A. (1986). "Wave Digital Filters: Theory and Practice." Proc. IEEE 74(2).

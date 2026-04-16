---
title: WDF Adaptors
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [waveguide, scattering, dsp, impedance, physical-modeling]
sources:
  - /w/pasp/adaptors.tex
  - /l/l420/WaveDigitalFiltersIntro/wdfi-content.tex
---

# WDF Adaptors

An adaptor is a memoryless N-port interface that interconnects wave digital
elements by implementing scattering appropriate for the physical connection
type (parallel or series). It computes exactly the same as a scattering
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

The one-multiply form is most efficient in custom VLSI.
The Kelly-Lochbaum form may be faster in parallel hardware.

## Two-Port Series Adaptor

Series connection: common velocity, forces sum to zero.

Same reflection coefficient formula; scattering relations differ by sign:
$$
\begin{aligned}
f_1^- &= -\rho\, f_1^+ + (1+\rho)\, f_2^+\\
f_2^- &= (1-\rho)\, f_1^+ + \rho\, f_2^+
\end{aligned}
$$

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
v_J \;=\; \frac{2 \sum_{i=1}^{N} R_i\, v_i^+}{\sum_{i=1}^{N} R_i}.
$$

## Compatible Port Connections

When connecting a WDF element to adaptor port i:
- Signal f^- leaving the element becomes f_i^+ at the adaptor port
- Signal f_i^- leaving the adaptor port becomes f^+ entering the element
- Arrows must align in the wave flow diagram

This "compatible connection" ensures physical consistency.

## The Dependent Port

In an $N$-port adaptor, one port can be designated **dependent** — its
port impedance is computed from the others to eliminate one multiply:
$$
R_{\text{dep}} \;=\; \text{function of the other } R_i.
$$

This makes the adaptor's scattering matrix have one fewer independent
coefficient. The dependent port must connect to the root of the
WDF tree (or to an element that can tolerate an imposed $R_0$).

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

## References
[^1]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford, §Adaptors.
[^2]: Fettweis, A. (1986). "Wave Digital Filters: Theory and Practice." Proc. IEEE 74(2).

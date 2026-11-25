---
title: WDF Elements
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [waveguide, scattering, dsp, impedance, physical-modeling, nonlinear]
sources:
  - /l/l420/WaveDigitalFiltersIntro/wdfi-content.tex
  - /l/l420/WaveDigitalFilters/WDFIntro.tex
  - /l/dttd/WDF
  - raw/papers/werner-dissertation-2016.txt
  - https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Elements.html
---

# WDF Elements

Each physical element is digitized independently via the bilinear transform,
producing a reflectance function.[^1][^2] By choosing the port impedance $R_0$ to cancel
the element's instantaneous reflection, the delay-free path is eliminated.
Here $c = 2/T$ is the bilinear-transform constant.

## One-Port Reactive Elements

### Mass (Inductor, $L = m$)
- Impedance: $R_m(s) = ms$
- Reflectance: $\rho_m(s) = \dfrac{ms - R_0}{ms + R_0}$ — first-order allpass
- Choose $R_0 = mc \;\Rightarrow\; \rho_m(z) = -z^{-1}$ (pure inverting delay)
- State: one sample of memory

### Spring (Capacitor, $C = 1/k$)
- Impedance: $R_k(s) = k/s$
- Reflectance: $\rho_k(s) = \dfrac{k/s - R_0}{k/s + R_0}$ — first-order allpass
- Choose $R_0 = k/c \;\Rightarrow\; \rho_k(z) = +z^{-1}$ (pure non-inverting delay)
- State: one sample of memory

### Dashpot (Resistor, $R = \mu$)
- Impedance: $R_\mu(s) = \mu$ (real constant)
- Reflectance: $\rho_\mu = \dfrac{\mu - R_0}{\mu + R_0}$ — real constant
- Choose $R_0 = \mu \;\Rightarrow\; \rho_\mu = 0$ (perfect absorption, no reflection)
- Stateless (memoryless)

## Summary Table

| Element | Analog | $R(s)$ | $R_0$ choice | $\rho(z)$ | Memory |
|---------|--------|--------|--------------|-----------|--------|
| Mass $m$    | Inductor $L=m$   | $ms$  | $mc$  | $-z^{-1}$ | 1 delay |
| Spring $k$  | Capacitor $C=1/k$ | $k/s$ | $k/c$ | $+z^{-1}$ | 1 delay |
| Dashpot $\mu$ | Resistor $R=\mu$ | $\mu$ | $\mu$ | $0$ | none |

## Two-Port Elements

### Transformer (turns ratio $N:1$)
- Scales impedance by $N^2$
- Used for mechanical advantage, gear ratios

### Gyrator (gyration resistance $r$)
- Swaps force and velocity (with sign): $F_2 = r V_1,\; F_1 = -r V_2$
- Dualizes whatever is behind it: mass $\leftrightarrow$ spring, series $\leftrightarrow$ parallel
- In wave variables with port impedances matched to $r$: a crossed pair of wires with one sign inversion

## Nonlinear Elements

### Diode, Transistor, etc.
- Described by a nonlinear $v$-$i$ (or $f$-$v$) characteristic
- In WDF: nonlinear element at the root of the connection tree
- Reflected wave computed by solving $f^- = g(f^+)$ where $g$ encodes
  the nonlinear characteristic and the port impedance
- Only one nonlinear element per tree can be solved explicitly
  (multiple nonlinearities require iterative methods or the K-method -
  see [[wdf-multiple-nonlinearities]])

### The K-Method (Borin et al., 2000)
- Pre-solve the nonlinear scattering junction as a lookup table
- Maps incoming wave to outgoing wave for a specific nonlinear element
- Applicable to WDFs and DWG nonlinear junctions alike

### Multiple Nonlinearities
- Werner et al. (2015-)[^3]: grouped nonlinearities, multi-port formulation
- Resolve delay-free loops via iterative Newton-Raphson or
  explicit approximation methods
- Active research area: neural-network junction solvers, Lipschitz-bounded networks,
  explicit CPWL models ([[wdf-applications]])

## Energy and Passivity

- Reactive elements (mass, spring) are allpass → energy conserving
- Dissipative elements (dashpot) absorb energy → passive
- Combined system is passive: total energy can only decrease or stay constant
- This guarantees **stability** of any WDF tree built from passive elements

## Related Concepts
- [[wave-digital-filters]] — the framework
- [[wdf-adaptors]] — connecting elements together
- [[wdf-applications]] — where these elements are used
- [[scattering-junctions]] — the same reflectance formula in DWGs

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Wave Digital Elements](https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Elements.html), [Reflectances of Elementary Impedances](https://ccrma.stanford.edu/~jos/pasp/Reflectances_Elementary_Impedances.html), [Choosing Impedance to Simplify Element Reflectance](https://ccrma.stanford.edu/~jos/pasp/Choosing_Impedance_Simplify_Element.html), [Waveguide Transformers and Gyrators](https://ccrma.stanford.edu/~jos/pasp/Waveguide_Transformers_Gyrators.html), [Impedance](https://ccrma.stanford.edu/~jos/pasp/Impedance.html)

## References
[^1]: Smith, J.O. III. MUS420 Lectures on Wave Digital Filters.
[^2]: Fettweis, A. (1986). "Wave Digital Filters." Proc. IEEE 74(2).
[^3]: Werner, K.J. et al. (2015). "Resolving Wave Digital Filters with Multiple/Multiport Nonlinearities." DAFx.

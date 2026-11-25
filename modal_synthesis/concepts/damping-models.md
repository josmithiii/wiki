---
title: Damping Models
created: 2026-04-10
updated: 2026-11-25
type: concept
tags: [damping, modal, vibration, physical-modeling, dsp, acoustics]
sources:
  - https://ccrma.stanford.edu/~jos/pasp/Frequency_Dependent_Damping.html
---

# Damping Models

Damping governs how quickly each mode decays. Choosing the right model affects
both physical accuracy and synthesis cost.

## Viscous Damping (Rayleigh / Proportional)

The standard linear model[^2]. Damping force proportional to velocity.

- Equation of motion: $m\ddot{x} + c\dot{x} + kx = f(t)$
- Loss factor $\eta$ relates to damping ratio: $\eta = 2\zeta$
- In modal coordinates: each mode gets independent decay rate $\sigma_n$
- $\sigma_n = \zeta_n \omega_n$ (rad/s)
- Rayleigh damping: $C = \alpha M + \beta K$ — makes $\sigma_n = \alpha/2 + \beta\omega_n^2/2$
- Advantage: diagonal in modal basis; each mode decays independently
- DSP realization: complex pole pair at $s = -\sigma_n \pm j\omega_{d,n}$
  where $\omega_{d,n} = \sqrt{\omega_n^2 - \sigma_n^2}$ (damped natural frequency)

## Thermoelastic Damping

Loss mechanism from heat flow driven by mechanical strain - important in thin metal bars and plates at audio frequencies.

- Caused by thermoelastic coupling: compression heats, rarefaction cools
- Peak loss at thermal relaxation frequency: $f_{\text{peak}} = 1/(2\pi\tau) = \pi\kappa / (2 \rho c_p d^2)$
  (Zener, flexural vibration; $\kappa$ = thermal conductivity, $c_p$ = specific heat, $d$ = thickness)
- Zener model gives frequency-dependent loss factor:
$$\eta_{\text{TE}}(\omega) \;=\; \Delta_E\, \frac{\omega\tau}{1 + (\omega\tau)^2}$$
  where $\tau = \rho c_p d^2/(\pi^2\kappa)$ = thermal relaxation time, $\Delta_E$ = relaxation strength
- Significant for thin metal plates, MEMS resonators, metal (vibraphone, glockenspiel) bars
- Practically: broadens the loss curve vs. viscous - modes near $f_{\text{peak}}$ decay faster

## Frequency-Dependent Damping

Real materials show damping that varies with frequency[^1]. Cannot be captured by
simple viscous model.

### Structural Damping (Hysteretic)
- Loss factor $\eta$ is constant with frequency (or weakly dependent)
- Stress-strain phase lag: $\sigma = E(1 + j\eta)\epsilon$
- For small $\eta$, $s$-domain poles at $s_n \approx \omega_n(-\eta/2 \pm j)$, i.e. $\sigma_n \approx \eta\,\omega_n/2$ (constant $Q = 1/\eta$)
- Common for rubber, polymers; also used as default in FEM software

### Power-Law Damping
- $\eta(\omega) = \eta_0 (\omega/\omega_0)^\alpha$, $\alpha \in [-1, 1]$
- Metals: $\alpha \approx 0$ (nearly constant loss factor above 100 Hz)
- Wood: $\alpha \approx +0.1$–$+0.3$ (increasing with frequency)
- Rubber: $\alpha \approx -0.5$ (decreasing with frequency)

### Measured / Tabulated Damping
- For accuracy: fit measured $Q_n$ values per mode, use per-mode $\sigma_n$
- No analytical model required -- each resonator pole set independently
- Standard in modal analysis workflows; see [[modal-analysis-measurement]]

## Practical Implications for Synthesis

| Model | DSP Cost | Physical Accuracy | Use Case |
|---|---|---|---|
| Uniform viscous | Lowest | Low | quick prototype |
| Rayleigh ($\alpha$, $\beta$) | Low | Medium | general metals/wood |
| Per-mode fitted | Low | High | measured instruments |
| Thermoelastic | Medium | High (metals) | metal bars, plates |
| Frequency-dependent | Medium | High | polymers, composites |

- Q-factor and decay time: $Q_n = \omega_n/(2\sigma_n)$, so $T_{60,n} = 6.91 / \sigma_n = 13.8\, Q_n / \omega_n \approx 2.2\, Q_n / f_n$
- High Q (low damping): bells, singing bowls, steel bars
- Low Q (high damping): rubber mallets, felt, foam-covered objects
- See [[material-properties-and-modes]] for per-material damping values
- Damping affects resonator pole placement; see [[resonator-bank-implementation]]
- Per-band damping regressed from a corpus of room IRs, anchored to $T_{60}$: see [[corpus-driven-parametric-modal-reverb]]

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Frequency-Dependent Damping](https://ccrma.stanford.edu/~jos/pasp/Frequency_Dependent_Damping.html), [Well Posed PDEs for Modeling Damped Strings](https://ccrma.stanford.edu/~jos/pasp/Well_Posed_PDEs_Modeling.html)
- [[jos_books/entities/filters-book|Filters]]: [Quality Factor (Q)](https://ccrma.stanford.edu/~jos/filters/Quality_Factor_Q.html), [Decay Time is Q Periods](https://ccrma.stanford.edu/~jos/filters/Decay_Time_Q_Periods.html), [Relating Pole Radius to Bandwidth](https://ccrma.stanford.edu/~jos/filters/Relating_Pole_Radius_Bandwidth.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Audio Decay Time (T60)](https://ccrma.stanford.edu/~jos/mdft/Audio_Decay_Time_T60.html)

## References

[^1]: JOS, "Frequency-Dependent Damping," in *PASP*: https://ccrma.stanford.edu/~jos/pasp/Frequency_Dependent_Damping.html
[^2]: Woodhouse, J. (1998). "Linear damping models for structural vibration." JSV 215(3).

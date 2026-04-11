---
title: Damping Models
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [damping, modal, vibration, physical-modeling, dsp, acoustics]
sources:
  - https://ccrma.stanford.edu/~jos/pasp/Damping.html
  - https://hal.science/hal-00830400/document
---

# Damping Models

Damping governs how quickly each mode decays. Choosing the right model affects
both physical accuracy and synthesis cost.

## Viscous Damping (Rayleigh / Proportional)

The standard linear model. Damping force proportional to velocity.

- Equation of motion: m*x'' + c*x' + k*x = f(t)
- Loss factor (eta) relates to damping ratio: eta = 2*zeta
- In modal coordinates: each mode gets independent decay rate sigma_n
- sigma_n = zeta_n * omega_n (rad/s)
- Rayleigh damping: C = alpha*M + beta*K -- makes sigma_n = alpha/2 + beta*omega_n^2/2
- Advantage: diagonal in modal basis; each mode decays independently
- DSP realization: complex pole pair at s = -sigma_n +/- j*omega_d,n
  where omega_d,n = sqrt(omega_n^2 - sigma_n^2) (damped natural frequency)

## Thermoelastic Damping

Loss mechanism from heat flow driven by mechanical strain -- dominant in metals at audio frequencies.

- Caused by thermoelastic coupling: compression heats, rarefaction cools
- Peak loss at thermal relaxation frequency: f_peak = kappa / (2*pi*cp*rho*d^2)
  where kappa = thermal conductivity, d = plate thickness
- Zener model gives frequency-dependent loss factor:
  eta_TE(omega) = Delta_E * (omega*tau) / (1 + (omega*tau)^2)
  where tau = thermal relaxation time, Delta_E = thermoelastic coupling coefficient
- Significant for thin metal plates, MEMS resonators, xylophone bars
- Practically: broadens the loss curve vs. viscous -- modes near f_peak decay faster

## Frequency-Dependent Damping

Real materials show damping that varies with frequency. Cannot be captured by
simple viscous model.

### Structural Damping (Hysteretic)
- Loss factor eta is constant with frequency (or weakly dependent)
- Stress-strain phase lag: sigma = E*(1 + j*eta)*epsilon
- Results in s-domain poles: s_n = omega_n * (-eta/2 +/- j*sqrt(1 - eta^2/4))
- Common for rubber, polymers; also used as default in FEM software

### Power-Law Damping
- eta(omega) = eta_0 * (omega/omega_0)^alpha, alpha in [-1, 1]
- Metals: alpha ~ 0 (nearly constant loss factor above 100 Hz)
- Wood: alpha ~ +0.1..+0.3 (increasing with frequency)
- Rubber: alpha ~ -0.5 (decreasing with frequency)

### Measured / Tabulated Damping
- For accuracy: fit measured Q_n values per mode, use per-mode sigma_n
- No analytical model required -- each resonator pole set independently
- Standard in modal analysis workflows; see [[modal-analysis-measurement]]

## Practical Implications for Synthesis

| Model | DSP Cost | Physical Accuracy | Use Case |
|---|---|---|---|
| Uniform viscous | Lowest | Low | quick prototype |
| Rayleigh (alpha+beta) | Low | Medium | general metals/wood |
| Per-mode fitted | Low | High | measured instruments |
| Thermoelastic | Medium | High (metals) | xylophone, plates |
| Frequency-dependent | Medium | High | polymers, composites |

- Q-factor and decay time: T60_n = 6.91 / sigma_n = 6.91 * Q_n / omega_n
- High Q (low damping): bells, singing bowls, steel bars
- Low Q (high damping): rubber mallets, felt, foam-covered objects
- See [[material-properties-and-modes]] for per-material damping values
- Damping affects resonator pole placement; see [[resonator-bank-implementation]]

## References

[^1]: https://ccrma.stanford.edu/~jos/pasp/Frequency_Dependent_Damping.html
[^2]: Woodhouse, J. (1998). "Linear damping models for structural vibration." JSV 215(3).
[^3]: https://hal.science/hal-00830400/document

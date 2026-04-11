---
title: Material Properties and Modes
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [material, vibration, acoustics, modal, physics-modeling]
sources:
  - /w/pasp/damping.tex
  - https://ccrma.stanford.edu/~jos/pasp/Frequency_Dependent_Damping.html
---

# Material Properties and Modes

## Overview
A vibrating object's modal parameters (frequencies, damping, mode shapes) depend on
its geometry AND its material properties. Understanding this link enables synthesis
of "any material" from first principles or perceptual parameterization.

## Key Material Properties

| Property | Symbol | Units | Effect on Modes |
|----------|--------|-------|-----------------|
| Young's modulus | E | Pa | Higher E → higher f_k (stiffer) |
| Poisson's ratio | nu | dimensionless | Affects mode shapes for 2D/3D |
| Density | rho | kg/m^3 | Higher rho → lower f_k |
| Loss factor (damping) | eta | dimensionless | Higher eta → faster decay (d_k) |

## Frequency Scaling Laws
For a given geometry scaled by factor s (all dimensions × s):
- Natural frequencies: f_k ∝ 1/s  (larger object → lower pitch)
- This is why large bells are deeper than small bells

Frequency vs. material:
  f_k ∝ sqrt(E / rho) / (characteristic_length)
For a bar: f_k = k^2 * pi/(2L^2) * sqrt(E*I / (rho*A))

Practical implication: two objects of same shape but different materials
have all frequencies scaled by sqrt(E2/rho2) / sqrt(E1/rho1).

## Damping and Material
Damping d_k is harder to predict from first principles than frequency.
Sources of damping in a vibrating object:
1. **Internal (material) damping**: viscoelastic losses within material
   - Metals: very low (Q ~ 1000-10000)
   - Wood: moderate (Q ~ 50-200)
   - Rubber: high (Q ~ 5-20)
2. **Boundary damping**: energy lost at supports/contacts
3. **Acoustic radiation damping**: energy radiated as sound (usually small)
4. **Thermoelastic damping**: conversion of strain to heat (important for MEMS)

## Rayleigh Damping Model
Simple model for FEM: C = alpha*M + beta*K
- alpha: mass-proportional damping (dominates at low freq)
- beta: stiffness-proportional damping (dominates at high freq)
- d_k = alpha/2 + beta*omega_k^2/2

This is a good approximation for many materials; real damping often
requires measuring each mode's Q separately.

## Typical Material Parameters (for synthesis)
| Material | E (GPa) | rho (kg/m^3) | eta (avg) | Perceptual character |
|----------|---------|--------------|-----------|---------------------|
| Steel | 200 | 7800 | 0.001 | Bright, long ring |
| Aluminum | 70 | 2700 | 0.002 | Bright, medium ring |
| Wood (spruce) | 10 | 400 | 0.01-0.03 | Warm, moderate ring |
| Glass | 70 | 2500 | 0.001 | Very bright, long ring |
| Concrete | 30 | 2400 | 0.05 | Dull, short ring |
| Rubber | 0.001-0.1 | 1100 | 0.1-0.5 | Thud, very short ring |

## Perceptual Material Attributes
Researchers (Klatzky, Pai, McAdams) have identified perceptual dimensions:
1. **Hardness**: perceived from spectral centroid + attack steepness
   (harder = higher centroid, faster attack)
2. **Size**: perceived from fundamental frequency (lower = larger)
3. **Damping**: perceived from T60 / spectral envelope decay rate
4. **Roughness**: from surface micro-structure (affects friction / scrape sounds)

## Morphing Between Materials
For synthesis, can interpolate material parameters:
  f_k(alpha) = f_k^(A) * (1-alpha) + f_k^(B) * alpha  [linear blend of freq]
  d_k(alpha) = d_k^(A) * (1-alpha) + d_k^(B) * alpha  [linear blend of damping]

Or more physically: interpolate E and rho, recompute f_k.
This gives intuitive "material slider" for a sound designer.

## Related Concepts
- [[mode-shapes-and-eigenvalues]] — how E and rho enter the eigenvalue problem
- [[impact-synthesis]] — how material properties affect contact force profile
- [[modal-synthesis-overview]] — use of material-derived mode parameters
- [[fem-bem-for-modal-synthesis]] — FEM requires E, nu, rho as inputs

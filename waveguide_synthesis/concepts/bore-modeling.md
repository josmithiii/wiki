---
title: Bore Modeling
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [wind, waveguide, physical-modeling, acoustics, impedance, dsp]
sources:
  - /w/pasp/reeds.tex
  - /w/pasp/idealtubesummary.tex
  - /w/pasp/cones.tex
  - /w/pasp/brasses.tex
  - /w/pasp/flute.tex
---

# Bore Modeling

Acoustic tubes (clarinet, trumpet, flute, vocal tract) propagate pressure
and velocity waves. Digital waveguides model these as bidirectional delay
lines with scattering at diameter changes, tone holes, and bell.

## Cylindrical Tubes

Plane-wave propagation in a uniform cylinder:
- Wave impedance: R = rho * c / A (A = cross-sectional area)
- Pressure waves: p^+(n) = R * u^+(n),  p^-(n) = -R * u^-(n)
- Volume velocity U = v * A is conserved at junctions

### Piecewise Cylindrical (Kelly-Lochbaum) Model
- Approximate bore as concatenated cylindrical sections
- At each area change: scattering junction with k = (R_2 - R_1)/(R_2 + R_1)
- Accurate when wavelength >> tube diameter (low-frequency regime)
- Above lambda ~ sqrt(A): higher-order modes appear (Bessel functions)

## Conical Tubes

Cones propagate spherical waves (not plane waves):
- Wave variable: p_x = pressure * radial distance x
- Satisfies the same 1D wave equation as a cylinder
- Cylindrical tube = limiting case (cone apex at infinity)
- Exact traveling-wave solution exists only for cones (Putland)

### Bore Approximation Methods
- **Piecewise conical sections** with scattering junctions (Causse et al.)
- **Sturm-Liouville formulation** (Berners): bore curvature as potential
- **BEM** (Henwood): needed when multi-mode excitation occurs

## Bell Radiation

The bell acts as a frequency-dependent crossover:
- Low frequencies: mostly reflected back into bore (closed-end behavior)
- High frequencies: pass through and radiate (open-end behavior)
- Crossover frequency: wavelength ~ bell diameter (~1500 Hz for clarinet)
- Bell flare lowers crossover by gradually reducing impedance (transformer)
- Far-field pattern ∝ 2D Fourier transform of exit aperture

## Tone Holes

Open and closed tone holes create local impedance perturbations:
- Open hole: low impedance shunt to outside air → reflection + radiation
- Closed hole: small mass loading → slight detuning
- Modeled as T-junction scattering or as shunt impedance in the waveguide

## Related Concepts
- [[waveguide-overview]] — bidirectional delay lines
- [[scattering-junctions]] — area-change reflections in the bore
- [[reed-and-bow-models]] — nonlinear excitation at the mouthpiece
- [[artificial-reverberation]] — tube networks generalize to reverb

## References
[^1]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.
[^2]: Scavone, G. (1997). "An Acoustic Analysis of Single-Reed Woodwind Instruments..." PhD thesis, Stanford/CCRMA.

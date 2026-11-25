---
title: Bore Modeling
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [wind, waveguide, physical-modeling, acoustics, impedance, dsp]
sources:
  - /w/pasp/reeds.tex
  - /w/pasp/idealtubesummary.tex
  - /w/pasp/cones.tex
  - /w/pasp/brasses.tex
  - /w/pasp/flute.tex
  - /w/pasp/tonehole.tex
  - https://ccrma.stanford.edu/~jos/pasp/Ideal_Acoustic_Tube.html
  - https://ccrma.stanford.edu/~jos/pasp/Woodwinds.html
---

# Bore Modeling

Acoustic tubes (clarinet, trumpet, flute, vocal tract) propagate pressure
and velocity waves. Digital waveguides model these as bidirectional delay
lines with scattering at diameter changes, tone holes, and bell.[^1]

## Cylindrical Tubes

Plane-wave propagation in a uniform cylinder:
- Wave impedance: $R = \rho c / A$ ($A$ = cross-sectional area)
- Pressure waves: $p^+(n) = R\, u^+(n)$,  $p^-(n) = -R\, u^-(n)$
- Volume velocity $u = v A$ (particle velocity times area) is conserved at junctions

### Piecewise Cylindrical (Kelly-Lochbaum) Model
- Approximate bore as concatenated cylindrical sections
- At each area change: scattering junction with $k = (R_2 - R_1)/(R_2 + R_1)$
- Accurate when wavelength $\gg$ tube diameter (low-frequency regime)
- Once the wavelength shrinks to the order of the diameter, transverse
  (higher-order, Bessel-function) modes propagate and the 1D model breaks down
- The same structure is the Kelly-Lochbaum vocal tract: [[waveguide-vocal-models]]

## Conical Tubes

Cones propagate spherical waves (not plane waves):
- Wave variable: $x\,p(t,x)$, pressure times distance $x$ from the cone apex
- It satisfies the same 1D wave equation as pressure in a cylinder
- Cylindrical tube = limiting case (cone apex at infinity)
- The cone is essentially the most general bore with exact traveling waves (Putland)

### Bore Approximation Methods
- **Piecewise conical sections** with scattering junctions (Causse et al.)
- **Sturm-Liouville formulation** (Berners): bore curvature as potential
- **BEM** (Henwood): needed when multi-mode excitation occurs

## Bell Radiation

The bell acts as a frequency-dependent crossover:
- Low frequencies: mostly reflected back into the bore (inverted, as at an ideal open end)
- High frequencies: pass through and radiate in an increasingly directional beam
- Crossover frequency: wavelength ~ bell diameter (~1500 Hz for clarinet)
- Bell flare lowers the crossover by gradually reducing wave impedance (like a transformer)
- Far-field pattern ∝ 2D Fourier transform of exit aperture

## Tone Holes

Open and closed tone holes create local impedance perturbations:
- Open hole: shunt inertance (air mass in the hole) to outside air → reflection + radiation
- Closed hole: shunt compliance (small added volume) → slight detuning
- Modeled as a two-port loaded junction, or as a three-port junction with a short
  side branch (Scavone[^2]); see [[wdf-applications]] for the wave digital tonehole

## Related Concepts
- [[waveguide-overview]] — bidirectional delay lines
- [[scattering-junctions]] — area-change reflections in the bore
- [[reed-and-bow-models]] — nonlinear excitation at the mouthpiece
- [[artificial-reverberation]] — tube networks generalize to reverb

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Ideal Acoustic Tube](https://ccrma.stanford.edu/~jos/pasp/Ideal_Acoustic_Tube.html), [Conical Acoustic Tubes](https://ccrma.stanford.edu/~jos/pasp/Conical_Acoustic_Tubes.html), [Tonehole Modeling](https://ccrma.stanford.edu/~jos/pasp/Tonehole_Modeling.html), [Bell Models](https://ccrma.stanford.edu/~jos/pasp/Bell_Models.html), [Single-Reed Instruments](https://ccrma.stanford.edu/~jos/pasp/Single_Reed_Instruments.html)

## References
[^1]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010; online at <https://ccrma.stanford.edu/~jos/pasp/>.
[^2]: Scavone, G. (1997). "An Acoustic Analysis of Single-Reed Woodwind Instruments..." PhD thesis, Stanford/CCRMA.

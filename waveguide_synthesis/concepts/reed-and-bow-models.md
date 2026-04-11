---
title: Reed and Bow Models
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [reed, nonlinear, waveguide, wind, string, physical-modeling]
sources:
  - /w/pasp/reeds.tex
  - /w/pasp/reedboremech.tex
  - /w/pasp/brasses.tex
  - /w/pasp/flute.tex
---

# Reed and Bow Models

Sustained-tone instruments require a nonlinear excitation mechanism that
converts steady energy (breath, bow) into oscillation. In digital waveguide
models, these appear as nonlinear scattering elements at one end of the bore
or string.

## Single Reed (Clarinet/Saxophone)

### Physical Mechanism
- Player blows with mouth pressure P_m into mouthpiece
- Reed deflects under pressure difference P_d = P_m - P_b (bore pressure)
- Flow U through reed aperture depends nonlinearly on P_d
- At small P_d: reed opens, flow increases (positive resistance)
- At large P_d: reed closes, flow drops to zero (negative resistance region)
- Oscillation sustained by energy injection in the negative-resistance regime

### Digital Waveguide Implementation
- Bore = bidirectional delay line carrying pressure waves
- Reed = nonlinear reflection coefficient at mouthpiece end
- Incoming pressure wave p^+ arrives at reed
- Outgoing pressure p^- = f_reed(p^+, P_m, embouchure)
- Reed function is a memoryless nonlinear map (mass neglected)
- Embouchure controls: aperture width, damping, blowing pressure
- Implemented as lookup table or polynomial approximation

### Single-Period Oscillation Cycle
1. High-pressure front travels down bore from reed
2. Reflects with sign inversion at open bell end
3. Returns to reed as negative pressure
4. Reflects without sign inversion at closed mouthpiece end
5. Four bore traversals per period (clarinet: quarter-wave resonator)

## Lip Reed (Brass)

- Lips modeled as mass-spring oscillator (1 or 2 masses)
- Bernoulli flow between lips: p_m = p_l + (1/2) * rho * u_l^2
- Jet in mouthpiece dissipates kinetically (no pressure recovery)
- Cook's simplified model: second-order resonator, output squared and clipped
- More sophisticated: Rodet-Vergez 1- and 2-mass models

## Air Reed (Flute/Recorder)

- No mechanical reed; oscillation from jet-edge interaction
- Second feedback loop models jet propagation delay (mouth to edge)
- Nonlinearity: soft clipper y(x) = x - x^3 (jet saturation)
- Higher noise component than reed instruments (scaled by DC flow)
- Cook's SlideFlute (STK): simplified jet + bore + noise model

## Bowed String

- Bow-string interaction: nonlinear friction at contact point
- Helmholtz motion: stick-slip cycle creates sawtooth-like velocity wave
- In waveguide terms: bow = nonlinear scattering junction between
  two string segments (nut-side and bridge-side)
- Incoming waves from both sides determine stick/slip state
- Bow velocity and force are control parameters
- See [[friction-synthesis]] in the modal_synthesis wiki for friction physics

## Common Design Pattern

All sustained-excitation waveguide models share this structure:
1. **Linear resonator**: delay-line loop (bore or string) with loss filters
2. **Nonlinear element**: reed/lip/bow function at one junction
3. **Control inputs**: pressure, force, velocity, embouchure parameters
4. **Feedback**: reflected wave from resonator drives the nonlinear element

The nonlinear element typically sees only the incoming wave amplitude
and produces an outgoing wave — a memoryless or low-order dynamic map.

## Related Concepts
- [[waveguide-overview]] — the delay-line resonators these excite
- [[bore-modeling]] — the cylindrical/conical tube being driven
- [[scattering-junctions]] — the junction framework for excitation coupling
- [[string-modeling]] — bowed-string waveguide models

## References
[^1]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.
[^2]: Cook, P. (1992). "A Meta-Wind-Instrument Physical Model." PhD thesis, Stanford/CCRMA.
[^3]: McIntyre, M.E., Schumacher, R.T., & Woodhouse, J. (1983). "On the oscillations of musical instruments." JASA 74(5).

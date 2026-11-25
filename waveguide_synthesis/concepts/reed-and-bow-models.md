---
title: Reed and Bow Models
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [reed, nonlinear, waveguide, wind, string, physical-modeling]
sources:
  - /w/pasp/reeds.tex
  - /w/pasp/reedboremech.tex
  - /w/pasp/brasses.tex
  - /w/pasp/flute.tex
  - https://ccrma.stanford.edu/~jos/pasp/Woodwinds.html
  - https://ccrma.stanford.edu/~jos/pasp/Bowed_Strings.html
  - https://ccrma.stanford.edu/~jos/pasp/Brasses.html
---

# Reed and Bow Models

Sustained-tone instruments require a nonlinear excitation mechanism that
converts steady energy (breath, bow) into oscillation. In digital waveguide
models, these appear as nonlinear scattering elements at one end of the bore
or along the string.[^1][^3]

## Single Reed (Clarinet/Saxophone)

### Physical Mechanism
- Player blows with mouth pressure $P_m$ into mouthpiece
- Reed deflects under pressure difference $P_d = P_m - P_b$ (bore pressure)
- Flow $U$ through the reed aperture depends nonlinearly on $P_d$
- At small $P_d$: flow increases with pressure drop (positive resistance)
- At larger $P_d$: the reed is pushed closed and flow falls to zero (negative-resistance region)
- Oscillation sustained by energy injection in the negative-resistance regime

### Digital Waveguide Implementation
- Bore = bidirectional delay line carrying pressure waves
- Reed = nonlinear reflection coefficient at mouthpiece end
- Incoming pressure wave $p^+$ arrives at reed
- Outgoing pressure $p^- = f_{\text{reed}}(p^+, P_m, \text{embouchure})$
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
- Bernoulli flow between lips: $p_m = p_l + \tfrac{1}{2}\rho\, u_l^2$
- Jet in mouthpiece dissipates kinetically (no pressure recovery)
- Cook's simplified model[^2]: second-order resonator, output squared and hard-clipped
- More sophisticated: Rodet-Vergez 1- and 2-mass models

## Air Reed (Flute/Recorder)

- No mechanical reed; oscillation from jet-edge interaction
- Second feedback loop models jet propagation delay (mouth to edge)
- Nonlinearity: soft clipper $y(x) = x - x^3$ (jet saturation)
- Higher noise component than reed instruments (scaled by DC flow)
- Cook's SlideFlute (STK): simplified jet + bore + noise model

## Bowed String

- Bow-string interaction: nonlinear friction at contact point
- Helmholtz motion: stick-slip cycle creates sawtooth-like velocity wave
- In waveguide terms: bow = nonlinear scattering junction between
  two string segments (nut-side and bridge-side)
- Incoming waves from both sides determine stick/slip state
- Bow velocity and force are control parameters
- See [[modal_synthesis/concepts/friction-synthesis|friction synthesis]] for friction physics

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
- [[bowed-string-finite-difference-models]] — the finite-difference alternative (yehu, elasto-plastic friction)

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Single-Reed Instruments](https://ccrma.stanford.edu/~jos/pasp/Single_Reed_Instruments.html), [Digital Waveguide Single-Reed Implementation](https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Single_Reed_Implementation.html), [Modeling the Lips and Mouthpiece](https://ccrma.stanford.edu/~jos/pasp/Modeling_Lips_Mouthpiece.html), [Flutes, Recorders, and Pipe Organs](https://ccrma.stanford.edu/~jos/pasp/Flutes_Recorders_Pipe_Organs.html), [The Bow-String Scattering Junction](https://ccrma.stanford.edu/~jos/pasp/Bow_String_Scattering_Junction.html), [Nonlinear Elements](https://ccrma.stanford.edu/~jos/pasp/Nonlinear_Elements.html)

## References
[^1]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010; online at <https://ccrma.stanford.edu/~jos/pasp/>.
[^2]: Cook, P. (1992). "A Meta-Wind-Instrument Physical Model." PhD thesis, Stanford/CCRMA.
[^3]: McIntyre, M.E., Schumacher, R.T., & Woodhouse, J. (1983). "On the oscillations of musical instruments." JASA 74(5).

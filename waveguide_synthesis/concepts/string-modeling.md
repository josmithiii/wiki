---
title: String Modeling
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [string, waveguide, physical-modeling, guitar, dsp, damping]
sources:
  - /w/pasp/strings.tex
  - /w/pasp/plucked.tex
  - /w/pasp/damping.tex
  - /w/pasp/stiffstring.tex
  - /w/pasp/struckstring.tex
  - /w/pasp/coupling.tex
  - /w/pasp/piano-string.tex
---

# String Modeling

The vibrating string was the first application of digital waveguide synthesis
(Karplus-Strong, 1983; Smith, 1992) and remains the most developed.

## Basic Plucked-String Model

1. Bidirectional delay line of length $N = f_s / f_0$
2. Rigid terminations → sign inversion at each end → delay-line loop
3. Initial conditions: half the pluck shape in each delay line
4. Acceleration waves: pluck = impulse at pluck point (simplest case)

**Bandlimited pluck**: sharp corners alias; require lowpass-filtered initial shape.
In practice, bandwidth of the pluck shape spans the full range of hearing.

## Karplus-Strong / Extended Karplus-Strong

- **Karplus-Strong** (1983): delay loop + averaging filter $y(n) = [y(n-N) + y(n-N-1)] / 2$
- **Extended K-S** (Jaffe & Smith, 1983): generalize to arbitrary loop filter $G(z)$
- Loop filter controls: decay rate per frequency (damping), pitch fine-tuning
- Design constraint: $|G(e^{j\omega})| \le 1$ for stability (passive loop)

## Damping

Real strings lose energy at frequency-dependent rates:
- Lumped loss filter G(z) replaces per-sample attenuation g (factor N savings)
- Linear-phase symmetric FIR: keeps approximation convex for least-squares design
- Constraint: G(1) = 1 (no DC loss — strings sustain at 0 Hz indefinitely)
- Typical: 1st-order IIR or short FIR (3-9 taps)

## Stiffness / Dispersion

Stiff strings (piano, steel guitar) have inharmonic partials:
$$f_n = n f_0 \sqrt{1 + B n^2}$$
where $B = \pi^3 E a^4 / (4 K L^2)$ is the coefficient of inharmonicity.

- Modeled by allpass filter $H_s(z)$ in the loop
- Commutes with delay → lumped at one point
- Piano: dominant effect; nylon guitar: generally inaudible
- Perceptual threshold: $B_{\text{thresh}} = \exp[2.54\log(f_0) - 24.6]$

## Struck String (Hammer-String Interaction)

Mass $m$ at velocity $v_0$ strikes string (impedance $R$):
- Contact velocity: $v(t) = v_0\, e^{-2R t/m}$
- Time constant $\tau = m/(2R)$: heavy hammer = long contact
- Energy transfers gradually (not instantaneous impulse)
- More realistic than the ideal pluck for piano synthesis

## String Coupling

### Horizontal + Vertical Polarization
- Two orthogonal transverse planes coupled at the bridge
- Coupling matrix $H(z)$: eigenvectors = eigenpolarizations
- Eigenvalues give per-mode damping and tuning
- Asymmetric bridge admittance → two-stage decay (fast onset + slow sustain)

### Coupled Strings (Piano)
- Multiple strings per key, slightly mistuned
- Bridge motion couples all strings
- Creates beating and two-stage decay (Weinreich effect)
- Efficient scattering formulation for N coupled strings at a rigid bridge

### Longitudinal Waves
- Travel ~10x faster than transverse; weakly coupled
- Important in piano (audible), Finnish kantele
- Nonlinear coupling: transverse drives longitudinal at large amplitudes

## Commuted Synthesis

If excitation and pickup are fixed, commute the body filter to the input:
- Pluck → body IR → string delay loop (instead of pluck → string → body)
- Turns body response into part of the excitation signal
- Extremely efficient: one convolution replaces a complex body model
- Standard technique for guitar, harp, harpsichord synthesis

## Related Concepts
- [[waveguide-overview]] — the delay-line foundation
- [[delay-line-techniques]] — fractional delay, loop filter design
- [[scattering-junctions]] — bridge coupling, termination modeling
- [[bore-modeling]] — analogous waveguide approach for wind instruments

## References
[^1]: Karplus, K. & Strong, A. (1983). "Digital Synthesis of Plucked-String and Drum Timbres." CMJ 7(2).
[^2]: Smith, J.O. III (1992). "Physical Modeling Using Digital Waveguides." CMJ 16(4).
[^3]: Jaffe, D. & Smith, J.O. (1983). "Extensions of the Karplus-Strong Plucked-String Algorithm." CMJ 7(2).

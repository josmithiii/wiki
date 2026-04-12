---
title: Delay-Line Techniques
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [delay-line, dsp, waveguide, realtime]
sources:
  - /w/pasp/delay-interp.tex
  - /w/pasp/delay-var.tex
  - /w/pasp/delay-lossy-prop.tex
  - /w/pasp/delay-allpass-waveguide.tex
---

# Delay-Line Techniques

Digital waveguide models require precise control of delay length, including
fractional samples for pitch accuracy and smooth time variation for effects
and physical modeling.

## Integer Delay Lines

- Implemented as circular buffers: O(1) read/write per sample
- Length $N$ sets fundamental: $f_0 = f_s / N$ (for a string loop)
- Total loop delay = $N_{\text{delay}} + N_{\text{filter}}$ (delay from loop filters counts)

## Fractional Delay Interpolation

### Linear Interpolation
$$y(n + \eta) \;=\; (1 - \eta)\, y(n) + \eta\, y(n+1), \qquad \eta \in [0,1]$$
- One-multiply form: $y(n + \eta) = y(n) + \eta\,[y(n+1) - y(n)]$
- Cost: 1 multiply, 2 adds
- Accurate at low frequencies; degrades toward Nyquist
- Best at high sample rates where audio is oversampled
- STK class: `DelayL`

### First-Order Allpass Interpolation
$$y(n) \;=\; \eta\,[x(n) - y(n-1)] + x(n-1)$$
$$H(z) \;=\; \frac{\eta + z^{-1}}{1 + \eta\, z^{-1}}$$
- Flat magnitude response (unity gain at all frequencies)
- Preferred inside feedback loops (waveguide string models)
- Same cost as linear: 1 multiply, 2 adds
- Ramping $\eta$ from 0 to 1 smoothly "grows" one sample of delay
- STK class: `DelayA`

### Higher-Order Methods
- Lagrange interpolation: polynomial fit to M+1 samples
- Thiran allpass: maximally flat group delay at DC
- Windowed-sinc: best for high-quality table lookup (not feedback loops)

## Variable Delay Lines

Used for:
- **Vibrato/tremolo**: periodic delay modulation
- **Chorus/flange/phase**: multiple modulated delays mixed
- **Pitch shifting**: delay ramping with crossfade
- **Waveguide pitch control**: vary string/bore length in real time

Key constraint: interpolation filter must be stable and smooth during
parameter changes, especially inside feedback loops.

## Lossy Propagation

Real waves lose energy during propagation. Modeled by filtering:

### Frequency-Independent Loss
Substitute $z^{-1} \to g\, z^{-1}$ in the delay, $g \in [0,1]$:
$$y(n) \;=\; g^M\, x(n - M)$$

### Frequency-Dependent Loss
Substitute $z^{-1} \to G(z)\, z^{-1}$, where $|G(e^{j\omega})| \le 1$:
$$Y(z) \;=\; G^M(z)\, z^{-M}\, X(z)$$
$G(z)$ is the per-sample loss filter (typically low-order FIR or IIR).

### Lumped Loss (Key Efficiency Trick)
By LTI commutativity, $M$ per-sample loss filters = one filter $G^M(z)$
at a single point in the loop. This reduces computation by factor $M$.
Example: $N=500$ sample loop → 500× savings by lumping.

## Dispersion Filters

Stiff strings and other media have frequency-dependent propagation speed:
- Modeled as allpass filter $H_s(z)$ in the loop (flat magnitude, shaped phase)
- Commutes with delay (LTI) → lumped at one point, like the loss filter
- Design: specify desired inharmonicity, fit allpass coefficients
- See [[string-modeling]] for piano string dispersion

## Related Concepts
- [[waveguide-overview]] — the bidirectional delay lines these techniques serve
- [[scattering-junctions]] — connecting waveguides requires delay management
- [[string-modeling]] — primary application of fractional delay + loop filters
- [[artificial-reverberation]] — delay lines as building blocks for reverb

## References
[^1]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.
[^2]: Laakso, T.I. et al. (1996). "Splitting the unit delay." IEEE SPM 13(1).

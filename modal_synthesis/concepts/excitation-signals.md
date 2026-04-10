---
title: Excitation Signals
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [modal, impulse-response, dsp, physical-modeling, modal-synthesis, impact, friction]
sources:
  - https://ccrma.stanford.edu/~jos/pasp/Excitation.html
  - https://ccrma.stanford.edu/~jos/pasp/Impulse_Response.html
---

# Excitation Signals

Excitation is the input signal convolved with (or applied to) the modal resonator bank.
The choice of excitation shapes the perceptual character of the synthesized sound.

## Impulse

The mathematical ideal: Dirac delta delta(t).

- Spectrum: flat (white) across all frequencies
- Excites all modes simultaneously with equal amplitude at t=0
- Result: pure decay — the impulse response of the resonator bank
- In practice: single non-zero sample of amplitude A at t=0
- Use for: struck/hit sounds (hammer, mallet, collision), any transient event
- Modal synthesis: apply impulse to each mode's initial conditions
  — sets x_n(0) = 0, x_n'(0) = phi_n(x_drive) * F_impulse / m_n
- Extended impulse (shaped): raised-cosine or Hann-windowed pulse
  — controls spectral bandwidth, avoids exciting modes above f_cutoff
  — softer mallet = lower f_cutoff = less high-frequency mode content

## Noise Burst

Band-limited or broadband noise, windowed to finite duration.

- Duration tau sets spectral resolution: Delta_f ~ 1/tau
- Amplitude envelope: rectangular, Gaussian, or exponential attack + decay
- Use for: rough/grainy impacts, scraping onset, stochastic excitation
- Colored noise: pre-filter to shape input spectrum
  — Pink noise (1/f) for natural-sounding excitation
  — Bandpass noise to target specific mode groups
- Burst length effect: short burst ~ impulse; long burst ~ continuous noise input
- Key advantage over impulse: controllable onset smoothness, avoids clicks
- Common in percussion synthesis: drum hit = noise burst convolved with shell modes

## Continuous Excitation

Sustained signal driving the resonator bank indefinitely.

### White/Pink Noise Drive
- Stochastic steady-state output — statistical coloring by resonator
- Use for: wind noise through structures, cavity resonance, acoustic noise
- Output spectrum = |H(omega)|^2 * S_input(omega)

### Sinusoidal / Harmonic Drive
- Single frequency f_drive or harmonic series
- When f_drive near mode omega_n: resonance buildup (transient + steady state)
- Beating when f_drive slightly off resonance: |f_drive - f_n| beats per second
- Use for: bowed strings, singing bowls, friction drums, wind-excited structures

### Bow-Force Model (friction excitation)
- Nonlinear feedback: output velocity modulates friction force
- Stick-slip cycle generates broadband excitation during slip, near-silence during stick
- Yields Helmholtz motion for string; more complex for plates
- See [[friction-synthesis]] for full treatment

### Physical Contact Models
- Hertz spring model for impact: F = k_H * x^1.5 during contact
- Contact duration determines spectral content: shorter = more HF
- See [[impact-synthesis]] for parameter details

## Excitation Location (Modal Coupling)

The input force couples to mode n proportional to phi_n(x_drive):
- Excite at node of mode n: phi_n(x_drive) = 0 — mode not excited
- Excite at antinode: maximum energy transfer to that mode
- This is why striking a bell at the rim vs. near the nodal line changes tone

## Summary Table

| Excitation | Duration | Spectrum | Typical Use |
|---|---|---|---|
| Impulse | 1 sample | Flat | struck/hit |
| Shaped impulse | ~1ms | Bandlimited | mallet/hammer |
| Noise burst | 5-50ms | Shaped | rough impact, onset |
| Continuous noise | infinite | Shaped | wind, cavity, diffuse |
| Sinusoidal | infinite | Tonal | bowing, resonance |
| Bow-force model | infinite | Broadband (slip) | bowing, friction |

## Cross-References

- Mode coupling via shape functions: [[mode-shapes-and-eigenvalues]]
- Impact force model: [[impact-synthesis]]
- Friction/bow drive: [[friction-synthesis]]
- Resonator response to inputs: [[resonator-bank-implementation]]

---
title: Sinusoidal Parameter Interpolation
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [sinusoidal, modifications]
sources:
  - /w/sasp/sinespecinterp.tex
  - /w/sasp/additivesynth.tex
  - /w/sasp/oscbank.tex
---

# Sinusoidal Parameter Interpolation

Once partials are tracked, resynthesis interpolates amplitude,
frequency, and phase **between frames** to reconstruct a smooth
time-domain signal. Poor interpolation = audible artifacts at the
frame rate.

## Inputs

For partial $p$ at frames $m$ and $m+1$, separated by $R$ samples:
- Amplitudes $A_m, A_{m+1}$
- Frequencies (rad/sample) $\omega_m, \omega_{m+1}$
- Phases $\phi_m, \phi_{m+1}$ (unwrapped)

Goal: a smooth trajectory $A(n), \omega(n), \phi(n)$ for
$n \in [mR, (m+1)R]$ such that the oscillator
$y(n) = A(n)\cos\phi(n)$ matches measured samples at both frame
centers.

## Amplitude: Linear

$$A(n) \;=\; A_m + \frac{n - mR}{R}(A_{m+1} - A_m)$$
Simple, good enough for most signals. Non-negativity preserved.

## Phase: Cubic (McAulay-Quatieri)

For smooth, artifact-free partial continuation, use a **cubic phase
polynomial** satisfying 4 boundary conditions:
- $\phi(mR) = \phi_m$, $\phi((m+1)R) = \phi_{m+1} + 2\pi M^\ast$
- $\dot\phi(mR) = \omega_m$, $\dot\phi((m+1)R) = \omega_{m+1}$

$$\phi(n) \;=\; \phi_m + \omega_m(n-mR) + \alpha(n-mR)^2 + \beta(n-mR)^3$$

The integer $M^\ast$ is chosen so that the cubic has minimal "wiggle"
(McAulay-Quatieri unwrapping rule) — pick $M^\ast$ to minimize the
integral of $|\ddot\phi|^2$. Closed form:
$$M^\ast \;=\; \operatorname{round}\!\left[\frac{1}{2\pi}\!\left(\phi_m + \omega_m R - \phi_{m+1}\right) + \tfrac{R}{4\pi}(\omega_{m+1} - \omega_m)\right]$$

Once $M^\ast$ is fixed, $\alpha$ and $\beta$ are a $2\times 2$ linear solve.

## Frequency: Derivative of Phase

$\omega(n) = \dot\phi(n) = \omega_m + 2\alpha(n-mR) + 3\beta(n-mR)^2$ —
automatically quadratic when phase is cubic. Consistent with both
measurements.

## Simpler Alternative: Linear Frequency + Phase Reset

Interpolate $\omega$ linearly and ignore measured phase at $m+1$:
$$\phi(n) \;=\; \phi_m + \int_{mR}^{n}\omega(\tau)\,d\tau$$
Cheaper; fine for crossfades or incoherent resynthesis but loses
phase lock — causes **phasiness** in transparent resynthesis.

## Birth and Death

- **Birth**: fade amplitude in from 0 over one frame; phase continuous.
- **Death**: fade amplitude to 0 over one frame; track frequency
  unchanged so phase stays coherent during fade.

## Relation to Other Views

- **IFFT synthesis**: skip explicit oscillator; place interpolated
  main-lobe images directly in the spectrum at synthetic frame rate
  and inverse-FFT. See [[stft-modifications]].
- **Phase vocoder**: implicit oscillator-bank per bin, with phase
  continuation across frames. See [[phase-vocoder-and-tsm]].

## Related Concepts
- [[sinusoidal-modeling]] — upstream analysis
- [[qifft-peak-estimation]] — provides the frame parameters
- [[phase-vocoder-and-tsm]] — related phase management

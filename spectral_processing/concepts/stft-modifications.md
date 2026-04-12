---
title: STFT Modifications
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [stft, modifications, ola, fbs, perfect-reconstruction]
sources:
  - /w/sasp/modifications.tex
  - /w/sasp/ifftsynth.tex
  - /w/sasp/oscbank.tex
---

# STFT Modifications

Modifying the STFT is the heart of spectral audio processing:
equalization, denoising, effects, cross-synthesis, time/pitch scaling,
and additive resynthesis all work by altering $X_m(k)$ before
inversion.

## Safe vs. Unsafe Modifications

An STFT modification $Y_m(k) = T\{X_m(k)\}$ is **safe** if the
modified signal still inverts consistently under OLA or FBS. Failure
modes:

| Failure | Cause | Symptom |
|---------|-------|---------|
| Time-aliasing | $T$ implies an $h_m$ longer than FFT headroom | pre-echo |
| Bin crosstalk | sharp gain changes across $k$ | warbling, ringing |
| Frame discontinuity | $T$ differs much between frames | amplitude modulation at frame rate |
| Phase inconsistency | magnitude edit breaks phase coherence | "phasiness", roughness |

## Three Classes of Modification

### 1. Fixed multiplicative (filtering)
$Y_m(k) = H(k)\, X_m(k)$ with $H$ constant in $m$. Equivalent to LTI
filtering. Safe when the implied impulse response fits in the
zero-padding headroom (see [[overlap-add-stft]]).

### 2. Time-varying multiplicative
$Y_m(k) = H_m(k)\, X_m(k)$. Must vary **slowly** relative to frame
rate. Typical: noise reduction (spectral subtraction), dynamic
equalization, auto-gain.

### 3. Non-linear / resynthesis
Replace $X_m$ with a model: peak picks, phase vocoder magnitude edits,
cross-synthesis products. Beyond LTI framework; consistency must be
enforced explicitly.

## Inverse-FFT Synthesis

Build the output frame directly in the frequency domain:
1. Place synthetic spectral peaks (main lobe copies of $W$) at desired
   frequencies with desired amplitudes/phases.
2. IFFT to get a short time-domain chunk.
3. OLA with synthesis window.

Efficient alternative to an oscillator bank for large numbers of
partials. Used in [[sms-sines-plus-noise]] synthesis and
phase-vocoder resynthesis.

## Oscillator Bank Resynthesis

Sum of sinusoids with linearly interpolated amplitude, frequency, and
cubic phase between frames:
$$y(n) \;=\; \sum_p A_p(n)\cos\!\left[\phi_p(n)\right]$$
Preferred when partials are few (~50) and smooth; IFFT synthesis wins
for dense spectra (thousands of bins). See [[sinusoidal-parameter-interpolation]].

## Cross-Fading Between Models

When switching representations (sinusoidal ↔ noise ↔ raw STFT), cross
fades in the spectrogram domain must be aligned with frame boundaries
to avoid clicks.

## Design Rules

1. Keep $R \le M/2$ — plenty of overlap for smoothing.
2. Zero-pad by $\ge 2\times$ to absorb filter ringing.
3. Smooth $H_m(k)$ both in $k$ (avoid ringing) and in $m$ (avoid
   modulation).
4. For magnitude-only edits, re-derive phase by phase continuation
   (phase-vocoder style).

## Related Concepts
- [[overlap-add-stft]], [[filter-bank-summation-stft]] — host frameworks
- [[phase-vocoder-and-tsm]] — principled time/pitch modification
- [[cross-synthesis-and-morphing]] — applications

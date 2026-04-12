---
title: Cross-Synthesis and Morphing
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [cross-synthesis, applications, modifications]
sources:
  - /w/sasp/cross-synth.tex
  - /w/sasp/vocoder.tex
  - /w/sasp/vocoder-by-fft.tex
---

# Cross-Synthesis and Morphing

Combining two signals in the STFT domain so that each contributes a
distinct aspect (e.g., excitation vs resonance, magnitude vs phase).
The phase vocoder and FFT filter bank provide a clean substrate.

## Excitation × Spectral Envelope

Classical **channel vocoder** idea, FFT-modernized:
1. Analyze **modulator** (e.g., voice) $\to$ time-varying spectral
   envelope $E_m(\omega)$.
2. Analyze **carrier** (e.g., synth pad) $\to$ STFT $C_m(\omega)$.
3. Shape: $Y_m(\omega) = E_m(\omega)\cdot C_m(\omega) / |C_m(\omega)|\cdot|C_m(\omega)|$
   — equivalently, multiply the carrier's magnitude by the modulator's
   envelope while keeping the carrier's phase.

Result: the carrier "speaks" with the modulator's formants — a
talking synthesizer.

Spectral envelope can be extracted via LPC, cepstral smoothing, or
channel bank — see [[f0-and-spectral-envelope]].

## Magnitude/Phase Exchange

$$Y_m(\omega) \;=\; |A_m(\omega)|\, e^{j\angle B_m(\omega)}$$
Mix one signal's magnitude with another's phase. Phase typically
dominates perceptually for transient/temporal structure, magnitude
for timbral identity. Useful for morphing experiments.

## Spectral Interpolation / Morphing

Weighted combination of two STFTs in log-magnitude and unwrapped
phase:
$$|Y_m(\omega)| \;=\; |A_m(\omega)|^{1-\alpha}\cdot|B_m(\omega)|^{\alpha}$$
$$\angle Y_m(\omega) \;=\; (1-\alpha)\,\angle A_m(\omega) + \alpha\,\angle B_m(\omega)$$
Geometric mean of magnitudes + linear interpolation of unwrapped
phase. Better than linear magnitude (which introduces beating).

For musically sensible morphs, align features first:
- Match pitches (pitch-shift one source).
- Align attack times.
- Match loudness envelopes.

## Convolution Cross-Synthesis

$$Y_m(\omega) \;=\; A_m(\omega)\cdot B_m(\omega)$$
Equivalent to short-time convolution — $B$ acts as an FIR filter
changing per frame. Used for:
- "Convolution reverb" (fixed $B$)
- Source-filter synthesis (voice as $A$, tract as $B$)
- Spectral masking effects

Requires OLA headroom for the effective impulse response — see
[[overlap-add-stft]].

## Pitch / Envelope Separation

Cleanest cross-synthesis factors signals into **source** (harmonic
structure, $f_0$, noise) and **filter** (spectral envelope):
1. Extract envelope $E$ via LPC or cepstrum (see [[f0-and-spectral-envelope]]).
2. Flatten (whiten) the source: $S = X / E$.
3. Recombine with another envelope: $Y = S_a \cdot E_b$.

This is the **source-filter cross-synthesis**, generalizing the LPC
vocoder.

## Applications

- Talking instruments / cross-synth effects ("vocoder" plugin)
- Sound design by combining textures
- Time-varying reverb and convolution effects
- Voice morphing
- Cross-adaptive audio effects

## Related Concepts
- [[phase-vocoder-and-tsm]] — phase management backbone
- [[stft-modifications]] — framework rules
- [[f0-and-spectral-envelope]] — separation of source/filter
- [[spectral-audio-applications]] — broader application context

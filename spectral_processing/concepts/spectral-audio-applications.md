---
title: Spectral Audio Applications
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [applications, audio-coding, loudness, history]
sources:
  - /w/sasp/applications.tex
  - /w/sasp/audiocoding.tex
  - /w/sasp/loudness.tex
  - /w/sasp/vocoder.tex
  - /w/sasp/vocoder-long.tex
  - /w/sasp/vocoder-today.tex
  - /w/sasp/history-sasp.tex
---

# Spectral Audio Applications

Where the theory lands in real systems. The FFT + filter bank is the
workhorse of modern audio.

## Audio Coding (MPEG, AAC, Opus)

**Goal**: compress audio at near-transparent quality using perceptual
models.

Pipeline:
1. **Analysis filter bank** — uniform or hybrid cosine-modulated
   (MPEG-1 Layer 3: 32-band + MDCT; AAC: pure MDCT; Opus: CELT MDCT).
2. **Psychoacoustic model** — compute masking threshold per band
   from a separate FFT using [[loudness]] / masking theory.
3. **Quantization** — allocate bits so quantization noise sits under
   the masking threshold.
4. **Entropy coding** — Huffman, arithmetic, range coding.
5. **Synthesis filter bank** — inverse of the analysis bank.

MDCT (Modified Discrete Cosine Transform) is a **lapped** transform
= critically sampled cosine-modulated filter bank with 50% overlap
and time-domain aliasing cancellation. See [[multirate-filter-banks]].

## Loudness and Masking

- **Equal-loudness contours** (Fletcher-Munson / ISO-226): sensitivity
  vs frequency and SPL.
- **Critical bands** (Bark / ERB): ear's frequency resolution,
  $\sim 24$ bands.
- **Masking**: loud tone raises threshold of nearby quiet tones
  (simultaneous) and temporally adjacent tones (pre/post).
- **Excitation patterns**: spread audio energy via a rounded-exponent
  spreading function; compute specific loudness per band; integrate
  to instantaneous loudness.

Drives coding bit allocation, perceptual metrics, dynamic range
compression, and mixing tools.

## Vocoders (Historical to Modern)

- **Dudley channel vocoder** (1939): analog filter bank + energy
  envelopes + voiced/unvoiced excitation.
- **Voder** (1939): hand-operated speech synthesizer at World's Fair.
- **Phase vocoder** (Flanagan 1966): FFT + analytic-signal per band;
  birthed [[phase-vocoder-and-tsm]].
- **LPC vocoder** (1960s-70s): source-filter model for speech coding.
- **Sinusoidal / SMS** (McAulay-Quatieri, Serra 1980s).
- **Modern**: neural vocoders (WaveNet, HiFiGAN) replace deterministic
  synthesis, but analysis is still STFT/mel.

## Effects Built on STFT

| Effect | Mechanism |
|--------|-----------|
| Denoising | Spectral subtraction with masking-based gain |
| Pitch correction | Peak frequency shift + phase lock |
| Time stretching | Phase vocoder TSM |
| Convolution reverb | OLA FFT convolution with impulse response |
| Cross-synthesis | STFT magnitude × carrier |
| Spectral freeze | Loop a single $X_m$ across frames |
| Robotization | Zero the phase per frame |
| Whisperization | Randomize phase |

## Analysis / Display

- **Spectrograms** — STFT magnitude in dB
- **Reassigned spectrograms** — sharpened via derivative estimators
- **Loudness spectrograms** — excitation pattern × time
- **Constant-Q transforms** — log-frequency display for music
- **Cochleagrams** — auditory filter bank magnitudes

## Physical Modeling Intersection

Spectral methods supply analysis data to physical models:
- Tune waveguide loop filters to measured tone partials ([[waveguide_synthesis]]).
- Fit modal data from QIFFT to modal synthesizer ([[modal_synthesis]]).
- Estimate excitation signals by inverse-filtering through modeled
  resonators.

## Related Concepts
- [[multirate-filter-banks]] — coder banks
- [[phase-vocoder-and-tsm]] — modification backbone
- [[cross-synthesis-and-morphing]] — vocoder-style effects
- [[noise-spectrum-analysis]] — basis of perceptual measurements

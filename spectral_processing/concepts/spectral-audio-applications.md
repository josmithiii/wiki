---
title: Spectral Audio Applications
created: 2026-04-11
updated: 2026-11-25
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
  - https://ccrma.stanford.edu/~jos/sasp/History_Spectral_Audio_Signal.html
  - https://ccrma.stanford.edu/~jos/sasp/Applications_STFT.html
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
   from a separate FFT using loudness / masking theory.
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
  $\sim 24$ bands; a first-order allpass (bilinear) frequency warping
  approximates the Bark scale closely (SASP [Appendix E](https://ccrma.stanford.edu/~jos/sasp/Bilinear_Frequency_Warping_Audio_Spectrum.html)).
- **Masking**: loud tone raises threshold of nearby quiet tones
  (simultaneous) and temporally adjacent tones (pre/post).
- **Excitation patterns**: spread audio energy via a rounded-exponent
  spreading function; compute specific loudness per band; integrate
  to instantaneous loudness.

Drives coding bit allocation, perceptual metrics, dynamic range
compression, and mixing tools.

## Vocoders (Historical to Modern)

- **Dudley channel vocoder** (begun 1928 at Bell Labs, published 1939):
  analog filter bank + energy envelopes + voiced/unvoiced excitation.
- **Voder** (1939): hand-operated speech synthesizer at World's Fair.
- **Phase vocoder** (Flanagan & Golden 1966): amplitude *and* phase of
  each complex bandpass channel; reimplemented with the FFT by Portnoff
  (1976). See [[phase-vocoder-and-tsm]].
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
| Convolution reverb | OLA FFT convolution ([[overlap-add-stft]]) with a room impulse response |
| Cross-synthesis | STFT magnitude × carrier |
| Spectral freeze | Loop a single $X_m$ across frames |
| Robotization | Zero the phase per frame |
| Whisperization | Randomize phase |

## Analysis / Display

- **Spectrograms** — STFT magnitude in dB ([[short-time-fourier-transform]]);
  **reassigned** spectrograms sharpen them via derivative estimators
- **Loudness spectrograms** — excitation pattern × time; **cochleagrams**
  — auditory filter bank magnitudes; **constant-Q** — log-frequency display

## Physical Modeling Intersection

Spectral methods supply analysis data to physical models:
- Tune waveguide loop filters to measured partial decays ([[waveguide_synthesis/concepts/string-modeling|string modeling]], [[waveguide_synthesis/concepts/waveguide-parameter-optimization|parameter optimization]]).
- Fit modal frequencies and dampings from [[qifft-peak-estimation|QIFFT]] peak tracks for a modal synthesizer ([[modal_synthesis/concepts/modal-analysis-measurement|modal analysis]]).
- Estimate excitation signals by inverse-filtering through modeled
  resonators.

## Related Concepts
- [[multirate-filter-banks]] — coder banks
- [[phase-vocoder-and-tsm]] — modification backbone
- [[cross-synthesis-and-morphing]] — vocoder-style effects
- [[noise-spectrum-analysis]] — basis of perceptual measurements

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Applications of the STFT](https://ccrma.stanford.edu/~jos/sasp/Applications_STFT.html), [Perceptual audio coding](https://ccrma.stanford.edu/~jos/sasp/Perceptual_audio_coding.html), [Loudness Spectrogram](https://ccrma.stanford.edu/~jos/sasp/Loudness_Spectrogram.html), [Bilinear Audio Frequency Warping](https://ccrma.stanford.edu/~jos/sasp/Bilinear_Frequency_Warping_Audio_Spectrum.html), [Spectral Audio Modeling History](https://ccrma.stanford.edu/~jos/sasp/History_Spectral_Audio_Signal.html)
- [[jos_books/entities/pasp-book|PASP]]: [Loop Filter Identification](https://ccrma.stanford.edu/~jos/pasp/Loop_Filter_Identification.html)

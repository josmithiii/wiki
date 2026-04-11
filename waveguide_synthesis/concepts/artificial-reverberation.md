---
title: Artificial Reverberation
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [reverb, fdn, sdn, waveguide, dsp, room]
sources:
  - /w/pasp/reverb.tex
  - /w/pasp/reverb-problem.tex
  - /w/pasp/reverb-fdn.tex
  - /w/pasp/reverb-sdn.tex
  - /w/pasp/reverb-jcrev.tex
  - /w/pasp/reverb-freeverb.tex
---

# Artificial Reverberation

Reverberation = sum of all reflection paths from source to listener.
Brute-force simulation (waveguide mesh of a concert hall) is prohibitively
expensive. Practical algorithms use delay-line networks with carefully
chosen feedback structures.

## The Problem

Exact simulation of a room with 3 sources, 2 ears, 1s T60 at 50 kHz:
~30 billion multiply-adds/second. A 3D waveguide mesh: ~5 quadrillion ops/s.
Instead, we approximate using structured delay networks.

## Early Reflections

- First ~80-100 ms: discrete echoes from walls, ceiling, floor
- Modeled by tapped delay line (TDL) with per-tap filtering
- Each tap: correct delay, amplitude (1/r spreading), air absorption filter
- Spatialization of early reflections strongly affects perceived room size

## Late Reverberation

After ~100 ms, echo density is so high that individual reflections merge
into a statistical process. Requirements:
- Echo density > ~1000/sec (perceptual threshold)
- Gaussian pressure distribution
- Exponential energy decay (straight-line EDC on dB scale)
- Frequency-dependent T60

## Schroeder Reverberators (JCREV, Freeverb)

### Schroeder (1962) / JCREV (Chowning, 1972)
- Series allpass filters → parallel feedback comb filters → mixing matrix
- Allpass: AP(N,g) = (-g + z^{-N}) / (1 - g*z^{-N})
- Feedback comb: FBCF(N,g) = 1 / (1 - g*z^{-N})
- 5 series allpasses produce ~810 echoes/sec

### Freeverb (Jezar, 2000)
- 8 parallel lowpass-feedback comb filters → 4 series allpasses
- Stereo: right channel delays offset by 23 samples
- Public-domain C++; no sample-rate normalization (fixed delay lengths)

## Feedback Delay Networks (FDN)

The modern standard for algorithmic reverb (Gerzon 1971; Jot 1991):
- N parallel delay lines with NxN lossless feedback matrix A
- Loss filters on each delay line for per-band T60 control
- Tonal correction filter E(z) decouples T60 from spectral shape

### Feedback Matrix Choices
- **Hadamard H_N**: recursive 2x2 embedding; multiply-free for N = power of 4
- **Householder A_N = I - (2/N)*u*u^T**: multiply-free for N = power of 2;
  cost: 2N-1 adds for matrix-vector product; equivalent to physical
  scattering at an N-waveguide junction
- N=4 Householder is uniquely "balanced" (all entries equal magnitude)

### Design Principle
Start from lossless prototype (infinite T60), tune for perceptually white
impulse response, then add per-band loss filters for desired decay.

## Scattering Delay Networks (SDN)

Bridges FDN and physical room modeling:
- One scattering junction per wall, positioned to reproduce first-order
  reflections exactly (correct delay, amplitude, filtering)
- Higher-order reflections reuse same waveguide segments (approximate)
- 3D room: 6 junctions, interconnected by digital waveguides
- Parameters (room dimensions, wall absorption) directly control network
- Perceptually adequate for rooms > ~10 m^3

## Related Concepts
- [[waveguide-overview]] — the delay lines reverb is built from
- [[scattering-junctions]] — FDN feedback = scattering at virtual junction
- [[waveguide-meshes]] — brute-force physical room simulation
- [[delay-line-techniques]] — interpolation for tuning delay lengths

## References
[^1]: Schroeder, M.R. (1962). "Natural Sounding Artificial Reverberation." JAES 10(3).
[^2]: Jot, J.-M. & Chaigne, A. (1991). "Digital Delay Networks for Designing Artificial Reverberators." AES Conv. 90.
[^3]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.

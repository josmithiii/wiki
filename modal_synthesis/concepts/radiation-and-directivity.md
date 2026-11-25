---
title: Radiation and Directivity
created: 2026-04-10
updated: 2026-11-25
type: concept
tags: [modal-synthesis, acoustics, physical-modeling, fem, bem]
sources:
  - /w/pasp/modal.tex
---

# Radiation and Directivity

Modal synthesis typically outputs a scalar signal (sum of mode contributions at
a pickup point). In reality, each mode radiates sound differently into space
depending on its shape, frequency, and the object's geometry.

## Radiation Efficiency vs. Mode Shape

Not all modes radiate sound equally:
- **Monopole-like modes** (net volume change): the most efficient radiators at low frequencies
  - Radiation efficiency $\sim (ka)^2$ for small $ka$ ($k$ = wavenumber, $a$ = object size)
  - Example: guitar top plate "breathing" mode (~100 Hz)
- **Dipole modes** (one half moves up, other down): partial cancellation
  - Radiation efficiency $\sim (ka)^4$ for small $ka$
- **Higher-order modes** (quadrupole, etc.): poor radiation at low frequencies
  - Radiation efficiency $\sim (ka)^{2(n+1)}$ for multipole order $n$ (monopole $n=0$)
- Above $ka \approx 1$ (object size ~ wavelength), all modes radiate efficiently

### Implications for Synthesis
- Low modes with high symmetry dominate the far-field sound
- Many high-Q modes visible in vibration measurements are acoustically weak
- Perceptual mode reduction can exploit this: drop poorly radiating modes first
- See [[realtime-modal-synthesis]] for perceptual pruning strategies

## Acoustic Transfer Function

The full pipeline from excitation to listener ear:
1. Excitation force → modal velocity (mechanical transfer function)
2. Modal velocity → surface pressure (radiation impedance)
3. Surface pressure → far-field sound (acoustic transfer / HRTF)

### BEM for Acoustic Transfer (James et al. 2006)[^1]
- Precompute acoustic transfer per mode using BEM
- Each mode radiates at one frequency, so its transfer is a single direction- and distance-dependent pattern
- Store compactly as a few equivalent multipole sources (spherical-harmonic expansions)
- At runtime: combine precomputed radiation patterns weighted by mode amplitudes
- Enables spatially accurate sound for moving listener/object; extended to nonlinear thin shells in [^3]

### Simplified Models
- **Point source per mode**: ignore directivity, scale by radiation efficiency
- **Multipole expansion**: monopole + dipole + quadrupole per mode
- **HRTF convolution**: post-process mono output with head-related transfer function

## Directivity Patterns

| Mode Type | Pattern | Example |
|-----------|---------|---------|
| Breathing (0,0) | Omnidirectional | Guitar body ~100 Hz |
| Rocking (1,0) | Figure-8 / dipole | Guitar body ~200 Hz |
| Higher plate modes | Complex lobes | Cymbal, bell |
| Tube open end | Piston in baffle | Trumpet bell radiation |

## Near-Field vs. Far-Field

- Near-field ($r < a$): evanescent mode contributions significant
- Far-field ($r \gg a$): only propagating components — directivity pattern stable
- Transition region: both contribute — BEM needed for accuracy
- Most synthesis assumes far-field listening (simplifies to amplitude + delay)

## Practical Considerations

- For interactive applications, directivity is often ignored (mono sum of modes)
- For VR/AR spatialization: precomputed acoustic transfer is worthwhile
- Radiation filtering can be approximated as a gentle low-shelf boost
  to monopole-like modes and high-shelf cut to higher-order modes
- Recording-based approaches ([[waveguide_synthesis/concepts/commuted-synthesis|commuted synthesis]]) capture radiation implicitly:
  a measured body response already includes the path to the microphone[^2]

## Related Concepts
- [[fem-bem-for-modal-synthesis]] — BEM computation of acoustic transfer
- [[modal-synthesis-overview]] — the synthesis pipeline this extends
- [[mode-shapes-and-eigenvalues]] — spatial patterns that determine radiation
- [[gpu-modal-synthesis]] — GPU acceleration enables per-mode radiation
- [[sav-nonlinear-string-with-measured-body]] — measured bridge-to-air radiation as a parallel pole-residue bank

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Body Modeling](https://ccrma.stanford.edu/~jos/pasp/Body_Modeling.html), [Commuted Synthesis](https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html), [Spherical Waves from a Point Source](https://ccrma.stanford.edu/~jos/pasp/Spherical_Waves_Point_Source.html)

## References
[^1]: James, Barbič & Pai (2006). "Precomputed Acoustic Transfer." ACM TOG (SIGGRAPH).
[^2]: Smith, J.O. III. *Physical Audio Signal Processing*, [Commuted Synthesis](https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html).
[^3]: Chadwick, An & James (2009). "Harmonic Shells: A Practical Nonlinear Sound Model for Near-Rigid Thin Shells." ACM TOG (SIGGRAPH Asia).

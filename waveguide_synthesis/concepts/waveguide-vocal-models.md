---
title: Waveguide Vocal Models
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [voice, waveguide, physical-modeling, dsp, acoustics]
sources:
  - /l/wgr/Sections/Advancements/SpeechProcessing.tex
  - /w/pasp/idealtubesummary.tex
---

# Waveguide Vocal Models

The vocal tract was the first acoustic system modeled with digital scattering
theory (Kelly & Lochbaum, 1962). Modern waveguide vocal models range from
1D piecewise-cylindrical tubes to 3D waveguide meshes driven by MRI geometry.

## Kelly-Lochbaum Model (1962)

- Vocal tract approximated as concatenated cylindrical tube sections
- Each section has wave impedance $R_m = \rho c / A_m$
- Scattering junctions at area changes: $k_m = (A_m - A_{m+1}) / (A_m + A_{m+1})$
- Glottal source at one end, lip radiation at the other
- Led directly to ladder/lattice digital filters and LPC for speech

## SPASM — Singing Voice (Cook, 1991-93)

"Singing Physical Articulatory Synthesis Model":
- Nasal tract branching via variable 3-port velum/pharynx junction
- Turbulence noise injectable at any point along the vocal tract
- Variable glottal and lip reflection coefficients
- Separate radiation outputs for neck, lip, and nose
- Interactive real-time control
- Related: "Pink Trombone" (online interactive vocal synth)

## 2D/3D Waveguide Mesh Vocal Tract

Advances beyond the 1D plane-wave assumption:

### 2D Mesh Models
- 2D relaxation introduces lateral modes (Mullen et al., 2003-2007)
- Approximately linear formant-bandwidth control across vowels
- Real-time dynamic articulation via impedance mapping on fixed mesh

### 3D Mesh Models
- Match measured transfer functions of physical vocal-tract analogs
- Close acoustic match over wide frequency band (Speed et al., 2013-14)
- MRI-derived geometry with time-varying impedance maps (Gully, 2018)
- Diphthong synthesis with improved formant accuracy
- Voiced stop consonants via controlled occlusions (Gully, 2019)

## Non-Human Vocal Models

- **Birdsong**: syrinx modeled with waveguide synthesis (Smyth, 2002-03)
  - Bifurcated airway with vibrating membranes
- **Mammalian vocalizations**: lion roar, wolf growl (Wilkinson, 2016)
  - Effective for harsh, spectrally dense sounds

## Parameter Estimation for Vocal Tract

- Kestian & Smyth (2010): precompute K-L lookup table mapping areas to formants;
  nearest-neighbor match at runtime
- Sudholt et al. (2023): DDSP gradient descent on K-L area sections;
  outperforms genetic algorithms and black-box neural methods in listening tests
- Xu & Reiss (2025): Transformers for Pink Trombone area optimization;
  surpasses neural audio synthesis for vowel reconstruction

See [[waveguide-parameter-optimization]] for the full optimization taxonomy.

## Related Concepts
- [[scattering-junctions]] — the area-change junctions in the vocal tract
- [[bore-modeling]] — same waveguide principles applied to wind instruments
- [[waveguide-meshes]] — 2D/3D meshes used for advanced vocal tract models
- [[waveguide-parameter-optimization]] — calibrating vocal tract models

## References
[^1]: Kelly, J. & Lochbaum, C. (1962). "Speech synthesis." 4th ICA, Copenhagen.
[^2]: Cook, P. (1993). "SPASM: a real-time vocal tract physical model controller." ICMC.
[^3]: Tablas de Paula et al. (2025). "Four Decades of Digital Waveguides." JAES.

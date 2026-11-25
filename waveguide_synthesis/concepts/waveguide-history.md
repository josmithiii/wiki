---
title: Waveguide History
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [waveguide, history, physical-modeling]
sources:
  - /l/wgr/Sections/HistoricalBackground.tex
  - https://ccrma.stanford.edu/~jos/pasp/History_Enabling_Ideas_Leading.html
---

# Waveguide History

Digital waveguide synthesis draws on three centuries of physics and half a
century of DSP. This page traces the key milestones.[^1][^2]

## Foundations (1747-1962)

- **1747**: d'Alembert's traveling-wave solution of the wave equation
- **1759**: Lagrange — first calculation of reflection/transmission at string junction
- **1823**: Fresnel — scattering theory in optics
- **1871**: Lord Rayleigh — proportionality of pressure and velocity in traveling waves
- **1886**: Heaviside — "telegrapher's equations"; introduced the term "impedance"
- **1947**: Tustin — bilinear transform (later used in wave digital filters)
- **1962**: Kelly & Lochbaum — earliest known digital scattering vocal-tract model (Bell Labs)
  - Computer-music accompaniment by Max Mathews

## Pre-Waveguide DSP (1961-1983)

- **1961**: Schroeder & Logan — delay-line reverberators
- **1971**: Fettweis — [[wave-digital-filters|wave digital filters]] (WDFs)
- **1971**: Gerzon — orthogonal feedback delay networks
- **1979**: Moorer — lowpass-feedback comb filters for reverb
- **1983**: Karplus & Strong — "Digitar" algorithm (wavetable-as-delay-loop)
  - Not understood as physical modeling at the time
  - David Jaffe brought it to Julius Smith for signal-processing extensions

## Digital Waveguide Synthesis (1983-1994)

- **1983**: Jaffe & Smith — Extended Karplus-Strong (signal-processing extensions)
  - Pitch tuning via allpass interpolation
  - Pick-position comb filter
  - Dynamic level control
- **1985**: Smith — "A New Approach to Digital Reverberation Using Closed Waveguide
  Networks" — the founding DWG paper
  - Motivated by Gary Kendall's instability problems with feedback reverb
  - Key insight: closed lossless waveguide networks are inherently allpass/stable
- **1986**: Smith — "Efficient Simulation of the Reed-Bore and Bow-String Mechanisms"
  - First DWG clarinet and simplified bowed string
- **1989**: Yamaha licenses DWG technology from Stanford
- **1991**: Cook — SPASM singing voice model
- **1992**: Välimäki et al. — real-time DWG flute
- **1993**: Van Duyne & Smith — 2D digital waveguide mesh
- **1993**: Smith; Karjalainen et al. — [[commuted-synthesis|commuted synthesis]]
- **1994**: Van Duyne & Smith — wave digital piano hammer
- **1994**: Yamaha VL1 "Virtual Lead" synthesizer — first commercial DWG product

## Expansion (1995-2010)

- **1995**: Van Duyne & Smith — tetrahedral 3D mesh
- **1996**: Cook — Synthesis Tool Kit (STK), later maintained with Scavone
- **1996**: Scavone & Smith — tonehole modeling
- **2000**: Van Walstijn — wave digital tonehole
- **2000**: Freeverb (Jezar) — public-domain Schroeder reverberator
- **2004**: Essl, Serafin, Cook & Smith — theory of [[banded-waveguides|banded waveguides]]
- **2005**: Karjalainen, Huang & Smith — waveguide networks for room response (SDN precursor)

## Modern Era (2010-present)

- **2015**: De Sena et al. — Scattering Delay Networks (SDN) with perceptual validation
- **2017**: Stevens et al. — Waveguide Web for outdoor acoustics
- **2020**: Engel et al. — DDSP framework (differentiable DSP)
- **2023**: Sudholt et al. — DDSP applied to Kelly-Lochbaum vocal tract
- **2025**: Tablas de Paula, Smith, Välimäki & Reiss — "Four Decades of Digital
  Waveguides" (JAES review)
- **2025**: Tablas de Paula et al. — differentiable time-variant FDL optimization
- **2025**: Mezza et al. — differentiable SDN reverb
- **2025**: Xu & Reiss — Transformer-based Pink Trombone optimization

## The Patent Story

Stanford's DWG patent was initially rejected because "closed lossless networks"
were deemed "perpetual motion machines" lacking utility. After extensive back
and forth, it was issued — making lossless reverberator prototypes arguably
the first patented virtual perpetual-motion invention in the US.

## Related Concepts
- [[waveguide-overview]] — the technical foundations
- [[scattering-junctions]] — from Lagrange (1759) to Kelly-Lochbaum (1962)
- [[waveguide-parameter-optimization]] — the modern DDSP frontier
- [[artificial-reverberation]] — where it all started (1985)

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [History of Enabling Ideas](https://ccrma.stanford.edu/~jos/pasp/History_Enabling_Ideas_Leading.html), [Karplus-Strong Algorithms](https://ccrma.stanford.edu/~jos/pasp/Karplus_Strong_Algorithms.html), [Digital Waveguide Models](https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Models_I.html), [History of FDNs for Artificial Reverberation](https://ccrma.stanford.edu/~jos/pasp/History_FDNs_Artificial_Reverberation.html)

## References
[^1]: Tablas de Paula, Smith, Välimäki & Reiss (2025). "Four Decades of Digital Waveguides." JAES.
[^2]: Smith, J.O. III. *Physical Audio Signal Processing*, W3K Publishing, 2010; online at <https://ccrma.stanford.edu/~jos/pasp/>.

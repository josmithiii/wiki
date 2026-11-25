---
title: Waveguide vs. Modal Synthesis
created: 2026-04-09
updated: 2026-11-25
type: comparison
tags: [waveguide, modal-synthesis, physical-modeling, dsp, comparison]
sources:
  - /w/pasp/modal.tex
  - https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
---

# Waveguide vs. Modal Synthesis

## Overview
Both are physically motivated approaches to sound synthesis, but they model
different aspects of vibration and suit different instruments/objects.

## Core Distinction
- **Waveguide synthesis**: models wave *propagation* through a medium
  (delay lines, scattering junctions)
- **Modal synthesis**: models *resonant modes* (eigenfrequencies of the system)

They are mathematically equivalent for linear systems -- but the representations
differ in efficiency and what is natural to control.

## Comparison Table

| Dimension | Waveguide | Modal |
|-----------|-----------|-------|
| Representation | Traveling waves, delay lines | Standing waves, eigenmode sum |
| Core DSP element | Delay line + filter | Resonator (biquad) |
| Excitation | Bow, reed, breath (flow-pressure) | Impact, impulse force |
| Geometry | 1D structures (strings, bores) | Any dimensionality |
| Mode count | Implicit (all modes up to Nyquist) | Explicit, finite $N$ |
| Real-time cost | $O(1)$ per sample per delay loop (memory $O(L)$) | $O(N)$ — number of modes |
| Pitch control | Change delay length | Scale all $f_k$ |
| Damping | Lowpass filter in loop | Pole radius per mode |
| Nonlinearity | Natural (reed, bow at junction) | Requires feedback loop |
| Best for | Strings, woodwinds, brass | Bars, plates, bells, shells |

## 1D Equivalence
For a lossless string: waveguide = modal (exactly).
- $N$-mode modal sum of string = output of Smith's digital waveguide model (1992);
  Karplus-Strong (1983) is a special case of this equivalence
- They differ only in how parameters are specified

## When to Use Which

Use **waveguide** when:
- Instrument has clear 1D waveguide topology (string, bore, horn, rod)
- Nonlinear interaction at a defined excitation point (reed, bow)
- Real-time pitch control is key (variable delay length)
- Continuous sound source (sustained notes)

Use **modal** when:
- Object is 2D or 3D (plate, bowl, bell, room)
- Small number of damped masses and springs gives an adequate model (mallet, lips, reed)
- Modes are measured or computed numerically (FEM)
- Impact or pluck excitation (no feedback needed)
- Need to change pickup position without recomputing all modes
- More GPU parallelism desired

## Hybrid Approaches
- **Modal + waveguide**: use modal for body resonance, waveguide for string
  (e.g., guitar body modeled as modes, string as waveguide); see [[coupled-structures]]
- **Delay-loop expansion**: one filtered delay loop per quasi-harmonic series of modes
- **Banded waveguides**: one band-limited delay loop per mode of a bar, bowl or glass, keeping
  waveguide-style nonlinear excitation ([[waveguide_synthesis/concepts/banded-waveguides|banded waveguides]])
- **Commuted synthesis**: fold the body's modal IR into the excitation (next section)

## Commuted Synthesis Shortcut
String and body are both LTI, so they commute. Precompute the body impulse response
$$h_{\text{body}}(t) \;=\; \sum_k a_k\, e^{-d_k t}\, \sin(2\pi f_k t)$$
convolve it offline with the excitation, $a(t) = e(t) * h_{\text{body}}(t)$, and play that
table into the string loop: $y = a * h_{\text{string}}$. The hundreds of body resonators never run
at synthesis time - at the cost of a body frozen into the table (no run-time changes to
pickup or modes). See [[waveguide_synthesis/concepts/commuted-synthesis|commuted synthesis]].

## DAFx26 additions

- DAFx26 offers a direct contrast case: a **finite-difference plus modal** bowed-string model of the Chinese yehu (two stiff strings, elastic bow hairs, a measured modal bridge, radiation as a parallel biquad bank) versus the delay-line route to the same instrument class - see [[waveguide_synthesis/entities/source-papers#paper-zheng-yehu-physical-model-2026]].
- The **65-guitar** pipeline keeps the body as a modal load coupled at an interior bridge point rather than commuting it into the excitation, which is the modal counterpart of the commuted shortcut above: [[entities/source-papers#paper-ducceschi-65-classical-guitars-2026]]
- On the reverb side, a **differentiable FDN** fitted to measured RIRs (waveguide wiki) and a **corpus-driven modal reverberator** (this wiki) attack the same problem from the two sides of this comparison: [[waveguide_synthesis/entities/source-papers#paper-ibnyahya-differentiable-fdn-rir-2026]] and [[entities/source-papers#paper-ducceschi-corpus-driven-modal-reverberator-2026]]

## Related Concepts
- [[modal-synthesis-overview]] -- modal synthesis in full detail
- [[resonator-bank-implementation]] -- modal DSP
- [[friction-synthesis]] - nonlinear feedback excitation: natural at a waveguide junction, a feedback loop in modal form
- [[waveguide_synthesis/concepts/waveguide-overview|waveguide overview]] - the waveguide side in full detail

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Modal Expansion](https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html), [Delay Loop Expansion](https://ccrma.stanford.edu/~jos/pasp/Delay_Loop_Expansion.html), [Commuted Synthesis](https://ccrma.stanford.edu/~jos/pasp/Commuted_Synthesis.html), [Digital Waveguide Models](https://ccrma.stanford.edu/~jos/pasp/Digital_Waveguide_Models.html), [Physical Models](https://ccrma.stanford.edu/~jos/pasp/Physical_Models.html)
- [[jos_books/entities/filters-book|Filters]]: [Digital Waveguide Oscillator Example](https://ccrma.stanford.edu/~jos/filters/State_Space_Analysis_Example_The.html)

# Waveguide Synthesis Wiki — Build Plan

## Pass 1: PASP Ingestion — DONE (2026-04-11)

### Pages Written (8)
- [x] waveguide-overview — bidirectional delay lines, d'Alembert, I/O
- [x] scattering-junctions — Kelly-Lochbaum, multiport, WDF adaptors
- [x] delay-line-techniques — fractional delay, interpolation, lossy propagation
- [x] string-modeling — K-S/EKS, damping, stiffness, coupling, commuted synthesis
- [x] bore-modeling — cylindrical/conical tubes, tone holes, bell radiation
- [x] reed-and-bow-models — single reed, lip reed, air reed, bow friction
- [x] artificial-reverberation — FDN, SDN, Schroeder/JCREV/Freeverb
- [x] waveguide-meshes — 2D/3D grids, dispersion, room acoustics

### PASP Chapters Ingested (~30)
delay-waveguide, strings, plucked, damping, stiffstring, struckstring,
coupling, piano-string, guitar-bridge, acoustic-guitars, electric-guitars,
reeds, reedboremech, brasses, flute, cones, idealtubesummary, woodwinds,
delay-interp, delay-var, delay-lossy-prop, delay-allpass-waveguide,
adaptors, mesh, reverb-problem, reverb-fdn, reverb-sdn, reverb-jcrev,
reverb-freeverb, reverb-early

### PASP Errors Fixed (7)
- brasses.tex:94 — duplicate "and and"
- damping.tex:117 — "miminizer" → "minimizer"
- reverb-freeverb.tex:1 — \kdefq{JCRev} → \kdefq{Freeverb}
- delay-var.tex:25 — missing "in" before \chref
- reverb-fdn.tex:113 — stray period after \right] in Hadamard matrix
- piano-string.tex:71 — "damping due R_2" → "damping due to R_2"
- piano-string.tex:119-125 — inharmonicity formula B: SI² → I; /16 → /4

## Pass 2: JAES Review Ingestion — DONE (2026-04-11)

Source: /l/wgr/ — "Four Decades of Digital Waveguides"
(Tablas de Paula, Smith, Välimäki, Reiss — JAES 2025)

### Sections Ingested
- HistoricalBackground.tex — K-S history, DWG conceptualization, WDF relation
- Foundations.tex — traveling waves, scattering, strings, tubes, mesh, commuted synth
- Advancements/InstrumentModelling.tex — winds, strings, brasses, percussion, STK/Faust
- Advancements/ArtificialReverberation.tex — SDN, waveguide web, Treeverb
- Advancements/SpeechProcessing.tex — K-L, SPASM, 2D/3D mesh vocal tract, birdsong
- Parameter Optimization/ParameterOptimisation.tex — full taxonomy of methods

### Pages Written (5)
- [x] commuted-synthesis — LTI commutativity, body IR precomputation
- [x] banded-waveguides — closed wavetrains for cymbals, bells, percussion
- [x] waveguide-vocal-models — K-L, SPASM, 2D/3D mesh vocal tract, non-human
- [x] waveguide-parameter-optimization — physics, filter, genetic, neural/DDSP
- [x] waveguide-history — timeline from d'Alembert (1747) to DDSP (2025)

### JAES Errors Fixed (1)
- ArtificialReverberation.tex:18 — "junction,but" → "junction, but"

## Remaining Work

### Entity Pages — TODO
- [ ] pasp-book — Smith's Physical Audio Signal Processing (online book)
- [ ] stk-toolkit — Cook & Scavone's Synthesis Toolkit
- [ ] four-decades-paper — the JAES review paper itself

### PASP Chapters Not Yet Ingested
Some PASP chapters were skimmed but could yield more detail:
- extexc.tex — external excitation of waveguide string at arbitrary point
- nonlin.tex — memoryless nonlinearities in waveguide models
- lumped.tex — lumped element modeling (masses, springs, dashpots)
- app-physics.tex — wave equation derivations
- tonehole.tex — detailed tonehole scattering model
- coupledstrings.tex (in instruments/) — piano coupled strings eigenanalysis
- reverb-late.tex, reverb-perceptual.tex — late reverb and perceptual criteria
- SoundEffects.tex (JAES) — not yet read

### Cross-Wiki Integration — TODO
- [ ] Add wikilinks from modal_synthesis pages to waveguide_synthesis pages
  - waveguide-vs-modal.md already cross-links
  - coupled-structures.md mentions commuted synthesis → link
  - nonlinear-modal-synthesis.md mentions string collisions → link to string-modeling
- [ ] Consider whether dsp_synthesis/ should be merged/retired
- [ ] Update ~/wiki/README.md if dsp_synthesis is retired

### Possible Future Pages
- wave-digital-filters — WDF adaptors, lumped element modeling, nonlinear circuits
- waveguide-sound-effects — flanging, chorus, Leslie, environmental effects
- waveguide-networks — general allpass DWN theory, reverb prototypes

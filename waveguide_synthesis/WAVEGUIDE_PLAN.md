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
See waveguide_synthesis/log.md for details.

## Pass 2: JAES Review Paper — TODO

Source: /l/wgr/ — "Four Decades of Digital Waveguides"
(Tablas de Paula, Smith, Välimäki, Reiss — JAES 2025)

### Sections to Ingest
- /l/wgr/Sections/HistoricalBackground.tex — K-S history, DWG conceptualization
- /l/wgr/Sections/Foundations.tex — interacting traveling waves, scattering
- /l/wgr/Sections/Advancements.tex — waveguide networks, mesh, SDN, waveguide web
- /l/wgr/Sections/Advancements/InstrumentModelling.tex — state-of-art instruments
- /l/wgr/Sections/Advancements/ArtificialReverberation.tex — modern reverb
- /l/wgr/Sections/Advancements/SpeechProcessing.tex — vocal tract models
- /l/wgr/Sections/Advancements/SoundEffects.tex — effects, environmental sound
- /l/wgr/Sections/Parameter Optimization/ParameterOptimisation.tex — classical, evolutionary, neural
- /l/wgr/Sections/Conclusion.tex

### Actions
1. Read all sections, extract content beyond what PASP covers
2. Update existing pages with new material (post-2010 developments)
3. Write new pages (see below)

## Pass 2: New Pages Written (5) — DONE (2026-04-11)

### Concepts
- [x] commuted-synthesis — LTI commutativity, body IR precomputation
- [x] banded-waveguides — closed wavetrains for cymbals, bells, percussion
- [x] waveguide-vocal-models — K-L, SPASM, 2D/3D mesh vocal tract
- [x] waveguide-parameter-optimization — physics, filter, genetic, neural/DDSP
- [x] waveguide-history — timeline from d'Alembert to DDSP

### Entities — TODO
- [ ] pasp-book — Smith's Physical Audio Signal Processing (online book)
- [ ] stk-toolkit — Cook & Scavone's Synthesis Toolkit
- [ ] four-decades-paper — the JAES review paper itself

### Comparisons
- Cross-link to modal_synthesis/comparisons/waveguide-vs-modal.md (in index.md)

## Pass 3: Cross-Wiki Integration — TODO

- Add wikilinks from modal_synthesis pages to waveguide_synthesis pages
- Consider whether dsp_synthesis/ should be merged/retired
- Update ~/wiki/README.md if dsp_synthesis is retired

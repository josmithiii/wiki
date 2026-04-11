# Modal Synthesis Wiki — TODO

## Factual Errors to Fix

1. **modal-synthesis-overview.md:42** — Rath & Rocchesso (2005) was CPU-based contact sound, not GPU. GPU was James et al. (2006).
2. **gpu-modal-synthesis.md:29** — Cook & Scavone (1999) was PhISEM/STK, not GPU synthesis. Remove or correct.
3. **gpu-modal-synthesis.md:34-35** — "CUDA Implementation (2006-era)" heading is wrong — CUDA didn't exist until 2007. James (2006) used OpenGL fragment shaders. Retitle and fix.
4. **realimpact-dataset.md:17** — Wrong authors and citation. Correct: Clarke, Gao, Wang, Rau, Xu, Wang, James, Wu. arXiv:2306.09944 (2023), ICCV — not Georg et al., not ICASSP, not arXiv:2206.08524.
5. **resonator-bank-implementation.md:30** — `s2_k[n-2]` should be `s1_k[n-2]` (single state variable, two delays).
6. **realtime-modal-synthesis.md:38** — "Tyically" → "Typically"
7. **damping-models.md:83** — Reference [^1] display text doesn't match URL. Fix link.
8. **rigid-body-sound-synthesis.md:89** — Remove Ren et al. wind noise reference (not rigid-body contact).
9. **friction-synthesis.md:53** — Add full citation for Serafin (PhD thesis, Stanford/CCRMA, 2004).
10. **waveguide-vs-modal.md:41** — Karplus-Strong is not "a pair of delay lines." The equivalence is with Smith's digital waveguide model (1992). Karplus-Strong is a special case.

## Sources to Ingest

### PASP LaTeX (text, no conversion needed)
- /w/pasp/modal.tex — JOS modal synthesis chapter (authoritative)
- /w/pasp/damping.tex — JOS damping treatment

### Bilbao / DAFx papers (pdf2txt.py first)
- /l/dttd/NonlinearModalSynthModeCoupling-Poirot-Bilbao-EURASIP-2024.pdf — nonlinear mode coupling
- /l/dttd/NonlinearCoupledResonatorsBilbao-DAFx23_paper_42.pdf — coupled nonlinear resonators
- /l/dttd/CollisionsBilbao2015.pdf — collision modeling
- /l/dttd/BilbaoCollisions-ISMA-2024.pdf — updated collision work
- /l/dttd/RealTimeGuitarSynthesisBilbao-DAFx24.pdf — coupled string+body real-time
- /l/dttd/TunableCollisionsPianoHammerDAFx23.pdf — piano hammer contact tuning
- /l/dttd/QuadraticSplineCollisions-DAFx24.pdf — spline collision models

### ML / differentiable modal synthesis (pdf2txt.py first)
- /l/dttd/DifferentiableModalSynthPlanarString-2407.05516v1.pdf — differentiable modal synth
- /l/dttd/DiffImpact-294_diffimpact_differentiable_rend.pdf — differentiable impact rendering
- /l/dttd/SynthMatch-DDSP-Diaz-Hayes-RigidBodyModal-ICASSP23.pdf — DDSP rigid-body modal
- ~/wiki/modal_synthesis/raw/papers/DiffSound-2409.13486v1.pdf — already on disk

### Measured modal analysis (pdf2txt.py first)
- /l/dttd/modal-analysis-of-different-types-of-classical-guitar-bodies.pdf

### Fetch from arXiv
- arXiv:2306.09944 — Clarke et al., RealImpact (correct citation)
- arXiv:2206.05931 — Jin et al., NeuralSound

## New Pages to Write (after ingesting sources)

1. **nonlinear-modal-synthesis.md** — Mode coupling, parametric resonance, tension-modulated modes, collision nonlinearities. Sources: Poirot-Bilbao EURASIP 2024, Bilbao collisions.
2. **coupled-structures.md** — String-bridge-body coupling, multi-object energy transfer. Sources: Bilbao guitar DAFx24, PASP.
3. **ml-modal-parameter-estimation.md** — NeuralSound, DiffSound, DiffImpact, differentiable modal synth. Sources: arXiv papers above.
4. **radiation-and-directivity.md** — Radiation efficiency vs. mode shape, monopole/dipole radiation, BEM acoustic transfer revisited.
5. **stochastic-modal-synthesis.md** — Statistical Energy Analysis (SEA), high-frequency mode density, noise-band synthesis above mode resolution limit.

## Empty `sources:` Fields to Fill

Every page currently has `sources: []` except damping-models.md and excitation-signals.md. After ingesting, add proper source references to all pages.

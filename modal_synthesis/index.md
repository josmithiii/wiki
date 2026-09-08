# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-09-08 | Total pages: 20

## Entities
- [[realimpact-dataset]] — 150k calibrated impact recordings from 50 objects; ML training resource
- [[entities/source-papers]] - distilled source-paper catalog (DAFx26 pass-1 ingestion)

### DAFx26 source-paper anchors
- [paper-ducceschi-65-classical-guitars-2026](entities/source-papers.md#paper-ducceschi-65-classical-guitars-2026) - measured bridge/radiation modes for 65 guitars driving an O(N) SAV nonlinear string
- [paper-giampiccolo-era-violin-bridge-2026](entities/source-papers.md#paper-giampiccolo-era-violin-bridge-2026) - Eigensystem Realization Algorithm for violin bridge admittances
- [paper-ducceschi-corpus-driven-modal-reverberator-2026](entities/source-papers.md#paper-ducceschi-corpus-driven-modal-reverberator-2026) - six user controls regressed onto thousands of modal reverb parameters
- [paper-bittner-diagonal-ssm-plate-reverb-2026](entities/source-papers.md#paper-bittner-diagonal-ssm-plate-reverb-2026) - diagonal complex-valued SSM shown equivalent to a parallel second-order all-pole bank
- [paper-lee-klein-bottle-reverberation-2026](entities/source-papers.md#paper-lee-klein-bottle-reverberation-2026) - closed-form modes of non-orientable 2D manifolds for impossible-geometry reverb
- [paper-ducceschi-bunkervik-spatial-reverb-2026](entities/source-papers.md#paper-ducceschi-bunkervik-spatial-reverb-2026) - modal spatial reverb with shared frequencies and position-interpolated residues
- [paper-gabrielli-dafx-challenge-overview-2026](entities/source-papers.md#paper-gabrielli-dafx-challenge-overview-2026) - the 1st DAFx Challenge: tasks, metrics, full Task A and Task B rankings, gain-bias finding
- [paper-marttila-transformer-pso-taska-2026](entities/source-papers.md#paper-marttila-transformer-pso-taska-2026) - Task A winner: Transformer plus normalizing flow plus PSO refinement
- [paper-park-two-stage-evolutionary-taska-2026](entities/source-papers.md#paper-park-two-stage-evolutionary-taska-2026) - Task A 2nd at machine precision with training-free CMA-ES plus ternary search
- [paper-garofalo-differentiable-modal-plate-2026](entities/source-papers.md#paper-garofalo-differentiable-modal-plate-2026) - Task A: differentiable modal plate synthesizer optimized at inference time
- [paper-diaz-count-density-networks-2026](entities/source-papers.md#paper-diaz-count-density-networks-2026) - Task B winner: per-bin mode-density networks on a 1/20-octave grid
- [paper-bittner-matrix-pencil-ssm-taskb-2026](entities/source-papers.md#paper-bittner-matrix-pencil-ssm-taskb-2026) - Task B: matrix-pencil SSM initialization with closed-form least-squares gains
- [paper-franchino-subband-ar-pole-harvesting-2026](entities/source-papers.md#paper-franchino-subband-ar-pole-harvesting-2026) - Task B: multi-view subband AR pole harvesting with no plate priors
- [Other challenge entries (not distilled)](entities/source-papers.md#other-challenge-entries-not-distilled) - one line each for challenge reports 78, 79, 80, 81, 84, 85, 89, 90, 91

## Concepts
- [[damping-models]] — viscous, thermoelastic, and frequency-dependent damping; per-mode decay rates and DSP pole placement
- [[excitation-signals]] — impulse, noise burst, and continuous excitation; modal coupling via mode shapes at drive point
- [[fem-bem-for-modal-synthesis]] — computing mode shapes and frequencies numerically from CAD + material data
- [[friction-synthesis]] — continuous rubbing/bowing sounds via nonlinear feedback loop on resonator bank
- [[gpu-modal-synthesis]] — massively parallel resonator bank on GPU; enables ~100k+ modes in real time
- [[impact-synthesis]] — impact sound from Hertz contact model + modal response; core use case of modal synth
- [[material-properties-and-modes]] — how E, rho, eta affect mode frequencies, damping, and perceptual character
- [[modal-analysis-measurement]] — experimental extraction of mode parameters via FRF + pole-fitting algorithms
- [[modal-synthesis-overview]] — top-level: physics-based synthesis by summing N decaying sinusoidal modes
- [[mode-shapes-and-eigenvalues]] — math of eigenmodes: K*phi = omega^2*M*phi; modal superposition; orthogonality
- [[realtime-modal-synthesis]] — CPU/GPU strategies, perceptual mode reduction, LOD, latency budget for interactive synthesis
- [[resonator-bank-implementation]] — N parallel biquad IIR filters implementing modal coordinates; cost and GPU SIMD
- [[rigid-body-sound-synthesis]] — real-time physics-engine + modal synth pipeline for games/VR
- [[nonlinear-modal-synthesis]] — mode coupling, collisions, tension modulation; energy-conserving numerical methods
- [[coupled-structures]] — string-bridge-body coupling, commuted synthesis, state-space multi-I/O approach
- [[ml-modal-parameter-estimation]] — neural mode prediction, differentiable modal synthesizers, audio-domain training
- [[radiation-and-directivity]] — radiation efficiency vs. mode shape, acoustic transfer, directivity patterns
- [[stochastic-modal-synthesis]] — SEA, high-frequency mode density, noise-band synthesis above mode resolution limit

## Comparisons
- [[waveguide-vs-modal]] — delay-line waveguide vs. eigenmode resonator bank: equivalence, tradeoffs, hybrid use

## Queries

# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-09-08 | Total pages: 22

## Entities
- [[entities/source-papers]] - distilled source-paper catalog (DAFx26 pass-1 ingestion)

### DAFx26 source-paper anchors
- [paper-tablas-differentiable-karplus-strong-2026](entities/source-papers.md#paper-tablas-differentiable-karplus-strong-2026) - differentiable extended Karplus-Strong sound matching; time-domain fractional delay gradients
- [paper-camara-articulatory-biphonic-singing-2026](entities/source-papers.md#paper-camara-articulatory-biphonic-singing-2026) - differentiable Kelly-Lochbaum copy-synthesis of Tuvan sygyt overtone singing
- [paper-smyth-loopback-fm-tvdl-2026](entities/source-papers.md#paper-smyth-loopback-fm-tvdl-2026) - loopback FM implemented with a time-varying delay line, wrapped without phase distortion
- [paper-zheng-yehu-physical-model-2026](entities/source-papers.md#paper-zheng-yehu-physical-model-2026) - finite-difference bowed-string model of the Chinese yehu with a measured modal bridge
- [paper-chowdhury-performance-oriented-wdf-2026](entities/source-papers.md#paper-chowdhury-performance-oriented-wdf-2026) - declarative circuit DSL and compiler emitting abstraction-free WDF code
- [paper-giampiccolo-fulltone-ocd-wdf-2026](entities/source-papers.md#paper-giampiccolo-fulltone-ocd-wdf-2026) - explicit CPWL wave digital model of the Fulltone OCD pedal
- [paper-giampiccolo-kan-vs-mlp-wdf-2026](entities/source-papers.md#paper-giampiccolo-kan-vs-mlp-wdf-2026) - KANs vs MLPs as the learned nonlinear-junction solver inside a WDF
- [paper-coppola-fast-parametric-fdn-matrices-2026](entities/source-papers.md#paper-coppola-fast-parametric-fdn-matrices-2026) - lossless FDN feedback matrices from recursive Kronecker products, O(N log N)
- [paper-dalsanto-nonlinear-shimmer-fdn-2026](entities/source-papers.md#paper-dalsanto-nonlinear-shimmer-fdn-2026) - five ways to put nonlinear/time-varying pitch shifting inside a stable FDN loop
- [paper-ibnyahya-differentiable-fdn-rir-2026](entities/source-papers.md#paper-ibnyahya-differentiable-fdn-rir-2026) - 16-line differentiable FDN fitted to measured RIRs by gradient descent
- [paper-abate-concatenation-driven-convolution-2026](entities/source-papers.md#paper-abate-concatenation-driven-convolution-2026) - concatenative output as an evolving IR; single-engine FFT kernel interpolation
- [paper-valentin-iris-ir-navigation-2026](entities/source-papers.md#paper-valentin-iris-ir-navigation-2026) - IRIS VST3 plugin for 2D navigation of impulse-response collections
- [paper-stonge-fdn-sandbox-sffdn-2026](entities/source-papers.md#paper-stonge-fdn-sandbox-sffdn-2026) - sfFDN real-time C++ FDN library plus the FDN Sandbox GUI and optimizers
- [paper-franchino-adac-differentiable-to-faust-2026](entities/source-papers.md#paper-franchino-adac-differentiable-to-faust-2026) - ADAC compiles trained differentiable audio graphs to FAUST with a stability certificate

## Concepts
- [[waveguide-overview]] — bidirectional delay line models for 1D wave propagation; d'Alembert solution
- [[scattering-junctions]] — reflection/transmission at impedance discontinuities; Kelly-Lochbaum; WDF adaptors
- [[delay-line-techniques]] — fractional delay, interpolation, variable delay, lossy propagation, dispersion filters
- [[string-modeling]] — plucked/struck/bowed strings; Karplus-Strong to piano; coupling and commuted synthesis
- [[bore-modeling]] — cylindrical/conical tubes; piecewise K-L model; tone holes; bell radiation
- [[reed-and-bow-models]] — nonlinear excitation: single reed, lip reed, air reed, bow-string friction
- [[artificial-reverberation]] — FDN, SDN, Schroeder reverberators; early/late decomposition
- [[waveguide-meshes]] — 2D/3D waveguide grids; dispersion; room acoustics and membrane simulation
- [[commuted-synthesis]] — LTI commutativity shortcut; precompute body IR, excite string with it
- [[banded-waveguides]] — closed wavetrains on 2D/3D objects modeled as 1D loops; cymbals, bells
- [[waveguide-vocal-models]] — Kelly-Lochbaum vocal tract, SPASM singing, 2D/3D mesh vocal models
- [[waveguide-parameter-optimization]] — physics-based, filter design, genetic, neural/DDSP calibration
- [[waveguide-history]] — timeline from d'Alembert (1747) through K-S (1983) to DDSP (2025)
- [[wave-digital-filters]] — lumped-element modeling via bilinear transform + wave variables; modularity
- [[wdf-adaptors]] — parallel/series adaptors; one-multiply form; N-port; dependent port
- [[wdf-elements]] — mass, spring, dashpot, transformer, gyrator, nonlinear elements; K-method
- [[wdf-applications]] — piano hammer, tonehole, analog circuit emulation, differentiable/neural WDFs
- [[viola-wdf-plugin-generator]] — VIOLA: automatic SPICE-to-VST pipeline via WDFs (Giampiccolo et al., JAES 2025)
- [[wdf-arbitrary-port-adaptation]] — general formula for adapting any junction port via MNA/Thévenin resistance
- [[wdf-r-type-adaptors]] — MNA-derived scattering for arbitrary (non-series/parallel) topologies (Werner et al., DAFx 2015)
- [[wdf-multiple-nonlinearities]] — SPQR + R-type root + K-method framework for multiple/multiport NLs (Werner et al., DAFx 2015)

## Comparisons
- See [[modal_synthesis/comparisons/waveguide-vs-modal]] for waveguide vs. modal synthesis comparison

## Queries

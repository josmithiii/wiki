# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Wave digital filters live in the sibling `waveguide_synthesis/` wiki (`wdf-*` pages).
> Last updated: 2026-09-10 | Total pages: 17

## Entities
- [[entities/source-papers]] - distilled source-paper catalog (DAFx26 pass-1 ingestion)
- [[hasy-asic]] - 65 nm ASIC computing the alias-free oscillator-sync spectral transform

### DAFx26 source-paper anchors
- [paper-mcclellan-time-varying-va-stability-2026](entities/source-papers.md#paper-mcclellan-time-varying-va-stability-2026) - CQLF stability proofs for time-varying trapezoidal VA filters
- [paper-oyama-moog-ladder-nonlinearity-2026](entities/source-papers.md#paper-oyama-moog-ladder-nonlinearity-2026) - SPICE-referenced comparison and stage ablation of five digital Moog ladders
- [paper-fontana-allpass-clipping-prevention-2026](entities/source-papers.md#paper-fontana-allpass-clipping-prevention-2026) - clipping prevention for time-varying first/second-order allpass filters
- [paper-zea-adaptive-multirate-qp-2026](entities/source-papers.md#paper-zea-adaptive-multirate-qp-2026) - residual-driven adaptive multi-rate QP solver for nonlinear circuit DAEs
- [paper-thompson-compressor-control-voltage-2026](entities/source-papers.md#paper-thompson-compressor-control-voltage-2026) - compressor evaluation against measured gain-reduction control voltage, plus SSL dataset
- [paper-gabrielli-polyadaa-2026](entities/source-papers.md#paper-gabrielli-polyadaa-2026) - ADAA with higher-order Lagrange reconstruction via Chebyshev polynomial approximation
- [paper-roth-alias-free-oscillator-sync-2026](entities/source-papers.md#paper-roth-alias-free-oscillator-sync-2026) - alias-free hard/soft oscillator sync by Fourier spectral resampling, with a 65 nm ASIC
- [paper-argentieri-arbitrary-polygon-oscillator-2026](entities/source-papers.md#paper-argentieri-arbitrary-polygon-oscillator-2026) - arc-length polygonal synthesis over arbitrary polygons, morphing, and sliced polyhedra
- [paper-dittmar-pulsetable-synthesis-2026](entities/source-papers.md#paper-dittmar-pulsetable-synthesis-2026) - pulsetable (pulse-forming) synthesis of wind tones, with a DDSP proposal
- [paper-tabata-fm-parameter-estimation-2026](entities/source-papers.md#paper-tabata-fm-parameter-estimation-2026) - FM ratio estimation using rational-ridge structure of the Wasserstein loss landscape
- [paper-braun-fm-shared-embeddings-2026](entities/source-papers.md#paper-braun-fm-shared-embeddings-2026) - DX7 graph neural network and joint audio/parameter embeddings for preset retrieval
- [paper-kallinen-deep-regularized-rnn-va-2026](entities/source-papers.md#paper-kallinen-deep-regularized-rnn-va-2026) - deep control-conditioned LSTMs plus gammatone loss for artifact-free time-varying control
- [paper-massi-fno-sample-rate-independent-va-2026](entities/source-papers.md#paper-massi-fno-sample-rate-independent-va-2026) - Fourier neural operators giving sample-rate-independent neural VA
- [paper-balasubramaniam-apple-silicon-neural-audio-2026](entities/source-papers.md#paper-balasubramaniam-apple-silicon-neural-audio-2026) - neural inference backends benchmarked under realistic DAW contention on Apple Silicon
- [paper-huang-snapdragon-gpu-neural-audio-2026](entities/source-papers.md#paper-huang-snapdragon-gpu-neural-audio-2026) - integrated-GPU neural audio inference benchmarks on Snapdragon
- [paper-sato-wavenet-pruning-ios-2026](entities/source-papers.md#paper-sato-wavenet-pruning-ios-2026) - 90% magnitude pruning plus a sparse engine runs a WaveNet amp model on iPhone CPU

## Concepts
- [[virtual-analog-overview]] - what VA covers, the method families, and where each DAFx26 paper fits
- [[tpt-zdf-filters]] - trapezoidal / bilinear discretization of state-space prototypes, and the zero-delay-feedback solve
- [[time-varying-filter-stability]] - common quadratic Lyapunov functions, the discretization theorem, SVF / Sallen-Key / ladder bounds
- [[moog-ladder-filter-models]] - ladder topology, lineage, and five implementations scored against a SPICE reference
- [[allpass-clipping-prevention]] - bounding modulated first/second-order allpass output by clamping the coefficient increment
- [[antiderivative-antialiasing]] - ADAA fundamentals: the antiderivative formula, its ill-conditioning, FIR/IIR kernels
- [[polyadaa]] - higher-order Lagrange reconstruction made tractable by Chebyshev approximation of the nonlinearity
- [[alias-free-oscillator-sync]] - hard/mirrored/pulsar sync as a linear spectral-resampling transform plus additive synthesis
- [[real-time-neural-inference-deployment]] - the callback-deadline model and Apple Silicon backends under DAW contention
- [[mobile-gpu-neural-audio]] - when a Snapdragon integrated GPU beats the CPU for streaming neural audio
- [[neural-model-compression]] - 90% iterative magnitude pruning plus a sparse engine for WaveNet amp models on iPhone
- [[state-space-circuit-solvers]] - nonlinear circuit DAEs as one convex QP per sample, with the nonlinear residual driving adaptive step size
- [[neural-va-architectures]] - stability-regularized control-conditioned LSTMs and the gammatone-filterbank loss
- [[fourier-neural-operators-va]] - frame-based FNOs giving VA models that run at sample rates they were not trained on

## Comparisons
- [[ladder-nonlinearity-ablation]] - saturator function versus placement versus which ladder stages stay nonlinear

## Queries

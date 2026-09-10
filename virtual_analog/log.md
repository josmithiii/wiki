# Activity Log

## [2026-09-08] create | virtual_analog sub-wiki scaffold + DAFx26 pass-1 ingestion
- Created SCHEMA.md (domain, 32k context budget, LaTeX math rule, frontmatter spec, VA tag taxonomy), index.md, log.md, and entities/ concepts/ comparisons/ queries/ raw/.
- Rationale: VA filters, ADAA, oscillators and neural VA are not waveguide material, so they get their own wiki; wave digital filters stay in waveguide_synthesis (wdf-* pages) and are cross-linked, not duplicated.
- Added virtual_analog to the "Active Wikis" list in ~/wiki/README.md and to SUBWIKIS in ~/wiki/Makefile.
- Ingested 16 DAFx26 sources (pass 1, catalog only) from /l/dttd/DAFx26/:
  paper_28 (McClellan, time-varying VA filter stability), paper_29 (Oyama, Moog ladder nonlinearity),
  paper_31 (Zea & Rivera, adaptive multi-rate QP), paper_47 (Gabrielli & Squartini, PolyADAA),
  paper_45 (Fontana et al., allpass clipping prevention), paper_26 (Kallinen et al., deep regularized RNNs),
  paper_27 (Massi et al., Fourier neural operators), paper_30 (Thompson & Heilemann, compressor control voltage),
  paper_49 (Roth et al., alias-free oscillator sync), paper_32 (Argentieri & Scagliola, arbitrary polygon oscillator),
  paper_37 (Tabata et al., FM parameter estimation), paper_33 (Braun & Finkelstein, FM shared embeddings),
  paper_16 (Balasubramaniam et al., Apple Silicon benchmarks), paper_18 (Huang et al., Snapdragon iGPU benchmarks),
  demo_67 (Sato & Silverstein, WaveNet pruning for iOS), demo_60 (Dittmar et al., pulsetable synthesis).
- Created entities/source-papers.md with those 16 catalog entries plus cross-reference-only entries for the three DAFx26 WDF papers (paper_23, paper_24, paper_25) that live in waveguide_synthesis.
- Created concepts/virtual-analog-overview.md (98 lines) orienting the method families.
- Copied the 16 text extractions into raw/ (gitignored) and wrote raw/MANIFEST.md and raw/SUMMARIES.md.
- Pass 2 (deep distillation of the three-star papers into dedicated concept pages) is pending.

## [2026-09-10] distill | DAFx26 pass 2 - core concept pages for virtual_analog
- Deep-read the full text of paper_28, paper_29, paper_45, paper_47, paper_49, paper_16, paper_18 and demo_67 (from /l/dttd/DAFx26/txt/, copies in raw/) and distilled them into 11 new pages, splitting where the 100-line budget required it.
- VA filter theory: concepts/tpt-zdf-filters.md (trapezoidal/bilinear state-space discretization and the ZDF solve, plus the one-pole worked example) and concepts/time-varying-filter-stability.md (CQLF definitions, equivalence with Laroche's matrix-norm criterion 2, the theorem that a continuous-time CQLF survives trapezoidal discretization with proof sketch, the filter-sweep corollary, and the SVF / Sallen-Key / Moog / diode-ladder results with their counterexamples at k = 2.89 and k = 8.91).
- Ladders: concepts/moog-ladder-filter-models.md (topology, the "1+4" saturation count, the Moog-to-D'Angelo lineage, the SPICE-referenced metric set, and the five-implementation table) plus concepts/ladder-nonlinearity-ablation.md (the common-core ablation, saturator function versus placement, and the earlier-stage result with the fidelity/cost rules).
- Allpass: concepts/allpass-clipping-prevention.md (first/second-order forms, the static-counterpart deviation identity, the coefficient-increment clamp, the half-budget split for second order, cost table, and the BIBO argument).
- Antialiasing: concepts/antiderivative-antialiasing.md (ADAA fundamentals, F_1 formula, the 0/0 branch, higher-order and IIR kernels) and concepts/polyadaa.md (Lagrange reconstruction, why no closed form exists, the Chebyshev/DCT-I solution with rectangular and triangular moments, the algorithm, and the SNR and timing tables).
- Oscillators: concepts/alias-free-oscillator-sync.md (hard sync, the pre-rotation plus sinc spectral-resampling transform in complex and real form, mirrored and pulsar sync with the versinc terms, complexity) and entities/hasy-asic.md (65 nm, 6 mm^2, 512 harmonics at 96 kHz/24 bit, 8240 cycles ~= five sample periods, CORDIC plus 32 column processors, SINAD figures, known control-logic bugs).
- Deployment: concepts/real-time-neural-inference-deployment.md (callback deadline versus RTF, the BNNSGraph/RTNeural/LibTorch/ONNX/anira comparison, and the Tracktion Engine contention results including the 158.5 % p99 / 355 xrun case at zero contention), concepts/mobile-gpu-neural-audio.md (Snapdragon QCS6490 five-model sweep, borrowed parallelism, inter-run GPU bimodality) and concepts/neural-model-compression.md (iterative local magnitude pruning at 90 % sparsity, the sparse iOS engine, RTF ~ 0.6 at block 256, int16-level match).
- Updated concepts/virtual-analog-overview.md so its method-family lists point at the new concept pages instead of only at catalog anchors; updated index.md (14 pages) accordingly.
- Not done in this pass: paper_26 / paper_27 (neural VA architectures) and paper_31 (QP circuit solver) remain catalog-only.

## [2026-09-10] distill | DAFx26 pass 2 addendum - optional papers
- After the six required topics were built and verified, distilled the three optional papers as well.
- paper_31 (Zea & Rivera) -> concepts/state-space-circuit-solvers.md: the state-space DAE form, the first-order linear surrogate for the nonlinear device constraint with Hurwitz K_k, the equality-constrained QP and its minimum-norm/pseudo-inverse collapse, the O(h^2) post-step residual as an adaptive defect indicator, and the SPICE-referenced results for the diode clipper, common-emitter amplifier and Colpitts oscillator with execution times.
- paper_26 (Kallinen et al.) -> concepts/neural-va-architectures.md: control-conditioning schemes, the LSTM stability constraints and their reparameterization, the spectral-norm variant, deep concatenation conditioning, the gammatone-filterbank loss, and the ESR/control-noise table showing that regularized models prefer depth to width.
- paper_27 (Massi et al.) -> concepts/fourier-neural-operators-va.md: the FNO layer and why fixed mode count gives sample-rate invariance, the frame-based windowed/overlap-add adaptation, the modified frequency-domain skip branch with spectral zero-pad oversampling, and the Big Muff Pi results at 24/48/88.2/96 kHz against the LIDL-RNN baseline (which cannot downsample at all).
- Linked all three from concepts/virtual-analog-overview.md and added them to index.md (18 pages).

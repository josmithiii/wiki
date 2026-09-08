---
title: Source Papers -- Distilled Catalog
created: 2026-09-08
updated: 2026-09-08
type: entity
tags: [reference, comparison, va-filters, neural-va, oscillator, real-time]
sources:
  - /l/dttd/DAFx26/README_JOS.md
  - /l/dttd/DAFx26/DAFx26_paper_16.pdf
  - /l/dttd/DAFx26/DAFx26_paper_18.pdf
  - /l/dttd/DAFx26/DAFx26_paper_26.pdf
  - /l/dttd/DAFx26/DAFx26_paper_27.pdf
  - /l/dttd/DAFx26/DAFx26_paper_28.pdf
  - /l/dttd/DAFx26/DAFx26_paper_29.pdf
  - /l/dttd/DAFx26/DAFx26_paper_30.pdf
  - /l/dttd/DAFx26/DAFx26_paper_31.pdf
  - /l/dttd/DAFx26/DAFx26_paper_32.pdf
  - /l/dttd/DAFx26/DAFx26_paper_33.pdf
  - /l/dttd/DAFx26/DAFx26_paper_37.pdf
  - /l/dttd/DAFx26/DAFx26_paper_45.pdf
  - /l/dttd/DAFx26/DAFx26_paper_47.pdf
  - /l/dttd/DAFx26/DAFx26_paper_49.pdf
  - /l/dttd/DAFx26/DAFx26_demo_60.pdf
  - /l/dttd/DAFx26/DAFx26_demo_67.pdf
---

# Source Papers -- Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>` ID used
in `index.md`, so inbound links like `[[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]]`
resolve inside this page. Blocks are distilled from the text extractions in
`raw/` (gitignored); see `raw/MANIFEST.md` for the filename-to-PDF mapping.

Unless noted otherwise, every entry below is from the *Proceedings of the 29th
International Conference on Digital Audio Effects (DAFx26), Cambridge, MA, USA,
1-4 September 2026*, and this is a **pass-1 catalog**: bullets are seeded from
the annotated bibliography at `/l/dttd/DAFx26/README_JOS.md` plus the abstract
and opening sections of each paper. Deep distillation into concept pages is
pass 2.

When any single paper needs deeper treatment than the bullet summary supports,
promote it to a dedicated `entities/paper-<slug>.md` file and leave the section
here as a cross-link.

---

## VA filter theory and stability

### paper-mcclellan-time-varying-va-stability-2026

**"Stability Analysis of Time-Varying Virtual Analog Filters"** - Russell McClellan (independent, Somerville MA) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_28.txt`

- Problem: musical VA filters discretize a continuous-time state-space prototype with trapezoidal integration (TPT/ZDF), but cutoff and resonance are modulated, so the running system is linear *time-varying* and ordinary frozen-coefficient pole analysis proves nothing about BIBO stability.
- Method: imports **common quadratic Lyapunov functions** (CQLFs) from the control-systems literature. Key theorem: a CQLF $V(x) = x^T P x$ valid for the continuous-time family is **preserved through trapezoidal discretization**, so stability can be proved in the simpler continuous-time domain and inherited by the digital filter.
- Results: new stability proofs for the **state-variable filter** and the **Sallen-Key filter** under arbitrary time-varying parameters, and new bounds on the stable time-varying parameter range for the **Moog ladder** and **diode ladder**; counterexamples show the bounds are close to tight.
- This is the rigorous answer to "is it safe to modulate cutoff at audio rate", which practitioners usually settle empirically.
- Relates to [[virtual-analog-overview]] (TPT/ZDF family) and to the energy/passivity arguments used for [[wave-digital-filters]] in the waveguide wiki, which get stability from passivity rather than from a Lyapunov certificate.
- Limitation: a CQLF is sufficient, not necessary - failure to find one does not prove instability, and the ladder bounds are conservative.
- Tags: va-filters, tpt-zdf, stability, time-varying, ladder-filter, state-variable, reference

### paper-oyama-moog-ladder-nonlinearity-2026

**"Quantifying Nonlinear Behavior in Digital Moog Ladder Filters: Cross-Implementation Comparison and Common-Core Ablation"** - Hiroyuki Oyama (independent, Tokyo) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_29.txt`

- Problem: digital Moog ladders are habitually compared by linear frequency response, which hides the musically important differences that only appear under saturation.
- Method: an open, reproducible **SPICE-referenced** evaluation framework with two parts - (1) five existing digital ladder implementations scored against one common SPICE reference, and (2) a controlled **common-core ablation** on a SPICE-referenced TPT/ZDF core in which individual stage nonlinearities are removed.
- Result 1: close linear agreement can mask substantial nonlinear divergence between implementations.
- Result 2: nonlinear behavior depends not only on saturator choice and placement but on *which* of the four ladder stages carries it - retaining the **earlier-stage** nonlinearities preserves harmonic behavior better than retaining only later-stage ones.
- Lineage cited: Stilson & Smith 1996, Rossum, Huovilainen, Fontana, Zavalishin, D'Angelo & Valimaki.
- Useful as the fidelity-versus-cost reference when simplifying nonlinear structure for embedded targets.
- Limitation: one filter family, one SPICE reference; perceptual relevance of the divergence measures is not established by listening tests.
- Tags: ladder-filter, va-filters, tpt-zdf, spice, nonlinear, benchmark, comparison

### paper-fontana-allpass-clipping-prevention-2026

**"A Clipping Prevention Method for All-Pass Digital Filters with Time-Varying Coefficients"** - Federico Fontana (Udine), Silvia Pasin, Alberto Bernardini (Politecnico di Milano), Stefano D'Angelo (Orastron) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_45.txt`

- Problem: first- and second-order allpass sections with modulated coefficients can overshoot unit magnitude even when the input never clips - the usual energy-preserving structures do not bound the output during coefficient transients.
- Method: control the **deviation** between the output of the time-varying allpass and that of an equivalent *static* allpass with frozen coefficients, and adaptively limit that deviation at runtime so the output stays below a prescribed threshold (typically $|y| \le 1$).
- The limiter is active only during the short transients where clipping would occur; afterwards coefficients are released to reach their target values, preserving the numerical properties of the allpass.
- Requires no assumption about internal energy evolution - only that the input is not already clipping.
- Cheap enough for embedded audio hardware; directly relevant to modulated allpass chains in phasers and in [[artificial-reverberation]] allpass diffusers.
- Limitation: derived for first- and second-order sections; behavior of long cascades and of the resulting (mild) transient nonlinearity is not perceptually evaluated.
- Tags: allpass, time-varying, stability, va-filters, embedded, real-time

---

## Circuit-level and grey-box modeling

### paper-zea-adaptive-multirate-qp-2026

**"Residual-Driven Adaptive Multi-Rate Quadratic Programming Framework for Nonlinear Analog Audio Circuit Emulation"** - Miguel Zea, Luis A. Rivera (Universidad del Valle de Guatemala) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_31.txt`

- Starts from a state-space **differential algebraic equation** (DAE) circuit formulation and replaces the nonlinear device relations inside a convex **quadratic program** by a first-order surrogate linear constraint, so each time step is a single QP solve rather than a Newton iteration plus a separate integration update.
- The post-step **nonlinear residual** is shown to be a valid defect indicator, and drives adaptive step-size control - hence "residual-driven adaptive multi-rate".
- Evaluated against SPICE on a diode clipper, a BJT common-emitter amplifier, and a **Colpitts oscillator** (i.e. it survives a self-oscillating circuit, not just a memoryless clipper).
- Adaptive step sizing considerably improves agreement with SPICE; a pseudo-inverse implementation is essentially equivalent to the full equality-constrained QP on these cases.
- Positioned as a bridge between SPICE-like interpretability and VA efficiency; the constraint-stabilization idea is borrowed from rigid-body dynamics.
- Contrast with the wave-variable route in [[wave-digital-filters]] and with the K-method/Newton solvers in [[wdf-multiple-nonlinearities]].
- Limitation: no real-time benchmark reported; multi-rate scheduling cost in an audio callback is untested.
- Tags: circuit-modeling, state-space, spice, nonlinear, oscillator, reference

### paper-thompson-compressor-control-voltage-2026

**"Evaluating Dynamic Range Compressor Models Using Control-Voltage Measurements: An Approach and Dataset"** - Benjamin R. Thompson, Michael C. Heilemann (University of Rochester) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_30.txt`

- Problem: the quantity that defines a compressor is its time-varying gain, but recovering that gain from input/output audio alone is an ill-conditioned inverse problem, so models are scored with waveform-domain proxy metrics.
- Method: instrument the hardware and capture the **gain-reduction control voltage** directly alongside audio, then score a model's gain trajectory against the measured control voltage.
- Result: grey-box models trained on proxy losses did **not** reach parity with a model trained directly on the gain control signal when judged by the control trajectory; waveform-domain metrics assigned similar errors to models the direct metric clearly separated.
- Deliverable: a released **Solid State Logic bus compressor dataset** with the gain control voltage captured alongside the audio output.
- Methodologically the strongest argument at DAFx26 for measuring the internal control signal rather than only the terminals.
- Limitation: one device, one topology (VCA bus compressor); control-voltage access requires opening the unit, so the method does not generalize to arbitrary hardware.
- Tags: compressor, dataset, grey-box, benchmark, circuit-modeling, reference

---

## Antialiasing and oscillators

### paper-gabrielli-polyadaa-2026

**"PolyADAA: Improving Aliasing Reduction in Memoryless Nonlinearities Using Lagrange Interpolation and Polynomial Approximation"** - Leonardo Gabrielli, Stefano Squartini (Universita Politecnica delle Marche) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_47.txt`

- Observation: the accuracy bottleneck in **antiderivative antialiasing** (ADAA) is no longer the antiderivative order but the discrete-to-continuous reconstruction, which classical ADAA fixes at **linear** (order-1 Lagrange) interpolation.
- Method: derive the ADAA output for **higher-order Lagrange** reconstruction. There is no general closed form for an arbitrary nonlinearity, so the nonlinearity $f(x)$ is first approximated by **Chebyshev polynomials**, which makes the ADAA integral analytically tractable term by term.
- Numerical examples show substantially lower aliasing than standard ADAA at comparable order, with the usual ADAA trade-offs (a small lowpass bias and a transient at low input levels) discussed.
- Natural companion to oversampling: a way to buy aliasing suppression without raising the sample rate, relevant to saturators, waveshapers and oscillators alike.
- See [[virtual-analog-overview]] for where ADAA sits among the antialiasing options.
- Limitation: memoryless nonlinearities only; the Chebyshev fit adds design-time work per nonlinearity and per amplitude range.
- Tags: adaa, antialiasing, nonlinear, oversampling, va-filters, reference

### paper-roth-alias-free-oscillator-sync-2026

**"Alias-Free Oscillator Synchronization via Additive Synthesis"** - Jonas Roth, Domenic Keller, Oscar Castaneda, Christoph Studer (ETH Zurich) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_49.txt`

- Problem: oscillator sync (a slave oscillator reset by a master) is a staple analog-synth timbre whose naive digital implementation aliases badly, because the reset introduces a discontinuity at an arbitrary sub-sample instant.
- Method: work entirely in the **Fourier series**. Starting from a finite set of coefficients for a bandlimited free-running waveform, derive **linear spectral-resampling transforms** that map those coefficients to the coefficients of the bandlimited *synchronized* waveform - alias-free by construction rather than by correction.
- Supports conventional **hard sync** plus two additional **soft-sync** modes.
- Hardware: **HASY**, a 6 mm$^2$ ASIC in 65 nm CMOS that generates one 96 kHz, 24-bit alias-free synchronized waveform with up to **512 harmonics** and computes the spectral-resampling transform within five audio-sample periods.
- Contrast with the correction-based family (BLEP/BLAMP, polyBLEP) and with ADAA in [[entities/source-papers#paper-gabrielli-polyadaa-2026]]; also catalogued from the additive-synthesis side in the spectral wiki.
- Limitation: cost scales with the harmonic count, which is why a tapeout was needed; on a general-purpose CPU the method is expensive for low-pitched, harmonic-rich waveforms.
- Tags: oscillator-sync, oscillator, additive, antialiasing, asic, real-time

### paper-argentieri-arbitrary-polygon-oscillator-2026

**"Arbitrary Polygon Oscillator: Generalizing Polygonal Synthesis to Arbitrary Shapes, Morphing, and Three-Dimensional Polyhedra"** - Antonio Argentieri, Francesco Scagliola (Conservatorio di Bari) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_32.txt`

- Polygonal synthesis traverses a polygon perimeter with a phasor; prior formulations use constant *angular* velocity on regular parametric polygons. This work adopts constant **arc-length (perimeter) velocity** and a unified engine that accepts vertex data of any origin.
- Three generalizations: (1) arbitrary vertex buffers, so irregular and star-shaped closed polygons become waveform generators; (2) a hybrid interpolation algorithm that morphs between polygons with **unequal vertex counts**, passing through shapes with no parametric description; (3) a 3-D extension where a convex polyhedron rotated about three axes is sliced by a fixed horizontal plane, the cross-section giving a continuously variable polygon.
- Antialiasing: four-point **polyBLAMP** correction derived from runtime Bezier tangents (so no per-shape analytical derivation) plus adaptive oversampling.
- Implemented in RNBO (Cycling '74) with geometry caching to avoid per-sample recomputation.
- Limitation: no formal aliasing measurements against a bandlimited reference are quoted in the abstract; the polyBLAMP correction is geometric rather than exact.
- Tags: oscillator, polyblep, antialiasing, oversampling, wavetable

### paper-dittmar-pulsetable-synthesis-2026

**"Pulsetable Synthesis of Wind Instrument Tones"** - Christian Dittmar, Simon Schwar, Manuel Peters, Stefan Balke, Meinard Muller (Fraunhofer IIS / AudioLabs Erlangen) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_60.txt`

- Revives **pulse-forming** synthesis (Fricke and Voigt's Variophon lineage): sound production is modeled as periodic repetition of a shaped pulse that carries the instrument's spectral envelope.
- Single-cycle waveforms ("pulses") are stored in **pulsetables indexed by fundamental frequency**; synthesis reads them periodically and then applies time-varying lowpass filtering, amplification and reverberation.
- Control is by three contours - $f_0$, brightness, loudness - whose interplay produces attack transients, vibrato and growl; case studies use real wind-instrument recordings.
- Explicitly proposes the framework as a **DDSP** synthesizer whose parameters a neural network could learn from data.
- Includes a useful historical section (Fransson's bassoon circuits, Martinetta, Yamaha VL1); related in spirit to FOF/formant-wave and pulsar synthesis, and complementary to the physical wind models in [[bore-modeling]].
- Limitation: demo paper - no quantitative or listening evaluation, and the DDSP integration is proposed, not built.
- Tags: wavetable, oscillator, additive, differentiable, tutorial, history

---

## FM synthesis and parameter estimation

### paper-tabata-fm-parameter-estimation-2026

**"FM Parameter Estimation with Low-Order Rational Constraints on Wasserstein Loss Landscape"** - Ryoya Tabata, Masaki Iwaya, Kazunobu Kondo (Yamaha) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_37.txt`

- Problem: recovering FM frequency parameters from a target sound is hard because distinct parameter settings give similar spectra, producing many local minima in the loss landscape.
- Analysis: for two-operator FM under practical FFT-based spectral representations, the **Wasserstein (optimal-transport) distance** landscape has **non-differentiable ridges at rational frequency ratios**, arising from negative-frequency folding and spectral ordering transitions.
- Method: exploit that structure - constrain the frequency ratio in each optimization run to the interval bounded by two consecutive low-order rationals, run gradient descent inside each interval, and keep the lowest-loss candidate across intervals.
- Ablations show that *maintaining* the constraint throughout optimization beats random initialization and beats constraining only the initialization, with the gap widening at higher modulation index.
- Companion to [[entities/source-papers#paper-braun-fm-shared-embeddings-2026]] on the retrieval side of the same inverse problem.
- Limitation: two-operator FM only; extension to six-operator DX7-class topologies is not demonstrated.
- Tags: fm-synthesis, parameter-estimation, differentiable, oscillator

### paper-braun-fm-shared-embeddings-2026

**"FM Synthesizer Audio-Parameter Shared Embeddings"** - David Braun, Adam Finkelstein (Princeton) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_33.txt`

- Problem: preset retrieval ("find the patch that makes this sound") normally treats synthesis parameters as a flat vector, throwing away signal routing and parameter interaction.
- Contribution 1: a **graph neural network** whose message-passing structure imitates FM signal flow - operators as nodes, modulation as edges, feedback as an attenuated edge. Message-passing weights are shared across all nodes and layers, so arbitrary topologies of any size can be encoded.
- Contribution 2: a SLAP/CLAP-style multimodal contrastive objective learning **joint embeddings of audio and FM parameters**, enabling audio-to-preset retrieval from a gallery.
- Target: Yamaha **DX7** - six identical sinusoid operators wired by one of 32 routing algorithms. With all topologies seen in training, DX7-GNN and two baselines all retrieve well; with topologies **held out**, DX7-GNN substantially outperforms both baselines while having the fewest parameters.
- Ablations support the claim that imitating FM signal flow in the parameter encoder is what buys generalization to unseen routings.
- Limitation: retrieval from a fixed gallery, not free parameter regression; envelope and performance parameters are secondary to routing in this formulation.
- Tags: fm-synthesis, parameter-estimation, graph-neural-network, neural-va, dataset

---

## Neural and grey-box VA

### paper-kallinen-deep-regularized-rnn-va-2026

**"Deep Regularized RNNs for Virtual Analog Modeling"** - V. Valtteri Kallinen, Lauri Juvela (Aalto University), Thom Sherson (Neural DSP) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_26.txt`

- Context: RNNs (LSTM/GRU) are the workhorse of **black-box** VA. Device controls are supplied as conditioning inputs, but when the conditioning is **time-varying** (a knob being turned) the models emit audible noise artifacts.
- Known fix: regularize the RNN dynamics toward asymptotic stability - which removes the artifacts but costs modeling accuracy.
- Contribution: close that quality gap with (1) **deep control-conditioned LSTMs** and (2) a **gammatone filterbank (GFB) loss** in place of a plain spectral loss.
- Result: the regularized models reach comparable accuracy to unregularized baselines while remaining artifact-free under time-varying control.
- Sits in the black-box corner of the taxonomy laid out in [[virtual-analog-overview]] (white-box / grey-box / black-box).
- Limitation: stability regularization is still a soft constraint, not a certificate in the sense of [[entities/source-papers#paper-mcclellan-time-varying-va-stability-2026]].
- Tags: neural-va, rnn, stability, time-varying, amplifier, real-time

### paper-massi-fno-sample-rate-independent-va-2026

**"Fourier Neural Operators for Sample-Rate-Independent Virtual Analog Modeling"** - Oliviero Massi, Alessandro Ilic Mezza, Alberto Bernardini (Politecnico di Milano) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_27.txt`

- Problem: a time-domain neural VA model implicitly encodes its training sample rate in its weights, so running it at another rate changes the realized dynamics. Existing sample-rate-independent RNN modifications are tailored to **upsampling** and do not handle downsampling.
- Method: a **Fourier Neural Operator** (FNO) adapted to fixed-duration audio frames. The learned map is defined over a fixed *temporal support* and evaluated on uniform grids of different densities, so one trained model applies at unseen sampling resolutions in either direction.
- Result on a nonlinear transistor circuit: competitive accuracy in upsampling scenarios and directly applicable to **downsampling**, where the sample-rate-independent recurrent baseline is not.
- Principled answer to a practical deployment headache (the DAW runs at 44.1, 48, 96 or 192 kHz; the model was trained at one of them).
- Limitation: frame-based, so not a lowest-latency architecture; one circuit tested.
- Tags: neural-va, fno, circuit-modeling, nonlinear, real-time

---

## Real-time deployment of neural audio

### paper-balasubramaniam-apple-silicon-neural-audio-2026

**"Real-Time Neural Audio on Apple Silicon: Benchmarking Inference Frameworks Under Realistic DAW Contention"** - Dharanipathi Rathna Kumar Balasubramaniam, Saravanabalagi Ramachandran, Joseph Timoney (Maynooth University) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_16.txt`

- Problem: neural plugin inference libraries (RTNeural, anira) prioritize portability, leaving macOS/Apple Silicon performance on the table; and published benchmarks measure models **in isolation**, not sharing a CPU with a full mix.
- Method: benchmark **BNNSGraph**, RTNeural, LibTorch, ONNX Runtime and anira on architectures common in neural audio plugins, inside a **Tracktion Engine** harness that builds mix sessions with configurable plugin load alongside the neural plugin, sweeping buffer size and contention level.
- Apple's BNNSGraph compiles the whole model graph ahead of time (operation fusion, weight repacking, memory-copy elimination) and targets the on-chip matrix co-processors; it is designed for real-time use, so it can run **on the audio thread** without anira's buffering/worker-thread scheme.
- Reported quantities are **tail latency and deadline violations** rather than mean throughput - the right metric for a callback - and the study asks whether isolated rankings survive realistic contention.
- Also a good summary of why GPU/NPU paths are generally not callback-safe.
- Limitation: macOS/Apple Silicon only; results are architecture- and model-size-specific.
- Tags: real-time, apple-silicon, benchmark, neural-va, plugin

### paper-huang-snapdragon-gpu-neural-audio-2026

**"Benchmarking Integrated GPU Acceleration of Real-Time Neural Audio Inference on Snapdragon"** - Avery Huang, Gautham Srinivasan, Akito van Troyer, Victor Zappi (Northeastern University / Berklee) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_18.txt`

- Question: can the **integrated GPU** of a mobile SoC accelerate streaming neural audio under per-callback deadlines?
- Method: five models spanning **769 parameters** (an oscillator) to **6 million** (a convolutional autoencoder), deployed in a custom C++ audio engine on a Qualcomm **Snapdragon** SoC via the QNN SDK, sweeping batch and block sizes, CPU versus GPU.
- Findings characterize when iGPU acceleration wins, when **per-call overhead** cancels the benefit, and how model size and architecture determine GPU suitability; makes the throughput-versus-deadline distinction that a single "real-time factor" number hides.
- Because the Snapdragon family shares hardware and toolchain across boards, phones and laptops, the trends are argued to transfer beyond the tested device.
- Mobile companion to [[entities/source-papers#paper-balasubramaniam-apple-silicon-neural-audio-2026]].
- Limitation: one vendor's SDK; no plugin-host contention scenario as in the Apple Silicon study.
- Tags: real-time, gpu, embedded, benchmark, neural-va

### paper-sato-wavenet-pruning-ios-2026

**"WaveNet-Style Guitar Amplifier Model Pruning for Real-Time iOS Deployment"** - Ryota Sato, Eli Silverstein (Stanford EE) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_67.txt`

- Problem: WaveNet-style convolutional amp/pedal models are accurate but expensive, which has confined them to desktops or dedicated DSP hardware.
- Method: **iterative magnitude pruning** removes **90% of the network weights** with no perceptible quality loss, plus a custom **sparse C++ inference engine** that converts the sparsity into actual compute savings rather than zero-multiplies.
- Result: sustained low-latency real-time operation on a **CPU-only iPhone** implementation where the dense model cannot run; on-device output matches the trained model to within **int16 quantization error**.
- Demo format: visitors play a guitar through the iPhone app and A/B the pruned on-device model against the physical pedal it emulates. Code at `https://github.com/ryos17/wavenet-imp`.
- Complements the framework benchmarks above: pruning attacks the model, not the runtime.
- Limitation: demo paper; no formal listening test behind "no perceptible loss", and the sparse engine's advantage depends on the achievable sparsity pattern.
- Tags: pruning, wavenet, neural-va, ios, real-time, amplifier, plugin

---

## Wave digital filter papers (catalogued in `waveguide_synthesis`)

DAFx26's three wave-digital papers are VA papers by topic, but WDFs are covered
canonically in the waveguide wiki (see [[wave-digital-filters]] and
[[wdf-applications]]), so they are catalogued there and only cross-referenced here.

- **Performance-Oriented Wave Digital Circuit Emulation** (Chowdhury & Rau, MIT) - declarative circuit DSL plus a compiler emitting abstraction-free WDF code: [[waveguide_synthesis/entities/source-papers#paper-chowdhury-performance-oriented-wdf-2026]]
- **Explicit Wave Digital Model of the Fulltone OCD Pedal** (Giampiccolo et al., PoliMi) - CPWL approximation of a grouped MOSFET/germanium clipping stage giving an explicit, iteration-free WDF: [[waveguide_synthesis/entities/source-papers#paper-giampiccolo-fulltone-ocd-wdf-2026]]
- **KANs vs MLPs for VA Modeling in WDFs** (Giampiccolo et al., PoliMi / Arturia) - Kolmogorov-Arnold networks as the nonlinear-junction solver inside a WDF, matching MLP accuracy with about 70% fewer parameters: [[waveguide_synthesis/entities/source-papers#paper-giampiccolo-kan-vs-mlp-wdf-2026]]

---
title: Source Papers -- Distilled Catalog
created: 2026-09-08
updated: 2026-09-10
type: entity
tags: [reference, comparison, waveguide, reverb, fdn, differentiable]
sources:
  - /l/dttd/DAFx26/README_JOS.md
  - /l/dttd/DAFx26/DAFx26_paper_01.pdf
  - /l/dttd/DAFx26/DAFx26_paper_04.pdf
  - /l/dttd/DAFx26/DAFx26_paper_05.pdf
  - /l/dttd/DAFx26/DAFx26_paper_10.pdf
  - /l/dttd/DAFx26/DAFx26_paper_23.pdf
  - /l/dttd/DAFx26/DAFx26_paper_24.pdf
  - /l/dttd/DAFx26/DAFx26_paper_25.pdf
  - /l/dttd/DAFx26/DAFx26_paper_35.pdf
  - /l/dttd/DAFx26/DAFx26_paper_36.pdf
  - /l/dttd/DAFx26/DAFx26_paper_38.pdf
  - /l/dttd/DAFx26/DAFx26_paper_39.pdf
  - /l/dttd/DAFx26/DAFx26_paper_43.pdf
  - /l/dttd/DAFx26/DAFx26_demo_61.pdf
  - /l/dttd/DAFx26/DAFx26_demo_68.pdf
  - /l/dttd/DAFx26/DAFx26_demo_71.pdf
  - /l/dttd/DAFx26/DAFx26_demo_73.pdf
---

# Source Papers -- Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>` ID used
in `index.md`, so inbound links like
`[[entities/source-papers#paper-smyth-loopback-fm-tvdl-2026]]` resolve inside
this page. Blocks are distilled from the text extractions in `raw/`
(gitignored); see `raw/MANIFEST.md` for the filename-to-PDF mapping.

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

## Strings, tubes and voice

### paper-tablas-differentiable-karplus-strong-2026

**"Sound Matching with a Differentiable Karplus-Strong Algorithm"** - Pablo Tablas de Paula, David Marttila, Rodrigo Diaz, Iran Roman, Emmanouil Benetos, Joshua D. Reiss (Queen Mary University of London) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_38.txt`

- Self-supervised, **event-based** sound matching with a differentiable *extended* Karplus-Strong decoder in the Jaffe-Smith sense (damping, decay, pluck position, dynamics), avoiding external onset and $f_0$ detectors where possible.
- Key DSP finding: **time-domain fractional-delay interpolation** gives gradient accuracy comparable to frequency-sampling delay implementations while avoiding time-aliasing in highly resonant, time-varying settings - i.e. delay-line length really is differentiable in the time domain. See [[delay-line-techniques]].
- Key training finding: standard **spectral losses provide no meaningful directional gradient for onset times**, which badly degrades joint training of onsets with everything else.
- Training exclusively with parameter losses on synthetic data learns $f_0$, timbral parameters and onset times, but does not generalize to monophonic studio recordings of plucked guitar; external detectors plus audio losses generalize best, reducing the model's job to timbre optimization.
- Honest negative result: harmonics-plus-noise baselines still win on most reconstruction metrics, though the KS decoder recovers interpretable parameters and captures pluck transients naturally.
- Relates to [[string-modeling]] (extended KS) and [[waveguide-parameter-optimization]] (DDSP-style fitting); cautionary data for any differentiable string-model fitting.
- Tags: string, guitar, delay-line, differentiable, ml, optimization, comparison

### paper-camara-articulatory-biphonic-singing-2026

**"Differentiable Articulatory Copy-Synthesis of Biphonic Singing"** - Mateo Camara, Maria Pilar Daza-Llin, Fernando Marcos-Macias, Jose Luis Blanco (Universidad Politecnica de Madrid) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_39.txt`

- Target: *sygyt*, the Tuvan biphonic style in which a low drone is sustained while one harmonic in the 1-3 kHz region is selectively amplified. Standard low-dimensional tract parameterizations cannot produce the required narrowly focused resonance.
- Method: a **differentiable Kelly-Lochbaum waveguide** vocal tract (see [[waveguide-vocal-models]] and [[scattering-junctions]]) augmented with a **sublingual second source**, a **cubic B-spline** area-function parameterization, and **spatially varying learnable damping**, all optimized end-to-end by gradient descent from audio.
- Data: 20 segments from two independent sygyt datasets (5 singers, 10 pitches).
- Result: **30-38% reduction in log-spectral distance** relative to an articulatory baseline, with the largest gains in the overtone region; cepstral-envelope analysis shows more accurate recovery of the merged formant structure characteristic of sygyt.
- Also beats a DDSP harmonic-plus-noise baseline that has direct per-harmonic spectral control - the paper's argument that **explicit acoustic structure is a useful inductive bias**.
- Limitation: copy-synthesis of sustained segments, not a controllable singing synthesizer; the sublingual source is a modeling device whose physiological status is not established.
- Tags: voice, waveguide, scattering, differentiable, ml, optimization, acoustics

### paper-smyth-loopback-fm-tvdl-2026

**"Loopback Frequency Modulation Using a Time-Varying Delay Line"** - Tamara Smyth (UC San Diego) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_36.txt`

- Loopback FM (LBFM) is an oscillator that modulates **its own frequency**; this paper implements it with a **time-varying delay line** (TVDL), the same object used for pitch shifting, chorus and vibrato.
- A TVDL time-warps its input according to the delay function, altering instantaneous frequency and phase. Oscillatory delay functions stay bounded, but a **sustained** change in sounding frequency requires a delay term **linear in time**, bounded only by the input length.
- In LBFM the phase has both linear and oscillating terms, so the delay grows without bound; naive wrapping of the delay function or cross-fading between multiple TVDLs produces audible artifacts.
- Contribution: an alternate **closed-form representation of the LBFM oscillator** supplies exactly the information needed to wrap the delay function correctly and keep it bounded, giving output free of phase distortion and artifacts.
- Short and squarely in [[delay-line-techniques]] territory; continues Smyth's feedback-oscillator line of work.
- Limitation: single-oscillator treatment; no cost comparison against direct closed-form synthesis of the same signal.
- Tags: delay-line, waveguide, dsp, nonlinear, tutorial

### paper-zheng-yehu-physical-model-2026

**"Physical Model of the Chinese Yehu for Sound Synthesis"** - Zhen Zheng, Champ C. Darabundit, Gary Scavone (McGill University) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_43.txt`

- The yehu is a Chinese bowed string instrument with a coconut-shell resonator, a seashell bridge and two silk strings.
- Model: **finite-difference** scheme with two stiff strings coupled at the bridge, a bow with **elastic bow hairs**, a stopping finger, and a **modal model of the bridge** derived from measured bridge admittance (compare [[modal-analysis-measurement]] and [[coupled-structures]]).
- Solvers: **energy quadratization** gives a non-iterative solver for the finger-string contact force; an iterative solver handles **elasto-plastic** bow-string friction (see [[reed-and-bow-models]]).
- The measured **radiation transfer function** is realized as a bank of parallel second-order filters and applied to the simulated bridge force.
- Computational performance tests show the model runs in **real time**.
- Contrast with the waveguide route to bowed strings: this is FD/modal rather than delay-line, so it is the natural comparison case for [[waveguide-vs-modal]].
- Limitation: measurement-based characterization of one instrument; no listening test or comparison against recordings is quoted.
- Tags: string, physical-modeling, modal-synthesis, damping, acoustics, realtime

---

## Wave digital filters and circuit emulation

These three are virtual analog papers by topic; the VA context is catalogued in
`virtual_analog/` and the WDF specifics stay here with [[wave-digital-filters]]
and [[wdf-applications]].

### paper-chowdhury-performance-oriented-wdf-2026

**"Performance-Oriented Wave Digital Circuit Emulation"** - Jatin Chowdhury, Mark Rau (MIT) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_23.txt`

- Problem: WDFs are ideal for reusable software (see [[wdf-adaptors]], [[wdf-elements]]), but existing libraries pay heavily for run-time abstraction - virtual dispatch, pointer chasing, poor data layout.
- Method: a **static code generation** toolchain - a declarative circuit description language, a compiler that emits circuit simulation code with **minimal persistent state and no run-time abstraction**, and a minimal runtime library implementing specialized components as WDFs.
- Result: across several test circuits the generated models consistently outperform existing implementations (RT-WDF, FAUST `wdmodels`, `chowdsp_wdf`) and approach a **theoretical execution bound** derived for the circuit.
- Same "compile away the abstraction" argument as source-to-source DSP compilers; a useful reference point for FAUST-to-C++ translation work.
- Author is the `chowdsp_wdf` author, so the comparison against his own earlier library is credible.
- Limitation: linear/explicit circuit classes benefit most; the paper does not claim to remove the cost of iterative nonlinear solvers.
- Tags: waveguide, scattering, dsp, realtime, faust, comparison, reference

### paper-giampiccolo-fulltone-ocd-wdf-2026

**"Explicit Wave Digital Model of the Fulltone OCD Pedal Based on Canonical Piecewise-Linear Functions"** - Riccardo Giampiccolo, Stefano Polimeno, Carlo Macri, Alice Lenoci, Oliviero Massi, Alberto Bernardini (Politecnico di Milano) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_24.txt`

- Target: the Fulltone OCD (v2) overdrive, whose asymmetric clipping stage contains MOSFETs plus a germanium diode.
- Method: exploit the circuit topology to **group the MOSFETs and the diode into a single equivalent nonlinear element**, which makes an **explicit** wave digital realization possible - no iterative solver in the loop (contrast [[wdf-multiple-nonlinearities]]).
- The grouped nonlinear characteristic is approximated by a **canonical piecewise-linear (CPWL)** function, giving a compact and cheap explicit scattering relation.
- Validated against reference (SPICE-class) simulations and implemented both in MATLAB and as a real-time **JUCE** plug-in.
- Fits the pipeline story of [[viola-wdf-plugin-generator]]: schematic to WDF to plug-in, here done by hand with a topology-specific simplification.
- Limitation: the grouping trick is circuit-specific; CPWL accuracy near the clipping knees bounds the fidelity.
- Tags: waveguide, scattering, nonlinear, dsp, realtime, guitar

### paper-giampiccolo-kan-vs-mlp-wdf-2026

**"A Comparative Study of Kolmogorov-Arnold Networks and Multi-Layer Perceptrons for Virtual Analog Modeling in Wave Digital Filters"** - Riccardo Giampiccolo, Enrico Torres, Mauro G. De Bari, Samuel Limier, Alberto Bernardini (Politecnico di Milano / Arturia) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_25.txt`

- Context: hybrid grey-box WDFs already use an **MLP** to learn the scattering relation of a multiport nonlinear junction, keeping the model fully explicit (see [[wdf-applications]], neural/differentiable WDF section).
- This paper substitutes **Kolmogorov-Arnold Networks**, which parameterize the *activation functions* (learned splines on edges) instead of relying on learned weight matrices.
- Result: for the case study, KANs match MLP accuracy with roughly **70% fewer parameters**, at the cost of **increased computational complexity** per evaluation.
- Reading: KANs are attractive when memory footprint dominates (embedded targets, or circuits with many nonlinear elements); MLPs remain preferable when compute dominates.
- Limitation: a single case study; no real-time plug-in benchmark, and the compute penalty is not quantified against a per-sample budget.
- Tags: waveguide, scattering, nonlinear, ml, comparison, dsp

---

## Artificial reverberation: FDNs, differentiable reverb, convolution

### paper-coppola-fast-parametric-fdn-matrices-2026

**"Fast Parametric Matrices for Lossless Feedback Delay Networks"** - Andrea Coppola (Arturia) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_04.txt`

- Builds FDN feedback matrices as **recursive Kronecker products of $2 \times 2$ rotation and reflection kernels**, each kernel parameterized by a single angle $\theta_i$.
- This yields a family of orthogonal (hence lossless) $2^M \times 2^M$ matrices with **continuous control over network topology**, spanning from Householder/Hadamard-like mixing to nearly decoupled sub-networks.
- The recursive structure gives an $O(N \log_2 N)$ divide-and-conquer feedback operation, matching **fast Walsh-Hadamard transform** complexity while remaining parametric.
- Sound design payoffs: stereo cross-coupling, **selective freeze**, and time-varying angle modulation for resonance breaking - all while staying lossless.
- Builds on the Das/Abel/Canfield-Dafilou Kronecker work and Schlecht/Habets time-varying feedback matrices; see [[artificial-reverberation]].
- Limitation: restricted to $N = 2^M$; losslessness is a structural guarantee, not a guarantee of good modal density or echo distribution.
- Tags: reverb, fdn, dsp, realtime, reference

### paper-dalsanto-nonlinear-shimmer-fdn-2026

**"Shimmer Reverberation with Nonlinear Feedback Delay Networks"** - Gloria Dal Santo, Xiaojie Pi, Karolina Prawda, Sebastian J. Schlecht, Vesa Valimaki (Aalto / York / FAU Erlangen) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_05.txt`

- Shimmer reverb (pitch-shifted feedback, in the ValhallaShimmer sense) reformulated inside the **FDN** architecture: five distinct ways to place nonlinear and time-varying operations in the feedback loop.
- The design criterion is **energy preservation and stability** - keeping the loop bounded while a pitch shifter, which is neither linear nor time-invariant, sits inside it, with controllable decay.
- Covers a range from harmonically rich distortion to musically coherent pitch-shifted reverberation.
- Precedent cited: Abel and Werner's distortion effects inside modal reverberators; this is the FDN counterpart. See [[artificial-reverberation]].
- Explicitly bridges physically inspired structures with non-physical creative effect design.
- Limitation: stability arguments are per-approach and partly empirical; no formal proof covering arbitrary pitch-shift ratios.
- Tags: reverb, fdn, nonlinear, dsp, realtime

### paper-ibnyahya-differentiable-fdn-rir-2026

**"Gradient Descent Optimization of Room Impulse Responses with Parameter-Efficient Differentiable Feedback Delay Networks"** - Ilias Ibnyahya, Joshua D. Reiss (Queen Mary University of London) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_10.txt`

- Bridges convolution reverb (faithful but costly and uneditable) and FDN reverb (cheap and editable but hard to match to a room) by **fitting a fully differentiable FDN to a measured RIR** by gradient descent.
- Architecture: **16 delay lines at 48 kHz**, training *all* components jointly - delay lengths, feedback matrix, early-reflection taps, and frequency-dependent attenuation filters.
- Parameter efficiency trick: the attenuation filters are one **shared prototype** of parametric-EQ bands, with per-line gains fixed by the Jot proportionality condition. This decouples $T_{60}$ accuracy from filter structure, beats graphic-EQ attenuation filters on reverberation-time error with **fewer multiplications per sample**, and trains several times faster.
- Evaluated on **nine measured RIRs** from a small studio to a cathedral against three baselines (another differentiable FDN, an analysis-synthesis pipeline, a noise-shaped reverberator); lowest error on standard room-acoustic measures, direct-to-reverberant ratio, and multi-resolution spectral distance, with an ablation per trainable component.
- Cost: comparable per-sample computation to partitioned convolution at roughly **11x less memory**; trains in **under two minutes per RIR** on one consumer GPU.
- Good summary of the DDSP-FDN lineage (Lee et al. frequency-sampling FDN, Mezza et al., Dal Santo's RIR2FDN / FLAMO). See [[artificial-reverberation]] and [[waveguide-parameter-optimization]].
- Tags: reverb, fdn, room, differentiable, ml, optimization, dsp

### paper-abate-concatenation-driven-convolution-2026

**"A Unified Framework for Real-Time Concatenation-Driven Convolution"** - Niccolo Abate (CCRMA), Brian Hansen (UC Santa Cruz) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_01.txt`

- Unifies concatenative synthesis and real-time convolution: a corpus of audio segments is analyzed with perceptual features and organized on a **self-organizing map**, and the concatenative output is treated as a **continuously evolving impulse response** injected into a partitioned convolution engine.
- Central technical contribution: **single-engine frequency-domain kernel interpolation**. Instead of cross-fading the outputs of two convolution engines, the FFT-domain kernels of the current and target IRs are interpolated inside one engine, preserving internal convolution state and avoiding the warm-up energy dip of dual-engine cross-fading.
- Evaluated for computational efficiency and output-energy stability: lower cost under continuous IR updates, consistent output energy across interpolation conditions, audio-thread CPU usage within real-time constraints.
- Reframes the IR as navigable sonic material rather than a static filter; relevant to the convolution side of [[artificial-reverberation]].
- Limitation: no perceptual evaluation of the interpolation; SOM organization quality is not measured.
- Tags: reverb, room, dsp, realtime, tutorial

### paper-valentin-iris-ir-navigation-2026

**"IRIS: A VST3 Plugin for 2D Navigation of Impulse Response Collections"** - Luna Valentin, Celeste Betancur Gutierrez (CCRMA), Romain Michon (INRIA Lyon) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_71.txt`

- VST3 plug-in for arranging, navigating and auditioning measured or user-defined IR collections on a **two-dimensional navigation plane**, each IR a node positioned from metadata or by hand.
- During navigation, nearby responses are combined with **Gaussian distance weighting**, and a **bounded active set** limits the number of simultaneous convolutions.
- Features: smoothing, hysteresis, optional preprocessing, boundary attenuation, OSC control, coupled multichannel handling.
- Reports a short timing characterization giving practical real-time limits as a function of IR length, buffer size and active-set size.
- Explicitly a workflow/auditioning tool, **not** a physically optimal interpolation method, and with no perceptual validation - the honest framing is part of the contribution. See [[artificial-reverberation]].
- Tags: reverb, room, dsp, realtime, tutorial

---

## Tooling and deployment

### paper-stonge-fdn-sandbox-sffdn-2026

**"FDN Sandbox: Real-Time Experimentation and Analysis of FDNs"** - Alexandre St-Onge, Gary Scavone (McGill University) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_68.txt`

- **sfFDN**: a modular, real-time-capable open-source **C++ FDN library**, in the spirit of the MATLAB FDN Toolbox.
- Implements the canonical FDN plus recent extensions: **filter feedback matrices**, **velvet-noise decorrelation filters**, and **two-stage graphic equalizers** for attenuation and tone correction.
- Companion **FDN Sandbox** GUI application exposes these with real-time visualizations and an optimization framework wrapping **nine algorithms from the ensmallen library**, with built-in loss functions for colorless reverberation and for RIR matching.
- Directly useful as a reference implementation or as a component in JUCE work; complements [[artificial-reverberation]] and [[entities/source-papers#paper-ibnyahya-differentiable-fdn-rir-2026]].
- Limitation: demo paper - no benchmark against other FDN implementations, and the optimizers are gradient-free wrappers rather than a differentiable FDN.
- Tags: reverb, fdn, dsp, realtime, stk, reference

### paper-franchino-adac-differentiable-to-faust-2026

**"Compiling Differentiable Audio Graphs to Real-Time DSP"** - Facundo Franchino (MIT), Sebastian J. Schlecht (FAU Erlangen) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_61.txt`

- Problem: differentiable audio processors are designed in ML frameworks but deployed by hand-porting to a DSP language - error-prone, hard to verify, and it detaches research prototypes from usable tools.
- **ADAC**: a compiler that lowers a trained model to a framework-agnostic intermediate representation and emits **FAUST** code whose impulse response matches the source model **to within floating-point arithmetic noise**, direct paths included.
- The optimization loop is made *audible*: the model inside a running plug-in is hot-swapped after each gradient step.
- The exported processor carries a small set of macro-controls chosen to leave stability intact, and a **stability certificate** computed from the shipped parameters is checked before the plug-in is built.
- Demonstration: an FDN is trained and exported to a working plug-in. See [[artificial-reverberation]] and [[waveguide-parameter-optimization]].
- Limitation: demo paper; the supported operator set of the IR and the classes of model that can be certified are not fully characterized.
- Tags: faust, differentiable, ml, dsp, realtime, fdn, reference

---

## Theory, topology and measurement

### paper-essl-circular-buffer-monodromy-2026

**"Winding Numbers and Monodromy of Vector Bundles over a Circular Buffer"** - Georg Essl (University of Wisconsin - Milwaukee) - DAFx26, Cambridge MA, Sept 2026 - `raw/DAFx26_paper_35.txt`

- Reinterprets the ordinary circular buffer as a **trivial real line bundle** over a discrete circle: each sample position is a fiber, and the transition map between neighbouring fibers is a scalar multiply.
- A single $-1$ transition in the loop makes the bundle non-trivial - the **Mobius circular buffer**, the same object as the Johnson (twisted) ring counter and as Trautmann's twisted string; **monodromy** $\mu = A^n$ is the effect of going once around.
- Generalises to the **$r$-circular shift matrix**; $r = 1$ gives the classic shift, $r = -1$ the skew-circulant, unimodular complex $r$ a circle bundle. The **winding number** $w$ is the least $k$ with $\mu^k = I$.
- Explains the half fundamental and odd-harmonic spectrum of mixed Dirichlet-Neumann waveguides (capped organ pipe, clarinet) as monodromy modulation of the DFT spectrum. See [[concepts/circular-buffer-topology-monodromy]] for the full distillation.
- Frames the Berdahl et al. chaotic-oscillator-in-a-delay-loop design as **variable monodromy** with a fixed winding number, and sketches braids as the vector-bundle generalisation.
- Limitation: expository and structural; no synthesis results, listening tests, or FDN application (explicitly listed as future work).
- Tags: delay-line, waveguide, wave-equation, reference, tutorial

### paper-wieland-polymap-pickups-2026

**"PolyMap: A 64-Channel Polyphonic Guitar Pickup System"** - David Wieland, Jonas Roth, Christoph Studer (ETH Zurich) - DAFx26 demo paper, Cambridge MA, Sept 2026 - `raw/DAFx26_demo_73.txt`

- Master's-thesis hardware: an **8 x 8 grid of 64 active pickups** (Cycfi Nu Capsules) on a custom eight-string guitar - every string sensed individually at **eight positions** between bridge and neck.
- All 64 channels are digitised inside the instrument (eight 8-channel ADCs, 48 kHz / 24 bit, simultaneous sampling) and shipped over a single coaxial cable as **MADI** from an FPGA; power is injected on the same cable.
- Measured **5.4 ms** end-to-end latency at a 32-sample buffer, and channel noise floors of $-73$ to $-67$ dBFS (the pickups dominate; disabling them gives $-90$ dBFS).
- Enables per-string effects, virtual (interpolated) pickup position, phase-inverted blending, and controlled measurement of comb-filter pickup-position effects on one instrument. See [[entities/polymap-pickup-system]].
- Design files, plug-in and sample audio are open-source.
- Limitation: demo paper; noise performance is pickup-limited, and 64-channel tracks are confirmed working only in Reaper.
- Tags: guitar, string, dsp, realtime, reference

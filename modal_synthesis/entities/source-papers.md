---
title: Source Papers -- Distilled Catalog
created: 2026-09-08
updated: 2026-09-08
type: entity
tags: [reference, comparison, modal, modal-synthesis, room, ml]
sources:
  - /l/dttd/DAFx26/README_JOS.md
  - /l/dttd/DAFx26/DAFx26_paper_03.pdf
  - /l/dttd/DAFx26/DAFx26_paper_06.pdf
  - /l/dttd/DAFx26/DAFx26_paper_11.pdf
  - /l/dttd/DAFx26/DAFx26_paper_40.pdf
  - /l/dttd/DAFx26/DAFx26_paper_41.pdf
  - /l/dttd/DAFx26/DAFx26_demo_72.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_76.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_77.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_82.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_83.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_86.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_87.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_88.pdf
---

# Source Papers -- Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>` ID used
in `index.md`, so inbound links like
`[[entities/source-papers#paper-giampiccolo-era-violin-bridge-2026]]` resolve
inside this page. Blocks are distilled from the text extractions in `raw/`
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

## Instrument modal modeling

### paper-ducceschi-65-classical-guitars-2026

**"Measurement-Informed Nonlinear Modal Synthesis of 65 Classical Guitars"** - Michele Ducceschi, Riccardo Russo, Craig J. Webb (University of Bologna) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_40.txt`

- Full plucked-string-plus-body pipeline for a whole population of instruments: from the public **Mores dataset** of impulse-response measurements on **65 classical guitars**, extract per-instrument modal parameters of the **bridge compliance** and of the **bridge-to-air radiation path**.
- String model: transverse vibration under a **geometrically exact elastic potential**, coupled at an interior bridge point to the measured body data - so the body is a modal load at the bridge rather than being commuted into the excitation (contrast [[commuted-synthesis]] and [[coupled-structures]]).
- The nonlinear potential is quadratized by the **Scalar Auxiliary Variable** (SAV) method, so the equations of motion become linear in a scalar variable and a known gradient vector **at the continuous level**, not merely after discretization.
- After time discretization the coupled system is inverted with **two sequential Sherman-Morrison rank-one updates** - one for the bridge coupling, one for the SAV nonlinearity - giving an $O(N)$ algorithm per time step.
- Two regularization techniques prevent long-term drift of the auxiliary variable; the pipeline is demonstrated by synthesizing plucked tones across all frets and strings for each of the 65 guitars.
- Worth reading for the SAV trick alone; see [[nonlinear-modal-synthesis]] for the energy-quadratization family.
- Limitation: no listening test against recordings of the measured instruments; the measured body data are linear, so nonlinearity lives entirely in the string.
- Tags: modal, modal-synthesis, string, vibration, impulse-response, dataset, physical-modeling

### paper-giampiccolo-era-violin-bridge-2026

**"Eigensystem Realization of Violin Bridge Admittances"** - Riccardo Giampiccolo, Alessandro Ilic Mezza, Raffaele Malvermi, Mirco Pezzoli, Alberto Bernardini, Fabio Antonacci (Politecnico di Milano) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_41.txt`

- Applies the **Eigensystem Realization Algorithm** (ERA - Hankel-matrix SVD, the NASA structural-dynamics method) to measured violin **bridge admittance** impulse responses, producing a reduced-order **state-space** model in one algebraic step instead of a multi-stage modal fit.
- No explicit modal parameterization is required; dominant system dynamics fall out of the singular-value truncation. See [[modal-analysis-measurement]].
- Evaluated on a dataset of modern and historical violins (including a Stradivari) against established modal and state-space identification baselines.
- Results: lower reconstruction error in **both time and frequency domains**, better preservation of perceptually relevant features, and more accurate reproduction of the target **frequency-dependent energy decay** than the baselines.
- Practical relevance: body-filter design from measurements, for [[coupled-structures]] and for virtual-instrument bridge filters.
- Limitation: **passivity is not guaranteed** by ERA, which the authors discuss - a real concern when the realization is embedded in a feedback loop such as a bowed-string model.
- Tags: modal, eigenmode, impulse-response, string, dsp, comparison, reference

---

## Modal reverberation

### paper-ducceschi-corpus-driven-modal-reverberator-2026

**"A Corpus-Driven Parametric Modal Reverberator"** - Michele Ducceschi, Leonardo Gabrielli, Riccardo Simionato, Riccardo Russo (Bologna / UnivPM / Bordeaux) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_06.txt`

- Answers the practical objection to modal reverberators: nobody can set thousands of per-mode frequencies, dampings and residues by hand.
- Method: modal-decompose a large curated corpus of measured room IRs into per-mode frequency, damping and residue plus a short **early-reflection FIR**; build a per-IR feature table of **50 variables** (standard acoustic indices, per-band damping and density statistics, amplitude distributions, FIR descriptors).
- Six acoustically meaningful user controls are selected and **orthogonalized by PCA** because they are strongly correlated across the corpus; per-band damping and modal density are then predicted by **robust linear models in log space**.
- Residue amplitudes follow the **diffuse-field equipartition** relation, and early-reflection energy is set directly from the clarity-index definition - so two of the hardest quantities come from acoustics rather than regression.
- Net effect: a six-number perceptual specification maps onto thousands of modal parameters driving a bank of second-order resonators (see [[resonator-bank-implementation]]).
- Regression diagnostics and corpus-distribution analysis confirm the generated IRs are acoustically plausible and span the training parameter space.
- Limitation: validation is statistical, not perceptual - no listening test versus measured spaces.
- Tags: modal, modal-synthesis, resonator, room, damping, impulse-response, ml, dataset

### paper-bittner-diagonal-ssm-plate-reverb-2026

**"Diagonal Complex-Valued State Space Models for System Identification and Modeling of Metal Plate Reverbs"** - Matthias Bittner, Matthias Wess, Dominik Dallinger, Daniel Schnoll, Axel Jantsch (TU Wien) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_03.txt`

- Bridges the deep **state space model** (S4-style) literature and modal synthesis: shows that a *restricted diagonal complex-valued* SSM is **exactly equivalent to a bank of parallel second-order all-pole filters** - i.e. a modal resonator bank (see [[resonator-bank-implementation]]).
- Trains it efficiently with the **parallel scan** algorithm for state computation, so long-memory modal behavior is learnable without sequential recurrence.
- Proposes **Matrix Pencil guided eigenvalue initialization**, which improves both synthesis quality and system-identification performance over generic SSM initialization - classical pole estimation used as the initializer for a learned model.
- Validated on the DAFx plate reverb benchmark: accurate impulse-response reconstruction plus meaningful recovery of physically interpretable modal parameters, which black-box neural plate models do not give.
- Companion to the same group's Task B challenge entry, [[entities/source-papers#paper-bittner-matrix-pencil-ssm-taskb-2026]]; see also [[ml-modal-parameter-estimation]].
- Limitation: linear, time-invariant plate behavior only; nonlinear plate effects are out of scope.
- Tags: modal, eigenmode, resonator, room, ml, neural, differentiable, inference

### paper-lee-klein-bottle-reverberation-2026

**"Modal Structure of Plate Boundaries and Klein Bottle Reverberation"** - Jin Woo Lee, Mark Rau (MIT) · DAFx26, Cambridge MA, Sept 2026 · `raw/DAFx26_paper_11.txt`

- Departs from the usual "observe, then model" order: models the acoustics of objects that **cannot exist** physically.
- Studies wave propagation on compact two-dimensional **non-orientable manifolds** - the Mobius band and the Klein bottle, which cannot be embedded in $\mathbb{R}^3$ without self-intersection.
- Derives **closed-form eigenfrequencies and mode shapes** for these topologies via the quotient-space construction, i.e. by identifying boundary points with a twist (see [[mode-shapes-and-eigenvalues]]).
- Modal structures are **verified against finite-difference time-domain** simulation, so the closed forms are not just formal.
- Result: shows how the topological character imposed by the boundaries shapes the acoustic resonances, and offers the quotient-space framework as a practical route to reverb synthesis on geometries with no physical counterpart.
- Limitation: linear, lossless-to-lightly-damped ideal plates; the perceptual payoff of non-orientable topology is asserted rather than tested.
- Tags: modal, eigenmode, wave-equation, vibration, room, reference

### paper-ducceschi-bunkervik-spatial-reverb-2026

**"Bunkervik Spatial Reverb Demo"** - Michele Ducceschi, Craig J. Webb (University of Bologna) · DAFx26 demo paper, Cambridge MA, Sept 2026 · `raw/DAFx26_demo_72.txt`

- Real-time plug-in for a **dynamic spatial reverb** built from acoustic measurements of the Bunkervik creative arts space (a tunnel) in Brescia, Italy.
- A modal synthesis reverberation engine is fitted to measured IRs from **three positions** in the tunnel.
- Key device: a **common set of modal frequencies** shared across positions, with only the **residue weights and FIR taps** interpolated, so the receiver can be moved continuously through the space without re-fitting poles.
- Real-time controls for high-frequency content, damping and microphone rotation, all modulatable by two LFOs.
- Same modal machinery as [[entities/source-papers#paper-ducceschi-corpus-driven-modal-reverberator-2026]]; see [[resonator-bank-implementation]] and [[realtime-modal-synthesis]].
- Limitation: demo paper - three measurement positions, no perceptual validation of the interpolation between them.
- Tags: modal, modal-synthesis, resonator, room, realtime, impulse-response

---

## The 1st DAFx Parameter Estimation Challenge (plate reverb)

### paper-gabrielli-dafx-challenge-overview-2026

**"The 1st DAFx Challenge: Physical and Modal Parameter Estimation for Plate Reverberation"** - Leonardo Gabrielli (Universita Politecnica delle Marche), Michele Ducceschi (University of Bologna) · DAFx26 challenge overview, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_76.txt`

**The reference model.** Everything is synthetic, generated from the damped
**Kirchhoff-Love** plate equation with simply supported boundaries, solved
modally: mode $m$ is a second-order all-pole section with residue
$\Phi_m(x_i,y_i)\,\Phi_m(x_o,y_o)$ and loss coefficient
$\sigma_m = \eta_0 + \eta_1 \Omega_m^2$, and the plate response at the output
point is the parallel sum of $M$ such sections. No measurement of a real plate
is involved.

**Task A - physical parameter identification.** Recover the six identifiable
quantities
$S(P) = \{\mu := \rho h,\; D/\mu,\; T_0/\mu,\; L_y,\; x_o,\; y_o\}$
from one impulse response. The raw parameters $(\rho, h, E, T_0)$ enter the
equation of motion only through those invariants, so a one-parameter family of
raw tuples gives the identical IR; working with $S(P)$ makes the ground truth
unique. All six are identifiable **only if absolute IR amplitude is preserved**
(the biquad numerator is proportional to $1/(\rho h)$), so displacement IRs were
distributed with absolute scale intact as `.npz` alongside a normalized `.wav`.
Metric: NMSE on the normalized parameter vector, with spectral MSE reported as
an auxiliary. Baseline: particle swarm optimization with a multi-scale spectral
loss.

**Task B - modal parameter identification.** Recover the (unknown number of)
modal frequency/decay/gain triples. Metric:
$\mathrm{RE} = \mathrm{RE}_0 + \lambda\min(1, \Delta M / M)$ with $\lambda = 1$,
where $\mathrm{RE}_0$ is the mean of the per-component relative errors for
frequency, decay and gain (each clipped at 1) and $\Delta M$ is the mode-count
error; the metric lies in $[0,2]$. Baseline: peak picking with parabolic
frequency refinement, half-power-bandwidth damping, and a single-mode gain
estimate.

**Participation.** 13 participants, 22 methods (12 Task A, 10 Task B), scored on
16 secret test IRs.

**Task A final ranking (Table 3, by mean NMSE).** 1. Marttila 13-A2 (QMUL),
$1.8\times10^{-13}$; 2. Park & Yi 10-A (UIUC), $1.9\times10^{-11}$;
3. Lee 9-A (ALAMODE), $1.0\times10^{-4}$; 4. Sechet 5-A, $4.7\times10^{-4}$;
5. Marttila 13-A1, $1.1\times10^{-3}$; 6. Heminway 7-A; 7. Guo 4-A;
8. Lipkin 8-A; 9. Lu 2-A; 10. Kim 11-A; 11. Garofalo 6-A (median
$6.1\times10^{-6}$, mean 0.018); 12. **PSO baseline**, 0.048; 13. Yang 1-A,
0.056; 14. constant-predictor baseline, 0.120. Two methods reach machine
precision by opposite routes - a Transformer trained on 327,680 IRs with PSO
polishing, and training-free CMA-ES.

**Task B final ranking (Table 4, by mean RE).** 1. Marttila 13-B1 (QMUL count-density),
0.328; 2. Marttila 13-B2, 0.337; 3. Lu 2-B, 0.539; 4. Heminway 7-B, 0.643;
5. Bittner 3-B, 0.743; 6. Zhang 4-B, 0.862; 7. Franchino 9-B, 0.957;
8. Jung 12-B2, 1.066; 9. Jung 12-B1, 1.102; 10. Cogliati 8-B, 1.485;
baseline 1.968.

**Headline findings.**
- Task A is essentially solved *within the training/search range*; the organizers note the winning network has learned to interpolate a deterministic simulator, and the untested directions are the interesting ones.
- Task B is much harder: the best entry uses about a sixth of the metric's dynamic range, and the gap between the two QMUL entries and third place is wide.
- Every method estimates **frequencies and decays far better than gains**: the winner reaches $\mathrm{RE}_\Omega = 0.013$ and $\mathrm{RE}_\sigma = 0.058$ but $\mathrm{RE}_b = 0.847$, and **no** entry gets gain relative error below 0.83.
- A complementary **frequency-domain evaluation** (mean $L_1$ error on $\log|H(f)|$) reorders the Task B ranking and exposes a systematic gain bias the per-mode metric is blind to - e.g. one QMUL variant reproduces the right spectral shape roughly 30 dB too low.
- Rank correlates strongly with getting the **mode count** right ($\Delta M$ ranges from 125 to 5242).
- Tags: modal, eigenmode, resonator, room, damping, ml, comparison, reference, dataset

### paper-marttila-transformer-pso-taska-2026

**"Transformer-Based Plate Parameter Estimation with Differentiable and Particle-Swarm Refinement"** - David Marttila, Rodrigo Diaz, Pablo Tablas De Paula, Ilias Ibnyahya, Chin-Yun Yu (QMUL) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_82.txt`

- **Task A winner** (method A2, mean NMSE $1.8\times10^{-13}$).
- Method A1: an **Audio Spectrogram Transformer** encoder plus a Transformer regressor, followed by **differentiable IR refinement**.
- Method A2: the same encoder conditions a **continuous normalizing flow**; sampled candidates are refined by **particle swarm optimization** and gradient polishing.
- Both preserve the absolute IR scale, which is what makes surface density $\mu$ recoverable at all.
- On a 100-IR synthetic holdout, both refinement procedures cut waveform and parameter errors by **more than three orders of magnitude** relative to the unrefined neural output - the strongest evidence in the challenge that neural nets are best used as *initializers*, not answers.
- Trained on 327,680 IRs, five times the next-largest training set; the organizers note this amounts to learning to interpolate the simulator inside its training range.
- Limitation: matched synthetic setting only; generalization outside the generator's parameter ranges is untested.
- Tags: modal, ml, neural, differentiable, inference, comparison, dataset

### paper-park-two-stage-evolutionary-taska-2026

**"Accurate Plate Reverb Parameter Estimation Using Two-Stage Evolutionary Search"** - Byunghoo Park, Jayeon Yi, Takyoung Kim, Minje Kim (UIUC) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_83.txt`

- **Task A, ranked 2nd** (mean NMSE $1.9\times10^{-11}$) with **no training at all** - the training-free counterpart to the QMUL winner.
- Treats the problem as black-box optimization: feed candidate parameters to the simulator, score the resulting IR against the target.
- Stage 1: **CMA-ES** recovers five of the six parameters under an **amplitude-normalized** loss, which makes the search robust but destroys the only cue to surface density.
- Stage 2: **ternary search** on the un-normalized loss recovers surface density alone.
- Includes an analysis of why the log-compression in the common multi-scale spectral loss degrades recovery, plus a pathological failure mode and an ablation justifying two stages over a unified CMA-ES search.
- Validated on 50 held-out IRs.
- Limitation: many forward-simulator evaluations per IR; cost scales with simulator speed.
- Tags: modal, comparison, reference, dsp

### paper-garofalo-differentiable-modal-plate-2026

**"Parameter Estimation via Differentiable Modal Plate Synthesis"** - Filippo Garofalo, Alessandro Antonio Lillo, Alessandro Ilic Mezza, Riccardo Giampiccolo, Alberto Bernardini (Politecnico di Milano) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_77.txt`

- **Task A**: a fully **differentiable modal plate synthesizer** in PyTorch, with the six parameters recovered by inference-time gradient descent on a **multi-scale spectral loss** backpropagated through the plate model - a clean white-box DDSP example (see [[ml-modal-parameter-estimation]]).
- Non-convexity is handled with a two-phase strategy: many short **probe optimizations** (Latin hypercube starts), then full-scale refinement from the best candidate. About 13 minutes per IR.
- Reported to reduce prediction error by roughly an order of magnitude versus a constant predictor and the PSO baseline on eight IRs.
- In the official ranking it placed **11th by mean NMSE** but with a **median of $6\times10^{-6}$**: it either nails the answer or falls into the wrong basin - the classic non-convex DDSP failure mode, and the reason the organizers report medians alongside means.
- Limitation: single-restart-family search; no learned initializer to escape bad basins.
- Tags: modal, differentiable, ml, neural, comparison

### paper-diaz-count-density-networks-2026

**"Count-Density Networks for Modal Plate Parameter Estimation"** - Rodrigo Diaz, Pablo Tablas De Paula, David Marttila, Ilias Ibnyahya, Chin-Yun Yu (QMUL / Fraunhofer HHI) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_87.txt`

- **Task B winner by a wide margin**: 0.328 and 0.337 for the two variants, versus 0.539 for third place.
- Formulation change that wins: instead of picking spectral peaks and estimating triples one at a time, **jointly infer a per-bin mode density** on a 1/20-octave log-frequency grid together with the corresponding decay rates and gains, so the unknown mode count is part of the regression rather than a preprocessing decision.
- Variant 1: pooled spectral features with time-domain and absolute-scale conditioning in a **real-valued convolutional count-density network**. Variant 2: a **complex-valued Transformer** count-density network.
- Component errors: frequencies essentially perfect ($\mathrm{RE}_\Omega = 0.013$), decays good (0.058), gains poor (0.847) - the same gain failure as every other entry.
- On an independently generated 100-IR comparison set both estimators beat the evaluated classical baselines.
- Caveat from the overview: the complex-Transformer variant reproduces the correct spectral **shape about 30 dB too low**, which the per-mode metric cannot see.
- Tags: modal, eigenmode, ml, neural, inference, comparison

### paper-bittner-matrix-pencil-ssm-taskb-2026

**"Non-Iterative Modal Parameter Estimation for Plate Reverbs via Matrix-Pencil-Guided State Space Model Initialization"** - Matthias Bittner, Axel Jantsch (TU Wien) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_86.txt`

- **Task B, ranked 5th** (RE 0.743); the most classical-DSP-flavoured Task B entry.
- Pipeline: estimate the total mode count, then initialize the eigenvalues of a **diagonal complex-valued state space model** (equivalently a bank of parallel second-order all-pole filters) with the **Matrix Pencil** method.
- Exploiting the linearity of the resulting system, the state impulse responses are computed and the **modal gains obtained in closed form by least squares** - gradient-based optimization is replaced outright.
- Keeps an interpretable system representation, which black-box neural plate models do not.
- Companion to the full paper [[entities/source-papers#paper-bittner-diagonal-ssm-plate-reverb-2026]]; see [[modal-analysis-measurement]] for the pole-fitting family this belongs to.
- Limitation: mode-count estimation is the weak link, and matrix-pencil conditioning degrades in dense high-frequency regions.
- Tags: modal, eigenmode, resonator, dsp, inference, reference

### paper-franchino-subband-ar-pole-harvesting-2026

**"Multi-View Subband Autoregressive Pole Harvesting for Modal Plate Identification"** - Facundo Franchino, Jatin Chowdhury, Jin Woo Lee, Mark Rau (MIT), Soohyun Kim (CCRMA) · DAFx26 challenge report, Cambridge MA, Sept 2026 · `raw/DAFx26_challenge_88.txt`

- **Task B, ranked 7th** on the per-mode metric (RE 0.957) but nearly exact above 1 kHz in the organizers' frequency-domain re-evaluation, overshooting at low frequencies.
- Pure signal processing: a **matching-pursuit anchor stage** seeds a **multi-view subband autoregressive** (linear-prediction) pole harvester run on the raw IR **and its first two finite differences**.
- The trick: linear filtering changes residues but **leaves pole locations fixed**, so the three views expose complementary subsets of the same pole set.
- Bands where the AR order saturates are **recursively split**, and any remaining under-resolved region is completed from an IR-derived saturation indicator.
- Gains assigned by a **global ridge least-squares** fit in the damped-biquad atom convention.
- Uses only the unnormalized IR - no plate parameters, no analytical modal-frequency or decay laws, no `.wav` files, no Task A information. See [[modal-analysis-measurement]].
- Tags: modal, eigenmode, resonator, dsp, impulse-response, reference

### Other challenge entries (not distilled)

Listed for completeness; one line each, cataloged from the overview's Tables 3
and 4 plus the annotated bibliography. Full text is in `raw/` and the PDFs are at
the paths given.

- **Physics-Inspired Feature Fusion for Plate Parameter Estimation from Acoustic Impulse Responses** - Guo, Zhang, Chen, Liu, Huang (Wuhan U. / Hunan U.). Task A, 7th: pretrained CNN backbone fused with 15 hand-crafted IR features. `/l/dttd/DAFx26/DAFx26_challenge_78.pdf`
- **ALAMODE: Automated Learning of Acoustical Modal Parameters via Differential Evolution** - Lee, Chowdhury, Franchino, Rau (MIT), Kim (CCRMA). Task A, 3rd (mean NMSE $1\times10^{-4}$): three-stage gradient-free differential-evolution search on a fast physics simulator - frequency-determining parameters, then output position, then mass density from amplitude. `/l/dttd/DAFx26/DAFx26_challenge_79.pdf`
- **A Multi-Resolution Spectrogram Approach for Estimating the Physical Parameters of a Plate Reverb** - Anderson (UMN Duluth), Lipkin, Chen, Thompson, Cogliati, Heilemann (U. Rochester). Task A, 8th: ResNet-18 on multi-resolution spectrograms with spectral phase as an extra channel to disambiguate output position. `/l/dttd/DAFx26/DAFx26_challenge_80.pdf`
- **Simulation-Based Plate-Reverb Parameter Estimation from a Single Impulse Response** - Lu, Reiss (QMUL). Task A, 9th: non-iterative tree-ensemble regression from hand-crafted amplitude/spectral/decay descriptors, 6 ms per IR, beating a single PSO run. `/l/dttd/DAFx26/DAFx26_challenge_81.pdf`
- **Simulation-Based Inference for Plate Reverb System Identification** - Sechet, Evrard, Kowalski (Paris-Saclay). Task A, 4th: a network learns a posterior over plate parameters from simulator samples, then is fine-tuned per test IR with extra simulation rounds, returning a distribution rather than a point estimate. `/l/dttd/DAFx26/DAFx26_challenge_84.pdf`
- **Neural Networks for Physical Parameter Estimation of Plate Reverberation from Impulse Responses** - Yang (independent). Task A, 13th, below the PSO baseline: time-domain CNN-GRU regressor trained on only 1000 simulator IRs. `/l/dttd/DAFx26/DAFx26_challenge_85.pdf`
- **Peak-Residual Modal Estimation with Learned Calibration and High-Band Density Correction** - Jung (independent). Task B, 8th and 9th on the per-mode metric (4th and 5th in the frequency domain): prominence-graded peak picking, iterative residual passes, a learned mode-count target, and a small MLP recalibrating decay and gain without moving frequencies. `/l/dttd/DAFx26/DAFx26_challenge_89.pdf`
- **Band-Count Dense Modal Estimation with Fixed-Frequency Differentiable Resonator Refinement** - Lu, Reiss (QMUL). Task B, 3rd on the per-mode metric (RE 0.539) but **1st on the organizers' frequency-domain re-evaluation**: ExtraTrees predict mode counts per band, a dense frequency grid is laid down, then decay and gain are refined with a differentiable all-pole resonator bank while frequencies stay fixed. Most of the gain over the baseline comes from getting the mode count right. `/l/dttd/DAFx26/DAFx26_challenge_90.pdf`
- **A Dual-Stream Framework Combining Audio Spectrogram Transformer and Dynamic Mode Decomposition for Plate Modal Parameter Estimation** - Zhang, Chen, Guo, Liu, Huang (Wuhan U. / Hunan U.). Task B, 6th: AST global features fused with **Dynamic Mode Decomposition** local modal descriptors - a low-rank linear operator fit across STFT frames whose eigenvalues give frequency and decay. `/l/dttd/DAFx26/DAFx26_challenge_91.pdf`

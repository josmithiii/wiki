---
title: Source Papers — Distilled Catalog
created: 2026-04-15
updated: 2026-04-16
type: entity
tags: [reference, comparison]
---

# Source Papers — Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>`
ID used in `index.md`, so inbound links like
`[paper-zhang-wang-deep-anc](entities/source-papers.md#paper-zhang-wang-deep-anc)`
resolve inside this page. Blocks are distilled from the original
extractions in `raw/` (gitignored); see `raw/MANIFEST.md` for the
filename-to-PDF mapping.

When any single paper here needs deeper treatment than the bullet
summary supports (extra figures, sub-sections, its own tag taxonomy),
promote it to a dedicated `entities/paper-<slug>.md` file and leave
the section here as a cross-link.

The `DRL-Control-Survey-2507.08196.txt` extraction is intentionally
**not** given a section here — it contains no ANC content and is cited
inline in `concepts/deep-rl-anc.md` as a general-DRL background
reference only.

---

## Published references (pre-AI-ANC batch)

### paper-widrow-adaptive-noise-cancelling

**"Adaptive Noise Cancelling: Principles and Applications"** — Widrow, Glover, McCool, Kaunitz, Williams, Hearn, Zeidler, Dong, Goodlin · *Proc. IEEE* 63(12), Dec 1975 · `raw/ANC-Widrow-j1975adaptivenoise.txt` · distilled at [[lms-algorithm]]

- Foundational LMS adaptive-filter paper; describes the primary/reference architecture with the Widrow–Hoff update.
- Wiener-optimal analysis for stationary and non-stationary inputs; single and multiple reference channels.
- Demonstration applications: ECG 60 Hz hum removal, maternal-ECG cancellation, antenna sidelobe cancelling, speech-in-noise.
- **Does not** address a plant between filter output and error sensor — FxLMS (see [[fxlms-algorithm]]) is the later extension.
- Appendix B derives a finite-length causal approximation — the same causality constraint reappears in acoustic ANC.
- Tags: lms, anc, history, reference, tutorial, person

### paper-wise-leventhall-lf-anc

**"Active Noise Control as a Solution to Low-Frequency Noise Problems"** — Wise & Leventhall · *J. Low-Freq. Noise, Vib. Active Ctrl.* 29(2), 2010 · `raw/ANC-for-LF.txt`

- Tutorial on why LF noise needs active (not passive) control and what limits the achievable reduction.
- Coherence bound: max attenuation $\approx -10\log_{10}(1-\gamma^2)$; $\gamma^2 \ge 0.9$ needed for $>10$ dB.
- Plane-wave duct modes are easily controllable; higher-order modes require arrays and spatial sampling.
- Application focus: schools (ANSI 35 dBA HVAC goal), duct-mounted ANC, room-mode control.
- Good canonical reference for the causality, secondary-path, and coherence-floor sections of the wiki.
- Tags: anc, duct, room, room-modes, acoustics, causality, tutorial

### paper-zhang-wang-deep-anc

**"Deep ANC: A Deep Learning Approach to Active Noise Control"** — Zhang & Wang · *Neural Networks* 141, Sep 2021 · `raw/DeepANC-nihms-1690502.txt` · primary source for [[deep-anc-crn]]

- Convolutional recurrent network (CRN) supervised to output real/imag spectrogram of the anti-noise signal given the reference.
- Implicitly absorbs loudspeaker nonlinearity and secondary-path dynamics into the learned mapping — no explicit $\hat{S}(z)$.
- Multi-condition training gives generalization across untrained noise types; delay-compensated strategy preserves causality.
- Benchmarks show wideband reduction beyond linear FxLMS under nonlinear actuators.
- Natural bridge between classical FxLMS and modern deep ANC; cited frequently in ML-ANC comparison pages.
- Tags: anc, feedforward, fxlms, secondary-path, loudspeaker, causality, comparison

### paper-andersen-oticon-hearing-aids

**"Creating Clarity in Noisy Environments by Using Deep Learning in Hearing Aids"** — Andersen et al. (Oticon / Eriksholm) · *Seminars in Hearing* 42(3), 2021 · `raw/DeepLearningHearingAids-10-1055-s-0041-1735134.txt`

- Industrial review from Oticon on noise reduction in commercial hearing aids.
- Classical pipeline: adaptive beamformer (MVDR / GSC) + spectral postfilter; limited by stationarity assumptions.
- Deep-learning postfilter replaces the spectral suppression stage; trained on real + synthetic speech/noise pairs.
- Reports measured gains in SNR, objective intelligibility, and subjective listening effort under clinical conditions.
- Useful for grounding the wiki in practical deployment constraints (power, < 10 ms latency, personalization).
- Tags: anc, headphones, microphone, comparison, tutorial

### paper-gaikwad-ai-hearing-aids

**"AI-Driven Adaptive Noise Cancellation for Hearing Aids"** — Gaikwad · *IJFMR* 3(6), Nov–Dec 2021 · `raw/AI-ANC-HearingAids-61500.txt`

- Compact CNN with attention for real-time speech-vs-noise separation on hearing aids.
- Hardware target: binaural dual-mic + low-power SoC; sub-10 ms end-to-end latency.
- Claims 12 dB SNR gain and ~45% speech-intelligibility improvement vs MVDR / MWF beamforming baselines.
- Frames cocktail-party problem as non-stationary noise tracking that classical beamformers cannot handle.
- Position/review character; limited numeric rigor but useful as an entry point to the neural-ANC hearing-aid literature.
- Tags: anc, headphones, microphone, comparison, tutorial

### paper-khan-selective-nc-review

**"Advances in Intelligent Hearing Aids: Deep Learning Approaches to Selective Noise Cancellation"** — Khan, Asif, Nasir, Bhatti, Sheikh (NUST Islamabad) · arXiv 2507.07043, 2025 · `raw/DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt`

- Systematic review tracing ML-for-hearing-aids from NMF / CASA → DNN / LSTM → CRN / Transformer.
- Reports SOTA: CRN real-time inference <10 ms; Transformer architectures reaching ~18.3 dB SI-SDR on reverberant benchmarks.
- Flags deployment gaps: hardware–software co-design, continual learning, personalization, regulatory approval, lack of standardized benchmarks.
- Functions as landscape reference for the neural / selective-cancellation side of the wiki.
- An earlier duplicate extraction `DeepLearningHearingAids-2507.07043v2.txt` was removed 2026-04-14 after the PDF was deleted from `/l/dttd/`.
- Tags: anc, headphones, comparison, reference, tutorial

### paper-sarkar-latent-fxlms

**"Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters"** — Sarkar, Zhuang, Lu, Corey, Singer, Mittal (UIUC / Stony Brook / UIC) · arXiv 2507.03854, 2025 · `raw/LatentFxLMS-2507.03854v1.txt` · discussed at [[fxlms-algorithm]] (Latent FxLMS variant) and [[neural-system-identification]]

- Replaces direct FxLMS weight updates with updates in the **latent space of a pre-trained autoencoder** whose decoder outputs the FIR cancellation filter.
- Observation exploited: when the primary source moves over a bounded spatial region, converged FxLMS filters lie on a **low-dimensional manifold** in $\mathbb{R}^L$; constraining adaptation to that manifold accelerates convergence.
- Offline: train an autoencoder on converged FxLMS weight vectors $\mathbf{w}^*$, one per sampled source position. Online: perform the FxLMS gradient step on the latent code $\mathbf{z}$ (not $\mathbf{w}$), then set $\mathbf{w}(n) = D(\mathbf{z}(n))$.
- Studies two neural constraints: (1) VAE for a disentangled latent space; (2) **mixup**, requiring that convex combinations of impulse responses in the dataset round-trip correctly through the autoencoder.
- Also introduces a **latent-normalized** update rule analogous to NLMS but in $\mathbf{z}$-space.
- Result: latent-normalized LFxLMS with a **mixup-trained autoencoder** gives significantly faster convergence and **comparable steady-state MSE** to standard FxLMS. VAE-only decoders perform noticeably worse — the disentanglement constraint is *not* the active ingredient.
- Positioning: distinct from Deep ANC (Zhang & Wang 2021) — this method *accelerates* FxLMS rather than *replacing* it, and uses a shallow autoencoder sized for hardware integration.
- Caveat: only demonstrated for constrained primary-source regions; interpolation to unseen positions is flagged as future work.
- Tags: anc, fxlms, feedforward, secondary-path, stability, comparison, tutorial

---

## Patents

### paper-guerci-fan-anc-patent

**"Active Fan Blade Noise Cancellation System"** — Guerci · US 5,448,645, issued 1995 · `raw/ActiveFanBladeNoiseCancellation-US5448645.txt`

- Patent (RGI): phase-cancelling a single fan's blade-pass tone with a speaker array.
- Mic captures fan sound → bandpass at BPF (= RPM × blade count) → audio amp → speaker array driven anti-phase, equal amplitude per channel.
- Self-tuning: filter center frequency tracks fan speed; periodic updates.
- Non-adaptive in the LMS sense — fixed-structure phase inverter with tracked center frequency.
- Mainly of historical interest: early commercial precedent for tonal fan ANC.
- Tags: anc, loudspeaker, microphone, history, industrial, comparison

### paper-abali-fan-phase-cancellation-patent

**"Mutual Active Cancellation of Fan Noise and Vibration"** — Abali, Guthridge, Harper, Manson, Marr Jr. (IBM → Lenovo) · US 7,282,873 B2, filed 2004, issued 2007 · `raw/PhaseCancelingFans-US7282873B2.txt`

- Patent: multiple fans in a computer enclosure are phase-locked to the same set speed via tachometer feedback, then driven with a controlled **relative phase** so their pressure waves destructively interfere at a target region.
- No loudspeakers or error mics — cancellation is entirely mechanical, by modulating inter-fan phase.
- Addresses both acoustic noise and vibration simultaneously.
- Interesting counterpoint to loudspeaker-based ANC: cheap, no secondary-path modeling, but only works when the noise sources are themselves controllable.
- Tags: anc, history, industrial, comparison

---

## AI-ANC ingestion batch (2026-04-14)

### paper-helwani-nnsi

**"Generative Modeling Based Manifold Learning for Adaptive Filtering Guidance"** — Helwani, Smaragdis, Goodwin · ICASSP 2023 · `raw/NNSI-Helwani-ICASSP2023.txt` · primary source for [[neural-system-identification]]

- **Topology-aware VAE** over impulse responses; disentangled latent space enforced via DIP-VAE-II regularization; simplicial-complex topology constraint relates mic-array geometry to the IR manifold via the Kirchhoff–Helmholtz integral.
- **Retraction-based manifold optimization** on the VAE latent space. First-order (Euler) and second-order (Newton) variants are both derived.
- Demonstrated on **acoustic impulse-response tracking** — *not* directly on FxLMS (FxLMS extension is Sarkar et al. 2025 *Latent FxLMS*; see [[fxlms-algorithm]]).
- Training set: 200 synthetic RIRs (6×6×2 m shoebox, Pyroomacoustics). Test: unseen RIRs at 20 dB SNR. Converges faster than RLS and $\ell_1$-regularized RLS due to dimensionality reduction.
- Limitations noted: manifold is dataset-dependent; no explicit secondary-path modeling; FxLMS integration not tested in this paper.
- Tags: anc, rls, secondary-path, acoustics, reference, comparison

### paper-zhang-pinn-anc

**"An Active Noise Control System Based on Soundfield Interpolation Using a Physics-informed Neural Network"** — Zhang, Ma, Abhayapala, Samarasinghe, Bastine · arXiv 2309.10605, 2023 · `raw/PINN-ANC-Zhang-2309.10605.txt` · canonical primary source for [[pinn-virtual-sensing]]

- **Canonical PINN-for-ANC paper.** PINN is a small MLP (1 hidden layer, 16 neurons, $\tanh$) mapping $(n, x, y, z) \to p(n,x,y,z)$.
- Loss = MSE at monitoring mics + wave-equation residual $\nabla^2 p - (1/c^2)\partial_t^2 p$. Trained via autodiff (TensorFlow), $5\times 10^5$ epochs, LR $10^{-3}$.
- Geometry: **8 monitoring mics on a $r = 0.26$ m sphere outside the ROI**, virtual error mics at $\pm 0.1$ m ear positions; 2 secondary sources, 1 primary (300 / 400 / 500 Hz tones); $F_s = 24$ kHz.
- ANC integration: the PINN-interpolated virtual error signals $e_v$ are fed into an **otherwise-standard FxLMS loop** — critically, the controller is unchanged.
- Reported: ~8 dB improved interpolation error vs spherical-harmonic baseline; **$-13$ dB** additional steady-state noise reduction; $-10$ dB residual at ears.
- Tags: anc, feedforward, fxlms, microphone, wave-equation, acoustics, comparison

### paper-piml-sound-field-survey

**"Physics-Informed Machine Learning for Sound Field Estimation"** *(IEEE SPM invited survey)* — Koyama et al. · *IEEE SPM* 2024 · `raw/PINN-SoundField-Survey-2408.14731.txt`

- Five-category taxonomy of PIML for sound-field estimation: **(1) basis expansion** (plane-wave / spherical harmonic / equivalent source, inherently satisfy PDE); **(2) PDE-kernel KRR**; **(3) linear regression with PDE regularization**; **(4) NN with PDE loss** (vanilla PINN); **(5) hybrid architectures** that embed physics into the layer design (e.g. Point Neuron).
- Application domains surveyed: room acoustics, VR/AR audio, HRTF estimation, beamforming, source localization, **spatial ANC**, nearfield holography, RIR reconstruction. Both frequency- and time-domain formulations.
- Key framing: physics constraints are essential priors; pure black-box NNs produce unphysical artifacts in low-data regimes.
- No cross-method benchmark — the paper is taxonomy, not evaluation.
- Use as umbrella reference on [[pinn-virtual-sensing]].
- Tags: wave-equation, acoustics, reference, tutorial, comparison

### paper-olivieri-volumetric-pinn

**"Physics-Informed Neural Network for Volumetric Sound Field Reconstruction of Speech Signals"** — Olivieri, Karakonstantis, Pezzoli, Antonacci, Sarti, Fernandez-Grande · arXiv 2403.09524, 2024 · `raw/PINN-Volumetric-2403.09524.txt`

- **Time-domain** PINN reconstructing 3-D pressure fields from sparse mics; tested on real measured rooms via **MeshRIR** dataset.
- Loss combines wave-equation residual + mic-position MSE, weighted. Supports derived fields (particle velocity, intensity) via autodiff.
- **Broadband** speech inputs — crucial for the ANC use case, since most PINN acoustic papers are single-frequency.
- Beats frequency-domain equivalent-source and time-domain RIR-ESM baselines on reconstruction error.
- Tags: wave-equation, acoustics, reference, comparison

### paper-borrel-1d-pinn

**"Physics-Informed Neural Networks for One-Dimensional Sound Field Predictions with Parameterized Sources and Impedance Boundaries"** — Borrel-Jensen, Engsig-Karup, Jeong · arXiv 2109.11313, 2021 · `raw/PINN-1D-ParamSources-2109.11313.txt`

- **Early PINN-acoustics paper** (2021); 1-D only, framed as "stepping stone to 3-D".
- Novel: parameterized *moving* Gaussian sources + **frequency-dependent impedance** boundaries via rational admittance decomposition and auxiliary differential equations (NADE sub-net).
- Target use case is game/VR acoustics (real-time surrogate replacing gigabyte IR lookup tables), not ANC — include as historical context only.
- Reports errors $<2\%$ / 0.2 dB on test scenarios; data-free training (physics loss only).
- Tags: wave-equation, impedance, history, reference

### paper-chen-deepset-pinn

**"Permutation-Invariant Physics-Informed Neural Network for Region-to-Region Sound Field Reconstruction"** — Chen, Zhao, Ma, Cheng, Burnett · arXiv 2601.19491, 2025 · `raw/PINN-PermutationInvariant-2601.19491.txt`

- **Deep-set architecture** $\hat{P}(\mathbf{r},\mathbf{s},f) = \rho(\phi(\mathbf{r}) + \phi(\mathbf{s}))$. Summation in latent space guarantees permutation invariance between source and receiver positions, which *automatically* enforces **acoustic reciprocity** $P(\mathbf{r},\mathbf{s}) = P(\mathbf{s},\mathbf{r})$ without a loss term.
- Region-to-region ATF interpolation (both source and receiver varying over domains) — stronger than point-to-region.
- Two MLPs ($\phi$, $\rho$), 2 hidden layers × 128 neurons, $\tanh$. Helmholtz loss + data loss, $\lambda = 1$. One model per frequency bin (limitation).
- Outperforms kernel ridge regression by **$>5$ dB NMSE above 1 kHz** on UTS 60-speaker / 64-mic anechoic dataset.
- Tags: wave-equation, acoustics, array, comparison

### paper-bi-point-neuron

**"Point Neuron Learning: A New Physics-Informed Neural Network Architecture"** — Bi & Abhayapala · arXiv 2408.16969, 2024 · `raw/PINN-PointNeuron-2408.16969.txt`

- Embeds the **free-space Green's function** (0-th order spherical Hankel $h_0^{(1)}$) as the neuron activation, so every forward pass **strictly satisfies the Helmholtz equation by construction** — no PDE loss term required.
- Neuron parameters are interpretable: weights = source amplitudes, biases = source locations.
- Complex-valued throughout (no separate real/imag pipelines).
- Only observation-MSE + $\ell_1$ regularization; closed-form complex gradients derived.
- Outperforms vanilla PINN and kernel ridge regression on 2-D/3-D reverberant reconstruction.
- Tags: wave-equation, acoustics, comparison, reference

### paper-feng-meta-delayless-anc

**"Meta-Learning-Based Delayless Subband Adaptive Filter using Complex Self-Attention for Active Noise Control"** — Feng & So · arXiv 2412.19471, 2024 · `raw/MetaLearning-DelaylessSubband-2412.19471.txt` · primary source for [[meta-learning-anc]]

- **Strongest match to Sarkar et al. 2025 ref [5]**: a single-headed attention RNN with learnable feature embedding is the **meta-learner**; it outputs a *predicted gradient* $\tilde{g}(n)$ that replaces the FxLMS gradient, so the filter update is $\mathbf{w}(n+1) = \mathbf{w}(n) - \mu\tilde{g}(n)$.
- Inputs to the meta-learner: subband filtered-reference $x_{f,k}(n)$ and subband error $e_k(n)$ after a polyphase analysis filter bank (downsampling $D$); FFT applied post-filter bank for stable features.
- **Delayless subband** novelty: update rate is reduced by $D$ (e.g. $D = 16$ gives a 1 kHz update from 16 kHz samples), relaxing the real-time compute budget without introducing subband-delay artifacts. Skip-updating strategy further reduces update frequency for constrained devices.
- Multi-condition meta-training over diverse noise types and environments; a loudspeaker saturation model is included in the training distribution, so the learned rule is **implicitly nonlinear-robust**.
- Explicitly addresses partial-secondary-path knowledge (main delay only needed, not full $\hat{S}$).
- Tags: anc, fxlms, feedforward, secondary-path, stability, comparison

### paper-xiao-meta-sfanc

**"Meta-Learning Based Selective Fixed-Filter Active Noise Control System with ResNet Classifier"** — Xiao, Liu, Dai, Lan · arXiv 2504.19173, 2025 · `raw/MetaLearning-SFANC-ResNet-2504.19173.txt`

- **Selective Fixed-Filter ANC (SFANC):** a pre-trained filter bank $\{W_i\}$, one per noise category; incoming noise is classified, best-matched filter selected, optionally fine-tuned. Fast response without online-learning lag.
- **Meta-learning contribution:** MAML-FxLMS pre-trains filters so each is already one-or-two gradient steps from the optimum on *homologous unseen* noises. Inner loop batches multiple inputs to widen the receptive field and speed convergence.
- **ResNet classifier:** mel-spectrogram → ResNet → one of $N$ noise categories (trained on ESC-50). Replaces prior frequency-band heuristics that failed on broadband real-world noise.
- Faster steady-state convergence than vanilla FxLMS; higher classification accuracy than non-learned SFANC.
- Note: meta-learning is *over the filter-bank initialization*, not over a weight-update rule — complementary to the Feng & So 2024 paper.
- Tags: anc, fxlms, comparison, reference

### paper-yang-coinit-meta-anc

**"Co-Initialization of Control Filter and Secondary Path via Meta-Learning for Active Noise Control"** — Yang et al. · arXiv 2601.13849, 2026 · `raw/MetaLearning-CoInit-2601.13849.txt` · relevant to both [[meta-learning-anc]] and [[neural-secondary-path]]

- **Joint MAML** over two initializations: control filter $\Phi \in \mathbb{R}^{L_w}$ **and** secondary-path FIR model $\Psi \in \mathbb{R}^{L_s}$, both meta-learned from a small library of measured in-ear headphone paths.
- Inner loop: Phase A (auxiliary-noise secondary-path ID, $T_A$ steps) → Phase B (FxLMS control update, $T_B$ steps). Validation on held-out segment; meta-gradients $\nabla_\Phi, \nabla_\Psi$ combined with forgetting factors $\lambda_w, \lambda_s$.
- **Critical distinction from neural secondary-path modeling:** Yang et al. do **not** replace $\hat{S}$ with a neural surrogate. They warm-start the classical online-secondary-path FIR model and the classical FxLMS filter from meta-learned coefficients; the **runtime algorithm is unchanged**. This is pure initialization, not architectural substitution.
- Error-jump detector (canceller-norm threshold) re-initializes on acoustic-environment change.
- Dataset: RWTH Aachen IKS PANDAR — 46 measured in-ear paths (23 subjects × 3 fit conditions), band-limited 200–2000 Hz, $F_s = 16$ kHz.
- Tags: anc, fxlms, feedforward, secondary-path, headphones, comparison, reference

### paper-dai-speech-preserving-anc

**"Speech-Preserving Active Noise Control: a Deep-Learning Approach in Reverberant Environments"** — Dai Shuning (thesis; advisor Gan Woon Seng) · arXiv 2604.10979, 2026 · `raw/DeepANC-SpeechPreserving-Reverberant-2604.10979.txt` · follow-up discussed at [[deep-anc-crn]]

- **Follow-up to Zhang & Wang 2021 Deep ANC.** End-to-end CRN with LSTM; complex-spectrum-mapping (CSM) processes STFT real/imaginary parts jointly.
- **Speech-preservation loss:** a selective-retention term identifies speech-like spectral regions and penalizes their suppression while still cancelling environmental noise. Framing: "semantic separation" rather than pure noise power reduction.
- Uses the Image Source Method for **reverberant** training environments (configurable geometry and $RT_{60}$) — the main extension beyond Zhang & Wang 2021.
- Evaluates on ESC-50 + custom datasets with three scenarios: pure noise, speech + noise, transients. Metrics: NR (dB), PESQ, STOI.
- Reports superior NR vs FxLMS on non-stationary babble; PESQ/STOI confirm speech retention.
- The extracted text is partly from a thesis; figures and full config tables are omitted by pdf2txt.
- Tags: anc, feedforward, comparison, headphones, room

### paper-luo-gfanc

**"Deep Generative Fixed-Filter Active Noise Control"** — Luo, Shi, Shen, Ji, Gan · arXiv 2303.05788, 2023 · `raw/GFANC-Luo-2303.05788.txt` · supervised precursor to the GFANC-RL paper below

- **Not a PPO/SAC-style policy,** despite the "policy over filters" framing — GFANC is a **1-D CNN** (~0.22 M params) that outputs a binary weight vector $\mathbf{g}(n) \in \{0,1\}^M$ per noise frame, selecting which of $M$ sub-filters to activate.
- Sub-filter decomposition: a single broadband pre-trained filter $c$ is converted to $C$ via DFT, partitioned into $M$ subbands using conjugate symmetry, and each subband is converted back to time-domain FIR $c_m$. $y(n) = \sum_m g_m\,\mathbf{x}^T(n)\mathbf{c}_m$.
- Auto-labeling of binary selection vectors via LMS convergence on training segments — removes manual labeling.
- 97.2% label-prediction accuracy; beats SFANC on real recorded noise; no gradient-feedback divergence risk because it's fixed-filter.
- **Not true DRL** — included on [[deep-rl-anc]] as the contrasting "policy over filter bank" supervised baseline.
- Tags: anc, fxlms, comparison, reference

---

## DRL-ANC ingestion batch (2026-04-15)

### paper-luo-gfanc-rl

**"GFANC-RL: Reinforcement Learning-based Generative Fixed-Filter Active Noise Control"** — Luo, Ma, Shi, Gan · *Neural Networks* 178, 2024, DOI [10.1016/j.neunet.2024.106687](https://doi.org/10.1016/j.neunet.2024.106687) · `raw/GFANC-RL-Luo-NeuralNetworks-2024.txt` · primary source for [[deep-rl-anc]]

**Bottom line:** the earliest ingested paper that genuinely models ANC as a Markov decision process and trains with a standard DRL algorithm (SAC). Eliminates the labelling burden of supervised GFANC and the non-differentiable binary-weight problem through RL's stochastic policy.

- **Algorithm:** Soft Actor-Critic with discrete-action stochastic policy $\pi(\mathbf{g}\mid\mathbf{x})$. Dual critics, experience replay, entropy regularization with automatic temperature tuning.
- **MDP formulation:** state $s_t = \mathbf{x}_t$ (1-second noise reference frame). Action $a_t = \mathbf{g}_t \in \{0,1\}^{15}$ (binary selection vector over $M = 15$ sub-filters spanning 20–7980 Hz). Transition $T(\mathbf{x}_{t+1}\mid\mathbf{x}_t,\mathbf{g}_t) = T(\mathbf{x}_{t+1}\mid\mathbf{x}_t)$ — next frame is action-independent. Discount $\gamma = 0$. **Effectively a contextual bandit, not a full RL problem.**
- **Reward:** $r_t = 10\log_{10}\!\big(\sum_n d_t^2(n)/\sum_n e_t^2(n)\big)$ — instantaneous noise reduction at the error mic over the 1-second frame.
- **Sub-filter bank:** same orthogonal-subband decomposition as the supervised GFANC paper; $\mathbf{w}(n) = \sum_m g_m(n)\mathbf{c}_m$.
- **Training:** 80 000 synthetic 1-second noise instances (white noise through random bandpass filters), SNR = 5 dB for robustness. Offline. At deployment, control filter runs at sample rate; CNN policy runs at frame rate on a co-processor.
- **Baselines:** supervised GFANC, SFANC, adaptive FxLMS. *No comparison with other DRL algorithms* — not even vanilla policy gradient. Notable gap.
- **Headline numbers:** on real traffic / aircraft / drill noise, GFANC-RL gives **14.4 / 13.3 / 9.2 dB** NR vs FxLMS **7.1 / 4.2 / 3.9 dB** — roughly 7–9 dB over classical adaptive; comparable to supervised GFANC; ~5 dB over SFANC in some frames.
- **What it is *not*:** a PPO/SAC/TD3 agent emitting continuous speaker drive. Action space is discrete filter selection over a pre-computed fixed-filter basis.
- Tags: anc, feedforward, fxlms, loudspeaker, stability, comparison

### paper-li-rl-secondary-path

**"Reinforcement Learning Algorithm for Secondary Path Identification in Active Noise Control Systems"** — Li, Wu, Bai · *AIP Advances* 15(8):085021, 2025, DOI [10.1063/5.0285877](https://doi.org/10.1063/5.0285877) · `raw/RL-SecondaryPathID-LiWuBai-AIPAdvances-2025.txt` · relevant to both [[deep-rl-anc]] and [[neural-secondary-path]]

**Bottom line:** first paper in the wiki that benchmarks **PPO, DDPG, DQN** and a new **GRPO** variant head-to-head on a real ANC subproblem (nonlinear secondary-path identification), then plugs the best performer back into a real-vehicle closed-loop FxLMS test. GRPO wins; PPO is fast but unstable.

- **What is learned:** the parameters of a **3-layer fully-connected nonlinear neural network** (64 → 64 → 32) that models $\hat{S}(z)$. The RL agent optimizes weights; it is not learning a higher-level "when to step $\hat{S}$" policy.
- **MDP specifics:** state $s_t = \mathbf{x}(n)$; action $a_t$ is either the discrete Q-network output (DQN) or continuous parameter updates (DDPG / PPO / GRPO). Reward $r_t = -|d(n) - \hat{y}(n)|$. Experience replay with random minibatches.
- **Algorithms compared:** DQN, DDPG, PPO, and **GRPO** (Group Relative Policy Optimization with periodic-prediction auxiliary module). Relative modeling errors on real vehicle data: DQN 89.40%, DDPG 92.04%, PPO 89.36%, **GRPO 87.02%**. PPO shows large reward-curve fluctuations; GRPO is the speed–stability sweet spot.
- **GRPO's periodic-prediction module:** a second FFT-based agent extracts frequency-regularity features from the noise and feeds them back into the primary actor-critic via a KL-divergence constraint and a regularized-advantage term. Novel contribution of the paper.
- **Full-loop deployment:** identified $\hat{S}$ is plugged into a closed-loop FxLMS-style controller ("RL-FxLMS"). Tested on **real ZSL-92 armored-vehicle** cabin noise at idle / 1500 / 2100 / 2700 rpm, front/rear error mics. Max NR: **6.5 dB idle, 8.8 dB at 2700 rpm.** MSE reduction 53.1% (0.32 → 0.15), SNR +5.1 dB, relative modeling error 12.6%. $F_s = 16$ kHz.
- **Gaps:** single platform; no comparison with classical nonlinear-ID baselines (Volterra, NLMS variants); no ablation isolating the periodic module from the KL constraint; embedded real-time feasibility not discussed.
- Tags: anc, fxlms, secondary-path, stability, industrial, comparison

### paper-wang-metric-vs

**"Transferable Selective Virtual Sensing Active Noise Control Based on Metric Learning"** — Wang et al. (NTU) · arXiv 2409.05470, 2024 · `raw/TransferableVirtualSensing-MetricLearning-Wang-2409.05470.txt` · adjacent to [[pinn-virtual-sensing]]

**Bottom line:** a lightweight 1-D CNN (~13 k params) uses cosine similarity in its learned embedding space to **select** which of $K$ pre-trained auxiliary filters $H_o(z) = P_p(z) - S_p(z)W_{\text{opt}}(z)$ to apply at runtime. The filters themselves come from classical Moreau-style virtual-sensing FxLMS run offline.

- **Architecture:** 1-D CNN, three conv layers (10, 20, 20 filters) + residual block + max pool + two FC layers (1×620, 1×15). Min-max normalization of 1-second waveform input. **12 955 parameters** — explicitly sized for co-processor deployment.
- **"Metric learning" clarification:** *not* a triplet or contrastive loss. The CNN's feature-extraction module produces embeddings $E_x$ for the reference and $E_q$ for each pre-trained AF training noise; match score is cosine similarity $S_q = E_x^T E_q / \max(\|E_x\|_2\|E_q\|_2, \alpha)$; selected AF is $\arg\max_q S_q$. "Metric learning" here means "distance metric in an embedding space learned via feature extraction," not a metric-loss-trained network.
- **Auxiliary-filter bank:** for each of $K$ target noise classes, $H_o(z) = P_p(z) - S_p(z)W_{\text{opt}}(z)$ is pre-computed offline by running FxLMS with an error mic at the virtual target. Runtime uses the selected $H_o$ as the virtual error signal.
- **Transferability claim:** train on "System I" (15 AF classes, 80 000 synthetic waveforms) → 95.6% in-domain. Deploy on "System II" (5 AF classes, different acoustic paths, SNR 30 dB) **without retraining conv layers** → **92.6%**. Competing architectures (M3, M5, M6-res, M34-res) drop to 36.6–79.9%. Unseen real-world noise (genset + compressor) nearly matches oracle full-virtual-mic performance.
- **Positioning vs Zhang 2023 PINN-ANC:** both target ANC where the error mic is inaccessible. Zhang's PINN learns an *explicit field representation* constrained by the wave equation; Wang's CNN learns a *selector* over classical Moreau-style virtual-sensing filters. PINN wins on physical consistency and sparse-sensor extrapolation; metric learning wins on compute budget and cross-system transfer.
- **Gaps:** cosine similarity not ablated against other distance metrics; transfer tested only on two simulated systems; no domain-adaptation baseline; no acoustic-path-change robustness analysis.
- Tags: anc, fxlms, microphone, comparison, reference

### paper-shi-anc-review-2023

**"Active Noise Control in The New Century: The Role and Prospect of Signal Processing"** — Shi, Lam, Gan, Cheer, Elliott · *IEEE Signal Processing Magazine* 2023, arXiv 2306.01425 · `raw/ANC-NewCentury-Review-Shi-2306.01425.txt` · cross-cutting reference

**Bottom line:** the canonical modern ANC review (2023). Covers history, classical signal-processing challenges, modern commercial deployments, and some recent deep-learning applications. **Does not cover DRL or PINNs.** Useful as the go-to citation for the *classical* side of the wiki and as historical context.

- **Confirmed absent:** reinforcement learning, PPO, SAC, DDPG, policy gradient, reward, MDP, PINN, Helmholtz losses, wave-equation-constrained models, transformer or attention ANC.
- **Confirmed present:**
  - **History (Sec. 1):** Lueg 1936 → Olson & May 1950s → Widrow 1975 → Morgan 1980 / Burgess 1981 (FxLMS) → DSP revolution → commercial headphones / aircraft / automotive through 2023.
  - **Technical bottlenecks (Sec. 2):** causality constraints in portable ANC, transducer and acoustic nonlinearity (qualitative only), MCANC/MIMO trade-offs, mic-placement optimization, psychoacoustic design, classical Moreau-style virtual sensing.
  - **Recent AI/signal-processing advances (Sec. 4):** deep-learning direct filter replacement (LSTM, CNN, CRN — flags latency concern); CNN-based filter selection (SFANC / GFANC — cites the ingested GFANC-Luo 2023 paper); meta-learning for hyperparameter tuning (one citation, ref [49], a modified MAML for ANC); spatial ANC via spherical-harmonic decomposition; head-tracking and remote sensing for moving quiet zones.
  - **Novel applications:** ANC windows and sound barriers, machinery enclosures, pillows, fMRI scanners, wireless distributed ANC.
- **Overclaim caveat:** the review pre-dates Latent FxLMS (2025), the PINN-ANC literature (2023–2025), and everything in the meta-learning ingestion batch. Always cite as "as of 2023."
- Tags: anc, lms, fxlms, secondary-path, causality, history, reference, tutorial, headphones, duct, room

---

## Classical ANC Reviews (2026-04-16)

### paper-kuo-morgan-anc-tutorial-1999

**"Active Noise Control: A Tutorial Review"** — Kuo & Morgan · *Proc. IEEE* 87(6):943–973, June 1999 · `raw/ANC-Tutorial-Review-1999-2010913102917710.txt` · canonical ANC tutorial

**The** foundational ANC tutorial review. Co-author Dennis R. Morgan independently derived FxLMS; his treatment here is authoritative.

- **Coverage:** broadband/narrowband feedforward ANC, feedback ANC, multichannel ($J \times K \times M$) ANC, online secondary-path modeling (Eriksson additive-noise method, delay-compensated LMS), lattice/frequency-domain/subband/RLS structures, DSP implementation, applications (duct, automotive exhaust, headphones, transformer, vibration).
- **FxLMS derivation:** from mean-square cost function via steepest descent; secondary-path compensation is the key difference from standard LMS; convergence bound $0 < \mu < 2/(\lambda_{\max} S_{\max}^2)$.
- **Causality constraint:** electrical delay must not exceed acoustic delay from reference mic to cancelling speaker; when violated, only narrowband/periodic noise can be controlled.
- **Coherence bound:** $\text{NR}(f) = -10\log_{10}(1 - \gamma_{dx}^2(f))$ — same formula as [Wise & Leventhall 2010](#paper-wise-leventhall-lf-anc).
- **Applications demonstrated:** 20 dB broadband duct attenuation; automobile exhaust system; active headset; transformer hum; telephone ringer cancellation.
- **Position in the wiki:** the classical "textbook" that [[fxlms-algorithm]], [[lms-algorithm]], and [[neural-secondary-path]] build upon. Shi 2023 and Lu et al. 2021 both cite this as the standard reference.
- Tags: anc, fxlms, lms, secondary-path, feedback, feedforward, duct, stability, causality, tutorial, reference, history, person

### paper-lu-anc-survey-part1-2021

**"A survey on active noise control in the past decade—Part I: Linear systems"** — Lu, Yin, de Lamare, Zheng, Yu, Yang, Chen · *Signal Processing* 183:108039, 2021 · DOI [10.1016/j.sigpro.2021.108039](https://doi.org/10.1016/j.sigpro.2021.108039) · `raw/ANC-Survey-Part1-1-s2.0-S0165168421000785-main.txt`

Comprehensive decade survey (2009–2020) of linear ANC algorithms. Companion Part II covers nonlinear ANC and applications.

- **Algorithm families reviewed:** filtered-x (FxLMS + 8 variants, FxAP, FxRLS, subband SAF, lattice), filtered-e (FeLMS), filtered-u (FuLMS/FuRLS for IIR controllers). Includes detailed timeline tables tracing each variant's origin.
- **Practical considerations:** 21 online secondary-path estimation methods cataloged; acoustic feedback solutions; virtual error sensing; frequency mismatch; analog ANC; ASAC (active structural acoustic control); GPU/PU complexity reduction.
- **Novel 2010s methods:** psychoacoustic ANC (perceptual loudness weighting), sparse ANC (zero-attracting / proportionate NLMS), convex combination (fast + slow filter mixing $\lambda(n)$), fractional-order calculus updates (Grünwald–Letnikov), 3-D zone-of-quiet via spherical harmonics, **selective ANC** (pre-tuned filter bank — direct precursor to SFANC/GFANC), distributed ANC over WASNs (incremental IFxLMS + diffusion DFxNLMS).
- **Bridges** Kuo & Morgan 1999 and Shi et al. 2023: covers the decade of algorithmic refinement between them. Explicitly cites Kuo & Morgan 1999 as ref [36].
- **Selective ANC note:** Sec. 4.6 describes the pre-tuned filter-bank selection paradigm later scaled up by [Luo et al. 2023](#paper-luo-gfanc) and [Luo et al. 2024](#paper-luo-gfanc-rl).
- **Companion:** Part II (below) covers nonlinear ANC and applications.
- Tags: anc, fxlms, lms, nlms, rls, secondary-path, stability, feedback, feedforward, hybrid-control, duct, room, industrial, reference, tutorial

### paper-lu-anc-survey-part2-2021

**"Active noise control techniques for nonlinear systems"** — Lu, Yin, de Lamare, Zheng, Yu, Yang, Chen · arXiv [2110.09672v2](https://arxiv.org/abs/2110.09672) / *Signal Processing* 181:107929, 2021 · `raw/ANC-Survey-Part2-NonlinearSystems-2110.09672v2.txt` · companion Part II to [Part I](#paper-lu-anc-survey-part1-2021)

Comprehensive decade survey (2009–2020) of **nonlinear ANC (NLANC)**: the algorithms, heuristic methods, novel approaches, implementations, and applications that Part I's linear coverage does not reach.

- **NLANC algorithm families (Sec. 3):** Volterra series (VFxLMS and robust variants — exponential cost growth), Hammerstein / Wiener / Hammerstein-Wiener block models, **FLANN** (trigonometric expansion — most popular NLANC controller), Chebyshev / Legendre / EMFN orthogonal polynomial filters, bilinear filters with diagonal-channel structure.
- **Heuristic global optimization (Sec. 4):** GA, BSA, PSO, BFO, firefly, fireworks algorithms — many bypass secondary-path estimation entirely. PSO with Wilcoxon norm gains ~5 dB over MSE-based methods.
- **Novel NLANC methods (Sec. 5):** spline adaptive filters (LUT-based, low cost, FIR/IIR variants), kernel adaptive filters (RKHS mapping via Gaussian/logistic kernels — good modeling but growing network size), nonlinear distributed ANC over WASNs.
- **Implementations (Sec. 6):** DSP (fixed-point ~2 dB degradation), FPGA (filtered-weight FxLMS, parallel folding), VLSI (compact folded FsLMS).
- **Applications (Sec. 6):** fMRI (>40 dB), open-window ANC (16-channel, 5 dB), headphones (feedback FxLMS, virtual sensing, CBBANC), zone-of-quiet, spatial ANC (mode-domain), periodic/repetitive noise (ILC+RC for exhaust), transformer hum (15 dB, 84–97% energy density reduction), vehicle ANC.
- **Future challenges:** theoretical gaps for impulsive-noise convergence, KAF sparsification, IoT-ANC integration, computational complexity barrier for real-time NLANC, optimal parameter selection.
- **Neural networks:** pre-deep-learning NN methods (RBF, RNN, fuzzy) mentioned from 1995–2008 but marginal in the 2009–2020 survey decade. The deep ANC wave (CRN, meta-learning, PINN, DRL) came after this paper's coverage window.
- **Position in the wiki:** completes the Lu et al. 2021 two-part survey. Part I → linear foundations → Part II → nonlinear extensions. Together they bridge [[paper-kuo-morgan-anc-tutorial-1999]] (1999) and [[paper-shi-anc-review-2023]] (2023).
- Tags: anc, fxlms, lms, secondary-path, stability, feedback, feedforward, duct, room, headphones, industrial, reference, tutorial

---

## Pending ingestion (no PDF in `/l/dttd/` yet)

These are referenced in concept-page footnotes but have no `raw/` extraction:

- **Morgan 1980** — "An Analysis of Multiple Correlation Cancellation Loops with a Filter in the Auxiliary Path," *IEEE Trans. ASSP* 28(4):454–467. Paywalled at IEEE. Earliest known FxLMS filtered-x analysis, referenced by [[fxlms-algorithm]]. Secondary-source fallback: Kuo & Morgan, *Active Noise Control Systems*, Wiley 1996.
- **Burgess 1981** — "Active Adaptive Sound Control in a Duct: A Computer Simulation," *J. Acoust. Soc. Am.* 70(3):715–726. Paywalled at AIP/ASA. Earliest known full adaptive duct-ANC simulation, referenced by [[fxlms-algorithm]]. Secondary-source fallback: Elliott, *Signal Processing for Active Control*, Academic Press 2001.
- **Ryu, Lim, Lee 2024** — "Narrowband Active Noise Control with DDPG Based on Reinforcement Learning," *International Journal of Automotive Technology*. Paywalled at Springer; no arXiv preprint surfaced. Would fill the continuous-drive DRL-ANC gap on [[deep-rl-anc]].

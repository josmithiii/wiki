---
title: Neural Secondary-Path Modeling for ANC
created: 2026-04-14
updated: 2026-04-15
type: concept
tags: [anc, secondary-path, fxlms, stability, loudspeaker, headphones, comparison]
sources:
  - raw/DeepANC-nihms-1690502.txt
  - raw/MetaLearning-CoInit-2601.13849.txt
  - raw/RL-SecondaryPathID-LiWuBai-AIPAdvances-2025.txt
---

# Neural Secondary-Path Modeling

Three primary sources in the wiki cover this topic across the
"how radically should we replace classical $\hat{S}(z)$?" spectrum:

- **Zhang & Wang 2021** *Deep ANC* — *implicit*; no explicit plant
  model at runtime. The plant is absorbed into the end-to-end
  controller network.
- **Yang et al. 2026** *co-initialization* — classical FIR plant model,
  but with **meta-learned** starting coefficients; runtime algorithm
  unchanged.
- **Li, Wu, Bai 2025** *RL plant identification* — explicit **nonlinear
  neural-network** $\hat{S}(z)$ whose weights are fit by a deep RL
  agent (DQN/DDPG/PPO/GRPO compared); runs inside a closed-loop
  RL-FxLMS controller on a real ZSL-92 armored vehicle.

The generative-prior route (NNSI-style manifold constraint on $\hat{S}$)
is still speculative — none of the ingested papers apply NNSI directly
to a plant model. Physics-informed plant models (Thiele–Small + Helmholtz
differentiable blocks) are also still unrepresented.

## The problem

Every feedforward ANC system needs a model of the secondary path
$\hat{S}(z)$ — the transfer function from the control signal through the
DAC, amplifier, loudspeaker, acoustic propagation, and error microphone.
Classical FxLMS requires this estimate to have **phase error below 90°**
across the adaptation bandwidth (see [[fxlms-algorithm]]). In real
deployments $S(z)$ drifts:

- **Temperature and humidity** change the speed of sound and the driver's
  mechanical parameters.
- **Wind and airflow** modulate the acoustic path, especially outdoors
  (rooftop fans, HVAC outlets).
- **Fit and placement** (active [[headphones]], in-ear) change with every
  wear.
- **Nonlinear effects** (voice-coil heating, cone excursion, port
  compression) break the LTI assumption at high drive.

Classical practice: identify $\hat{S}(z)$ offline with white-noise probe
signals, or re-identify online with injected perturbation noise. Both are
unsatisfying — offline identification fails to track drift, and online
probe injection adds residual noise that degrades the ANC result.

## Neural alternatives

### 1. Implicit — subsumed in a Deep ANC controller

In [[deep-anc-crn]] the loss function includes the physical secondary path
during training, so the controller network implicitly learns to
pre-compensate $S(z)$. No explicit $\hat{S}(z)$ is maintained at runtime.
Upside: simple, nothing to identify online. Downside: the network freezes
the (training distribution of) $S(z)$, so large deployment drift forces
retraining.

### 2. Meta-learned FIR initialization — Yang et al. 2026

Yang et al.[^yang26] propose the minimal-intrusion neural approach:
**keep the classical FIR plant model and the classical runtime algorithm,
but meta-learn their starting coefficients across a library of measured
plants.** At deployment, initialize $\hat{\mathbf{s}} \gets \Psi$ (the
meta-learned secondary-path FIR) and $\mathbf{w}\gets\Phi$ (the meta-learned
controller), then run standard online secondary-path modeling (OSPM) and
standard FxLMS. The update equations are unchanged — this is **pure
initialization**, not architectural substitution.

The meta-training inner loop has two phases per task:

- **Phase A** ($T_A$ steps): secondary-path identification with auxiliary
  noise $v(n)$, updating $\hat{\mathbf{s}}$ toward the task's true $\mathbf{s}$.
- **Phase B** ($T_B$ steps): FxLMS control-filter update, using the
  freshly-adapted $\hat{\mathbf{s}}$.

Meta-gradients $\nabla_\Phi, \nabla_\Psi$ are accumulated with separate
forgetting factors $\lambda_w, \lambda_s$ that down-weight older tasks.

At deployment, an **error-jump detector** (threshold on canceller norm)
triggers re-initialization when the acoustic environment changes — e.g.
in-ear headphones refitted.

Dataset: **RWTH Aachen IKS PANDAR** — 46 measured in-ear paths (23
subjects × 3 fit conditions), band-limited 200–2000 Hz, $F_s = 16$ kHz.
Generalization on unseen in-ear paths improves with training-set diversity,
measured via log-spectral distance.

Why this matters: Yang et al. preserves every stability and convergence
guarantee of classical FxLMS while still getting a meta-learning speedup,
because the runtime algorithm is literally the same. For conservative
deployments — certified hearing aids, medical devices — this is a much
easier sell than a learned update rule or a neural plant surrogate.

Cross-referenced on [[meta-learning-anc]] as the initialization-only
extreme of the meta-learning-for-ANC spectrum.

### 3. Explicit nonlinear neural identification — Li, Wu, Bai 2025

Li, Wu & Bai[^liwubai25] parameterize the secondary path as a **3-layer
fully-connected nonlinear neural network** $\hat{S}_\theta$
(64 → 64 → 32) and fit $\theta$ using deep reinforcement learning. This
is the canonical "black-box nonlinear online ID" approach that the
previous version of this page flagged as an empty slot.

**What the RL agent learns.** $\theta$ — the weights of the plant
model. The state is the reference signal $\mathbf{x}(n)$, the action is
a weight update (discrete for DQN, continuous for DDPG / PPO / GRPO),
and the reward is the negative absolute error between the network's
prediction $\hat{y}(n)$ and the desired output $d(n)$ at the error
microphone:
$$
r_t = -\,|d(n) - \hat{y}(n)|.
$$
Experience replay with random minibatches stabilizes training.

**Algorithm comparison.** Four RL algorithms tested on real vehicle
data; the order of merit on relative modeling error (lower is better):

| Algorithm | RME |
| --- | --- |
| **GRPO** (their contribution) | **87.02%** |
| PPO | 89.36% (fast, unstable) |
| DQN | 89.40% |
| DDPG | 92.04% |

**GRPO** = Group Relative Policy Optimization with a periodic-prediction
auxiliary module. A second FFT-based agent extracts frequency-regularity
features from the reference noise and feeds them to the primary
actor-critic via a KL-divergence constraint and a regularized-advantage
term. See [[deep-rl-anc]] for the RL-algorithm discussion in more depth.

**Closed-loop deployment.** The identified $\hat{S}_\theta$ is plugged
into a closed-loop FxLMS variant they call "RL-FxLMS" and tested on a
real **ZSL-92 armored vehicle** at idle / 1500 / 2100 / 2700 rpm, with
front and rear error mics. Reported NR: **6.5 dB idle, 8.8 dB at
2700 rpm**, MSE reduction 53.1%, SNR improvement 5.1 dB. This is the
first evidence in the wiki that a fully-neural $\hat{S}$ can close a
real-vehicle ANC loop better than a classical linear FIR identifier.

**Probe signal.** The paper exercises the plant with the natural ANC
reference signal — no explicit auxiliary white-noise probe. Probe-free
operation is well-defined because the engine noise already has
broadband content at every tested RPM.

**What it does *not* establish.**

- **Single platform** — all results are on the ZSL-92 vehicle. No
  cross-vehicle or cross-environment transfer tested.
- **No Volterra baseline** — the natural classical nonlinear-ID baseline
  for comparison (Volterra series, NLMS variants) is not run. The only
  baseline is an unspecified LMS-based linear plant ID.
- **No ablation** separating GRPO's periodic-prediction module from its
  KL constraint, so we can't attribute the improvement to either alone.
- **Real-time feasibility on embedded hardware** is not discussed;
  training is offline, deployment uses a PC-scale inference environment.

### 4. Generative secondary-path priors (NNSI-style)

Train an autoencoder on a dataset of secondary paths collected across the
expected operating envelope (temperatures, positions, fit conditions).
Online, identify $\hat{S}$ by latent-space adaptation over the decoder —
the same NNSI trick that [[neural-system-identification]] applies to the
*controller* filter, here applied to the *plant* filter.

This is speculative — Helwani 2023 applies NNSI to acoustic IR tracking
but not to a plant-in-the-loop ANC setting, and Yang 2026 uses a flat FIR
rather than a neural-manifold parameterization. The natural experiment
is to stack Yang-style meta-learning with Helwani-style manifold
constraints: meta-learn the *manifold* across plants rather than the FIR
coefficients directly.

### 5. Physics-informed plant models

Encode the loudspeaker's Thiele–Small small-signal model and the acoustic
path's Helmholtz propagation as differentiable blocks, and learn only the
residual. Much higher sample efficiency than a black-box identifier when
the physics is partially known.

## Open questions for the project

- **Latent drift identification.** Can we identify the secondary path in
  the latent space of a pre-trained autoencoder faster than FxLMS
  adapts the controller? If yes, we get a clean separation of timescales:
  fast controller adaptation (Latent FxLMS) on top of a slowly drifting
  latent plant model.
- **Probe-free bounds.** Under what excitation conditions is probe-free
  online identification well-posed?
- **Joint vs decoupled identification.** Is it better to identify
  controller and plant jointly (end-to-end Deep ANC) or to keep them
  decoupled with explicit $\hat{S}$? The answer likely depends on the
  drift rate.

## Relation to other pages

- [[fxlms-algorithm]] — classical secondary-path requirement and the 90°
  phase-error bound.
- [[deep-anc-crn]] — the implicit / end-to-end alternative.
- [[meta-learning-anc]] — Yang 2026 co-init is cross-listed; this page
  treats the plant-model half of the contribution, the meta-learning page
  treats the controller-initialization half.
- [[neural-system-identification]] — the manifold-constrained ID framework
  that this page's item 4 instantiates.
- [[ai-anc-overview]] category 3 — where this page sits in the taxonomy.

[^yang26]: Yang et al., "Co-Initialization of Control Filter and Secondary Path via Meta-Learning for Active Noise Control," arXiv:2601.13849, 2026. See `raw/MetaLearning-CoInit-2601.13849.txt`.
[^liwubai25]: Li, W., Wu, C., Bai, F., "Reinforcement learning algorithm for secondary path identification in active noise control systems," *AIP Advances*, vol. 15, no. 8, 085021, 2025. DOI [10.1063/5.0285877](https://doi.org/10.1063/5.0285877). See `raw/RL-SecondaryPathID-LiWuBai-AIPAdvances-2025.txt`.

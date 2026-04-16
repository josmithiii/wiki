---
title: Deep Reinforcement Learning for Active Noise Control
created: 2026-04-14
updated: 2026-04-15
type: concept
tags: [anc, feedforward, feedback, array, loudspeaker, stability, comparison]
sources:
  - raw/GFANC-RL-Luo-NeuralNetworks-2024.txt
  - raw/RL-SecondaryPathID-LiWuBai-AIPAdvances-2025.txt
  - raw/GFANC-Luo-2303.05788.txt
  - raw/DRL-Control-Survey-2507.08196.txt
  - raw/ANC-NewCentury-Review-Shi-2306.01425.txt
---

# Deep Reinforcement Learning for ANC

Two primary sources in `raw/` now apply standard deep RL algorithms to
real ANC subproblems: **GFANC-RL** (Luo et al. *Neural Networks* 2024) uses
Soft Actor-Critic to train a CNN policy over a binary sub-filter
selection, and **Li, Wu, Bai** (*AIP Advances* 2025) benchmarks PPO, DDPG,
DQN, and a new GRPO variant on nonlinear secondary-path identification and
plugs the result into a closed-loop RL-FxLMS controller on a real armored
vehicle. Together they cover two of the three roles the taxonomy on
[[ai-anc-overview]] category 5 anticipates: *policy over a filter basis*
and *RL-guided plant identification*. What is **still missing** is a paper
where a DRL agent emits **continuous loudspeaker drive directly** on a
full acoustic plant — the purest "NN replaces the controller" instantiation
is not yet in the wiki.

## Framing

Treat ANC as a sequential control problem. At each step the agent observes
mic signals $\mathbf{o}(n)$ (reference mics, error mics, possibly virtual
sensors from [[pinn-virtual-sensing]]) and emits a speaker-drive vector
$\mathbf{a}(n)$. The reward is a combination of:

- **Negative residual power** at the error mic(s) — the standard ANC goal.
- **Hard constraints** on other sensors (e.g. upward-radiation bound on a
  rooftop array, SPL ceiling inside an enclosure).
- **Actuator penalties** — drive amplitude, slew, thermal loading.
- **Comfort / perceptual weighting** — A-weighting, loudness, annoyance models.

A policy $\pi_\theta(\mathbf{a}\mid\mathbf{o})$ is trained to maximize
expected discounted reward, typically with PPO, SAC, or TD3.

## Why RL rather than FxLMS

- **Hard constraints.** FxLMS minimizes a quadratic error and cannot
  directly enforce inequality constraints (e.g. "don't increase upward SPL").
  A constrained RL formulation (CPO, Lagrangian-PPO) handles this natively.
- **Nonlinear and non-differentiable plants.** Saturating drivers, ported
  enclosures, fan aerodynamic coupling, ground-reflection effects — all
  easy to include in a simulator but hard to put inside an adaptive filter.
- **Non-quadratic objectives.** Perceptual / psychoacoustic reward signals
  (loudness, annoyance) are non-differentiable but fine for RL.
- **Discovery of non-obvious strategies.** A well-tuned simulator and a
  capable policy class can surface control strategies that exploit edge
  diffraction, ground reflection, or transient pre-emphasis that no
  designer would hand-code.

## Why not RL rather than FxLMS

- **Sample efficiency.** FxLMS converges in thousands of samples; RL
  typically needs millions, achievable only in simulation.
- **Sim-to-real gap.** The acoustic simulator is the binding constraint;
  policies overfit to simulator artifacts unless the training is carefully
  randomized.
- **Stability guarantees.** Classical FxLMS has closed-form bounds on
  $\mu$ (see [[fxlms-algorithm]]); learned RL policies have none. Safety
  layers (projection onto a stabilizing set, CBFs) become necessary for
  real deployments.
- **Latency.** Large policy networks are too slow for sample-rate inference
  in active [[headphones]]; DRL-ANC is more plausible for duct / enclosure
  / room-scale problems where block processing at 100–1000 Hz is acceptable.

## Architectures to track

- **Actor-critic with CNN/MHA** over short STFT windows of the error mics.
- **Recurrent policies** for non-stationary noise statistics.
- **Model-based RL** — learn a differentiable plant model from operational
  data, plan with MPC, update policy via imitation or policy gradient.
- **Offline / batch RL** — train entirely from logged mic/driver data from
  a running classical system; avoids simulator-gap issues but requires
  exploration baked into the logged policy.

## Open questions for the research project

- Is there a published head-to-head of DRL-ANC vs FxLMS on a **shared
  benchmark** (geometry + noise distribution + plant)? If not, we should
  make one.
- Can we bootstrap a DRL policy from FxLMS — use FxLMS as a behavior-cloning
  teacher, then fine-tune on the reward that FxLMS cannot express?
- What is the right **safety wrapper** to let a learned policy run on real
  hardware without risking catastrophic drive signals?

## Relation to other AI-ANC approaches

DRL-ANC is the most radical departure from classical adaptive filtering in
[[ai-anc-overview]] — it drops the filter entirely. Compare:

- [[deep-anc-crn]]: end-to-end NN, supervised, no adaptation at runtime.
- [[fxlms-algorithm]] (Latent FxLMS variant): classical loop + NN guidance.
- [[neural-system-identification]]: classical loop + NN parameterization.
- [[meta-learning-anc]]: classical loop + NN update rule.
- **Deep RL (this page):** no classical loop, policy network from scratch.

## Primary sources ingested

### GFANC-RL (Luo, Ma, Shi, Gan — *Neural Networks* 2024)

The first truly-RL paper in the wiki. Luo et al.[^luorl24] reformulate
the supervised GFANC architecture (described below as
[the 2023 precursor](#gfanc-2023--the-supervised-precursor)) as a
Markov decision process and train it with **Soft Actor-Critic**.

**MDP formulation.**

- **State** $s_t = \mathbf{x}_t$: a 1-second noise reference frame.
- **Action** $a_t = \mathbf{g}_t \in \{0,1\}^{M}$ with $M = 15$: a
  binary selection vector over the pre-decomposed sub-filter bank
  (same orthogonal-subband decomposition as supervised GFANC, spanning
  20–7980 Hz).
- **Reward**
$$
r_t = 10\log_{10}\!\frac{\sum_n d_t^2(n)}{\sum_n e_t^2(n)} \quad [\mathrm{dB}]
$$
  — instantaneous noise reduction at the error microphone over the
  1-second frame.
- **Transition** $T(\mathbf{x}_{t+1} \mid \mathbf{x}_t, \mathbf{g}_t) = T(\mathbf{x}_{t+1} \mid \mathbf{x}_t)$: the next observation is independent of the action.
- **Discount** $\gamma = 0$.

The last two facts together mean this is **effectively a contextual
bandit**, not a full sequential-decision problem. There is no
value-function bootstrapping — the SAC algorithm is used for its
entropy-regularized exploration and its discrete-action stochastic
policy, not for temporal credit assignment. This matters: GFANC-RL
proves that RL's *exploration* is useful for ANC labelling, but it does
not yet exercise the *credit-assignment* machinery that would let a
policy learn long-horizon behavior.

**Algorithm.** SAC with dual critics, experience replay, entropy
regularization with automatic temperature tuning, and a stochastic
policy $\pi(\mathbf{g}\mid\mathbf{x})$ over the discrete action space.
No comparison with PPO, DDPG, or TD3 is presented.

**Training.** 80 000 synthetic 1-second noise instances (white noise
passed through random bandpass filters), SNR = 5 dB for robustness.
Offline training. At deployment the control filter
$\mathbf{w}(n) = \sum_m g_m(n)\mathbf{c}_m$ runs at the audio sample rate
while the SAC policy $\pi$ runs at frame rate on a co-processor — this
inherits the latency-friendly architecture of the supervised GFANC.

**Results.** On real recorded traffic, aircraft, and drill noise,
GFANC-RL reaches **14.4 / 13.3 / 9.2 dB NR** versus adaptive FxLMS's
**7.1 / 4.2 / 3.9 dB**. Roughly 7–9 dB over classical adaptive control,
comparable to or slightly better than supervised GFANC, and ~5 dB over
SFANC in the frames where SFANC mispredicts a category.

**Significance.**

- First evidence that RL's unlabelled exploration can substitute for the
  auto-labelling step of supervised GFANC without sacrificing control
  quality.
- Solves the non-differentiability of GFANC's binary weight vector by
  using a stochastic policy rather than a hard classification head.
- Keeps the computationally-attractive "policy on a co-processor, control
  filter on the audio loop" split, which is what makes GFANC-family
  methods viable on real devices.

**What GFANC-RL does *not* prove.**

- It is not evidence that RL helps when the plant is nonlinear or when
  the source statistics are non-stationary on a timescale longer than
  one frame — $\gamma = 0$ precludes any learning beyond single-frame
  classification.
- It does not test whether a continuous-action policy (PPO/SAC over
  speaker drive) would do better than the binary-selection formulation.
- The sub-filter bank is fixed at train time; there is no adaptation of
  the basis itself. Combining this with NNSI-style manifold learning
  ([[neural-system-identification]]) is an obvious next step.

### RL for secondary-path identification (Li, Wu, Bai — *AIP Advances* 2025)

Li, Wu & Bai[^liwubai25] give the first clean
**PPO-vs-DDPG-vs-DQN** comparison on a real ANC task. Their target is
not the controller but the *plant model*: they parameterize the
secondary path $\hat{S}(z)$ as a **3-layer fully-connected nonlinear
neural network** (64 → 64 → 32) and treat its weight fitting as an RL
problem, then run a closed-loop RL-FxLMS control system on a real
ZSL-92 armored vehicle.

**MDP specifics.**

- **State** $s_t = \mathbf{x}(n)$: the noise reference signal.
- **Action** $a_t$: either the discrete Q-network output (DQN) or
  continuous parameter updates (DDPG / PPO / GRPO).
- **Reward** $r_t = -\,|d(n) - \hat{y}(n)|$: negative absolute error
  between the desired output $d$ and the NN's prediction $\hat{y}$.
- Experience replay with random minibatch sampling.
- Sampling rate $F_s = 16$ kHz.

**Algorithms compared (relative modeling error on real vehicle data):**

| Algorithm | RME |
| --- | --- |
| DQN | 89.40% |
| DDPG | 92.04% |
| PPO | 89.36% |
| **GRPO** | **87.02%** |

**PPO is the fastest to converge but has large reward-curve fluctuations**
— empirical confirmation of the "PPO stability in applied control" concern
flagged in the Agyei 2025 DRL-in-control survey (see below). **DDPG is
the worst performer.** **GRPO gives the best speed–stability balance.**

**GRPO — the paper's novel contribution.** Group Relative Policy
Optimization with a periodic-prediction auxiliary module: a second agent
(FFT-based) extracts frequency-regularity features from the reference
noise and feeds them back into the primary actor-critic via a
KL-divergence constraint and a regularized-advantage term. No ablation
isolates the periodic module from the KL constraint, so the contribution
is not fully decomposed.

**Full-loop deployment.** The identified $\hat{S}$ is plugged into a
closed-loop FxLMS variant they call "RL-FxLMS" and tested on real
ZSL-92 cabin noise at idle / 1500 / 2100 / 2700 rpm with front and rear
error mics. Reported max NR: **6.5 dB at idle, 8.8 dB at 2700 rpm**,
MSE reduction 53.1% (0.32 → 0.15), SNR improvement 5.1 dB.

**Where it belongs.** This paper sits on *two* concept pages. Its
**RL-algorithm comparison** belongs here — it's the only PPO/DDPG/DQN
benchmark on an ANC task in the wiki, and the instability result on PPO
is important. Its **nonlinear plant-ID** contribution belongs on
[[neural-secondary-path]], where it fills the "explicit online neural ID"
slot that was explicitly flagged as open in the previous pass.

**What it does *not* prove.** Only one platform, no comparison with
classical nonlinear ID (Volterra, NLMS variants), and no analysis of
real-time feasibility on embedded controllers.

## Adjacent sources already ingested

### GFANC 2023 — the supervised precursor to GFANC-RL

The 2023 supervised version of GFANC[^luo23] is worth contrasting
against the 2024 GFANC-RL version above. The architecture and the
sub-filter decomposition are the same; only the training signal
differs. In the supervised version, label vectors are auto-generated
by running LMS on training segments to convergence and thresholding.
The result is a classifier rather than a policy:

- **Architecture.** A small 1-D CNN (~0.22 M parameters) takes a frame of
  the incoming noise reference and outputs a binary weight vector
  $\mathbf{g}(n) \in \{0,1\}^M$ — one bit per sub-filter in a pre-decomposed
  filter bank.
- **Filter-bank decomposition.** A *single* broadband pre-trained filter $c$
  is transformed via DFT, partitioned into $M$ subbands using conjugate
  symmetry, and converted back to $M$ time-domain FIR sub-filters $c_m$.
  The output is
$$
y(n) = \sum_{m=1}^{M} g_m(n)\,\mathbf{x}^T(n)\,\mathbf{c}_m,
$$
  i.e. a data-driven subset selection over a fixed basis.
- **Training.** Supervised classification. Labels are auto-generated by
  running LMS on training segments to convergence and thresholding the
  resulting coefficients to a $\{0,1\}^M$ target. Binary cross-entropy
  loss, 97.2% test accuracy. **No reward, no environment rollout, no
  policy gradient.**
- **Relation to true DRL.** This is a *classifier over filters* rather
  than a *policy over actions*. The action space has no temporal
  structure that would benefit from value-function bootstrapping, and the
  training signal is dense supervision, not a reward to be maximized.

The 2023 version stayed here in the original "adjacent sources" list
because it was the closest we had to a neural policy over ANC filters.
GFANC-RL (2024) replaced the classifier with a SAC policy and moved into
the "primary sources" section above. For the rooftop-fan research
project, the next natural experiment is to generalize the binary action
space $\{0,1\}^M$ to a **continuous simplex** of sub-filter weights and
train with PPO/SAC/TD3 to get the first DRL-ANC variant with a truly
continuous action space.

### DRL-Control-Survey (Agyei et al. 2025) — background reference only

The Agyei, Sarhadi, Polani survey[^agyei25] benchmarks **DDPG, TD3, PPO,
and TD-MPC2** against LQI on four classical continuous-control problems:
a non-minimum-phase plant, a two-mass spring system, a nonlinear
underwater-vehicle model, and a quadrotor drone. It evaluates under
realistic constraints (time delays, measurement noise, external
disturbances, actuator saturation) — exactly the kinds of non-idealities
that an ANC deployment suffers from.

**The paper contains no ANC or acoustic content.** We keep it in `raw/`
as a pointer to the general DRL-in-control toolchain, the reward-function
normalization trick (negative LQI cost as shared reward across
algorithms), and the observation that TD-MPC2 — the newest of the four —
tends to dominate the baselines on nominal tasks but loses robustness
advantage under delays and disturbances. Treat this as the "which
algorithm should I start with?" reference for a future true DRL-ANC
study, not as evidence about ANC itself.

## Still missing from `raw/`

Even with GFANC-RL and Li/Wu/Bai, the DRL-ANC row of
[[ai-anc-overview]] is incomplete. The gaps:

- A paper where the RL agent's **action space is the continuous
  loudspeaker drive vector**, not a discrete filter selection. This is
  the purest "NN replaces the controller" instantiation and the one
  that would most benefit from sim-to-real randomization, CBF-based
  safety layers, and perceptual rewards.
- **Ryu, Lim, Lee 2024** "Narrowband Active Noise Control with DDPG"
  (International Journal of Automotive Technology, DOI
  10.1007/s12239-024-00102-x) applies DDPG directly to narrowband ANC
  without a secondary-path model. Paywalled at Springer; no arXiv
  preprint surfaced. This would fill part of the gap — narrowband only,
  continuous action space, no path model.
- **Constrained-RL** papers (CPO, Lagrangian-PPO) applied to SPL bounds
  or radiation-shaping constraints — central to the rooftop-fan use
  case, where the objective must include an upward-radiation constraint
  in addition to the community-side reduction goal.
- **Sim-to-real** studies for acoustic RL — randomization protocols,
  gap quantification, deployment reports.
- Post-2022 **survey** explicitly covering DRL for acoustic control.
  The Shi et al. 2023 review[^shi23] covers every other modern ANC
  direction but does not address DRL at all, which is why this page
  has no umbrella citation for its "why RL?" section.

[^luorl24]: Luo, Z., Ma, H., Shi, D., Gan, W. S., "GFANC-RL: Reinforcement Learning-based Generative Fixed-filter Active Noise Control," *Neural Networks*, vol. 178, article 106687, 2024. DOI [10.1016/j.neunet.2024.106687](https://doi.org/10.1016/j.neunet.2024.106687). See `raw/GFANC-RL-Luo-NeuralNetworks-2024.txt`.
[^liwubai25]: Li, W., Wu, C., Bai, F., "Reinforcement learning algorithm for secondary path identification in active noise control systems," *AIP Advances*, vol. 15, no. 8, 085021, 2025. DOI [10.1063/5.0285877](https://doi.org/10.1063/5.0285877). See `raw/RL-SecondaryPathID-LiWuBai-AIPAdvances-2025.txt`.
[^luo23]: Luo, Z., Shi, D., Shen, X., Ji, J., Gan, W. S., "Deep Generative Fixed-filter Active Noise Control," arXiv:2303.05788, 2023. See `raw/GFANC-Luo-2303.05788.txt`.
[^agyei25]: Agyei, A., Sarhadi, P., Polani, D., "Deep Reinforcement Learning in Applied Control: Challenges, Analysis, and Insights," arXiv:2507.08196, 2025. See `raw/DRL-Control-Survey-2507.08196.txt`.
[^shi23]: Shi, D., Lam, B., Gan, W.-S., Cheer, J., Elliott, S. J., "Active Noise Control in The New Century: The Role and Prospect of Signal Processing," *IEEE Signal Processing Magazine*, 2023; arXiv:2306.01425. See `raw/ANC-NewCentury-Review-Shi-2306.01425.txt`.

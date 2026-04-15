---
title: Deep Reinforcement Learning for Active Noise Control
created: 2026-04-14
updated: 2026-04-15
type: concept
tags: [anc, feedforward, feedback, array, loudspeaker, stability, comparison]
sources:
  - raw/GFANC-Luo-2303.05788.txt
  - raw/DRL-Control-Survey-2507.08196.txt
---

# Deep Reinforcement Learning for ANC

**Status: partial stub.** We do not yet have a primary source that applies
*genuine* deep reinforcement learning (PPO, SAC, TD3, TD-MPC2) to an ANC
problem. The two closest papers ingested so far — GFANC (2023) and a
general DRL-in-control survey (2025) — are adjacent but not central, and
are treated below as *contrast* examples that sharpen the definition of
what a true DRL-ANC paper would look like. The positive framing in the
rest of this page is therefore still a design prospectus for the research
project, not a review of established practice.

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

## Adjacent sources already ingested

### GFANC (Luo et al. 2023) — *not* true DRL, a useful contrast

Luo, Shi, Shen, Ji & Gan's "Deep Generative Fixed-filter ANC"[^luo23] is
sometimes framed as a "policy over filters," which invites confusion with
DRL. It is not:

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

GFANC belongs on this page only because it is the closest paper in the
literature to a "neural policy over ANC filters" framing, and the
distinction is worth spelling out precisely. For rooftop-fan ANC, the
same fixed-filter-bank idea could be *generalized* to a real policy that
outputs continuous weights (not just binary) over subfilters and is
trained with PPO/SAC — that would be a natural first DRL-ANC experiment
to run.

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

## Candidate primary sources to ingest (still missing)

Still nothing in `raw/` for:

- Surveys of DRL **specifically for acoustic control** (any post-2022).
- Application papers on duct ANC, open-plan offices, or HVAC systems
  using PPO/SAC/TD3 with real or high-fidelity simulated plants.
- Constrained-RL papers (CPO / Lagrangian methods) applied to SPL bounds
  or radiation-shaping constraints.
- Sim-to-real studies for acoustic RL — randomization protocols, gap
  quantification, deployment reports.

[^luo23]: Luo, Z., Shi, D., Shen, X., Ji, J., Gan, W. S., "Deep Generative Fixed-filter Active Noise Control," arXiv:2303.05788, 2023. See `raw/GFANC-Luo-2303.05788.txt`.
[^agyei25]: Agyei, A., Sarhadi, P., Polani, D., "Deep Reinforcement Learning in Applied Control: Challenges, Analysis, and Insights," arXiv:2507.08196, 2025. See `raw/DRL-Control-Survey-2507.08196.txt`.

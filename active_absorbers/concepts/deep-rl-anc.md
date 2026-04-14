---
title: Deep Reinforcement Learning for Active Noise Control
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, feedforward, feedback, array, loudspeaker, stability, comparison]
sources: []  # primary sources pending ingestion
---

# Deep Reinforcement Learning for ANC

**Status: stub.** We don't yet have primary sources for DRL-ANC in `raw/`;
JOS will add them. This page captures the framing so it can be expanded
in place once papers are ingested.

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

## Candidate primary sources to ingest

Not yet in `raw/`. When available:

- Surveys of DRL for acoustic control (any post-2022 review).
- Application papers on duct ANC, open-plan offices, and HVAC systems
  using PPO/SAC/TD3 with real or high-fidelity simulated plants.
- Constrained-RL papers (CPO / Lagrangian methods) applied to SPL bounds.
- Sim-to-real studies for acoustic RL — randomization protocols, gap
  quantification, deployment reports.

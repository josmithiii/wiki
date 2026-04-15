---
title: Meta-Learning Weight Updates for Adaptive ANC
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, fxlms, lms, comparison, stability]
sources:
  - raw/MetaLearning-DelaylessSubband-2412.19471.txt
  - raw/MetaLearning-SFANC-ResNet-2504.19173.txt
  - raw/MetaLearning-CoInit-2601.13849.txt
  - raw/LatentFxLMS-2507.03854v1.txt
---

# Meta-Learning Weight Updates

A complementary line to [[neural-system-identification]]: instead of
constraining the filter to a manifold, **learn the *update rule* itself** with
a neural network. The classical gradient step
$\mathbf{w}(n+1) = \mathbf{w}(n) + 2\mu\,e(n)\mathbf{x}'(n)$ (see
[[fxlms-algorithm]]) is replaced by
$$
\mathbf{w}(n+1) = \mathbf{w}(n) + f_\theta\!\big(\mathbf{w}(n),\,\mathbf{x}(n),\,e(n),\,\text{state}\big),
$$
where $f_\theta$ is a small neural network trained offline across many
instances of the adaptation problem. The network is a **learned optimizer**
for FxLMS, in the meta-learning sense of Andrychowicz et al. 2016 and
"learning to learn by gradient descent by gradient descent."

Sarkar et al. 2025[^sarkar25] explicitly contrast meta-learning with NNSI:
meta-learning outputs **weight-space updates**, while NNSI outputs
**latent-space updates** that are then decoded. Both try to beat vanilla
FxLMS convergence, but through different parameterizations.

Three meta-learning-for-ANC papers are ingested into the wiki, each
attacking a different part of the FxLMS machinery:

| Paper | What gets meta-learned | Classical analogue |
| --- | --- | --- |
| Feng & So 2024[^feng24] (delayless subband) | The **weight-update rule** itself (gradient predictor) | The $-e(n)\mathbf{x}'(n)$ step direction |
| Xiao et al. 2025[^xiao25] (MAML-SFANC) | A **filter-bank initialization** across noise categories | Selective-fixed-filter + online fine-tune |
| Yang et al. 2026[^yang26] (co-init) | Joint **starting coefficients** for the control filter *and* the secondary-path FIR | Offline secondary-path ID + online FxLMS |

See [[neural-secondary-path]] for the Yang paper's role on that page —
its secondary-path meta-initialization is cross-listed because it contributes
to both concepts.

## Training protocol (typical)

1. Collect a distribution over ANC scenarios — different reference
   statistics, different primary and secondary paths, different SNRs.
2. For each scenario, simulate a short adaptation trajectory of length $T$
   starting from $\mathbf{w}(0)$.
3. Differentiate through the whole trajectory with the network $f_\theta$
   *in* the update rule, and minimize a meta-loss such as the mean residual
   power over $T$ or the time to reach a threshold MSE.
4. Typical parameterizations of $f_\theta$: small LSTM over per-tap state
   (à la L2L), 1-D convolution across the filter, coordinate-wise MLP, or —
   in Feng & So 2024 — a **single-headed attention RNN** over a subband
   filtered-reference / error feature pair.

## Feng & So 2024 — learned gradient for delayless subband FxLMS

Feng & So[^feng24] is the strongest concrete match to Sarkar et al.'s
reference [5]. Their setup:

- **Meta-learner architecture:** a single-headed attention recurrent
  network over a learnable feature embedding of the filtered-reference and
  error signals. The RNN's output is the **predicted gradient**
  $\tilde{g}(n)$ that replaces the classical $-e(n)\mathbf{x}'(n)$
  direction, so the adaptive filter update becomes
$$
\mathbf{w}(n+1) = \mathbf{w}(n) - \mu\,\tilde{g}(n).
$$
- **Delayless subband front end:** a polyphase analysis filter bank
  downsamples the signals by a factor $D$, so the update rate drops from
  the sample rate (e.g. 16 kHz) to 16 kHz / $D$ (typically 1 kHz at
  $D = 16$). Crucially, because the architecture is *delayless*, no
  subband-delay artifacts are introduced into the cancellation path —
  this is the main engineering contribution over prior subband meta-learners.
- **Per-subband input features:** after the filter bank, an FFT produces
  stable spectral features fed to the attention RNN.
- **Skip-updating:** for resource-constrained devices, the update is
  skipped for additional frames, trading convergence speed for compute.
- **Multi-condition training:** the training distribution explicitly
  includes a **loudspeaker saturation nonlinearity**, so the learned
  update rule is implicitly robust to mild actuator clipping. This is the
  right answer to the "classical FxLMS assumes linear plant" gap
  highlighted on [[fxlms-algorithm]].
- **Partial secondary-path knowledge:** only the main delay of
  $\hat{S}(z)$ is required, not the full impulse response. This is a
  significant practical simplification.

The paper reports convergence faster than standard FxLMS and superior
steady-state error under nonlinearity. Compute: one attention-RNN forward
pass per subband update (every $D$ samples), which is cheap enough for
real-time.

## Xiao et al. 2025 — meta-learning over a filter bank (MAML-SFANC)

A complementary attack on the same problem:

**Selective Fixed-Filter ANC (SFANC)** keeps a *bank* of pre-trained FIR
filters, one per noise category, plus a classifier that picks the
best-matching filter at runtime. The filter is fixed per frame — no online
LMS — which eliminates adaptation lag and divergence risk but depends on
the bank and the classifier being accurate.

**Xiao et al.**[^xiao25] add two meta-learning ingredients:

1. **MAML-FxLMS pre-training.** Each filter in the bank is pre-trained so
   that *a few gradient steps* of online fine-tuning suffice to adapt it
   to a previously unseen noise of the same category. This is the
   standard MAML formulation applied to the filter bank's initialization.
2. **ResNet noise classifier.** Input: mel-spectrogram of the incoming
   noise frame. Output: one of $N$ categories (trained on ESC-50).
   Replaces prior SFANC classifiers that used frequency-band heuristics,
   which failed on real-world broadband noise.

The result is a hybrid that's closer in spirit to traditional SFANC but
with meta-learned initializations. Note what's *not* learned: the
weight-update rule itself stays as vanilla FxLMS — only the starting
coefficients are adapted. This makes it orthogonal to Feng & So 2024 and,
in principle, combinable with it.

## Yang et al. 2026 — joint co-initialization of filter and secondary path

Yang et al.[^yang26] extend the MAML framing further by meta-learning
**two** things at once: the control-filter initialization $\Phi$ and the
secondary-path FIR model initialization $\Psi$. At deployment, the runtime
algorithm is unchanged — standard OSPM (online secondary-path modeling) and
standard FxLMS both proceed from the meta-learned warm start. This is the
cleanest example of "meta-learning as initialization only": no neural
substitution of the plant model, no learned update rule. Full treatment is
on [[neural-secondary-path]], since the secondary-path half of the contribution
belongs there. The meta-learning half — the inner-loop structure with
phases A (auxiliary-noise plant ID) and B (FxLMS control update), the
forgetting factors $\lambda_w, \lambda_s$ in the meta-gradient update, the
RWTH Aachen IKS PANDAR in-ear headphone dataset — is the minimal-intrusion
baseline to beat.

## What the network sees

The input state passed to $f_\theta$ varies across the literature:

- **Current filter weights** $\mathbf{w}(n)$
- **Filtered reference** $\mathbf{x}'(n)$
- **Error** $e(n)$ and a short window of past errors
- **Running second-moment statistics** (for NLMS-style normalization)
- Sometimes the **reference signal spectrum** for narrowband vs broadband
  discrimination

## Strengths

- Can outperform FxLMS on the training distribution: faster convergence,
  lower steady-state error, implicit step-size tuning.
- Amortizes hyperparameter selection — the network learns effective $\mu$,
  leak factor, and regularization across scenarios.
- Can produce **stable** updates in regimes where classical FxLMS diverges,
  by learning to shrink the update near instability.

## Weaknesses

- **Distribution shift.** A meta-learner overfits its training distribution;
  deployment on a different plant or noise statistics degrades.
- **No stability guarantees.** Classical FxLMS has closed-form sufficient
  conditions on $\mu$ (see [[fxlms-algorithm]] stability section); a learned
  optimizer does not.
- **Training cost.** Differentiating through long trajectories is expensive
  and numerically delicate (exploding/vanishing meta-gradients).

## Relation to the research project

Meta-learning and NNSI target the same pain point — slow FxLMS convergence —
but from opposite directions. Two compelling experiments for our setting:

1. Train a Feng-&-So-style learned gradient predictor across a
   distribution of primary-source positions on the rooftop geometry, and
   compare against Latent FxLMS on the same distribution. If Latent FxLMS
   wins, the manifold structure is the dominant effect; if the
   meta-learner wins, the update-rule freedom matters more; if they tie,
   a hybrid ("learned update on a learned manifold") is worth trying.
2. Start from Yang-style co-init to warm the classical FxLMS pipeline,
   then enable Feng-&-So's learned gradient during steady-state tracking.
   This stacks initialization and update-rule meta-learning, which are
   disjoint contributions.

The no-free-lunch caveat: all three meta-learning variants assume access
to a training distribution that **covers** deployment. For the rooftop
geometry, sampling source positions on a spatial grid under several
representative weather conditions is realistic; for open-world headphone
use, it's much harder.

[^sarkar25]: Sarkar, K. et al., "Latent FxLMS: Accelerating Active Noise Control with Neural Adaptive Filters," arXiv:2507.03854, 2025. See `raw/LatentFxLMS-2507.03854v1.txt`.
[^feng24]: Feng, D., So, H. K. H. (attribution tentative), "Meta-Learning-Based Delayless Subband Adaptive Filter using Complex Self-Attention for Active Noise Control," arXiv:2412.19471, 2024. See `raw/MetaLearning-DelaylessSubband-2412.19471.txt`.
[^xiao25]: Xiao, Z., Liu, Y., Dai, S., Lan, Q. (attribution tentative), "Meta-learning based Selective Fixed-filter Active Noise Control System with ResNet Classifier," arXiv:2504.19173, 2025. See `raw/MetaLearning-SFANC-ResNet-2504.19173.txt`.
[^yang26]: Yang et al., "Co-Initialization of Control Filter and Secondary Path via Meta-Learning for Active Noise Control," arXiv:2601.13849, 2026. See `raw/MetaLearning-CoInit-2601.13849.txt`.

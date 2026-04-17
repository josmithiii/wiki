---
title: Classical ANC Methods (Overview)
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anc, fxlms, lms, secondary-path, feedback, feedforward, hybrid-control, stability, reference, tutorial]
sources:
  - raw/ANC-Tutorial-Review-1999-2010913102917710.txt
  - raw/ANC-Survey-Part1-1-s2.0-S0165168421000785-main.txt
  - raw/ANC-Survey-Part2-NonlinearSystems-2110.09672v2.txt
  - raw/ANC-NewCentury-Review-Shi-2306.01425.txt
---

# Classical ANC Methods (Overview)

Companion to [[ai-anc-overview]]. This page maps the **non-AI** ANC
landscape — every major algorithm family, control topology, and
application area documented in the four ingested survey papers.[^kuo99]
[^lu21a] [^lu21b] [^shi23]  Individual pages exist for [[lms-algorithm]]
and [[fxlms-algorithm]]; everything else is cataloged here.

The organizing axis is **what type of model sits in the control
path**: linear FIR/IIR, nonlinear polynomial expansion, or
heuristic/evolutionary optimizer.

---

## 1. Control topologies

| Topology | Reference mic? | Key trait | Typical use |
|---|---|---|---|
| **Feedforward** | yes | ref mic → $\hat{S}(z)$-filtered LMS → speaker | broadband duct, machinery |
| **Feedback** | no | error mic only; internal-model structure | headphones, narrowband |
| **Hybrid** | yes | sum of feedforward + feedback outputs | flexible; automotive, fMRI |

- **Feedforward** requires causal delay: electrical delay $\le$ acoustic delay from ref mic to speaker.[^kuo99]
- **Feedback** suffers the waterbed effect: suppression at some $f$ ⇒ boost at others.[^lu21a]
- **Hybrid** adds design flexibility but doubles filter count.

## 2. Linear adaptive algorithms

### 2.1 Filtered-x (FxLMS) family

The dominant family. See [[fxlms-algorithm]] for the core update rule.

| Variant | Key idea |
|---|---|
| FxNLMS | Normalized step $\mu/\|\hat{\mathbf{x}}\|^2$ |
| Leaky FxLMS | Weight-decay term for stability |
| Modified FxLMS | Bjarnason (1993): pre-filters reference through $\hat{S}^{-1}(z)$ |
| VSS-FxLMS | Variable step size — fast convergence + low residual |
| Frequency-domain FxLMS | Block FFT for long filters; $O(N\log N)$ per block |
| Subband FxLMS | Delayless or weight-transfer subband decomposition |
| Multichannel FxLMS | $J$ refs × $K$ speakers × $M$ error mics; $J{\cdot}K{\cdot}M$ filters |
| FxAP | Affine projection — decorrelates correlated inputs |
| FxRLS | Recursive least squares — fast convergence, $O(N^2)$ cost |

### 2.2 Filtered-e (FeLMS) family

Filters the *error* through $\hat{S}(z)$ instead of the reference.
Equivalent steady-state to FxLMS but different transient behavior;
sometimes preferred for narrowband or IIR controllers.[^lu21a]

### 2.3 Filtered-u (FuLMS) family

Updates both numerator and denominator of an **IIR** adaptive
controller. More compact than FIR for long acoustic paths but
stability must be enforced (leaky, SPR, BIBO constraints).[^lu21a]

### 2.4 Other linear structures

- **Lattice ANC** — decorrelates input; fast convergence on colored noise.
- **Convex combination** — runs a fast filter and a slow filter in
  parallel; output is $\lambda(n)$-weighted mix. Avoids the
  fast-convergence vs. low-residual trade-off.[^lu21a]
- **Sparse ANC** — zero-attracting / proportionate NLMS; exploits
  sparsity in long acoustic impulse responses.[^lu21a]
- **Fractional-order ANC** — Grünwald–Letnikov or Riemann–Liouville
  fractional derivatives in the LMS update; claimed faster convergence
  on certain noise classes.[^lu21a]

## 3. Secondary-path modeling

$\hat{S}(z)$ accuracy is critical — phase error > 90° destabilizes
FxLMS.[^kuo99]  Lu et al. Part I catalogs **21 online estimation
methods**.[^lu21a]

| Family | Example methods |
|---|---|
| Additive auxiliary noise | Eriksson (1991): inject white noise, adapt $\hat{S}$ with NLMS |
| Delay-compensated LMS | compensate plant delay in $\hat{S}$ update path |
| Variable-step-size | VSS schemes that track $S(z)$ drift |
| Simultaneous estimation | joint control-filter + $\hat{S}$ update (cross-coupling risk) |

- **Offline** is simplest (white noise excitation, system off).
- **Online** needed when $S(z)$ drifts (temperature, humidity, head
  movement). Auxiliary-noise power must be low enough not to be
  audible.
- For neural approaches to secondary-path modeling, see
  [[neural-secondary-path]].

## 4. Nonlinear ANC (NLANC) algorithms

When $P(z)$, $S(z)$, or actuator response is nonlinear, linear FxLMS
is suboptimal. Three sources of nonlinearity:[^lu21b]

1. **Primary path** — high SPL in ducts causes nonlinear propagation.
2. **Secondary path** — amplifier saturation, speaker overdriving.
3. **Components** — actuator harmonics, chaotic noise (blowers, fans).

### 4.1 Volterra series

Truncated Volterra expansion of the reference input. Universal
approximator (Stone-Weierstrass), but coefficient count
$N_c = (M{+}Q)!/(M!\,Q!) - 1$ grows exponentially in memory $M$ and
order $Q$. Practical use limited to SOV ($Q{=}2$) or TOV ($Q{=}3$).

- **VFxLMS** — baseline Volterra FxLMS (Tan & Jiang 1997/2001).
- **VFxlogLMP / VFxlogCLMP** — $\ell_p$-norm log cost; robust to
  impulsive noise ($\alpha$-stable, $\alpha \approx 1.1$–$1.2$).
- **VFxRMC** — maximum correntropy criterion with adaptive kernel size.

### 4.2 FLANN (Functional Link ANN)

**Most popular NLANC controller.** Single-layer trigonometric expansion:
$N_c = M(2b{+}1)$ — far fewer coefficients than Volterra at the same
memory and order.

| Variant | Key idea |
|---|---|
| FsLMS | baseline filtered-s LMS with trig expansion (Das & Panda 2004) |
| RFsLMS | logarithmic cost for Gaussian + impulsive robustness |
| GFLANN | adds cross-terms $x(n)\sin(b\pi x(n{-}k))$ |
| EFLANN | exponential factor in trig expansion — faster convergence |
| RFLANN | recursive (IIR) FLANN using past outputs as inputs |
| Block FsLMS | FFT-based block processing for throughput |

### 4.3 Hammerstein / Wiener block models

Cascaded memoryless-nonlinearity + linear-system blocks:

- **Hammerstein (N-L):** polynomial $g(n) = \sum p_j x^j(n)$ → linear FIR.
- **Wiener (L-N):** linear FIR → polynomial.
- **Hammerstein-Wiener (N-L-N):** both primary and secondary paths
  nonlinear.
- **Wiener-Hammerstein (L-N-L):** reversed cascade.

Few papers focus on these for ANC; mainly used when the nonlinearity
structure is known a priori.[^lu21b]

### 4.4 Orthogonal polynomial filters

Orthogonal basis ⇒ faster convergence than Volterra/FLANN:

- **Chebyshev (CN):** $T_{q+1}(x) = 2xT_q(x) - T_{q-1}(x)$;
  $N_c = 1 + Q(M{+}1) + M$. Outperforms FsLMS and VFxLMS on
  convergence rate.[^lu21b]
- **Legendre (LN):** $L_{q+1}(x) = [(2q{+}1)xL_q - qL_{q-1}]/(q{+}1)$;
  requires $x \in [-1,1]$ (tanh link). $N_c = QM + 1$.
- **Fourier (FN):** trig basis designed to avoid repetition/cancellation;
  universal approximator but border discontinuities cause oscillations.
- **EMFN:** even-mirror Fourier nonlinear; even-symmetric generalized
  Fourier series. Good for strong nonlinearities with saturated signals;
  second-order EMFN has same $N_c$ as SOV.[^lu21b]

### 4.5 Bilinear filters

Combines linear terms $x(n{-}i)$, feedback $y(n{-}t)$, and cross-products
$x(n{-}i)y(n{-}t)$. Handles strong nonlinear distortions with shorter
filter length than SOV. **Diagonal-channel structure** updates each term
group independently, reducing cost.[^lu21b]

FLANN-inspired bilinear extensions (3-D diagonal-channel, reweighted
bilinear) further improve modeling of nonlinear secondary paths.

### 4.6 Spline adaptive filters

Adaptive look-up table (LUT) with local polynomial spline interpolation.
Proposed 2013 for system ID, extended to ANC 2016.[^lu21b]

- **Advantages:** low computational cost vs VFxLMS/FsLMS; comparable
  or better MSE.
- **Variants:** FIR (2013), multichannel FIR (2015), IIR with feedback
  and FuLMS (2016).
- Parameters: span index $\varepsilon$, local parameter $u(n)$,
  spline basis matrix $\mathbf{\Omega}$, control point vector $\mathbf{q}$.

### 4.7 Kernel adaptive filters (KAF)

Maps input from space $\mathcal{U}$ to high-dimensional feature space
$\mathcal{F}$ via RKHS; kernel trick avoids explicit nonlinear mapping.
Output: $y(n) = \sum_j a_j \kappa(\mathbf{X}, \mathbf{X}_j)$.

- Standard kernel: Gaussian $\kappa(\mathbf{X},\mathbf{X}') = \exp(-\varsigma\|\mathbf{X}-\mathbf{X}'\|^2)$.
- Novel kernels: logistic, tan-sigmoid, inverse-tan.[^lu21b]
- **Limitation:** network size grows linearly with training data.
  Sparsification via quantization or set-membership schemes needed.
- First applied to NLANC in 2009; extended to nonlinear secondary
  path with multi-tonal sources in 2010+.

## 5. Heuristic / evolutionary optimization

Cast NLANC as a global optimization problem — avoids local minima
caused by nonlinear $S(z)$. **Key advantage: many work without
estimating the secondary path.**[^lu21b]

| Method | Year (ANC) | Key property |
|---|---|---|
| **GA** (Genetic Algorithm) | 1994 | selection/crossover/mutation; AGA + IPM variant |
| **PSO** (Particle Swarm) | 2006 | competition/cooperation; tanh saturation model; Wilcoxon norm ~5 dB over MSE |
| **BSA** (Backtracking Search) | 2010s | population-based EA + SQP; avoids local optima |
| **BFO** (Bacterial Foraging) | 2010s | chemotaxis-inspired; ~5 dB over GA in steady state |
| **FF** (Firefly) | 2010s | cascaded FLANN + FIR |
| **FWA** (Fireworks) | 2010s | three variants; strong global optimization |

## 6. Distributed ANC

Wireless acoustic sensor networks (WASNs): incremental or diffusion
strategies distribute the FxLMS/FxNLMS update across sensor nodes.
Lower cost than centralized multichannel.[^lu21a]

- **Linear:** IFxLMS (incremental), DFxNLMS (diffusion).
- **Nonlinear:** FLANN/LN + diffusion strategy for nonlinear
  distributed ANC.[^lu21b]

## 7. Novel linear methods (2010s)

| Method | Idea |
|---|---|
| **Selective ANC** | pre-tuned filter bank; noise classifier selects best filter at runtime — direct precursor to SFANC/GFANC ([[deep-rl-anc]]) |
| **Psychoacoustic ANC** | perceptual loudness weighting in cost function |
| **3-D zone-of-quiet** | spherical-harmonic decomposition for volumetric quiet zones |
| **IoT-ANC** | wireless ethernet replaces analog cables; proof-of-concept demonstrated |

## 8. Applications

| Domain | Key results | Refs |
|---|---|---|
| **Duct** | 20 dB broadband attenuation | [^kuo99] |
| **fMRI** | >40 dB via parallel feedback FNLMS; head-mounted piezo speakers | [^lu21b] |
| **Open window** | 16-channel, 5 dB below 2 kHz; natural ventilation preserved | [^lu21b] |
| **Headphones** | feedback FxLMS standard; virtual sensing, hybrid, CBBANC | [^lu21b] |
| **Zone-of-quiet** | spherical speaker arrays; RMT-based; memetic algorithm | [^lu21b] |
| **Spatial ANC** | mode-domain methods reduce cross-correlations; HOS scheme | [^lu21b] |
| **Periodic noise** | ILC + RC for repetitive exhaust (120 dB); 4 dB with freq-domain ILC | [^lu21b] |
| **Transformer** | 15 dB max; 84–97% sound energy density reduction | [^lu21b] |
| **Vehicle** | road noise: 4 dB broadband up to 1 kHz (8-ref multichannel) | [^lu21b] |
| **Other** | mobile phones, earmuffs, elevators, mufflers, washing machines, EEG | [^lu21b] |

## 9. Hardware implementations

| Platform | Trait | ANC use |
|---|---|---|
| **DSP** | fixed-point; ~2 dB degradation vs floating | FxLMS, FxNLMS, subband |
| **FPGA** | high throughput; parallel/folded architectures | FwFxLMS (larger step size), multichannel |
| **VLSI** | compact area; lowest resource | folded FsLMS (58% less area-delay vs FxLMS) |

## 10. Open challenges (as of 2021)

1. **Impulsive-noise theory** — convergence analysis for $\alpha$-stable
   noise and FLOM-based algorithms still missing.
2. **KAF sparsification** — network size curbs essential for real-time.
3. **Lab-to-practice gap** — most NLANC algorithms remain laboratory-stage;
   low-complexity NLANC is the critical need.
4. **Optimal parameter selection** — memory length, population size for
   heuristics, kernel bandwidth.
5. **IoT integration** — IoV, impulsive/nonlinear effects on wireless ANC.

For post-2021 challenges and AI-based approaches, see [[ai-anc-overview]].

## Reading map

- For **LMS foundations**, start at [[lms-algorithm]].
- For **FxLMS core update and variants**, see [[fxlms-algorithm]].
- For **neural / AI extensions** of any method above, see
  [[ai-anc-overview]] and its linked concept pages.
- For **selective ANC → SFANC → GFANC → GFANC-RL** evolution, trace
  from §7 above through [[deep-rl-anc]].

[^kuo99]: Kuo & Morgan, "Active Noise Control: A Tutorial Review," *Proc. IEEE* 87(6), 1999. See `raw/ANC-Tutorial-Review-1999-2010913102917710.txt`.
[^lu21a]: Lu et al., "A survey on active noise control — Part I: Linear systems," *Signal Processing* 183, 2021. See `raw/ANC-Survey-Part1-1-s2.0-S0165168421000785-main.txt`.
[^lu21b]: Lu et al., "Active noise control techniques for nonlinear systems," arXiv 2110.09672v2, 2022 / *Signal Processing* 181, 2021. See `raw/ANC-Survey-Part2-NonlinearSystems-2110.09672v2.txt`.
[^shi23]: Shi et al., "Active Noise Control in The New Century," *IEEE SPM*, 2023. See `raw/ANC-NewCentury-Review-Shi-2306.01425.txt`.

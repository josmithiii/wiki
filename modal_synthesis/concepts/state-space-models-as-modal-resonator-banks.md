---
title: State Space Models as Modal Resonator Banks
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, eigenmode, resonator, room, ml, neural, differentiable, inference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_03.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_86.pdf
  - /l/dttd/DAFx26/txt/DAFx26_paper_03.txt
  - /l/dttd/DAFx26/txt/DAFx26_challenge_86.txt
---

# State Space Models as Modal Resonator Banks

Deep **state space models** (S4/S5/LRU lineage) and modal synthesis are the same
object: Bittner et al. show a *restricted diagonal complex-valued* SSM is exactly a
bank of parallel second-order all-pole filters, then train it on plate-reverb IRs
with classical pole estimation as the initialiser[^1][^2]. See
[[resonator-bank-implementation]] and [[ml-modal-parameter-estimation]].

## The plate side
Each mode is an exact discrete-time all-pole biquad, $r_m = e^{-\sigma_m T_s}$:
$$q_{m,k+1}=2r_m\cos(\Omega_m T_s)q_{m,k}-r_m^2 q_{m,k-1}+w_m f_k,\qquad
G(z)=\sum_{m=1}^{M}\frac{w_m z}{z^2-2zr_m\cos(\Omega_m T_s)+r_m^2}.$$

## The SSM side, and the equivalence
Take a SISO diagonal SSM with **real** input and output weights and take the
*imaginary* part of the output (deep SSMs normally take the real part):
$$\tilde x_k = e^{\tilde\lambda T_s}\circ\tilde x_{k-1}+b\,u_k,\qquad
y_k=\Im\!\left(c^{\!\top}\tilde x_k\right),\qquad \tilde\lambda=\alpha+j\beta\in\mathbb{C}^H .$$
$z$-transforming gives a sum of first-order complex resonators,
$\tilde G(z)=\sum_i c_ib_i z/(z-e^{\tilde\lambda_i T_s})$; inverting and taking the imaginary
part gives a real IR that is a weighted sum of decaying sinusoids,
$$g_k=\sum_{i=1}^{H} c_i b_i\,e^{\alpha_i k T_s}\sin(\beta_i k T_s)
\;\Longrightarrow\;
G(z)=\sum_{i=1}^{H} c_i b_i\frac{z e^{\alpha_i T_s}\sin(\beta_i T_s)}{z^2-2ze^{\alpha_i T_s}\cos(\beta_i T_s)+e^{2\alpha_i T_s}} .$$
Coefficient comparison with the plate transfer function gives the dictionary
$$\Omega_m=\beta_i,\qquad \sigma_m=-\alpha_i,\qquad w_m=c_ib_i e^{\alpha_i T_s}\sin(\beta_i T_s).$$
So the learned SSM parameters **are** modal parameters, and vice versa - which is
what makes the model interpretable where a CNN/TCN/LSTM emulator is not. Stability
is imposed during training by $\alpha \leftarrow -|\alpha|$ and one-sided poles by
$\beta\leftarrow|\beta|$. Cost per step is $3H$ parameters and $5H$ MACs once $b$ and
$c$ are fused (only the state update is complex).

## Training
Per-IR overfitting, not generalisation: one SSM layer per target IR, 5000 steps of
L2 loss, AdamW with cosine annealing from $10^{-3}$, aggressive weight decay on $b$
only to keep gains small, $c$ fixed at one and untrained, and the usual SSM
step-scale factorisation $\lambda=\lambda'\circ\Delta$ with $\Delta$ learned in the log
domain. Long-memory modal behaviour is learnable without sequential recurrence
because the state is computed by the **parallel scan** (associative scan) algorithm.

## Matrix Pencil guided eigenvalue initialisation
Deep SSMs are sensitive to state-matrix initialisation (HiPPO for S4, its
diagonalisation for DSS/S4D/S5). Here the initialiser is classical pole estimation:
1. estimate $H_{\rm est}=128$ poles from the target IR with the **Matrix Pencil** method (a generalised eigenvalue problem on Hankel data, more noise-robust than Prony);
2. fit a second-order polynomial to the estimated decay-rate versus frequency relation;
3. draw the remaining $H-H_{\rm est}$ eigenvalues by log-uniform sampling of frequency over 20 Hz-10 kHz and evaluating the fitted decay law. Matrix Pencil only resolves modes well separated from noise, hence $H_{\rm est}\ll H$; the extrapolation supplies the dense high-frequency region.

## Results on the DAFx plate benchmark
50 synthetic IRs (1 s, 44.1 kHz) from the challenge repository,
$H\in\{128,256,512,1024,2048\}$, two initialisations, 500 trained models. Synthesis
quality, mean over the 50 IRs:

| $H$ | Norm. $L_2$ error MP / S5 | Norm. spectral mag. error MP / S5 |
|---|---|---|
| 128 | 0.155 / 0.259 | 0.624 / 0.635 |
| 512 | 0.039 / 0.105 | 0.218 / 0.513 |
| 2048 | **0.004** / 0.034 | **0.103** / 0.449 |
| challenge baseline | 0.281 | 0.830 |

Error falls with fewer "missing modes" (ground-truth count minus $H$), MP beats S5 at
every size, and even $H=128$ beats the challenge peak-picking baseline, which finds
only about 139 modes on average. System identification (relative errors $R_\Omega$,
$R_\sigma$, $R_w$, matched by nearest frequency) improves with $H$ for frequency
($0.957\to0.740$, MP) and decay ($0.970\to0.829$), but **gains get worse** (1.124 at
$H=128$ rising to 14.1 at $H=2048$): redundant states acquire outlier gains that
weight decay does not control. S5 init is worse on frequency, much worse on decay.

## Non-iterative variant (challenge Task B entry)
The same group's challenge submission removes gradient descent entirely[^2]:
- **Mode-count estimator.** Log-compress the magnitude response, cut it into overlapping local patches, mean-centre each, SVD the patch matrix, and exponentiate the entropy of the normalised singular values: a scalar "spectral richness" measure. Few modes means similar patches and few dominant singular vectors. An isotonic regression from that scalar to $M_{\rm total}$, fitted on 128 IRs, sets the model order.
- **Poles.** Matrix Pencil on the first second of the IR, subsampled by 4 (SVD cost is cubic); order $M_{\rm est}$ chosen as the fewest singular values explaining 99.999% of singular-value energy; then the same polynomial fit and extrapolation to $\Omega_{\max}=10$ kHz.
- **Gains in closed form.** Because the system is linear, run the initialised SSM once with a unit impulse, collect the state responses $X$, and solve $c = YX^{\!\top}(XX^{\!\top})^{-1}$; convert with $b_m=c_m e^{\alpha_m T_s}\sin(\beta_m T_s)$.

On 17 self-generated IRs this scores RE 0.78 versus 1.96 for the baseline, with
$\mathrm{RE}_\Omega=0.27$, $\mathrm{RE}_\sigma=0.77$, $\mathrm{RE}_b=0.97$ and
$\Delta M=335$ (baseline 3239); it ranked 5th of 10 in the official Task B evaluation
(see [[plate-reverb-parameter-estimation-challenge]]). Cost: about 30 s per IR for
the Matrix Pencil stage, roughly 42 minutes for the 16-file test set.

## Limits
Linear and time-invariant only (nonlinear plate behaviour is out of scope); modal gains are the weak point in both variants; state sizes above about 2k exceeded GPU memory for the parallel scan, so the least-squares stage ran on CPU; and Matrix Pencil conditioning degrades in dense high-frequency regions.

[^1]: [[entities/source-papers#paper-bittner-diagonal-ssm-plate-reverb-2026]] - Bittner, Wess, Dallinger, Schnoll & Jantsch, "Diagonal Complex-Valued State Space Models ... Metal Plate Reverbs," DAFx26.
[^2]: [[entities/source-papers#paper-bittner-matrix-pencil-ssm-taskb-2026]] - Bittner & Jantsch, "Non-Iterative Modal Parameter Estimation for Plate Reverbs via Matrix-Pencil-Guided State Space Model Initialization," DAFx26 challenge report.

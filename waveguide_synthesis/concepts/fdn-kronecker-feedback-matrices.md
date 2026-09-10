---
title: Kronecker FDN Feedback Matrices
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [fdn, reverb, dsp, realtime, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_04.pdf
  - raw/DAFx26_paper_04.txt
---

# Kronecker FDN Feedback Matrices

A parametric family of lossless FDN feedback matrices built by recursive
Kronecker products of $2 \times 2$ kernels, giving Hadamard-class speed plus
continuous, audio-rate control over network topology.[^coppola]

## Construction

Each kernel $K_i \in \mathbb{R}^{2\times2}$ is a rotation or a reflection with one angle:
$$\mathrm{Rot}(\theta) = \begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix},
\qquad
\widehat{\mathrm{Ref}}(\theta) = \begin{bmatrix}\cos\theta & \sin\theta\\ \sin\theta & -\cos\theta\end{bmatrix}$$
(the reflection uses a half angle so both kernels share one parameterisation).
The feedback matrix of size $N = 2^M$ is
$$\Psi_M = K_M \otimes K_{M-1} \otimes \cdots \otimes K_1,
\qquad \Psi_0 = I_1,\; \Psi_M = K_M \otimes \Psi_{M-1}.$$

- Orthogonality is **structural**: a Kronecker product of orthogonal matrices is
  orthogonal, so $\Psi_M$ is orthogonal at every value of every $\theta_i$ - no
  re-orthogonalisation step is ever needed, even under modulation.
- Orthogonal $\Rightarrow$ unilossless (satisfies $A E A^H = E$ with $E = I_N$), so the
  poles of $p_{A,\mathbf{m}}(z)$ stay unimodular for **any** delay vector. Decay is then
  imposed separately as $A = U\Gamma$ with $\gamma_i = 10^{-3 m_i/(T_{60} f_s)}$.
- $\theta_i = \pi/4$ for all kernels recovers the Hadamard matrix $H_{2^M}$ exactly:
  $\widehat{\mathrm{Ref}}(\pi/4) = H_2$. So Hadamard is one point in a continuum.

## Fast feedback multiply

The recursion gives a divide-and-conquer product in $O(N \log_2 N)$, matching the
fast Walsh-Hadamard transform. The in-place iterative form loops over
$c = 1..M$ levels, $h = 2^{c-1}$, applying kernel $K_c$ to element pairs
$(x_{b+j},\, x_{b+j+h})$. The matrix is never materialised: memory is $O(N)$ for
the state plus $O(\log_2 N)$ for the kernels, versus $O(N^2)$ for a dense matrix.

Benchmarks (C++17, MSVC, Intel Core Ultra 9 185H, ns per feedback operation):

| $N$ | naive | Eigen | proposed | proposed, one angle updated per sample |
|---|---|---|---|---|
| 16 | 54.9 | 27.1 | 26.9 | 33.2 |
| 32 | 233.2 | 48.5 | 31.0 | 37.8 |
| 64 | 1662.5 | 151.2 | 58.4 | 69.5 |

The gap widens under modulation (63.6x over naive at $N=64$) because the dense
baselines must rebuild the whole matrix when any $\theta_i$ changes, while this
algorithm refreshes only the affected $2 \times 2$ kernel.

## What the angles buy

- **Stereo cross-coupling.** Setting the outermost angle $\theta_M = 0$ makes
  $\Psi_M$ block-diagonal: two independent $N/2$ sub-FDNs. Raising $\theta_M$ grows
  off-diagonal blocks $F_1, F_2$; at $\theta_M = \pi/2$ the matrix is anti-block-diagonal.
  With $B$ and $C$ routed per channel, $\theta_M$ is a continuous stereo-width control.
  Sliding-window IACC (100 ms window, 50 ms hop, $N=32$, $T_{60}=10$ s) shows low
  coupling giving a channel-to-channel bounce, and $\theta_M \to \pi/4$ giving a wide
  decorrelated single network.
- **Selective freeze.** Any $\theta_i = 0$ splits the network in two; the kernel
  *position* sets the grouping. $\theta_1 = 0$ interleaves even- and odd-indexed
  delay lines, so with ascending delays both halves keep balanced echo density.
  Freeze (set $B = 0$, $\Gamma = I$) can then be applied to one half only - without
  decoupling, energy from the live half would pump into the frozen half.
- **Resonance breaking.** Modulating an angle moves the poles rather than the delay
  lengths, so it colours without chorusing. Pole-frequency histograms for an
  $8\times8$ network ($\theta_2$ modulated by a 1 Hz triangle of amplitude $\pi$) fall
  from $\sigma = 71.0$ to $\sigma = 24.8$. Practical settings: amplitude 2-15% of $\pi$,
  rate 0.1-1.0 Hz.

## Relations and limits

- Extends the Kronecker mixing matrices of Das, Canfield-Dafilou and Abel (one
  shared angle, fixed) to $M$ independent real-time angles, and supplies by
  construction the orthogonality that Schlecht and Habets found hard to preserve
  under feedback-matrix modulation.
- Restricted to $N = 2^M$. Losslessness is structural but says nothing about modal
  density or echo distribution; no perceptual evaluation was run.

## See also
- [[artificial-reverberation]] - FDN fundamentals and the other feedback matrices
- [[differentiable-fdn-design]] - fitting FDN parameters by gradient descent instead
- [[entities/source-papers#paper-coppola-fast-parametric-fdn-matrices-2026]] - catalog entry

[^coppola]: A. Coppola, "Fast Parametric Matrices for Lossless Feedback Delay Networks," DAFx26. See [[entities/source-papers#paper-coppola-fast-parametric-fdn-matrices-2026]].

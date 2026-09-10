---
title: Bowed-String Finite-Difference Models
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [string, physical-modeling, modal-synthesis, damping, acoustics, realtime]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_43.pdf
  - raw/DAFx26_paper_43.txt
---

# Bowed-String Finite-Difference Models

A full finite-difference bowed-string instrument, taken from the DAFx26 model of
the Chinese *yehu*: two stiff strings on a measured modal bridge, elastic bow
hairs, a stopping finger, and measured radiation.[^zheng] This is the FD/modal
route rather than the delay-line route - the natural comparison case for
[[reed-and-bow-models]].

## The instrument and the coupled system

The yehu has a coconut-shell resonator, a seashell bridge and two silk strings
(F4 and C5) with the bow hair passing *between* them; there is no fingerboard, so
the player stops the strings directly, usually both at once. Strings are modelled
over an extended domain from restraining loop to stub so the bridge coupling
dynamics are captured. For $i = 1,2$,
$$\mathcal{L}_{s,i}u_i = -J_{b,i}f_{b,i} - J_{f,i}f_{f,i} + J_{c,i}f_{c,i},$$
$$\mathcal{L}_{s,i} = \rho_i A_i\partial_t^2 - T_i\partial_x^2 + E_i I_i\partial_x^4
+ 2\rho_i A_i\left(\sigma_{0,i}\partial_t - \sigma_{1,i}\partial_t\partial_x^2\right),$$
simply supported at both ends. Bridge and body are $M$ mass-spring-damper modes
$M_m\ddot q_m + K_m q_m + R_m\dot q_m = -f_{c,1}-f_{c,2}$ with $K_m = M_m\omega_m^2$,
$R_m = M_m\sigma_m\omega_m$; the strings are assumed rigidly coupled, so string
displacement at $x_c$ equals $\sum_m q_m$.

## Two contrasting solvers

- **Finger contact, non-iterative.** Hunt-Crossley contact with potential
  $\Phi_i = K_f[\eta_i]_+^{\alpha+1}/(\alpha+1)$ and dissipation $\Theta_i = \beta K_f[\eta_i]_+^\alpha$ is
  **energy-quadratised**: writing $\Phi_i = \Psi_i^2/2$ turns the force into
  $f_{f,i} = \Psi_i g_i + \beta\Psi_i\,d\Psi_i/dt$ with an auxiliary variable that updates
  linearly, so no iteration is needed. A correction factor $\theta_i$ enforces
  $\mu_{t+}\Psi_i^{n-1/2}\ge 0$. The resulting $3\times3$ block system in
  $(u_1^{n+1}, u_2^{n+1}, U_f^{n+1})$ has diagonal-plus-rank-one blocks, inverted
  cheaply by **Sherman-Morrison** - which is what makes real time reachable.
- **Bow friction, iterative.** Elasto-plastic friction with average bristle
  deflection $z$: $f_b = \epsilon_0 z + \epsilon_1\,dz/dt$ and
  $\dot z = v_r\left(1 - \chi(v_r,z)\,z/z_{ss}(v_r)\right)$, with the Stribeck steady state
  $z_{ss}(v_r) = \mathrm{sign}(v_r)\frac{F_N}{\epsilon_0}\left(\mu_C + (\mu_S-\mu_C)e^{-(v_r/v_s)^2}\right)$
  and an adhesion map $\chi$ that ramps between the breakaway displacement $z_{ba}$
  and $|z_{ss}|$. Solved by Newton-Raphson on the residual in $(v_r^n,\mu_{t\circ}z^n)$.
  Passivity fails at $\chi = 1$ unless the bristle damping is made velocity
  dependent, $\epsilon_1(v_r) = \mu_C F_N/\sqrt{v_r^2+\gamma^2}$ with $\gamma = \mu_C F_N/\bar\epsilon_1$.
- **Elastic bow hairs.** The hair is a second-order element
  $M_h\ddot\zeta + K_h\zeta + R_h\dot\zeta = -f_b$, and the relative velocity includes it:
  $v_r = \partial_t\!\int J_b u\,dx + \dot\zeta - v_b$. A signed bow force $F_N$ selects which
  string is bowed, matching the monophonic playing technique.

## Measurement-based characterisation

- **Strings.** Density from mass and measured radius; Young's modulus, tension and
  loss coefficients by inverse modelling from wire-break excitation on an
  anti-vibration table with 3D-printed sensor bridges. String 1 (F4):
  $L = 0.38$ m, $\rho = 1350$ kg/m$^3$, $r = 0.40$ mm, $T = 64.29$ N, $E = 9.5\times10^9$ Pa,
  $\sigma_0 = 1.5844$ s$^{-1}$, $\sigma_1 = 0.0032$ m$^2$/s. String 2 (C5): $\rho = 1250$,
  $r = 0.55$ mm, $T = 50.61$ N, $E = 1\times10^{10}$ Pa.
- **Bridge.** Impact hammer plus laser Doppler vibrometer; the admittance is
  reduced by the filter diagonalisation method to **11 modes** (compare
  [[modal-analysis-measurement]]).
- **Radiation.** Bridge-force-to-pressure transfer function measured in a
  hemi-anechoic chamber, microphones 30 cm behind the soundbox, fitted with **25
  parallel second-order sections** in the warped frequency domain (parallel form
  for numerical robustness). Synthesis = filter the simulated bridge force.

## Results

- Simulated bridge velocity fits the measured hammer response and, with bow force
  and velocity tuned to 0.7 N and 0.3 m/s (they were not measurable during the
  experiment), the measured bowed steady state.
- Finger parameters are empirical, not measured: $K_f = 5\times10^5$, $\alpha = 2.3$,
  $\beta = 20$. Gestures demonstrated include string crossings, bow reversals,
  vibrato from small finger motion, and glides.
- Discrete energy error stays at order $10^{-15}$ over a 10 s simulation - near
  machine precision. Grid spacing must satisfy the usual stability bound $h_i \ge h_{\min,i}$.
- **Real time.** In C++ at 44.1 kHz, limiting $|F_N|$ to at least 0.05 N caps the
  Newton iterations at three; 10 s of audio takes 1.49 s on an Apple M1, about
  6.6x faster than real time.

Limitations: one measured instrument, no listening test or comparison against
recordings, a single finger, and no tension-modulated string (a stated future
route to physically correct vibrato).

## See also
- [[reed-and-bow-models]] - the waveguide route to bowed strings
- [[string-modeling]] - stiff-string and bridge-coupling background
- [[entities/source-papers#paper-zheng-yehu-physical-model-2026]] - catalog entry

[^zheng]: Z. Zheng, C. C. Darabundit, G. Scavone, "Physical Model of the Chinese Yehu for Sound Synthesis," DAFx26. See [[entities/source-papers#paper-zheng-yehu-physical-model-2026]].

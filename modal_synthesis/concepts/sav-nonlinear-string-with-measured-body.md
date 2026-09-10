---
title: SAV Nonlinear String with Measured Body
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal-synthesis, string, vibration, physical-modeling, impulse-response, dataset, dsp]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_40.pdf
  - /l/dttd/DAFx26/txt/DAFx26_paper_40.txt
---

# SAV Nonlinear String with Measured Body

Plucked tones for all 65 guitars of the Mores archive: a geometrically exact
nonlinear string, quadratised by the Scalar Auxiliary Variable (SAV) method and
coupled at the bridge to modal parameters measured per instrument[^1]. See
[[nonlinear-modal-synthesis]], [[coupled-structures]], [[modal-analysis-measurement]]
for the pole-fitting stage and [[damping-models]] for per-mode loss laws.

## Continuous model
$$\mu\,\partial_t^2 u = \mathcal{L}u + F + \delta_e f_e + \delta_b F_b,\qquad
\mathcal{L} = T_0\partial_x^2 - EI\,\partial_x^4 - \mu\sigma\,\partial_t$$
simply supported; pluck $f_e$ at $x_e$, bridge reaction $F_b$ at $x_b=\xi_b L$.
The potential splits as $V = Q + \phi_{\rm nl}$ ($Q$ = tension plus bending), with
the geometrically exact residual built on the Green-Lagrange strain of the slope
$\zeta \triangleq \partial_x u$:
$$\mathcal{V}(\zeta) = \frac{G}{2}\left(\sqrt{1+\zeta^2}-1\right)^2,\quad
G \triangleq EA - T_0 > 0,\quad \phi_{\rm nl}=\int_0^L \mathcal{V}(\partial_x u)\,dx \ge 0 .$$
Unlike Kirchhoff-Carrier (averaged strain, rank-one coupling), the pointwise
slope dependence is kept, so pitch glide and phantom partials survive.

## SAV quadratisation
Since $\phi_{\rm nl}\ge 0$, introduce one scalar unknown and its normalised gradient
$$\psi \triangleq \sqrt{2\phi_{\rm nl}+\varepsilon},\qquad
g \triangleq \frac{\delta\psi}{\delta u} = \frac{1}{\psi}\frac{\delta\phi_{\rm nl}}{\delta u}
\;\Longrightarrow\; \frac{\delta\phi_{\rm nl}}{\delta u} = \psi\,g,$$
gauge $\varepsilon>0$ keeping the denominator finite. The dynamics become **linear
in the unknowns already at the continuous level**:
$$\mu\,\partial_t^2 u = \mathcal{L}u - \psi\,g + \delta_e f_e + \delta_b F_b,
\qquad \dot\psi = \langle g, \dot u\rangle ,$$
exactly equivalent to the original PDE, with $H = K + Q + \psi^2/2 \ge 0$ so
unforced solutions stay bounded ($\delta\phi_{\rm nl}/\delta u = -\partial_x[S(\zeta)\zeta]$,
$S(\zeta)=G(\sqrt{1+\zeta^2}-1)/\sqrt{1+\zeta^2}$).

## Bridge coupling and modal projection
Measured driving-point compliance, $J$ modes:
$$H_b(\omega) = \sum_{j=1}^{J}\frac{\beta_j}{(\omega_j^b)^2 - \omega^2 + 2i\sigma_j^b\omega},
\quad m_j^b\!\left(\ddot r_j + 2\sigma_j^b\dot r_j + (\omega_j^b)^2 r_j\right) = -\beta_j F_b,$$
with compatibility $u(x_b,t) = u_b(t) = \sum_j r_j$. Stacking $M$ string modes $q$
and $J$ bridge modes $r$ into $y=[q;r]$, $N=M+J$:
$$\ddot y + C\dot y + \Omega^2 y = -\frac{\psi}{\mu}\tilde\eta + s\,f_e + f\,F_b,
\qquad \dot\psi = \eta^{\!\top}\dot q_{\rm nl},$$
$\eta = R^{\!\top}g$ (gradient projected through $R_{im}=\partial_x\chi_m(x_i)$ on a
uniform grid), $f = [\chi(x_b)/\mu;\,-\beta\oslash m^b]$. Only modes below
$f_{\rm nl}^{\max}$ join the nonlinearity: at 5 kHz, $M_{\rm nl}\approx 60$ of
$M\approx 200$ for a low E, with no audible loss. String damping follows
Woodhouse, $c_m = \sigma_{0,s} + \tfrac{1}{2}\eta_{f,s}\omega_m$,
$\sigma_{0,s}=6\ln 10/T_{60,s}$.

## O(N) update: two sequential Sherman-Morrison steps
Modal frequencies and dampings are pre-warped so each uncoupled mode reproduces
its analytic solution exactly (no numerical dispersion). With
$D \triangleq I + \frac{k^2}{4}\tilde\Omega^2 + k\tilde C$ diagonal,
$$\left(D + f\tilde v^{\!\top} + \tfrac{k^2}{4\mu}\,\tilde z^n(\tilde\eta^n)^{\!\top}\right) y^{n+1} = b^n :$$
two **rank-one** perturbations of a diagonal matrix, one from the bridge coupling
and one from the SAV nonlinearity. One Sherman-Morrison inversion each (bridge
first, giving $\tilde D^{-1}$, then the SAV term) removes both: nothing is
assembled or factorised and cost stays $O(N)$ per sample. $F_b$ then follows
explicitly, driving the radiation filters and a linear sympathetic-string bank.

## Two drift regularisations
- **Servo correction**: steer the gradient along the velocity direction so
  $\psi^{n-1/2}$ tracks $\psi_{\rm true}^{n-1/2}=\sqrt{2\phi_{\rm nl}(\zeta^n)+\varepsilon}$,
  $\bar g = \hat g - \frac{\psi^{n-1/2}-\psi_{\rm true}^{n-1/2}}{\|\zeta^n-\zeta^{n-1}\|}(\zeta^n-\zeta^{n-1})$
  (Eq. 40 of the paper; the norm is not squared, verified against the PDF).
- **Sign-flip constraint**: impose $\mu_{t+}\psi^{n-1/2}\ge 0$, giving
  $\gamma = -4\psi^{n-1/2}/\theta$ when $\theta\ne 0$ and $\theta<-4\psi^{n-1/2}$,
  else $\gamma=1$, with $\theta=(\eta^n)^{\!\top}\tilde D^{-1}(b_L^n-y^{n-1})$;
  final gradient $g^n=\gamma\bar g^n$. The analytic gradient alone misbehaves at audio rate.

## Extracting the body from the Mores dataset
65 instruments built 1803-2018, measured 2018-2019 at seven sites; bridge saddle
struck with a 9.8 g hammer, two 0.4 g accelerometers (bass and treble sides) plus
three microphones 10 cm above the top, 48 kHz/24-bit; FRF by the $H_1$ estimator
$H = YF/|F|^2$. Bridge accelerance fit: truncate to 3000 samples with a
raised-cosine fade; peak-pick over 20-10000 Hz (min prominence 0.5 dB, min spacing
1 Hz); $\sigma_j = \Delta\omega_{-3\rm dB}/2$ from the $-3$ dB bandwidth in a
$\pm15\%$ window; real-constrained Tikhonov least squares for residues
$\beta_j^{\rm acc}$; convert $\beta_j = \beta_j^{\rm acc}/(-\omega_j^2)$; discard
modes with $\omega_j < 0.2\sigma_j$. Radiation is fitted the same way in
pole-residue form $H_{\rm rad}=\sum_l b_l/(i\omega-p_l)+\bar b_l/(i\omega-\bar p_l)$,
separately for bass and treble sides, giving the stereo pair (mid-side width).
Ranges: 50-200 bridge modes and 80-300 radiation poles per side.

## Output and limits
- 6 strings $\times$ frets 0-15 per guitar, about 6240 notes, 5 s at 48 kHz; MATLAB cost 0.1-0.5 s per note (radiation bank dominates), whole library in hours.
- $\xi_b=0.995$, pluck fraction random in $[0.68,0.82]$, $\varepsilon=10^{-16}$, modal limit 10 kHz, $T_{60,s}\in[2.43,4.58]$ s, $\eta_{f,s}\in[2.0,2.5]\times10^{-4}$ s.
- Limits: no listening test versus recordings; the measured body is linear, so all nonlinearity lives in the string; multi-string bridge coupling, fret buzz and slides are future work; no real-time port yet.

[^1]: [[entities/source-papers#paper-ducceschi-65-classical-guitars-2026]] - Ducceschi, Russo & Webb, "Measurement-Informed Nonlinear Modal Synthesis of 65 Classical Guitars," DAFx26. Code: github.com/Nemus-Project/65_modelled_guitars

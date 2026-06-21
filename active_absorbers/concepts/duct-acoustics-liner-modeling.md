---
title: Duct-Acoustics & Liner Modeling — E3 Reading Note + Spec
created: 2026-06-20
updated: 2026-06-20
type: concept
tags: [hybrid-passive, acoustics, anc, tonal, reference]
sources:
  - https://sjoerdr.win.tue.nl/papers/boek.pdf
  - https://doi.org/10.1121/1.423870
  - https://doi.org/10.1098/rspa.1979.0046
  - https://doi.org/10.2514/2.1188
  - https://doi.org/10.1016/0022-460X(73)90040-2
  - https://doi.org/10.1126/sciadv.1501595
---

# Duct-Acoustics & Liner Modeling — E3 Reading Note + Spec

Reading guide and modeling spec for **E3** of the rooftop-fan
[[rooftop-fan-contenders]] roadmap: a 1-D plane-wave **lined-duct** transfer-
matrix model that outputs transmission/insertion loss, the substrate for E4
(passive liners) and E5 (FxLMS duct termination, [[fxlms-algorithm]]). The bet:
treat the fan's confined exhaust as a waveguide, where the free-field 50%/aperture
ceilings of [[electroacoustic-absorbers]] vanish and one-port matching works.

## Familiar vs new

The **two-port transfer-matrix (four-pole) method is the same scattering
formalism as digital-waveguide acoustic tubes** — home turf. What is *new* here:
(1) the **lined-wall impedance boundary** and its modal attenuation, (2) the
**liner impedance sub-models**, (3) the **muffler TL/IL/NR conventions**.

## Reading list (priority order)

**Tier 1 — E3 core**
- **Munjal, *Acoustics of Ducts and Mufflers*, 2nd ed. (Wiley 2014).** THE
  reference. Ch. 2 = plane-wave four-poles; dissipative-muffler ch. = lined
  ducts; precise TL/IL/NR definitions. ISBN 978-1-118-44312-5.
- **Rienstra & Hirschberg, *An Introduction to Acoustics*** — rigorous, **free**
  ([PDF](https://sjoerdr.win.tue.nl/papers/boek.pdf); staged in
  `incoming-pdfs/`). Duct modes, impedance walls, Ingard–Myers BC, vortex sound.
- **Cremer optimum impedance** — the wall impedance maximizing modal attenuation;
  read via **Tester, *JSV* 27 (1973)** [doi](https://doi.org/10.1016/0022-460X(73)90040-2).

**Tier 2 — liner impedance (E4)**
- **Maa, "Potential of microperforated panel absorber," *JASA* 104 (1998)**
  [doi](https://doi.org/10.1121/1.423870) — MPP/perforate impedance; the resonant-
  liner workhorse (extends `03_helmholtz_absorber.py`). **Ingested** →
  [paper-maa-mpp-1998](../entities/source-papers.md#paper-maa-mpp-1998); model below.
- **Howe, *Proc. R. Soc. A* 366 (1979)** [doi](https://doi.org/10.1098/rspa.1979.0046)
  — Rayleigh conductivity with mean flow (bias-flow theory backbone); then
  **Jing & Sun, *AIAA J.* 38 (2000)** [doi](https://doi.org/10.2514/2.1188) for
  the codeable thick-plate bias-flow impedance. (Eldredge & Dowling 2003 already
  in catalog.)
- **Ingard, *JASA* 25 (1953)** — orifice/Helmholtz impedance + end corrections.

**Tier 3 — active termination (E5)**: **Nelson & Elliott, *Active Control of
Sound* (1992)** — single-channel duct ANC; + Rivet/Lissek 2017 (catalog).
**Tier 4 — resonant metasurface (Tier-1 "think big")**: **Ma & Sheng, *Sci. Adv.*
2 (2016)** [doi](https://doi.org/10.1126/sciadv.1501595).

## Modeling decisions (settle before coding)

- **Output TL, not IL, for E3.** Transmission loss is termination-independent (a
  property of the element, anechoic load); insertion loss depends on source
  impedance + termination and belongs in E5 once those are pinned. NR = pressure
  difference across the element (mic-measurable). Munjal is the authority.
- **Locally-reacting wall** (admittance per unit area, no axial coupling in the
  liner) is the right first model; bulk-reacting only if a deep fibrous backing.
- **The duct target impedance is NOT $\rho c$.** In free field you match $\rho c$;
  in a lined duct the attenuation-optimal wall impedance is the finite complex
  **Cremer optimum**, not $\rho c$ and not $\infty$. Aim the liner there.

## E3 transfer-matrix element library

Four-pole convention $\begin{bmatrix}p_1\\ U_1\end{bmatrix}=\begin{bmatrix}A&B\\C&D\end{bmatrix}\begin{bmatrix}p_2\\ U_2\end{bmatrix}$, volume velocity $U=Su$, characteristic $Y=\rho c/S$.

| Element | Matrix / impedance | Ref |
|---|---|---|
| Hard-wall duct, length $L$ | $\begin{bmatrix}\cos kL & jY\sin kL\\ jY^{-1}\sin kL & \cos kL\end{bmatrix}$ | Munjal Ch.2 |
| Side-branch resonator $Z_b$ | shunt $\begin{bmatrix}1&0\\ Z_b^{-1}&1\end{bmatrix}$, $Z_b=R+j(\omega M-\tfrac1{\omega C})$, $f_0=\tfrac{c}{2\pi}\sqrt{\tfrac{S_n}{l_{\rm eff}V}}$ | Ingard 1953 |
| Lined section (wall admittance $\beta$) | complex axial $k_x(\beta)$ from the eigenvalue relation → propagation matrix | Munjal; Cremer/Tester |
| MPP perforate wall (no flow) | $z=r+j\omega m$, $k=d\sqrt{f}/10$; $r=\tfrac{32\eta t}{\sigma\rho_0 c d^2}k_r$, $\omega m=\tfrac{\omega t}{\sigma c}k_m$ | [[paper-maa-mpp-1998]] |
| Bias-flow perforate wall | orifice impedance from Howe conductivity $K_R(St)$, $St=\omega a/U$ | Howe 1979; Jing–Sun 2000 |

MPP-over-cavity-$D$ surface absorption: $\alpha=\tfrac{4r}{(1+r)^2+(\omega m-\cot(\omega D/c))^2}$, perfect ($\alpha_0{=}1$) at the $r{=}1$ match. Headline duct output: $\mathrm{TL}=20\log_{10}\!\big[\tfrac12\,|A+B/Y+CY+D|\big]$ (equal inlet/outlet area).

## Build order

E3 hard-wall + side-branch Helmholtz (sanity vs `03_helmholtz_absorber.py`) →
add lined-section $k_x(\beta)$ → E4 drop in Maa MPP then bias-flow wall admittance
→ E5 cascade an active termination. See [[hybrid-active-passive]],
[[tonal-periodic-anc]], [[classical-anc-overview]].

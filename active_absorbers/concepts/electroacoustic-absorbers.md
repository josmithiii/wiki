---
title: Electroacoustic Absorbers (shunt + feedback active impedance)
created: 2026-06-18
updated: 2026-06-19
type: concept
tags: [active-absorber, active-impedance, feedback, feedforward, loudspeaker, transducer, impedance, acoustics, stability, room, duct, history, reference]
sources:
  - raw/Olson-May-ElectronicSoundAbsorber-JASA1953.txt
  - raw/Lissek-Boulandet-Fleury-ElectroacousticAbsorbers-JASA2011.txt
  - raw/Rivet-Karkar-Lissek-BroadbandLF-ElectroacousticAbsorbers-2017.txt
---

# Electroacoustic Absorbers

An **electroacoustic absorber (EA)** is a loudspeaker whose acoustic
impedance *at the diaphragm* is shaped — by an electrical load and/or a
control loop — so that the diaphragm presents a chosen specific acoustic
impedance $Z_s(\omega)$ to the incident field, typically the matched
value $Z_s=\rho c$ for which the wave is absorbed without reflection.
This is the loudspeaker realization of **active impedance control**
(see [[hybrid-active-passive]] §1) and the direct answer to "can a
driven panel *terminate* a low-frequency wave by presenting the right
pressure-to-velocity ratio?" — yes, and the field has done it since 1953.

The defining modern insight (Lissek et al. 2011[^lissek-2011]) is that
**passive electrical shunts and active acoustic feedback are the same
thing** viewed from two sides: every feedback law has an equivalent
electrical network across the voice coil, and vice-versa. Contrast the
*hybrid passive+active* liners of [[hybrid-active-passive]] (a porous
layer doing the HF work, active loop pinning LF impedance): here the
loudspeaker diaphragm *itself* is the absorbing surface.

## 1. The absorption criterion

For 1-D normal incidence, with diaphragm specific impedance
$Z_s(s)=P_t(s)/V(s)$ (total pressure / diaphragm velocity), the
reflection coefficient and absorption coefficient are

$$
r(f)=\frac{Z_s(f)-\rho c}{Z_s(f)+\rho c},\qquad
\alpha(f)=1-\lvert r(f)\rvert^2 .
$$

Total absorption ($\alpha=1$) requires $Z_s=\rho c$: a **purely
resistive** match with zero pressure–velocity phase. The passive
loudspeaker cannot hold this away from its mechanical resonance because
$Z_s$ carries the reactive mass ($sM_{ms}/S_d$) and stiffness
($1/(sS_dC_{mc})$) terms. Control exists to flatten those reactances and
set the resistance — i.e. to make the diaphragm look like $\rho c$ over a
band, not just at one frequency.

## 2. The 1-DOF resonator model and its three knobs

A closed-box moving-coil driver below its first diaphragm mode is a
single mass–spring–damper. Lissek 2011[^lissek-2011] shows the
controlled diaphragm is *still* a 1-DOF resonator whose three parameters
— resonance $f_{EA}$, normalized resistance $\zeta_{EA}$, quality factor
$Q_{EA}$ — are set independently by three electrical knobs:

| Knob | Symbol | Physical effect |
|---|---|---|
| Shunt / source resistance | $R_s$ | adds electrical damping $(Bl)^2/(R_e+R_s)$ |
| Velocity-feedback gain | $C_v$ | acts as a **negative impedance** (motional feedback) |
| Pressure-feedback gain | $C_p$ | lowers apparent mass, raises compliance → widens band |

A "singular result": the resonance $f_{EA}$ barely moves under control;
$C_p$ trades apparent mass for bandwidth at nearly fixed center frequency.

## 3. Control families (increasing capability)

- **Open circuit (passive).** $\alpha<1$ at resonance; mechanical losses
  $R_{ms}\ll Z_{mc}$ are mismatched. The baseline to beat.
- **Shunt resistance (semi-active).** A single resistor across the coil
  adds loss; the *optimal* shunt
  $R_{opt}=(Bl)^2/(Z_{mc}-R_{ms})-R_e$ (≈ 5 Ω for the studied driver)
  gives **perfect absorption at resonance** but a narrow band. Always
  stable. This is the "shunt loudspeaker" of Fleming et al. 2007.
- **Velocity feedback = negative-impedance shunt.** Equivalent to a
  negative R–L across the coil; raising gain lowers $Q$ and broadens the
  band, but at high gain forces a rigid diaphragm (perfect *reflection*),
  so it is used in moderation.
- **Direct impedance control** (combined pressure+velocity feedback):
  the matched resistance is set *directly* by the gain ratio
  $C_v/C_p = Z_c = \rho c \approx 413\ \mathrm{Pa\,s/m}$; raising both
  gains at fixed ratio widens the band → **broadband $\rho c$ match**.
- **Hybrid sensor-/shunt-based + current drive** (Rivet et al.
  2017[^rivet-2017]): a single pressure sensor feeds a controller
  $\Theta(s)=I/P_t=(S_dZ_{st}-Z_m)/(Bl\,Z_{st})$ driving a *current*
  amplifier. Current drive removes the blocked coil impedance
  $Z_e=sL_e+R_e$ from the loop, killing the voice-coil-inductance roll-off
  that limited earlier sensorless-shunt and voltage-drive schemes — the
  practical key to *stable, broadband, low-frequency* absorption.

## 4. The matched-termination result (Olson & May → today)

The idea is old and the physics is forgiving:

- **Olson & May 1953**[^olson-1953] built the first EA — a co-located
  mic + amplifier + loudspeaker feedback giving **10–25 dB reduction over
  three octaves** in the LF range. Their "absorber" mode places a
  resistive screen matched to the radiation resistance $r_{A1}$ in front
  of the diaphragm; when the sensed pressure $p_3\to 0$, "100 percent
  absorption is obtained." That is exactly the
  pressure-and-velocity termination concept.
- **Why so little excursion is needed.** Absorbing a *propagating* wave
  only requires matching its particle velocity $u=p/(\rho c)$, which is
  small; displacement $\xi=p/(\rho c\,\omega)$ is **~1 µm at 80 dB / 100
  Hz**, scaling as $1/f$. The EA literature confirms this empirically —
  the drivers are ordinary small woofers, not high-excursion subs. The
  electrostatic-panel idea for rooftop fans is therefore well-posed *on
  excursion grounds*: the ESL excursion limit bites for *radiating* bass,
  not for *absorbing* it. **But** the 100% result above assumes a
  **one-port** surface (sealed back). An *open* diaphragm is a two-sided
  scatterer and is capped at 50% — see §5.

## 5. Why an open (dipole) diaphragm caps at 50%

The matched-termination result of §4 — $Z_s=\rho c \Rightarrow \alpha=1$
— is a **one-port** statement: it assumes the diaphragm radiates to the
incident side *only*, i.e. its back is sealed (Olson's enclosed
"zero-order radiator"; the closed boxes of Lissek and Rivet). Remove the
enclosure — as in an open electrostatic panel — and the diaphragm
radiates equally from both faces. It is then a symmetric two-port, and a
single such layer can absorb **at most one half** of a normally incident
plane wave, *regardless of excursion or control law*.

Model the open diaphragm as a limp resistive sheet of normalized
resistance $\rho = r/\rho c$: the velocity is continuous across it
(impermeable), and the pressure drops by $r\,v$. With incident, reflected,
and transmitted waves $p_i, p_r, p_t$ at $x=0$:

$$
\underbrace{p_i - p_r = p_t}_{\text{velocity continuity}},\qquad
\underbrace{(p_i+p_r)-p_t = \tfrac{r}{\rho c}\,p_t}_{\text{resistive pressure drop}} .
$$

Solving gives the transmission, reflection, and absorption coefficients

$$
t=\frac{2}{2+\rho},\qquad
\Gamma=\frac{\rho}{2+\rho},\qquad
A = 1-\lvert\Gamma\rvert^2-\lvert t\rvert^2 = \frac{4\rho}{(\rho+2)^2},
$$

which is maximized at $\rho = 2$ (sheet resistance $r = 2\rho c$), giving

$$
A_{\max} = \tfrac12 .
$$

The cap is **excursion-independent**: even with unlimited stroke the open
single layer re-radiates symmetrically and loses half the incident power
to transmission + reflection. This is exactly why Olson & May enclosed the
back and why every EA in §4 uses a closed box.

**Beating 50% while keeping an open structure** needs a second degree of
freedom so that *both* the reflected and transmitted waves can be nulled
at once (coherent perfect absorption):

- **Seal the back** → one-port → up to 100% (the EA route; excursion
  still trivial, but you give up the open panel).
- **Two independently driven layers** in tandem (two ESL diaphragms,
  separate drive) → control $\Gamma$ and $t$ simultaneously → ~100%.
- **Active rear termination** — a second active surface absorbing/nulling
  the back radiation.

A second, geometric limit applies on top of this: a diaphragm-sized patch
is **sub-wavelength** at 100 Hz ($\lambda = 3.4$ m), so it cannot carve a
wavelength-resolved "hole" in the wavefront — the shadow heals by
diffraction within a Fresnel distance $\sim S/\lambda$, and the absorbed
power is governed by the absorption *cross-section*, not the geometric
area. The one consolation is that a resonant dipole absorber's maximum
cross-section $\sigma_{\max}=3\lambda^2/8\pi \approx 1.4\ \mathrm{m}^2$ at
100 Hz exceeds a typical panel — a small resonant panel can grab flux from
wider than itself — but it remains under the 50% open-layer ceiling and is
narrowband. See [[rooftop-fan-contenders]] for the open-source coverage
problem this creates.

## 6. Bandwidth and numbers

Rivet 2017[^rivet-2017] parameterizes the target as
$Z_{st}(s)=s\,\mu M_{ms}/S_d + R_{st} + \mu/(s S_d C_{mc})$, where
$0<\mu<1$ scales the effective mass *and* stiffness down together to
widen the band. The efficient-absorption bandwidth is

$$
BW=\frac{S_d}{2\pi\mu M_{ms}}\,
\frac{\sqrt{(\sqrt2-1)^2(R_{st}+Z_c)^2-(R_{st}-Z_c)^2}}
{\sqrt{1-(\sqrt2-1)^2}},\quad |R_{st}-\sqrt2\,Z_c|\le Z_c .
$$

So bandwidth grows with $S_d/M_{ms}$ (large light diaphragm), while the
cabinet volume $V_b$ (via $C_{mc}$) sets the center $f_0$. Measured: a
Peerless 6½″ driver ($f_0\approx 84$ Hz, $\mu=0.15$, $R_{st}=\rho c$)
gives a **$\rho c$ match over ~410 Hz**, and as a duct termination
collapses the 44–300 Hz modal peak-to-dip range from **51.3 dB (rigid)
to 12.6 dB** — a 4:1 reduction. Lissek 2011 validated the same theory in
an ISO 10534-2 impedance tube, tuning absorption from near-total
reflection to near-total absorption.

## 7. Relevance to the rooftop-fan / electrostatic-absorber project

- **Feasibility of the ESL absorber.** §4 settles the excursion worry:
  micron-scale motion suffices to terminate ~100 Hz tones at realistic
  SPL. The catch is structural, not excursion (§5): an *open* electrostatic
  panel is a two-sided scatterer capped at 50%. To exceed that you must
  seal the back (one-port) or run two independently driven layers (CPA).
- **Sensorless / shunt route.** For an outdoor, many-unit, low-maintenance
  deployment, the shunt⇔feedback equivalence means a passive or
  synthesized **electrical network** can pull the driver toward $\rho c$
  without an exposed microphone — attractive for weather survivability.
- **Aperture caveat (the hard part).** Rivet's analysis assumes the
  absorber area ≈ the waveguide cross-section; if the absorber is much
  smaller than the duct (or, in free field, much smaller than the source's
  radiated wavefront) the uniform-pressure boundary assumption fails and a
  transverse-mode / FEM treatment is required. This is the open-source
  *coverage* problem for an open rooftop fan — see [[rooftop-fan-contenders]].
- **Where it fits:** EAs are the *active-impedance* leg complementary to
  the *hybrid passive+active* duct liners ([[hybrid-active-passive]] §2)
  and the pure anti-noise ANC of [[classical-anc-overview]].

## 8. Open issues

- **Stability vs. acoustic environment.** Gains are bounded by coil
  inductance, $R_e/L_e$ frequency dependence, and diaphragm higher-order
  modes; current drive (Rivet) removes the worst offender. Routh analysis
  (Lissek) gives $-R_e<R_s$, $C_v\ge0$ for the ideal model.
- **Free field vs. tube.** All three sources test 1-D / normal-incidence
  rigs; free-field open-loop margins are actually *larger* than in the
  tube (tube resonances dominate measured margins), but open free-field
  far-field cancellation of a real source is **not** demonstrated.
- **Per-mode / frequency-dependent target.** For rooms the optimal $R_{st}$
  is frequency-dependent and need not equal $\rho c$; outdoors the optimal
  termination impedance for a finite fan source is an open design question.

## Sources ingested

- **Olson & May 1953** — first electronic sound absorber; mic+amp+speaker
  feedback, 10–25 dB over 3 octaves, $p_3{=}0$ ⇒ 100% absorption mode. See
  `entities/source-papers.md#paper-olson-may-electronic-sound-absorber-1953`.
- **Lissek, Boulandet & Fleury 2011** — unifying shunt⇔feedback theory;
  1-DOF resonator with three knobs; direct impedance control $\rho c$ match.
  See `entities/source-papers.md#paper-lissek-boulandet-fleury-electroacoustic-absorbers-2011`.
- **Rivet, Karkar & Lissek 2017** — broadband LF EA via pressure-sensor
  feedforward + current drive; bandwidth law; ~410 Hz $\rho c$ match; duct
  modal damping. See
  `entities/source-papers.md#paper-rivet-karkar-lissek-broadband-lf-ea-2017`.

## Pending / related

- Bobber 1970 (active transducer as transmission-line characteristic
  impedance) and Fleming et al. 2007 (shunt loudspeakers) — cited heavily
  by Lissek 2011; not yet ingested.
- Guicking & Karcher 1984 (foundational active impedance control) — still
  paywalled; covered indirectly (see [[hybrid-active-passive]]).
- Boulandet & Lissek 2010/2014 (feedback-control optimization of EAs) — the
  immediate methodological predecessors of Rivet 2017.

See also: [[hybrid-active-passive]] (porous+active liners, metamaterials),
[[classical-anc-overview]] (anti-noise ANC and secondary-path modeling),
[[rooftop-fan-contenders]] (the fan-hum application and its aperture problem).

[^olson-1953]: H. F. Olson & E. G. May, "Electronic Sound Absorber," *J. Acoust. Soc. Am.* 25(6):1130–1136, 1953. Distilled in `entities/source-papers.md#paper-olson-may-electronic-sound-absorber-1953`.
[^lissek-2011]: H. Lissek, R. Boulandet & R. Fleury, "Electroacoustic absorbers: Bridging the gap between shunt loudspeakers and active sound absorption," *J. Acoust. Soc. Am.* 129(5):2968–2978, 2011. DOI 10.1121/1.3569707. Distilled in `entities/source-papers.md#paper-lissek-boulandet-fleury-electroacoustic-absorbers-2011`.
[^rivet-2017]: E. Rivet, S. Karkar & H. Lissek, "Broadband Low-Frequency Electroacoustic Absorbers through Hybrid Sensor-/Shunt-Based Impedance Control," *IEEE Trans. Control Syst. Technol.* 25(1), 2017. DOI 10.1109/TCST.2016.2547981. Distilled in `entities/source-papers.md#paper-rivet-karkar-lissek-broadband-lf-ea-2017`.

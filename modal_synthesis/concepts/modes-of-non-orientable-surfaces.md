---
title: Modes of Non-Orientable Surfaces
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, eigenmode, wave-equation, vibration, room, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_11.pdf
  - /l/dttd/DAFx26/txt/DAFx26_paper_11.txt
---

# Modes of Non-Orientable Surfaces

Physical modeling normally starts from an object that exists. Lee and Rau invert
that order and model the acoustics of surfaces that **cannot** exist in
$\mathbb{R}^3$ without self-intersection - the Mobius strip, the Klein bottle and
the real projective plane - deriving closed-form eigenfrequencies and mode shapes
and verifying them against FDTD[^1]. See [[mode-shapes-and-eigenvalues]] for the
underlying eigenproblem and [[resonator-bank-implementation]] for turning the
result into audio.

## Quotient-space construction
The wave equation on a 2D manifold $S$ is $\partial_t^2 p = c^2\Delta_S p$, with
separable solutions $p_{mn} = \phi_{mn}(r)[A\cos\omega_{mn}t + B\sin\omega_{mn}t]$
and $\Delta_S\phi_{mn}+k_{mn}^2\phi_{mn}=0$, $\omega_{mn}=c\,k_{mn}$. Every boundary
rule is a **generator** relating the fundamental domain
$\sigma=[0,L_x]\times[0,L_y]$ to an adjacent copy, tiling $\mathbb{R}^2$:

| Geometry | Identification | Tiling action |
|---|---|---|
| Dirichlet rectangle | $\phi=0$ on the edge | reflection with sign flip |
| Neumann rectangle | $\partial_n\phi=0$ | reflection, no sign flip |
| Torus $T^2$ | $(x,y)\sim(x+L_x,y)$, $(x,y)\sim(x,y+L_y)$ | pure translations |
| Mobius strip $M$ | $(x,y)\sim(x+L_x,\,L_y-y)$ | translation with transverse flip |
| Klein bottle $K$ | $(x,y)\sim(x+L_x,y)$ and $(x,y)\sim(-x,\,y+L_y)$ | one matched, one flipped pair |
| Real projective plane $\mathbb{RP}^2$ | $(x,y)\sim(x+L_x,-y)$ and $(x,y)\sim(-x,\,y+L_y)$ | two flipped pairs |

Rather than working on a curved or self-intersecting surface, one solves the
Helmholtz problem on the **flat** domain $\sigma$ with the right identification at
each edge. Two constraints then pin down each mode: lattice periodicity restricts
the Fourier support to the reciprocal lattice $\Lambda^*$, and the Helmholtz
equation requires $k_x^2+k_y^2=k_{mn}^2$, so $\phi_{mn}$ is a finite superposition
of the plane waves at the intersection of $\Lambda^*$ with a circle of radius $k_{mn}$.
An orientation-reversing ("phase-conjugating") identification is exactly what makes
the manifold non-orientable and reshapes that intersection.

## Closed forms
Normalised over $\sigma$; $m,n$ non-negative integers unless noted.

| Geometry | $\phi_{mn}(x,y)$ | $f_{mn}$ |
|---|---|---|
| Dirichlet rect. | $\frac{2}{\sqrt{L_xL_y}}\sin\frac{m\pi x}{L_x}\sin\frac{n\pi y}{L_y}$, $m,n\ge1$ | $\frac{c}{2}\sqrt{\frac{m^2}{L_x^2}+\frac{n^2}{L_y^2}}$ |
| Neumann rect. | $\frac{1}{\sqrt{L_x^{(2)}L_y^{(2)}}}\cos\frac{m\pi x}{L_x}\cos\frac{n\pi y}{L_y}$ | same as Dirichlet |
| Torus | $\frac{1}{\sqrt{L_xL_y}}\exp\!\left[2\pi i\left(\frac{mx}{L_x}+\frac{ny}{L_y}\right)\right]$, $m,n\in\mathbb{Z}$ | $c\sqrt{\frac{m^2}{L_x^2}+\frac{n^2}{L_y^2}}$ |
| Mobius | $\sqrt{\frac{2}{L_xL_y}}\sin\frac{m\pi x}{L_x}\exp\frac{i\pi n y}{L_y}$ | $\frac{c}{2}\sqrt{\frac{m^2}{L_x^2}+\frac{n^2}{L_y^2}}$, **$m+n$ odd** |
| Klein bottle | $\sqrt{\frac{2}{L_xL_y^{(1)}}}\cos\!\left[\pi\!\left(\frac{2mx}{L_x}-\frac{n}{2}\right)\right]\exp\frac{i\pi n y}{L_y}$ | $\frac{c}{2}\sqrt{\frac{4m^2}{L_x^2}+\frac{n^2}{L_y^2}}$ |
| $\mathbb{RP}^2$ | $\sqrt{\frac{2}{L_x^{(1)}L_y^{(1)}}}\cos\!\left[\pi\!\left(\frac{mx}{L_x}-\frac{m+n}{2}\right)\right]\cos\!\left[\pi\!\left(\frac{ny}{L_y}+\frac{m+n}{2}\right)\right]$ | $\frac{c}{2}\sqrt{\frac{m^2}{L_x^2}+\frac{n^2}{L_y^2}}$ |

Here $L^{(1)} = L(1+\delta_{\cdot=0})$ and $L^{(2)}=L(2-\delta_{\cdot=0})$ are
normalisation lengths accounting for modes uniform along one axis, which carry
double the energy. Wavenumber spacings differ: torus $k_x = 2m\pi/L_x$ (lattice
period $L_x$), Mobius and the rectangles $k_x=m\pi/L_x$ (period $2L_x$), Klein
$k_x = 2m\pi/L_x$ with $k_y=n\pi/L_y$.

## What the topology does to the sound
- **Mobius**: the anti-periodicity $\phi(x+L_x,y+L_y)=-\phi(x,y)$ forces $m+n$ odd, so every other diagonal of the frequency lattice is missing - the same frequency scale as the Dirichlet rectangle but a sparser, atypical resonance set, with fewer peaks and more inharmonic beating.
- **Klein bottle**: the factor 4 on $m^2$ halves the $x$-wavenumber spacing, so the lowest $x$-only mode sits at $c/L_x$ instead of $c/(2L_x)$. That pushes the $x$-ladder up and breaks the symmetry between dimensions: for $L_x \ne L_y$ the lattice has no rational substructure and the spectrum is inherently inharmonic. The $x$-parity is coupled to $n$ (cosine-like for even $n$, sine-like for odd).
- **$\mathbb{RP}^2$**: **co-spectral with the Neumann rectangle** - identical frequency formula and index set - yet audibly distinguishable, because the $\pi(m+n)/2$ phase offsets in both cosines make modes neither purely even nor purely odd and couple $m$ with $n$ in a way no rectangle can.
- **Torus**: densest spectrum of the six; no parity constraint, so the whole lattice $\mathbb{Z}^2$ is allowed, and its spectrum contains the rectangle's (even $m,n$) as a subset.
- Modes with $m=0$ or $n=0$ are invariant to one dimension; as $L_x/L_y$ departs from unity they pull away from the rest and amplify inharmonic beating. The Dirichlet rectangle has none ($\sin 0 = 0$) and tends to a harmonic 1D-string spectrum at extreme aspect ratios.

## FDTD verification
Explicit five-point-stencil scheme on the fundamental domain, $h=0.01$ m,
$cT = h/\sqrt{2}$ (so $T\approx20.6\,\mu$s, $f_s/2 = 24.3$ kHz at $c=343$ m/s),
Gaussian initial condition, boundaries enforced by ghost cells - mirrored with or
without sign flip for Dirichlet/Neumann, rolled across the boundary with or without
orientation flip for the periodic cases. Because the field is real, a receiver sees
the real Green's function, i.e. the degenerate-subspace sum
$\tilde\phi_{mn}(r_r,r_s)=\big[\sum_k(\phi_k(r_s)\phi_k(r_r))^2\big]^{1/2}$, which is what
gets compared to the analytic amplitudes. Over $L_x=3.0$ m, $L_y=2.0$ m and five
receiver positions up to 1 kHz: mean relative frequency error $\varepsilon_f = 0.02$-$0.03\%$
for all six topologies, with Modal Assurance Criterion 0.834 (torus) to 0.944
(Dirichlet, Mobius); the MAC spread is largely the 50 Hz main lobe of the Hann
window used to suppress spectral leakage.

## Use and limits
Audio is synthesised by adding Rayleigh damping (see [[damping-models]]) to these
modes, giving reverb on geometries with no physical counterpart (code and samples at
kleinreverb.github.io).
Limits: lossless-to-lightly-damped ideal surfaces, constant wave speed, 2D only -
the cavity analogue is not straightforward because non-orientability prevents a
consistent interior/exterior; the perceptual payoff of non-orientable topology is
argued from the mode lattice rather than tested by listening.

[^1]: [[entities/source-papers#paper-lee-klein-bottle-reverberation-2026]] - Lee & Rau, "Modal Structure of Plate Boundaries and Klein Bottle Reverberation," DAFx26.

---
title: Circular-Buffer Topology and Monodromy
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [delay-line, waveguide, wave-equation, reference, tutorial]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_35.pdf
  - raw/DAFx26_paper_35.txt
---

# Circular-Buffer Topology and Monodromy

Reading a delay loop as a **vector bundle over a discrete circle**, so that a sign flip in
the loop, the Mobius strip, mixed boundary conditions and chaotic oscillators in delay
lines all fall out of one construction.[^essl]

## Line bundles over a circular buffer
Draw a signal as samples over a discrete circle. Instead of assuming one shared Euclidean
plane, give each sample index its own **fiber** - a one-dimensional real vector space
holding all possible values there - and specify a linear **transition map** $t:\mathbb{R}\to\mathbb{R}$
between neighbouring fibers. Unitary maps leave exactly two real choices, $+1$ and $-1$.

- All transitions $+1$: the **trivial line bundle** - the ordinary circular buffer.
- One $-1$ transition: a non-trivial bundle - the **Mobius circular buffer**. The rim must
  be traversed twice before returning: the famous non-orientability.
- Topologically, $GL(1,\mathbb{R}) = \mathbb{R}\setminus\{0\}$ is homotopic to two points (orientation is
  separated) while $GL(1,\mathbb{C}) = \mathbb{C}\setminus\{0\}$ is homotopic to a circle - so complex data
  gives a **circle bundle** with a continuum of twists.

Previously unconnected instances: the Johnson (twisted) ring counter, Trautmann's
twisted-string waveguide, and the double-cover argument that mixed Dirichlet-Neumann
boundary conditions of the 1-D wave equation behave like a Mobius strip.

## $r$-circular shifts, monodromy, winding number

The shift is a matrix with $r$ in the wrap-around corner,
$$A = \begin{bmatrix}0&1&0&\cdots&0\\ 0&0&1&\cdots&0\\ \vdots&&\ddots&\ddots&\vdots\\ 0&0&\cdots&0&1\\ r&0&\cdots&0&0\end{bmatrix},
\qquad v_{t+1} = A v_t .$$
$r=1$ is the classic circulant shift $C$, $r=-1$ the skew-circulant (the Mobius shift $M$),
and any unimodular $r \in \mathbb{C}$ keeps $A$ unitary.

**Monodromy** is the effect of one full trip round the loop, $\mu = A^n$ for buffer length
$n$: $\mu_C = I$, $\mu_M = -I$, $\mu_A = rI$. The **winding number** $w$ is the least $k$ with
$\mu^k = I$: $w = 1$ for the classic buffer, $w = 2$ for Mobius ($\mu_M^2 = M^{2n} = I$), and
for $r = e^{i2\pi c/d}$, $w = d/\gcd(c,d)$. With real entries only the *parity* of sign
inversions matters - odd gives $-I$, even gives $I$.

## Spectral consequences
The DFT diagonalises circulant matrices, and the same holds for $r$-circulants. From
$\mu_A = rI$ the eigenvalues satisfy $\lambda^n = r$, so
$$\lambda(A)_k = r^{1/n}\,\omega_n^k, \qquad \omega_n = e^{2\pi i/n},$$
the factor $r^{1/n}$ being the **monodromy modulation** of the classic spectrum.

| $r$ | eigenvalues | fundamental | harmonics |
|---|---|---|---|
| $1$ | $e^{i2\pi k/n}$ | $2\pi/n$ (at $k=1$; $k=0$ is DC) | all |
| $-1$ | $e^{i2\pi(2k+1)/2n}$ | $\pi/n$ (at $k=0$) | odd only |
| $e^{i2\pi/m}$ | $e^{i2\pi(mk+1)/mn}$ | $2\pi/(mn)$ | $(mk+1)/m$ |

So the Mobius case loses the constant solution (the bundle is non-trivial), halves the
fundamental (the winding number doubled, i.e. the wavelength doubled), and leaves an
odd-harmonic series - exactly the behaviour of a capped organ pipe or a clarinet. All
frequencies are in fact shifted *up* by the modulation; adding $1/2$ to the harmonic
index gives $\tfrac12,\tfrac32,\dots$, which as ratios is the odd series. For a subharmonic
$r$, larger $m$ lowers the fundamental while barely moving the harmonics, so the series
looks increasingly sparse - $1, 8, 15, 22,\dots$ for $m = 7$.

## Variable monodromy and chaotic oscillators
Drop the requirement that the twist be the same on every lap. For one sample under
variable monodromy, a periodic orbit of length $w$ satisfies $\prod_{j=0}^{w-1}\mu_j = I$. This
is exactly the Berdahl-Sheffield-Pfalz-Marasco design that puts a chaotic map in a
circular buffer, using the full-loop value as the map's past value, $r_k = f(r_{k-n})$.
With the (topologically stable) sine circle map
$$x_k = x_{k-1} + \Omega + \frac{K}{2\pi}\sin(2\pi x_{k-1}) \bmod 1,$$
each iterate acts as a local monodromy. Berdahl et al. observed tones "centred around
$f_S/L$ or subharmonics thereof"; the refinement here is that the observed frequency
belongs to the periodic orbit's **winding number**, and the Mobius case $r = -1$ (period
doubling) should be expected even with real iterators. The winding number is robust: a
uniform orbit at $r = i$ and a non-uniform 4-periodic orbit from the sine circle map
have the *same* braid pattern.

## Braids for vector bundles
Attach a circular buffer to each dimension of a finite-dimensional bundle and monodromy
becomes matrix rather than scalar multiplication. Restricting to braid matrices makes
the twists drawable: identity and sign inversion are the two elementary moves, and they
also describe cross-connections between two buffers. Multiplication by $i$ composes to
$M = \left[\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right]$ - a 2-dimensional real bundle whose
squaring sign inversion is a Mobius twist, giving winding number 4. Left open:
extending this to multi-delay structures such as feedback delay networks.

## See also
- [[delay-line-techniques]] - the circular buffers this reinterprets
- [[waveguide-overview]] - mixed boundary conditions and the d'Alembert loop
- [[entities/source-papers#paper-essl-circular-buffer-monodromy-2026]] - catalog entry

[^essl]: G. Essl, "Winding Numbers and Monodromy of Vector Bundles over a Circular Buffer," DAFx26. See [[entities/source-papers#paper-essl-circular-buffer-monodromy-2026]].

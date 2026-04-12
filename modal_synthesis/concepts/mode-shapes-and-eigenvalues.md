---
title: Mode Shapes and Eigenvalues
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [eigenmode, modal, vibration, wave-equation, acoustics]
sources:
  - /w/pasp/modal.tex
---

# Mode Shapes and Eigenvalues

## Mathematical Foundation

A linear vibrating system satisfies:
$$M\ddot{x}(t) + C\dot{x}(t) + K x(t) = f(t)$$

where:
- $M$ = mass matrix (or scalar for lumped models)
- $C$ = damping matrix
- $K$ = stiffness matrix
- $f(t)$ = excitation force vector
- $x(t)$ = displacement vector

## Undamped Natural Frequencies
Drop damping: $M\ddot{x} + K x = 0$.
Seek solutions $x(t) = \phi\, e^{j\omega t}$:
$$K\phi \;=\; \omega^2 M\phi \qquad \text{(generalized eigenvalue problem)}$$

Solutions: $N$ pairs $(\omega_k^2,\, \phi_k)$
- $\omega_k = 2\pi f_k$ = $k$th natural frequency (rad/s)
- $\phi_k$ = $k$th mode shape (eigenvector)

## Mode Shape Properties
- Orthogonality: $\phi_i^T M \phi_j = 0$ for $i \ne j$
- Each $\phi_k$ describes the spatial deformation pattern at frequency $f_k$
- Normalized: $\phi_k^T M \phi_k = 1$ (mass normalization)

## Damped Modes
With proportional damping (Rayleigh damping): $C = \alpha M + \beta K$
- Modes remain real-valued (same shapes as undamped)
- Each mode $k$ gets decay rate $d_k = (\alpha + \beta\omega_k^2) / 2$
- $Q_k = \omega_k / (2 d_k)$

For general (non-proportional) damping: modes become complex-valued.
In practice, modal synthesis uses measured real decay rates per mode.

## Modal Superposition
Any response can be written as:
$$x(t) \;=\; \sum_k q_k(t)\, \phi_k$$

where $q_k(t)$ are modal coordinates satisfying decoupled 2nd-order ODEs:
$$\ddot{q}_k + 2 d_k \dot{q}_k + \omega_k^2 q_k \;=\; \phi_k^T f(t)$$

This decoupling is the key advantage — N independent SDOF oscillators.

## Continuous Systems
For continuous objects (plates, strings, membranes):
- PDE replaces matrix equation (e.g., wave equation, plate equation)
- Mode shapes are functions: phi_k(x,y) or phi_k(x,y,z)
- Frequencies and shapes depend on geometry and boundary conditions

Examples:
- Clamped circular plate: Bessel function mode shapes
- Rectangular membrane (drum): $\sin(m\pi x/L)\sin(n\pi y/W)$ patterns
- 1D string: $\phi_k(x) = \sin(k\pi x/L)$, $f_k = k f_1$ (harmonic series)

## Radiation and Pickup
Output pressure at microphone position $r_m$:
$$p(t) \;\sim\; \sum_k \phi_k(r_{\text{excite}})\, \phi_k(r_{\text{pickup}})\, q_k(t)$$

- $\phi_k(r_{\text{excite}})$ = mode shape at excitation point → determines input coupling
- $\phi_k(r_{\text{pickup}})$ = mode shape at pickup point → determines output coupling
- Changing pickup = changing a_k weights with no frequency change

## Related Concepts
- [[modal-synthesis-overview]] — top-level synthesis paradigm
- [[resonator-bank-implementation]] — DSP implementation of modal coordinates
- [[fem-bem-for-modal-synthesis]] — computing phi_k and omega_k numerically
- [[modal-analysis-measurement]] — measuring phi_k and omega_k experimentally

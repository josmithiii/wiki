---
title: FEM and BEM for Modal Synthesis
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [fem, bem, modal-synthesis, wave-equation, acoustics, vibration]
sources:
  - ~/wiki/modal_synthesis/raw/papers/DiffSound-2409.13486v1.pdf
---

# FEM and BEM for Modal Synthesis

## Overview
When you can't physically measure an object (doesn't exist yet, too small, too hot, etc.)
you can compute its modes numerically from its geometry and material properties.
Two main methods: Finite Element Method (FEM) and Boundary Element Method (BEM).

## Finite Element Method (FEM)

### What it does
Discretizes the interior volume of an object into small elements (tetrahedra, hexahedra).
Assembles mass matrix M and stiffness matrix K from element integrals.
Solves generalized eigenvalue problem: $K\phi = \omega^2 M \phi$.

### Inputs required
- Geometry: CAD file or mesh (STL, OBJ, etc.) → meshed into volumetric elements
- Material properties: Young's modulus $E$, Poisson's ratio $\nu$, density $\rho$
- Boundary conditions: free, clamped, pinned edges

### Typical outputs
- First few hundred mode shapes $\phi_k$ and frequencies $f_k$
- Adequate for synthesis up to ~5-10 kHz depending on mesh refinement

### Tools
- **Abaqus, ANSYS, NASTRAN**: commercial FEM packages
- **FEniCS, OpenFOAM**: open-source; FEniCS especially good for custom PDEs
- **COMSOL**: GUI-friendly, good for multiphysics (structural + acoustic)
- **Elmer**: open-source, good structural + acoustic coupling

### Mesh requirements
- Rule of thumb: at least 6 elements per wavelength at highest freq of interest
- For audio up to 10 kHz in steel ($c_L \approx 5000$ m/s): $\lambda_{\min} \approx 0.5$ mm
  → very fine mesh for large objects → millions of DOF

### Reduced-order models
Problem: full FEM has millions of DOF, but only ~100-500 modes needed for synthesis.
Solution: compute only first $N$ eigenpairs using iterative solvers (Arnoldi, Lanczos).
Cost: $O(N \cdot \text{DOF})$ not $O(\text{DOF}^3)$.

## Boundary Element Method (BEM)

### What it does
Discretizes only the surface of the object (2D boundary, not 3D volume).
Solves an integral equation for the acoustic pressure on the surface.
Coupled with FEM structure, it computes sound radiation from vibrating surfaces.

### Advantage over FEM
- Far-field acoustic radiation handled naturally (no artificial boundary)
- Fewer DOF than volumetric FEM for exterior acoustic problems
- Naturally computes transfer functions: force at point A → pressure at point B

### Acoustic BEM Transfer Function
Given surface velocity distribution $v_n(r)$ on object surface:
$$p(r_{\text{obs}}) \;=\; \mathcal{B}\, v_n$$

For modal synthesis, precompute "acoustic transfer vectors" (ATVs):
$$p_k(r_{\text{obs}}) \;=\; \mathcal{B}\, \phi_k(\text{surface})$$

Then: $p(r_{\text{obs}}, t) = \sum_k p_k(r_{\text{obs}})\, q_k(t)$
This is the "Precomputed Acoustic Transfer" approach (James & Pai 2002).

### Tools
- **FastBEM**: commercial, multipole-accelerated
- **BEM++**: open-source Python/C++ BEM library
- **Bempp-cl**: modern GPU-accelerated BEM

### Fast Multipole Method (FMM)
Reduces BEM cost from $O(N^2)$ to $O(N \log N)$:
- Groups far-field interactions hierarchically
- Essential for large surfaces (>10k boundary elements)

## Combined FEM-BEM Workflow
1. Build CAD model of object
2. Mesh: volumetric (FEM) + surface (BEM)
3. FEM: compute structural mode shapes $\phi_k$, frequencies $f_k$
4. BEM: compute acoustic transfer vectors $p_k(r_{\text{mic}})$
5. Damping: assign $d_k$ from material loss factor $\eta_k$ (or measure one sample)
6. Export: $\{f_k, d_k, p_k\}$ → resonator bank
7. Synthesize: $\sum_k p_k\, e^{-d_k t}\, \sin(2\pi f_k t)$

## Related Concepts
- [[mode-shapes-and-eigenvalues]] — the mathematical objects FEM/BEM compute
- [[modal-synthesis-overview]] — how these modes feed into synthesis
- [[modal-analysis-measurement]] — experimental alternative to FEM/BEM
- [[rigid-body-sound-synthesis]] — runtime pipeline using precomputed FEM/BEM data

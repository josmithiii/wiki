---
title: Modal Synthesis Overview
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [modal-synthesis, physical-modeling, resonator, acoustics, vibration]
sources:
  - /w/pasp/modal.tex
  - https://ccrma.stanford.edu/~jos/pasp/Modal_Expansion.html
---

# Modal Synthesis Overview

## What It Is
Modal synthesis generates sound by summing the responses of N resonant modes,
each representing a natural frequency of a vibrating object.
Unlike waveguide synthesis (which models wave propagation), modal synthesis
works in the eigenmode domain — each mode is a damped sinusoidal oscillator.

## Core Idea
Any linear, time-invariant vibrating system can be decomposed into modes.
Each mode k has three parameters:
- f_k — natural frequency (Hz)
- a_k — amplitude weight (depends on excitation/pick-up position)
- d_k — decay rate (damping, in dB/s or as Q-factor)

Sound output = sum over k of: a_k * exp(-d_k * t) * sin(2*pi*f_k * t)

This is exact for linear systems; works well for mildly nonlinear ones.

## Why It Matters
- Compact parameterization: a few hundred modes capture most audible content
- Modes can be measured (from real objects via impact hammer + microphone)
  or computed (via FEM/BEM from geometry + material data)
- Easy real-time synthesis: each mode = one biquad IIR filter or resonator
- Physically meaningful parameters: changing f_k tunes the pitch;
  changing a_k moves the mic/pickup; changing d_k changes material damping

## Historical Roots
- Introduced to computer music by Jean-Marie Adrien (IRCAM, 1991)
- Independently developed in mechanical engineering for structural analysis
- Related to Risset's additive synthesis but with physically motivated parameters
- Cook (1995, 2002) expanded to impact models and perceptual work
- Rath & Rocchesso (2005) demonstrated efficient CPU-based real-time contact sound
- James, Barbic & Pai (2006) showed real-time GPU modal synthesis using OpenGL fragment shaders

## Basic Signal Flow
1. Excitation signal e(t) — impulse, friction force, or arbitrary input
2. Each mode: H_k(z) = biquad bandpass filter centered at f_k with Q = f_k / (2*d_k)
3. Output = sum of all mode filter outputs

## Modes: Measured vs. Computed
- Measured: strike object, record IR, fit sinusoidal model (ESPRIT, MPS, etc.)
  Fast but limited to objects you can physically measure.
- Computed: FEM/BEM from CAD model + material parameters
  Flexible but computationally expensive to solve.
- Hybrid: compute modes, scale by measured damping constants

## Key Limitations
- Linearity assumption breaks for large deflections or contacts
- Mode count grows with frequency; above ~5 kHz often need statistical methods
- Nonlinear excitation (friction, bowing) requires feedback loops
- Moving contact point changes a_k in real time (computationally cheap)

## Related Concepts
- [[mode-shapes-and-eigenvalues]] — mathematical foundation
- [[resonator-bank-implementation]] — DSP realization
- [[impact-synthesis]] — most common excitation model
- [[friction-synthesis]] — bowing and scraping
- [[modal-analysis-measurement]] — how to measure modes from real objects
- [[fem-bem-for-modal-synthesis]] — numerical computation of modes
- [[waveguide-vs-modal]] — comparison with waveguide synthesis

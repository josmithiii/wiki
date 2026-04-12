---
title: Commuted Synthesis
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [commuted, waveguide, string, guitar, dsp, physical-modeling]
sources:
  - /w/pasp/plucked.tex
  - /w/pasp/acoustic-guitars.tex
  - /l/wgr/Sections/Foundations.tex
---

# Commuted Synthesis

Commuted synthesis exploits LTI commutativity to dramatically simplify
waveguide instrument models. Instead of running a complex body resonator
in real time, its impulse response is precomputed and folded into the
excitation signal.

## Principle

For a plucked-string instrument, the output is:
$$y[n] \;=\; e[n] * h[n] * b[n]$$
where $e[n]$ = excitation (pluck), $h[n]$ = string response, $b[n]$ = body response.

Since convolution is commutative, reorder to:
$$y[n] \;=\; [e[n] * b[n]] * h[n]$$

The term e[n] * b[n] is the "pluck response" — precompute and store it.
At runtime, only the string delay loop h[n] runs, excited by a table lookup
of the stored pluck response.

## Computational Savings

A guitar body has hundreds of resonances in the audio range.
Without commuting: must run a high-order parallel filter bank in real time.
With commuting: store one short wavetable per pluck style; run one FDL.

This transforms a difficult real-time problem into a trivial one:
- Wavetable playback (one sample read per output sample)
- Through a filtered delay loop (one FIR/IIR evaluation per sample)

## Implementation

1. Record or simulate the impulse response of body + string combined
2. Separate into: pluck response e[n]*b[n] and string loop filter G(z)
3. Inverse-filter the string to obtain body contribution:
   $y[n] * h^{-1}[n] = e[n] * b[n]$
4. Store the pluck response; vary excitation details via small filter
5. Body filter can be shared across multiple strings (same body)

## Applications

- **Guitar**: Karjalainen & Smith (1996), Välimäki et al. — plucked strings
- **Piano**: Smith (1995), Van Duyne (1995) — soundboard response commuted
- **Harp, harpsichord, mandolin, kantele, banjo**: all commutable
- **Bowed strings**: approximate as periodically plucked (Smith 1993, Jaffe 1995)

## Limitations

- Pickup/excitation position must be fixed (or a small set of precomputed IRs)
- Cannot change body resonances dynamically (e.g., hand on soundboard)
- Nonlinear interactions (string-body coupling) are approximated
- For interactive position changes, need separate body filter model

## Relation to Karplus-Strong

KSA can be derived as a commuted waveguide model:
- The delay loop = simplified waveguide string
- The initial wavetable contents = commuted pluck response
- The averaging filter = commuted loss + body coloring
- This interpretation explains why KSA sounds so good despite its simplicity

## Related Concepts
- [[string-modeling]] — the FDL being excited
- [[waveguide-overview]] — the LTI delay-line framework enabling commutation
- [[delay-line-techniques]] — loop filter design for the string model

## References
[^1]: Smith, J.O. (1993). "Efficient Synthesis of Stringed Musical Instruments." ICMC.
[^2]: Karjalainen, M., Välimäki, V. & Jánosy, Z. (1993). "Towards High-Quality Sound Synthesis of the Guitar and String Instruments." ICMC.
[^3]: Smith, J.O. III. "Physical Audio Signal Processing," CCRMA/Stanford.

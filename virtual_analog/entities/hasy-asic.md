---
title: HASY ASIC
created: 2026-09-10
updated: 2026-09-10
type: entity
tags: [asic, oscillator-sync, additive, real-time, oscillator]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_49.pdf
  - raw/DAFx26_paper_49.txt
---

# HASY ASIC

HASY ("hard sync") is a 65 nm CMOS chip from ETH Zurich that computes the
spectral-resampling transform of [[alias-free-oscillator-sync]] and resynthesizes the
result additively, in real time.[^1]

## Implementation

| | HASY | BFO (2023 additive ASIC) |
|---|---|---|
| Oscillator sync | yes (3 modes) | no |
| Voices x oscillators | 1 x 1 | 2 x 4 |
| Harmonics per oscillator | 512 | 1024 |
| Max clock | 250 MHz | 154 MHz |
| Area | 6 mm$^2$ (65 nm TSMC LP CMOS) | 3 mm$^2$ |
| Power | 242 mW at 200 MHz | 178 mW |

- Fixed point, about 24 bit; $f_\text{clk} = 2048 f_s \approx 196.6$ MHz for
  $f_s = 96$ kHz, 24-bit I2S output.
- Spectral-resampling engine: coefficient memory, a pre-processor doing the rotation
  and the trigonometric terms on a time-shared **CORDIC**, **32 parallel column
  processors** with hand-built dividers (zeroth/first-order Taylor fallback for
  denominators below $2^{-12}$), and an accumulation memory.
- 8240 clock cycles per transform regardless of sync mode, about 42 us - just over
  four sample periods, so a new transform every **five** audio samples (a ~19.2 kHz
  parameter update rate). Additive synthesis uses about one quarter of the 2048
  cycles per sample.
- 97 % of the cell area is the resampling engine; the additive oscillator is under 3 %.
- Accuracy: SINAD above 41 dB versus floating-point and analytical references when
  $f_\text{follow} > f_\text{lead}$. Integer $P$ is near-exact (the transform reduces
  to remapping harmonic $n$ to $nP$); $P < 1$ degrades because the synced coefficients
  then depend on high-index coefficients of the following oscillator that a fixed
  $N = 512$ does not have.

**Limitations:** the fabricated chip has control-logic bugs affecting part of the
configuration interface; a fully functional reimplementation and a polyphonic version
are in progress, along with a Eurorack module. Fabricated through a multi-project
wafer service - 100 chips, 10 packaged, about EUR 24,000 over five months.

## See also

[[alias-free-oscillator-sync]] - [[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-roth-alias-free-oscillator-sync-2026]] - Roth, Keller, Castaneda, Studer, "Alias-Free Oscillator Synchronization via Additive Synthesis", DAFx26.

---
title: Pending Sources — Wishlist
created: 2026-04-17
updated: 2026-04-17
type: summary
tags: [reference, anc]
sources: []
---

# Pending Sources — Wishlist

References we still want to track down. Paywalled journal articles,
books, and standards require a Stanford library proxy; NASA NTRS items
needed a browser (the NTRS endpoint kept returning 504 Gateway Timeout
to `curl`). Contributions welcome.

### How to contribute a PDF

**Anyone:** drop the PDF into the staging directory:

```bash
mkdir -p ~/wiki/active_absorbers/incoming-pdfs
cp YourFile.pdf ~/wiki/active_absorbers/incoming-pdfs/
```

Then ping JOS (or open a PR updating `incoming-pdfs/README.md` with the
filename, source URL, and the target scaffold page). An agent will pick
it up, move it to `/l/dttd/`, extract text, distill into
`raw/SUMMARIES.md` and `entities/source-papers.md`, and promote the
relevant concept page.

**JOS (host-side direct ingestion):**

```bash
mv YourFile.pdf /l/dttd/
ln -sf ../YourFile.pdf /l/dttd/ANC-Stuff/YourFile.pdf
cd ~/wiki/active_absorbers/raw && pdf2txt.py /l/dttd/ANC-Stuff/YourFile.pdf > YourFile.txt
```

## NASA NTRS (fetch via browser)

NTRS `curl` kept timing out — browser download is the reliable path.

- Brooks, Pope & Marcolini, *Airfoil Self-Noise and Prediction*, NASA RP-1218, 1989 — <https://ntrs.nasa.gov/citations/19890016302>
- Sutliff, Nallasamy, Heidelberg et al., *Active Noise Control of Low Speed Fan Rotor-Stator Modes*, NASA TM-107458, 1997 — <https://ntrs.nasa.gov/citations/19970017613>
- Sutliff, *A 20-Year Retrospective of the Advanced Noise Control Fan*, NASA 2019 — <https://ntrs.nasa.gov/citations/20190030361>

All three required to promote [[rooftop-fan-contenders]] from scaffold.

## For [[tonal-periodic-anc]]

- Kuo & Morgan 1996, *Active Noise Control Systems*, Wiley — ch. 5 narrowband
- Elliott 2001, *Signal Processing for Active Control*, Academic — RC/ILC chapter
- Swinbanks, *JSV* 27(3):411–436, 1973 — earliest sync-ref periodic ANC
- Chaplin & Smith, *Engineering* 223:672, 1983 — Essex waveform synthesis
- Bodson, Sacks & Khosla, *IEEE TAC* 39(9):1939, 1994 — harmonic adaptive IMP
- Hara, Yamamoto, Omata & Nakano, *IEEE TAC* 33(7):659, 1988 — foundational RC
- Ostashev & Wilson, *Acoustics in Moving Inhomogeneous Media*, 2nd ed. 2015 — outdoor-propagation FM/AM theory for the §8 robustness discussion

## For [[hybrid-active-passive]]

- Olson & May, *JASA* 25(6):1130, 1953 — electronic sound absorber
- Guicking & Karcher, *ASME JVA* 106:393, 1984 — active impedance control
- Guicking & Lorenz, *JVA* 106:389, 1984 — porous-plate active absorber
- Furstoss, Thenail & Galland, *JSV* 203(2):219, 1997 — surface impedance control
- Beyene & Burdisso, *JASA* 101(3):1512, 1997 — hybrid passive/active absorber
- Fang et al., *Nature Materials* 5:452, 2006 — negative-modulus metamaterial
- Ma, Yang, Xiao, Yang & Sheng, *Nature Materials* 13:873, 2014 — hybrid-resonance metasurface
- Ghaffarivardavagh et al., *Phys. Rev. B* 99:024302, 2019 — final ultra-open silencer (arXiv preprint is already ingested; fetch only for the published version)

## For [[psychoacoustic-anc]]

- Zwicker & Fastl, *Psychoacoustics: Facts and Models*, 3rd ed. 2007, Springer
- Aures, *Acustica* 59:130, 1985 — sensory pleasantness
- Kuo & Tsai / Kuo & Yang 1996 — broadband adaptive noise equalizer
- Rees & Elliott, Inter-Noise / *JSV* 2004 — active sound profiling
- Zhou & DeBrunner, *IEEE TSP* 55(5):1719, 2007 — perceptual ANC sequence
- Standards: ISO 1996-2:2017 (tonality $K_T$), DIN 45681:2005, ISO 532-1:2017 (Zwicker loudness), ANSI S12.9 Part 3
- Bao & Panahi, IEEE EMBS 2009 — A-weighted psychoacoustic ANC (ResearchGate often easier than proxy)

## For [[rooftop-fan-contenders]]

- Beranek & Vér (eds.), *Noise and Vibration Control Engineering*, 2nd ed., Wiley
- Hansen, Snyder, Qiu, Brooks & Moreau, *Active Control of Noise and Vibration*, 2nd ed., CRC 2012
- Tyler & Sofrin, *SAE Trans.* 70:309, 1962 — rotor-stator tone cutoff
- Neise, *JSV* 45(3):375, 1976 — centrifugal fan noise literature survey
- Neise & Koopmann, *JSV* 73(2):297, 1980 — fan-noise reduction by resonators
- Howe, *J. Fluids Struct.* 5:33, 1991 — serrated trailing edge theory

## For [[fxlms-algorithm]] and [[deep-rl-anc]]

- **Morgan 1980** (IEEE TASSP) — earliest known FxLMS filtered-x analysis; referenced by [[fxlms-algorithm]]
- **Burgess 1981** (JASA) — earliest known full adaptive duct-ANC simulation; referenced by [[fxlms-algorithm]]
- **Ryu, Lim, Lee 2024** (IJAT Springer) — DDPG for narrowband ANC without path model; would fill the continuous-drive DRL gap on [[deep-rl-anc]]

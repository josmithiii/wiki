# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-04-11] create | Wiki initialized
- Domain: Digital waveguide synthesis
- Structure created: SCHEMA.md, index.md, log.md
- Directories: raw/{articles,papers,assets}, entities/, concepts/, comparisons/, queries/

## [2026-04-11] ingest | PASP LaTeX chapters (first pass)
- delay-waveguide.tex, strings.tex, plucked.tex, damping.tex, stiffstring.tex
- struckstring.tex, coupling.tex, piano-string.tex, guitar-bridge.tex
- reeds.tex, reedboremech.tex, brasses.tex, flute.tex, cones.tex
- idealtubesummary.tex, woodwinds.tex, acoustic-guitars.tex, electric-guitars.tex
- delay-interp.tex, delay-var.tex, delay-lossy-prop.tex, delay-allpass-waveguide.tex
- adaptors.tex, mesh.tex, reverb*.tex (problem, fdn, sdn, jcrev, freeverb, early)

## [2026-04-11] fix | 7 PASP typos/errors
- brasses.tex:94 — duplicate "and and" → "and"
- damping.tex:117 — "miminizer" → "minimizer"
- reverb-freeverb.tex:1 — \kdefq{JCRev} → \kdefq{Freeverb}
- delay-var.tex:25 — missing "in" before \chref{simplestrings}
- reverb-fdn.tex:113 — stray period after \right] in Hadamard matrix display
- piano-string.tex:71 — "damping due R_2" → "damping due to R_2"
- piano-string.tex:119-125 — fixed inharmonicity formula B: SI² → I; /16 → /4; clarified I = second moment of area

## [2026-04-11] create | concepts/waveguide-overview.md
## [2026-04-11] create | concepts/scattering-junctions.md
## [2026-04-11] create | concepts/delay-line-techniques.md
## [2026-04-11] create | concepts/string-modeling.md
## [2026-04-11] create | concepts/bore-modeling.md
## [2026-04-11] create | concepts/reed-and-bow-models.md
## [2026-04-11] create | concepts/artificial-reverberation.md
## [2026-04-11] create | concepts/waveguide-meshes.md
## [2026-04-11] update | index.md — 8 pages

## [2026-04-11] ingest | JAES review "Four Decades of Digital Waveguides"
- /l/wgr/Sections/HistoricalBackground.tex — K-S, DWG origins, WDF relation
- /l/wgr/Sections/Foundations.tex — traveling waves, scattering, strings, tubes, mesh
- /l/wgr/Sections/Advancements/InstrumentModelling.tex — winds, strings, brasses, percussion, STK
- /l/wgr/Sections/Advancements/SpeechProcessing.tex — K-L, SPASM, 2D/3D mesh vocal tract
- /l/wgr/Sections/Advancements/ArtificialReverberation.tex — SDN, waveguide web
- /l/wgr/Sections/Parameter Optimization/ParameterOptimisation.tex — all optimization methods

## [2026-04-11] fix | 1 JAES review typo
- ArtificialReverberation.tex:18 — "junction,but" → "junction, but"

## [2026-04-11] create | concepts/commuted-synthesis.md
## [2026-04-11] create | concepts/banded-waveguides.md
## [2026-04-11] create | concepts/waveguide-vocal-models.md
## [2026-04-11] create | concepts/waveguide-parameter-optimization.md
## [2026-04-11] create | concepts/waveguide-history.md
## [2026-04-11] update | index.md — 13 pages

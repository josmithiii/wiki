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

## [2026-04-11] ingest | WDF sources
- /l/l420/WaveDigitalFiltersIntro/wdfi-content.tex — MUS420 WDF intro lecture
- /l/l420/WaveDigitalFilters/WDFIntro.tex — MUS420 WDF full lecture
- /w/pasp/adaptors.tex — PASP adaptor derivations
- /l/dttd/WDF/ — Werner, Yeh, Olsen, Bernardini papers
- /l/dttd/SMC_2022_Diff_WDFs.pdf, PyWDF-DAFx23.pdf, WDF-NeuralK-*.pdf

## [2026-04-11] create | concepts/wave-digital-filters.md
- Modularity problem, wave variables, delay-free loop elimination, comparison table
## [2026-04-11] create | concepts/wdf-adaptors.md
- Parallel/series 2-port, N-port, one-multiply form, dependent port
## [2026-04-11] create | concepts/wdf-elements.md
- Mass/spring/dashpot reflectances, transformer, gyrator, nonlinear, K-method
## [2026-04-11] create | concepts/wdf-applications.md
- Piano hammer, tonehole, analog circuits, differentiable/neural WDFs
## [2026-04-11] update | index.md — 17 pages

## [2026-04-15] ingest | Giampiccolo et al. JAES 2025 — VIOLA framework
- Source: /l/dttd/Automatic_Generation_of_Virtual_Analog_Audio_Plug_ins_based_on_WDFs_RG.pdf
- Saved raw text to raw/papers/automatic-generation-va-plugins-wdf.txt
- Created concepts/viola-wdf-plugin-generator.md — SPICE→WDF→VST pipeline, arbitrary port adaptation, SIM+DSR, Big Muff Pi & OD-250 results
- Updated concepts/wdf-applications.md — added VIOLA section + wikilink
## [2026-04-15] update | index.md — 18 pages

## [2026-04-15] create | concepts/wdf-arbitrary-port-adaptation.md
- Detailed explanation of the gap (symbolic S_nn=0) and new MNA-based formula
- Worked delta-network example showing both old and new methods
- Linked from viola-wdf-plugin-generator.md
## [2026-04-15] update | index.md — 19 pages

## [2026-04-15] ingest | Werner et al. DAFx-15 — Multiple/multiport nonlinearities
- Source: /l/dttd/WDF/RESOLVING_WAVE_DIGITAL_FILTERS_WITH_MULTIPLE_MULTIPORT_NONLINEARITIES.pdf
- Saved raw text to raw/papers/resolving-wdf-multiple-multiport-nonlinearities.txt
- Created concepts/wdf-multiple-nonlinearities.md — SPQR tree, R-type root, K-method, NLSS consolidation, Big Muff Pi case study
- Updated concepts/wdf-applications.md — linked Multiple Nonlinearities section
## [2026-04-15] update | index.md — 20 pages

## [2026-04-15] ingest | Werner, Smith & Abel DAFx-15 — R-type adaptors for arbitrary topologies
- Source: /l/va/WDF/WernerEtAlLinearDAFx15.pdf
- Saved raw text to raw/papers/werner-wdf-adaptors-arbitrary-topologies-dafx15.txt
- Created concepts/wdf-r-type-adaptors.md — MNA-derived scattering, ring resolution, Bassman & Tube Screamer case studies
## [2026-04-15] update | index.md — 21 pages

## [2026-04-15] ingest | Werner dissertation (Stanford, 2016)
- Source: /Users/jos/Documents/Students/KurtWerner/KurtJamesWernerDissertation-augmented.pdf
- Saved raw text to raw/papers/werner-dissertation-2016.txt (38k lines)
- No new concept page — content enriches existing pages
- Updated wave-digital-filters.md: Forward Euler structurally non-realizable (not just unstable); WDF vs state-space cost comparison
- Updated wdf-r-type-adaptors.md, wdf-multiple-nonlinearities.md, wdf-elements.md: added dissertation as source with chapter pointers

## [2026-09-08] ingest | DAFx26 proceedings - pass 1 (catalog only)
- Source: /l/dttd/DAFx26/ (29th Int. Conf. on Digital Audio Effects, Cambridge MA, 1-4 Sept 2026), annotated bibliography at /l/dttd/DAFx26/README_JOS.md
- Copied 14 pdftotext extractions into raw/ (gitignored) and created raw/MANIFEST.md (with a section for the pre-existing WDF extractions) and raw/SUMMARIES.md.
- Created entities/source-papers.md with 14 catalog entries:
  paper_38 (Tablas de Paula et al., differentiable Karplus-Strong), paper_39 (Camara et al., differentiable Kelly-Lochbaum sygyt),
  paper_36 (Smyth, loopback FM via time-varying delay line), paper_43 (Zheng, Darabundit, Scavone, Chinese yehu),
  paper_23 (Chowdhury & Rau, performance-oriented WDF codegen), paper_24 (Giampiccolo et al., Fulltone OCD CPWL WDF),
  paper_25 (Giampiccolo et al., KANs vs MLPs in WDFs), paper_04 (Coppola, fast parametric lossless FDN matrices),
  paper_05 (Dal Santo et al., nonlinear shimmer FDNs), paper_10 (Ibnyahya & Reiss, differentiable FDN RIR fitting),
  demo_68 (St-Onge & Scavone, sfFDN / FDN Sandbox), demo_61 (Franchino & Schlecht, ADAC to FAUST),
  paper_01 (Abate & Hansen, concatenation-driven convolution), demo_71 (Valentin et al., IRIS).
- Updated concepts/artificial-reverberation.md, string-modeling.md, delay-line-techniques.md, wdf-applications.md and waveguide-parameter-optimization.md with a DAFx26 see-also pointer plus a sources: entry (these pages are at or over the 100-line limit, so the bullets stay in the source-papers entries per SCHEMA).
- Updated concepts/waveguide-vocal-models.md with a full "DAFx26 additions" bullet list (page had headroom).
- Updated index.md: Entities section now lists the source-paper catalog and 14 anchors; 22 pages.
- The virtual analog context for paper_23/24/25 is catalogued in the new sibling wiki virtual_analog/.
- Pass 2 (deep distillation of the three-star papers into concept pages) is pending.

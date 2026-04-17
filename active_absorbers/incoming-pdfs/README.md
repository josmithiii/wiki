# incoming-pdfs — staging directory

> Free-to-download PDFs staged for ingestion into
> `/l/dttd/ANC-Stuff/`. PDFs themselves are **not** committed; this
> README is committed so provenance survives in git history after
> the staging directory is deleted.

Move/symlink recipe (run on host, with `/l/dttd/` write access):

```bash
cd ~/wiki/active_absorbers/incoming-pdfs
for f in *.pdf; do
  mv "$f" /l/dttd/"$f"
  ln -sf ../"$f" /l/dttd/ANC-Stuff/"$f"
done
# then extract:
cd /Users/jos/wiki/active_absorbers/raw
for f in /l/dttd/ANC-Stuff/*.pdf; do
  t=$(basename "$f" .pdf).txt
  [ -e "$t" ] || pdf2txt.py "$f" > "$t"
done
```

After the files are moved and extracted, I (Claude) will:
1. Append new rows to `raw/MANIFEST.md`.
2. Dense per-paper distillation in `raw/SUMMARIES.md`.
3. Promote the relevant scaffold concept pages
   (`tonal-periodic-anc`, `hybrid-active-passive`,
   `psychoacoustic-anc`, `rooftop-fan-contenders`) using these
   sources, removing their `sources: []` markers.
4. Add `paper-<slug>` entries to `entities/source-papers.md`.
5. Log the action in `log.md`.
6. Delete this staging directory.

## Staged files (2026-04-17) — free-to-download batch

### → tonal-periodic-anc

| File | Source URL | Provenance |
| --- | --- | --- |
| `Kuo-Tsai-FxLMS-QuickReview-APSIPA2011.pdf` | http://www.apsipa.org/proceedings_2011/pdf/apsipa260.pdf | APSIPA 2011 open proceedings — concise FxLMS / FxLMS-SF / narrowband survey |
| `Elliott-Nelson-ANC-IEEE-SPM-1993.pdf` | https://resource.isvr.soton.ac.uk/staff/pubs/Ref%203%20IEEE%20review%201993.pdf | ISVR author-hosted — foundational IEEE SPM ANC tutorial with explicit periodic/tonal treatment |

### → hybrid-active-passive

| File | Source URL | Provenance |
| --- | --- | --- |
| `Galland-HybridPassiveActive-FlowDuct-AppAcoust2005.pdf` | https://acoustique.ec-lyon.fr/publi/galland_applacoust05.pdf | ECL Lyon author-hosted — hybrid passive/active flow-duct absorber (successor to Furstoss 1997) |
| `Betgen-Galland-HybridLiner-AppAcoust2012.pdf` | https://acoustique.ec-lyon.fr/publi/betgen_applacoust12.pdf | ECL Lyon author-hosted — microperforated-panel hybrid liner, non-intrusive characterization |
| `Guicking-ActiveControl-Patents-Overview.pdf` | https://www.guicking.de/dieter/Ov-oK16.pdf | Guicking personal page — patents overview covering active-impedance-control lineage |
| `Mei-DarkAcousticMetamaterial-NatComm2012.pdf` | https://www.nature.com/articles/ncomms1758.pdf | *Nature Communications* open access — membrane locally-resonant metamaterial for LF absorption |
| `Ghaffarivardavagh-VentilatedMetamaterial-arxiv1801.03613.pdf` | https://arxiv.org/pdf/1801.03613 | arXiv preprint — Fano-like ventilated sub-wavelength silencer (precursor to 2019 *Phys. Rev. B*) |

### → psychoacoustic-anc

| File | Source URL | Provenance |
| --- | --- | --- |
| `Rivera-Zoelzer-PsychoacousticHybridANC-ICSV25-2018.pdf` | https://www.hsu-hh.de/ant/wp-content/uploads/sites/699/2018/08/ICSV25_full_paper_Rivera_Papantoni_Zoelzer.pdf | HSU Hamburg author-hosted — Zwicker-loudness-weighted hybrid ANC |

### → rooftop-fan-contenders

*(No NASA NTRS files staged — the NTRS download endpoint returned
504 Gateway Timeout on all three attempts. JOS to fetch by browser;
see "Still pending" section below.)*

## Still pending — grab via Stanford proxy

The following canonical references are paywalled or book-form and
were **not** downloaded. JOS will fetch via Stanford library proxy.
The scaffold pages reference these in their "Pending sources"
blocks.

### tonal-periodic-anc

- Kuo & Morgan 1996, *Active Noise Control Systems*, Wiley — ch. 5 narrowband.
- Elliott 2001, *Signal Processing for Active Control*, Academic — RC/ILC chapter.
- Swinbanks, *JSV* 27(3):411–436, 1973 — earliest sync-ref periodic ANC.
- Chaplin & Smith, *Engineering* 223:672, 1983 — Essex waveform synthesis.
- Bodson, Sacks & Khosla, *IEEE TAC* 39(9):1939, 1994 — harmonic adaptive IMP.
- Hara, Yamamoto, Omata & Nakano, *IEEE TAC* 33(7):659, 1988 — foundational RC.
- Ostashev & Wilson, *Acoustics in Moving Inhomogeneous Media*, 2nd ed. 2015 — outdoor-propagation FM/AM theory for §8 robustness.

### hybrid-active-passive

- Olson & May, *JASA* 25(6):1130, 1953 — electronic sound absorber.
- Guicking & Karcher, *ASME J. Vib. Acoust.* 106:393, 1984 — active impedance control.
- Guicking & Lorenz, *J. Vib. Acoust. Stress Rel. Des.* 106:389, 1984 — porous-plate active absorber.
- Furstoss, Thenail & Galland, *JSV* 203(2):219, 1997 — surface impedance control.
- Beyene & Burdisso, *JASA* 101(3):1512, 1997 — hybrid passive/active absorber.
- Fang et al., *Nature Materials* 5:452, 2006 — negative-modulus acoustic metamaterial.
- Ma, Yang, Xiao, Yang & Sheng, *Nature Materials* 13:873, 2014 — hybrid-resonance metasurface.
- Ma & Sheng, *Science Advances* 2:e1501595, 2016 — acoustic metamaterials review (likely open; worth checking).
- Ghaffarivardavagh et al., *Phys. Rev. B* 99:024302, 2019 — final ultra-open silencer (preprint is staged above).

### psychoacoustic-anc

- Zwicker & Fastl, *Psychoacoustics: Facts and Models*, 3rd ed. 2007, Springer.
- Aures, *Acustica* 59:130, 1985 — sensory pleasantness.
- Kuo & Tsai, *IEEE SPL* / Kuo & Yang 1996 — broadband adaptive noise equalizer.
- Rees & Elliott, Inter-Noise / JSV 2004 — active sound profiling.
- Zhou & DeBrunner, *IEEE TSP* 55(5):1719, 2007 — perceptual ANC sequence.
- ISO 1996-2:2017 (tonality $K_T$), DIN 45681:2005, ISO 532-1:2017 (Zwicker loudness), ANSI S12.9 Part 3 — standards.
- Bao & Panahi, IEEE EMBS 2009 — A-weighted psychoacoustic ANC (ResearchGate; retrieval via proxy easier).

### rooftop-fan-contenders

- Beranek & Vér (eds.), *Noise and Vibration Control Engineering*, 2nd ed., Wiley.
- Hansen, Snyder, Qiu, Brooks & Moreau, *Active Control of Noise and Vibration*, 2nd ed., CRC 2012.
- Tyler & Sofrin, *SAE Trans.* 70:309, 1962 — rotor-stator tone cutoff.
- Neise, *JSV* 45(3):375, 1976 — centrifugal fan noise literature survey.
- Neise & Koopmann, *JSV* 73(2):297, 1980 — fan-noise reduction by resonators.
- Howe, *J. Fluids Struct.* 5:33, 1991 — serrated trailing edge theory.
- **NASA NTRS — curl got 504 Gateway Timeout; JOS to fetch by browser:**
  - Brooks, Pope & Marcolini, *Airfoil Self-Noise and Prediction*, NASA RP-1218, 1989 — https://ntrs.nasa.gov/citations/19890016302
  - Sutliff, Nallasamy, Heidelberg et al., *Active Noise Control of Low Speed Fan Rotor-Stator Modes*, NASA TM-107458 (1997) — https://ntrs.nasa.gov/citations/19970017613
  - Sutliff, *A 20-Year Retrospective of the Advanced Noise Control Fan*, NASA 2019 — https://ntrs.nasa.gov/citations/20190030361

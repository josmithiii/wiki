---
title: JOS Book Series Overview
created: 2026-11-25
updated: 2026-11-25
type: concept
tags: [book, overview, mdft, filters, pasp, sasp]
sources:
  - https://ccrma.stanford.edu/~jos/pubs.html
  - /w/filters/bookseries.tex
---

# JOS Book Series Overview

Julius O. Smith III's music signal processing series is four books, all
free online at CCRMA and in print from W3K Publishing.  In each, the main
chapters hold roughly what is covered in class and the appendices hold both
elementary background and additional advanced topics.

| # | Hub page | Book | In one line |
|---|----------|------|-------------|
| 1 | [[mdft-book]] | [Mathematics of the DFT](https://ccrma.stanford.edu/~jos/mdft/) | the DFT formula and everything in it, with audio applications |
| 2 | [[filters-book]] | [Introduction to Digital Filters](https://ccrma.stanford.edu/~jos/filters/) | analysis and implementation of digital filters |
| 3 | [[pasp-book]] | [Physical Audio Signal Processing](https://ccrma.stanford.edu/~jos/pasp/) | computational physical models for delay effects and virtual instruments |
| 4 | [[sasp-book]] | [Spectral Audio Signal Processing](https://ccrma.stanford.edu/~jos/sasp/) | FFT-based analysis, processing, and synthesis of audio |

## Dependencies

- **MDFT** needs only high-school math; it supplies complex numbers,
  sinusoids, the DFT, the Fourier theorems, sampling theory, and decibels.
- **Filters** builds on MDFT (complex numbers above all) and adds the
  z transform, frequency response, poles and zeros, implementation
  structures, allpass and minimum-phase filters, state space, and the
  analog/Laplace background.
- **PASP** and **SASP** each build on the first two and are largely
  independent of each other.  They meet at sinusoidal modeling of resonant
  modes and at convolution-based reverberation.

Reading order for a newcomer: MDFT chapters 1-7, Filters chapters 1-9,
then PASP or SASP by interest, following links back into the appendices as
needed.

## How the books map onto this wiki

| Sub-wiki | Primary book | Also leans on |
|----------|--------------|---------------|
| `waveguide_synthesis/` | PASP (distilled from its LaTeX) | Filters (allpass, comb, state space) |
| `modal_synthesis/` | PASP ch. 8 and app. B | Filters (partial fractions, state space, resonators), MDFT (decay), SASP (peak estimation) |
| `spectral_processing/` | SASP (distilled from its LaTeX) | MDFT (DFT theorems, sampling), Filters (linear and minimum phase) |
| `virtual_analog/` | none (DAFx papers) | Filters (bilinear transform, analog filters, time-varying filters), PASP (lumped models, nonlinear elements) |
| `active_absorbers/` | none (ANC literature) | PASP (acoustics, impedance), Filters (stability, system identification), MDFT (correlation, coherence) |

MDFT and Filters are not distilled into sub-wikis of their own: their hub
pages plus [[book-topic-finder]] route a reader straight to the online
section, which is already short, self-contained, and hyperlinked.

## Using the books from the wiki

- Each topical page ends with a `## JOS online books` section of deep links
  and a link to the relevant hub page here, so the knowledge graph shows
  which pages rest on which book.
- Deep links are checked at build time against `jos_books/catalog/` (see
  the SCHEMA of this sub-wiki for the convention and the two `make` targets).
- To cite a book page in a paper, each book's "Citing this Work" link
  gives the form, e.g. Smith, J.O. "Delay Lines", in *Physical Audio Signal
  Processing*, <https://ccrma.stanford.edu/~jos/pasp/Delay_Lines.html>,
  online book, 2010 edition, accessed (date).

## Related

- [[book-topic-finder]] - topic to book-section lookup
- [[spectral_processing/concepts/sasp-overview|sasp-overview]] - the SASP plan as distilled in `spectral_processing/`
- [[waveguide_synthesis/concepts/waveguide-overview|waveguide-overview]] - where the PASP distillation starts

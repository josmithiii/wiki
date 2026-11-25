---
title: Filter Bank Summation STFT (FBS)
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [stft, fbs, dft-filter-bank, perfect-reconstruction, portnoff]
sources:
  - /w/sasp/fbs.tex
  - /w/sasp/dftfilterbank.tex
  - /w/sasp/stftfilterbank.tex
  - /w/sasp/fftfb.tex
  - /w/sasp/portnoffwin.tex
  - /w/sasp/downsampling.tex
  - https://ccrma.stanford.edu/~jos/sasp/Filter_Bank_Summation_FBS.html
---

# Filter Bank Summation STFT (FBS)

The **filter-bank view** of the STFT: each DFT bin $X_m(k)$ is the
output of a bandpass filter centered at $\omega_k = 2\pi k/N$.

## Derivation

Rewrite the sliding ($R=1$) STFT with $k$ fixed and time index $n$:
$$X_n(\omega_k) \;=\; \sum_{m} \big[x(m)e^{-j\omega_k m}\big]\, w(m-n)
\;=\; (x_k \ast \tilde w)(n), \qquad x_k(m) = x(m)e^{-j\omega_k m},\;\; \tilde w(n) = w(-n)$$

So each channel is a **demodulation** (frequency shift by $-\omega_k$)
followed by a **lowpass filter** whose impulse response is the flipped
window. Equivalently, $X_n(\omega_k) = e^{-j\omega_k n}(x\ast h_k)(n)$
with $h_k(n) = w(-n)e^{j\omega_k n}$: a bandpass filter centered at
$\omega_k$ (prototype $w$) followed by demodulation to baseband.

## DFT Filter Bank

The length-$N$ DFT is a uniform bank of $N$ bandpass filters with
identical prototype $W(\omega)$, evenly spaced at $\omega_k = 2\pi k/N$.
The sliding DFT ($R=1$) is oversampled by $N$; a hop of $R$ downsamples
every channel by $R$. $R=N$ is **critical sampling** (as many channel
samples as input samples); practical STFTs use $R<N$ and stay
oversampled, which is what makes them robust to modifications.

## Synthesis (Summation)

Reconstruct $x$ by remodulating each channel and summing. For $R=1$:
$$\hat{x}(n) \;=\; \sum_{k=0}^{N-1} X_n(\omega_k)\, e^{j\omega_k n}
\;=\; N\sum_{r} w(-rN)\, x(n-rN)$$

## FBS Perfect Reconstruction Condition

The sum above collapses to $\hat x(n) = N\,w(0)\,x(n)$ when the window
is zero at all nonzero multiples of $N$:
$$w(rN) \;=\; 0,\quad r = \pm 1, \pm 2, \dots \qquad (w \in \text{Nyquist}(N))$$
This holds trivially when $M \le N$. Equivalently, the channel
responses overlap-add to a constant around the unit circle,
$\sum_k W(\omega - \omega_k) = c$, i.e. $W \in \text{COLA}(2\pi/N)$.

Contrast with OLA's condition ($w\in\text{COLA}(R) \Leftrightarrow W \in \text{Nyquist}(2\pi/R)$).
The two are **Fourier duals** via the Poisson summation formula
([[dtft-and-fourier-theorems]]).

## Aliasing Cancellation

When $R > 1$, each channel is aliased. FBS perfect reconstruction
requires **aliasing cancellation** across channels upon resynthesis:
the imaging from remodulation cancels the aliasing from decimation.
This is the defining trick of maximally decimated filter banks.

## Portnoff Windows

A **Portnoff window** is longer than the FFT ($M > N$) yet still
Nyquist($N$): $w(n) = w_0(n)\,\operatorname{sinc}(n/N)$ for any taper
$w_0$. The windowed frame is **time-aliased** (wrapped) to length $N$
before the FFT. Choosing $M \gg N$ lets the channel filters approach
ideal bandpass filters of width $2\pi/N$ (less cross-talk), at the cost
of less robustness to spectral modifications, which disturb the
time-domain aliasing cancellation. The hop must still satisfy $R<N$.

## Complexity

- Direct filter bank: $N \cdot M$ mults/sample.
- FFT filter bank: one windowing pass plus one FFT per hop, about
  $\frac{M + N\log_2 N}{R}$ mults/sample — same output, much cheaper.
- Polyphase view: the window splits into $N$ polyphase components (one
  per FFT input sample), followed by the FFT as the modulation stage —
  see [[multirate-filter-banks]].

## When to Use FBS

- Bin signals interpreted as time series: **phase vocoder**,
  [[f0-and-spectral-envelope]] tracking, instantaneous frequency.
- Audio coding filter banks (MPEG, AAC): critically sampled
  cosine-modulated relatives (pseudo-QMF, MDCT) of the DFT bank.
- When the application wants per-channel processing rather than
  per-frame block processing.

## Related Concepts
- [[overlap-add-stft]] — dual OLA view
- [[short-time-fourier-transform]] — the common STFT
- [[multirate-filter-banks]] — generalization beyond uniform DFT
- [[phase-vocoder-and-tsm]] — canonical FBS application

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [STFT Filter Bank](https://ccrma.stanford.edu/~jos/sasp/STFT_Filter_Bank.html), [The DFT Filter Bank](https://ccrma.stanford.edu/~jos/sasp/DFT_Filter_Bank.html), [Nyquist(N) Windows](https://ccrma.stanford.edu/~jos/sasp/Nyquist_N_Windows.html), [Duality of COLA and Nyquist Conditions](https://ccrma.stanford.edu/~jos/sasp/Duality_COLA_Nyquist_Conditions.html), [Portnoff Windows](https://ccrma.stanford.edu/~jos/sasp/Portnoff_Windows.html), [Downsampled STFT Filter Banks](https://ccrma.stanford.edu/~jos/sasp/Downsampled_STFT_Filter_Banks.html)

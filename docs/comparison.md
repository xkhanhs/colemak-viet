# How Colemak-Viet was measured, and what it was measured against

Two separate bodies of work sit behind this layout, and they are not equally
reproducible from this repo. This page keeps them apart on purpose.

1. **The tables in the README**, produced by [`scripts/score-layouts.py`](../scripts/score-layouts.py).
   Anyone can re-run them, change the effort grid, and argue.
2. **The design study** that produced the layout in the first place, run in
   August and September 2026 in a separate repo, against a larger set of
   layouts and a heavier scoring model. Its scripts are not here. Its
   conclusions are summarised below and labelled as what they are: an earlier
   measurement you cannot re-run from this repository.

## The model

A model of typing, not typing. It knows nothing about rhythm, about how fast a
particular pair actually is for a particular hand, or about what you type all
day.

- **Corpus.** OpenSubtitles word-frequency lists with real counts
  ([hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords)),
  50k words each for Vietnamese and English. Vietnamese words are decomposed
  into Telex keystrokes first: tone marks move to the end of the syllable
  (`hoà` → `hoaf`), a circumflex doubles its vowel (`ê` → `ee`), horn and breve
  are `w`, and `đ` is `dd`.
- **Board.** A 3×10 row-staggered ANSI grid. Fingers follow **columns**, not the
  usual touch-typing assignment — the C key is pressed with the middle finger
  here, so `tr` counts as two fingers and not one. If you press C with your
  index finger, some of these same-finger numbers are worse for you than they
  read.
- **Cost per key**, approximating the colemak-mods effort grid:

  | | | | | | | | | | |
  |---|---|---|---|---|---|---|---|---|---|
  | 2.6 | 2.2 | 1.8 | 1.6 | 3.0 | 3.0 | 1.6 | 1.8 | 2.2 | 2.6 |
  | 1.8 | 1.3 | 1.1 | 1.0 | 2.2 | 2.2 | 1.0 | 1.1 | 1.3 | 1.8 |
  | 2.8 | 2.4 | 2.0 | 1.8 | 2.6 | 1.8 | 2.0 | 2.2 | 2.4 | 2.8 |

- **Effort** is the weighted mean cost per keystroke. **SFB** is the share of
  within-word bigrams that use one finger twice on two different keys.

### What counts as noise

When the same layouts were re-scored against a different corpus and three
different effort grids, rankings held but margins moved by up to 2%. Treat any
difference under about 2% as the model failing to have an opinion. This is not
a rhetorical caveat: it is why the design stopped where it did — see *What was
rejected*, below.

One known blind spot: the model charges Colemak-Viet for `gx` (2.1‰, from
`những` and `cũng`), because `g` and `x` both sit in the left index column. The
typist this was tuned for presses the B key with the *right* index, so for them
that pair is a hand alternation rather than a same-finger bigram. Your hands
decide which of the two is true.

## The 29-layout ranking (earlier study, September 2026)

Scored on the same Vietnamese corpus but with a heavier objective:
`effort + 15×SFB + 3×LSB + 2×(pinky use above 20%)`, with layouts taken verbatim
from [semilin/genkey](https://github.com/semilin/genkey), from their authors'
READMEs (Graphite, Canary), or from the author's repo images (Gallium). The
Colemak-Viet variant measured here is the one that had `x` in the top-right
corner rather than on the B key; the two score within 0.1% of each other.

**This table cannot be regenerated from this repository.** It is reproduced
because the conclusion matters and the method should be public, not because the
numbers are more authoritative than the ones you can run yourself.

| # | layout | score | SFB | LSB | home row | pinky | alternation | Cmd letters pushed right |
|---|---|---|---|---|---|---|---|---|
| 1 | Colemak-Viet | 1.815 | 0.90% | 1.01% | 61% | 21.0% | 51.6% | — |
| 2 | Workman | 2.102 (+16%) | 2.84% | 1.52% | 63% | 16.9% | 52.8% | — |
| 3 | FLAW | 2.204 (+21%) | 2.49% | 4.55% | 55% | 17.3% | 48.2% | t r z |
| 4 | Halmak | 2.270 (+25%) | 3.38% | 0.57% | 58% | 24.4% | 56.9% | a |
| 5 | RTNA | 2.290 (+26%) | 3.91% | 0.65% | 52% | 15.8% | 44.6% | c v s z |
| 6 | MTGAP30 | 2.291 (+26%) | 4.09% | 0.32% | 52% | 16.0% | 57.2% | c v s t r |
| 7 | Dvorak | 2.312 (+27%) | 3.40% | 2.77% | 67% | 18.4% | 56.5% | c v s t r z |
| 8 | APT | 2.344 (+29%) | 4.26% | 0.46% | 52% | 17.9% | 54.9% | a z |
| 9 | Norman | 2.363 (+30%) | 4.62% | 0.97% | 63% | 17.4% | 53.6% | r |
| 10 | ColemaQ | 2.370 (+31%) | 3.74% | 2.54% | 60% | 21.6% | 51.8% | v |
| 11 | Semimak JQ | 2.377 (+31%) | 4.03% | 2.13% | 54% | 19.0% | 52.1% | c a |
| 12 | Whorf | 2.397 (+32%) | 4.03% | 2.60% | 51% | 17.4% | 54.0% | c v a |
| 13 | Canary | 2.431 (+34%) | 4.45% | 2.18% | 54% | 19.4% | 49.3% | a z |
| 14 | ISRT | 2.458 (+35%) | 5.12% | 0.65% | 59% | 19.7% | 52.4% | a z |
| 15 | Semimak | 2.499 (+38%) | 4.64% | 2.95% | 54% | 19.0% | 51.8% | c a |
| 16 | Colemak DHk | 2.528 (+39%) | 4.86% | 2.35% | 59% | 21.6% | 50.9% | — |
| 17 | Colemak DH | 2.531 (+39%) | 4.86% | 2.35% | 60% | 21.6% | 50.9% | — |
| 18 | SIND | 2.534 (+40%) | 4.89% | 3.87% | 54% | 14.9% | 54.2% | v t r a z |
| 19 | Sturdy | 2.536 (+40%) | 5.44% | 1.55% | 50% | 15.8% | 50.4% | a |
| 20 | hyperroll | 2.581 (+42%) | 5.48% | 0.52% | 55% | 21.3% | 52.5% | a |
| 21 | Colemak Qi | 2.605 (+44%) | 5.67% | 1.41% | 59% | 21.6% | 50.0% | — |
| 22 | Graphite | 2.609 (+44%) | 6.18% | 1.58% | 56% | 17.8% | 53.2% | a |
| 23 | Colemak | 2.622 (+44%) | 4.86% | 3.84% | 66% | 21.6% | 50.9% | — |
| 24 | Gallium | 2.628 (+45%) | 6.13% | 1.84% | 56% | 16.2% | 53.2% | a |
| 25 | Colemak DH angle | 2.648 (+46%) | 5.29% | 2.35% | 60% | 23.0% | 50.9% | — |
| 26 | boo | 2.652 (+46%) | 6.41% | 1.27% | 59% | 18.5% | 52.0% | t r |
| 27 | Rolll | 2.679 (+48%) | 6.27% | 1.35% | 56% | 16.2% | 49.0% | c v s t r z |
| 28 | Hands Down (30-key) | 2.951 (+63%) | 6.90% | 7.21% | 56% | 15.4% | 50.9% | a z |
| 29 | QGMLWY | 3.173 (+75%) | 9.23% | 4.67% | 66% | 11.5% | 51.8% | a |

The interesting result is not the first row. It is that the whole modern
optimised-layout family — Graphite, Gallium, Canary, Sturdy, Semimak — lands
30–50% behind on Vietnamese, below plain Colemak-DH in several cases. They are
good layouts. They are optimised for English letter frequencies, and the five
Telex mark keys `s f r x j` are about a fifth of all Vietnamese keystrokes.
Workman does well by accident: it happens to keep `h` on the left hand, far from
`n` and `k`.

## What was rejected

The layout stopped changing because the model stopped being able to tell the
difference, not because every idea was tried and beaten.

- **A free optimisation** of all 24 letters scores 9–11% better. It also means
  relearning nearly the whole board, and eight annealing seeds produced eight
  different layouts within 1–2% of each other — the model cannot distinguish the
  arrangements of the 20 letters outside the home row. The only thing all eight
  agreed on was a home row containing `a h i n o s`, which this layout already
  has.
- **Dropping the Cmd-shortcut constraint** buys about 2%. One-handed shortcuts
  are nearly free, so the constraint stays.
- **Remapping the Telex mark keys** `s f r x j`: all 55,440 placements on eleven
  safe keys were scored on a 117-million-keystroke corpus. Standard Telex is
  already in the top 6%, the best alternative wins 1–3% depending on the effort
  grid, and a private mark layout costs you every other keyboard you touch —
  phones, other people's machines. Rejected.
- **`e`↔`i`** is the one candidate that kept winning across corpora and model
  variants, at about 2%. It is also exactly at the noise threshold, and its
  gain comes from `eu` and `em`, pairs the typist reports as easy in practice.
  Left alone, pending real typing data rather than another model.

## Open questions

- Should `z` go back to the left half? Since `x` took the B key, `z` sits in the
  top-right index slot and **Cmd+Z is no longer a one-handed shortcut**. Putting
  `x` back in the Y slot and `z` on B restores it, and the model rates the two
  arrangements as equivalent.
- The English same-finger cost (`yo`, `nd`, `wh`) has never been weighed against
  the Vietnamese gain in a single objective, because no one has said what the
  right mix of the two languages is. If you type more English than Vietnamese,
  that mix matters more than anything else on this page.
- Every number here is a model. The one honest measurement in this repo is that
  one person reached 50 wpm in about fifteen hours.

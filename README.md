# Colemak-Viet

A keyboard layout for people who type **Vietnamese** all day and English the rest
of the time. It starts from [Colemak](https://colemak.com) and the
[DH mod](https://colemakmods.github.io/mod-dh/), and moves twelve more keys —
because Colemak and Colemak-DH were both optimised for English, and Vietnamese
typed through Telex is a different stream of keystrokes.

Tiếng Việt: [README.vi.md](README.vi.md)

```
 `   1  2  3  4  5  6  7  8  9  0  -  =
 Tab   q  w  f  g  b     z  l  u  y  ;   [  ]  \
 Caps   a  h  s  t  p     m  n  e  o  i   '
 Shift   j  v  r  c  x     k  d  ,  .  /
```

Ready-made files for macOS, Windows and Linux are in [`dist/`](dist/) —
[how to install](#install).

## Why not just use Colemak-DH

Vietnamese is not typed the way it is written. With Telex — what almost every
Vietnamese typist uses — `nhiều` is eight keystrokes, `nhieeuf`, and the tone
mark lands at the end of the syllable. So the letter frequencies that matter are
the frequencies of the *keystrokes*, and they look nothing like English.

Colemak-DH puts `k`, `h` and `n` on the right index finger. Vietnamese opens
about an eighth of its words with `kh`, and `nh` is everywhere. On an
OpenSubtitles corpus of 50k Vietnamese words, those two bigrams alone are
30 per mille of everything typed, and they are both same-finger:

| layout | worst same-finger bigrams, Vietnamese |
|---|---|
| Colemak-DH-angle | `nh` 19.8‰, `kh` 11.0‰, `wc` 5.5‰, `ax` 4.1‰, `nj` 4.1‰ |
| Colemak-Viet | `eu` 3.8‰, `gx` 2.1‰, `aj` 0.5‰, `nd` 0.3‰, `ue` 0.3‰ |

That is the whole idea. Everything else follows from getting those pairs off one
finger without breaking the things Colemak got right.

## The numbers

Run them yourself: `./scripts/score-layouts.py --markdown`. The corpora are
OpenSubtitles frequency lists with real counts, Vietnamese words decomposed into
Telex keystrokes first. Lower effort is better; SFB is same-finger bigrams.

### Vietnamese

| layout | effort | SFB | home row | R pinky | L pinky | left hand | alternation |
|---|---|---|---|---|---|---|---|
| **Colemak-Viet** | **1.629** | **0.84%** | 61% | 5.9% | 13.8% | 54% | 52% |
| Workman | 1.631 (+0%) | 2.84% | 63% | 5.9% | 11.0% | 54% | 53% |
| Colemak-DH | 1.700 (+4%) | 4.86% | 60% | 10.6% | 11.0% | 50% | 51% |
| Dvorak | 1.719 (+5%) | 3.40% | 67% | 7.6% | 10.8% | 45% | 57% |
| Colemak-DH-angle | 1.724 (+6%) | 5.29% | 60% | 10.6% | 12.4% | 50% | 51% |
| Colemak | 1.747 (+7%) | 4.86% | 66% | 10.6% | 11.0% | 50% | 51% |
| QWERTY | 1.863 (+14%) | 8.30% | 41% | 0.7% | 11.0% | 55% | 52% |

Same-finger bigrams drop by a factor of six against Colemak-DH-angle, and the
right pinky — which carries `o`, the single heaviest letter in Vietnamese, on
stock Colemak — loses nearly half its work.

### English, honestly

English still works, and it is far better than QWERTY. But this layout was
tuned on a Vietnamese corpus with no English term in the objective, and it
shows in exactly the place you would expect:

| layout | effort | SFB | home row | R pinky | L pinky | left hand | alternation |
|---|---|---|---|---|---|---|---|
| **Colemak-Viet** | **1.555** | **5.85%** | 67% | 7.2% | 8.1% | 47% | 49% |
| Workman | 1.559 (+0%) | 2.47% | 68% | 7.2% | 7.9% | 50% | 53% |
| Colemak-DH | 1.575 (+1%) | **1.18%** | 67% | 9.1% | 7.9% | 44% | 55% |
| Colemak-DH-angle | 1.584 (+2%) | 1.31% | 67% | 9.1% | 7.9% | 44% | 55% |
| Colemak | 1.602 (+3%) | 1.18% | 71% | 9.1% | 7.9% | 44% | 55% |
| Dvorak | 1.687 (+8%) | 2.36% | 69% | 9.9% | 8.9% | 46% | 69% |
| QWERTY | 1.951 (+25%) | 5.93% | 32% | 1.5% | 7.9% | 54% | 51% |

Effort and home-row use are Colemak-class. Same-finger bigrams are not: at
5.85% they are five times Colemak-DH's and level with QWERTY. Three pairs
account for most of it — `yo` (17.5‰), `nd` (10.3‰), `wh` (7.8‰) — because `o`
moved under `y`, `d` moved under `n`, and `h` moved under `w`. On a
prose-weighted English list rather than subtitles the total falls to 4.7%,
still about four times Colemak-DH's, so it is not an artefact of *you* being
the commonest word in film dialogue.

**So:** if you type mostly Vietnamese, this is the better board and the English
cost is real but small. If you type mostly English, use
[Colemak-DH](https://colemakmods.github.io/mod-dh/) instead — it is better at
English than this will ever be.

## What changed, and why

Against Colemak-DH-angle (`qwfpb jluy; / arstg mneio / xcdvz kh,./`), twelve
keys move:

| change | why |
|---|---|
| `h` → left home, where `r` was | kills `kh` and `nh` outright; `h` is 69‰ of Vietnamese keystrokes against `r`'s 30‰, so it has the better claim on a home key, and `ho hu ha` become hand alternations |
| `r` → bottom left, where `d` was | still one-handed for Cmd+R |
| `d` → right index, bottom row | `dd` (for `đ`) is a key repeat, which costs nothing, and `d` ends up next to the vowels |
| `c` ↔ `v` | `c` is 42‰ and belongs on the index; `v` is 11‰ and can take the ring finger. Kills `wc` |
| `p` ↔ `g` | `g` is 51‰, mostly from `ng` at 44‰, and should not be paying the centre-column stretch |
| `o` ↔ `i` | `o` is the heaviest letter in Vietnamese at 131‰. It cannot sit on the pinky |
| `j` → bottom-left corner | `j` is the heavy tone mark; off the right index it stops colliding with `nj`, `mj`, `hj` |
| `x` → the B key | `x` is the rarest tone mark (5.5% of words) and parks in the stretch |
| `z` → the top-right index slot | `z` is effectively 0‰ in Vietnamese; it goes to the most expensive key on the board |

Two things are held fixed, and they rule out several arrangements that score
better:

- **`c v s t r a x` stay on the left half**, so Cmd+C/V/S/T/R/A/X remain
  one-handed. Dropping this constraint buys about 2% in the model, and costs
  every shortcut you already know.
- **The Telex mark keys `s f r x j` are not remapped.** They were audited: all
  55,440 ways of placing five marks on eleven safe keys were scored on a
  117-million-keystroke corpus, and standard Telex already sits in the top 6%.
  The best alternative wins 1–3% depending on the effort model — noise — and
  you would pay for it on every other keyboard you ever touch.

`;` keeps its stock position: Vietnamese barely uses it and code needs it.

More detail, including a ranking against 28 other layouts and the arguments
that were rejected: [docs/comparison.md](docs/comparison.md).

## Install

You need two things: this layout, and a Telex input method. They are
independent — an IME reads *characters*, not key positions, so Telex needs no
configuration to work with a remapped board.

### macOS

This key table is in daily use on macOS 26. Download this repo, then:

```bash
./scripts/build-layouts.py --install
```

or copy `dist/macos/Colemak-Viet.bundle` into `~/Library/Keyboard Layouts/`
yourself. **Log out and back in** — macOS does not pick up a newly added layout
bundle until then — then add it in System Settings → Keyboard → Input Sources.

To check that the system really is serving what is in this repo:

```bash
swift scripts/verify-macos-layout.swift
```

For Telex, use the built-in Vietnamese input method, or
[VTX](https://github.com/xkhanhs/vtx), or any other Telex IME.

### Windows — not tested

`dist/windows/colemak-viet.klc` is a source file for
[MSKLC](https://learn.microsoft.com/en-us/globalization/windows-keyboard-layouts),
which compiles it into an installer. Open it, build, install, then pick the
layout in Settings → Time & Language → Language & region.

Nobody has run this on Windows. If it misbehaves, please
[open an issue](../../issues) or send a PR — the fix belongs in
`scripts/build-layouts.py`, not in the generated file.

For Telex on Windows: [Unikey](https://www.unikey.org) or
[EVKey](https://evkeyvn.com).

### Linux — not tested

`dist/linux/colemak_viet` is an XKB symbols file:

```bash
sudo cp dist/linux/colemak_viet /usr/share/X11/xkb/symbols/
setxkbmap colemak_viet
```

On Wayland the same file is read through your desktop's input settings rather
than `setxkbmap`; on GNOME you may need to register it in
`/usr/share/X11/xkb/rules/evdev.xml` before it appears in the list.

Also untested. Issues and PRs welcome.

For Telex on Linux: [ibus-bamboo](https://github.com/BambooEngine/ibus-bamboo).

### Karabiner-Elements (macOS, no new input source)

`dist/karabiner/colemak-viet.json` remaps the twelve keys on top of whatever
layout you already use. Copy it to
`~/.config/karabiner/assets/complex_modifications/` and enable the rule. Useful
if something else on your machine is pinned to a specific input source.

## How long it takes to learn

About fifteen hours of practice to reach 50 wpm, coming from Colemak-DH-angle.
That is one person's experience, not a study — and it is the only real
measurement in this repo that is not a model. Starting from QWERTY will take
longer, and most of that time is spent on Colemak itself rather than on the
twelve keys this layout adds.

Two of the changes — `d`↔`h` and `c`↔`v` — carry about 70% of the total
benefit, so they can be learned first if you want to stage it.

## Building

```bash
./scripts/build-layouts.py          # layout.json → dist/
./scripts/test-layouts.py           # read all four outputs back, compare
./scripts/build-layouts.py --check  # fail if dist/ is stale
./scripts/score-layouts.py          # the tables above
```

[`layout.json`](layout.json) is the only place the letters are written down.
Everything in `dist/` is generated from it, so a change there reaches all four
platforms or none.

## Credits

- **Colemak**, by Shai Coleman — the layout this is a descendant of.
- **Colemak-DH** and the **angle mod**, by Stevep99 and the
  [ColemakMods](https://github.com/ColemakMods/mod-dh) community — the home-row
  and bottom-row work that this starts from.
- The measurements and the earlier design work were done inside
  [keybear](https://github.com/xkhanhs/keybear) (a typing trainer) and
  [VTX](https://github.com/xkhanhs/vtx) (a Telex input method for macOS).

Colemak-Viet is an independent mod. Nothing here is endorsed by either project,
and any mistake in it is this repo's.

## Licence

[MIT](LICENSE). The generated layout files are built from scratch by
`scripts/build-layouts.py`; no file from another layout project is redistributed
here.

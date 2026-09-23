#!/usr/bin/env python3
"""Score keyboard layouts on Vietnamese (Telex) and English word frequencies.

Everything the README claims about effort, same-finger bigrams and finger load
comes out of this script, so anyone can re-run it and argue with the numbers:

    ./scripts/score-layouts.py              # both languages, all layouts
    ./scripts/score-layouts.py --lang vi
    ./scripts/score-layouts.py --markdown   # the tables as they appear in docs/

Corpora are OpenSubtitles word-frequency lists (hermitdave/FrequencyWords, real
counts, not rank weights). They are downloaded on first run into corpus/, which
is not committed.

A model is not a hand. These numbers rank layouts; they do not predict your
speed, and a difference under ~2% is inside the noise this model showed when the
same layouts were re-measured against a different corpus and a different effort
grid. Read docs/comparison.md before treating any single figure as a verdict.
"""

import argparse
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
SOURCES = {
    "vi": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/vi/vi_50k.txt",
    "en": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_50k.txt",
}

# Layouts as three rows of ten, left to right on an ANSI board. Rows that carry
# an angle mod (Colemak-DH-angle, Colemak-Viet) already have the left half of
# the bottom row written in its shifted-by-one position.
LAYOUTS = {
    "QWERTY": ("qwertyuiop", "asdfghjkl;", "zxcvbnm,./"),
    "Dvorak": ("',.pyfgcrl", "aoeuidhtns", ";qjkxbmwvz"),
    "Colemak": ("qwfpgjluy;", "arstdhneio", "zxcvbkm,./"),
    "Colemak-DH": ("qwfpbjluy;", "arstgmneio", "zxcdvkh,./"),
    "Colemak-DH-angle": ("qwfpbjluy;", "arstgmneio", "xcdvzkh,./"),
    "Workman": ("qdrwbjfup;", "ashtgyneoi", "zxmcvkl,./"),
    "Colemak-Viet": ("qwfgbzluy;", "ahstpmneoi", "jvrcxkd,./"),
}

# Cost per physical key (lower is better), and the finger that presses it.
# Fingers follow COLUMNS, which is how the hands this was tuned for actually
# move: the C key is pressed with the middle finger, so `tr` is two fingers.
COST = {
    "top":    [2.6, 2.2, 1.8, 1.6, 3.0, 3.0, 1.6, 1.8, 2.2, 2.6],
    "home":   [1.8, 1.3, 1.1, 1.0, 2.2, 2.2, 1.0, 1.1, 1.3, 1.8],
    "bottom": [2.8, 2.4, 2.0, 1.8, 2.6, 1.8, 2.0, 2.2, 2.4, 2.8],
}
FINGER = ["Lp", "Lr", "Lm", "Li", "Li", "Ri", "Ri", "Rm", "Rr", "Rp"]
ROWS = ("top", "home", "bottom")

TONES = {"́": "s", "̀": "f", "̉": "r", "̃": "x", "̣": "j"}
SHAPES = {"̂", "̆", "̛"}


def telex(word: str) -> str:
    """The keys a Telex user actually presses to produce `word`.

    Tone marks move to the end of the syllable (`hoà` → `hoaf`), a circumflex
    doubles its vowel (`ê` → `ee`), horn and breve are `w`, and `đ` is `dd`.
    """
    base, tone = "", ""
    for char in unicodedata.normalize("NFD", word):
        if char in TONES:
            tone = TONES[char]
        elif char in SHAPES:
            base += base[-1] if char == "̂" else "w"
        elif char == "đ":
            base += "dd"
        else:
            base += char
    return base + tone


def corpus(lang: str) -> list[tuple[str, int]]:
    CORPUS.mkdir(exist_ok=True)
    path = CORPUS / f"{lang}_50k.txt"
    if not path.exists():
        print(f"fetching {SOURCES[lang]}", file=sys.stderr)
        urllib.request.urlretrieve(SOURCES[lang], path)
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].isdigit():
            keys = telex(parts[0]) if lang == "vi" else parts[0].lower()
            out.append((keys, int(parts[1])))
    return out


def keymap(layout: tuple[str, str, str]) -> dict[str, tuple[float, str, str]]:
    """character → (cost, finger, row)"""
    out = {}
    for row, chars in zip(ROWS, layout):
        for col, char in enumerate(chars):
            out[char] = (COST[row][col], FINGER[col], row)
    return out


def score(layout: tuple[str, str, str], words: list[tuple[str, int]]) -> dict:
    keys = keymap(layout)
    strokes = effort = home = pinky_r = pinky_l = left = 0.0
    bigrams = sfb = alt = 0.0
    skipped = 0

    for word, count in words:
        if any(char not in keys for char in word):
            skipped += count
            continue
        prev = None
        for char in word:
            cost, finger, row = keys[char]
            strokes += count
            effort += cost * count
            if row == "home":
                home += count
            if finger == "Rp":
                pinky_r += count
            if finger == "Lp":
                pinky_l += count
            if finger[0] == "L":
                left += count
            if prev is not None:
                bigrams += count
                pfinger, pchar = prev
                if pfinger == finger and pchar != char:
                    sfb += count
                if pfinger[0] != finger[0]:
                    alt += count
            prev = (finger, char)

    pct = lambda part, whole: 100 * part / whole if whole else 0.0
    return {
        "effort": effort / strokes,
        "sfb": pct(sfb, bigrams),
        "home": pct(home, strokes),
        "pinky_r": pct(pinky_r, strokes),
        "pinky_l": pct(pinky_l, strokes),
        "left": pct(left, strokes),
        "alt": pct(alt, bigrams),
        "coverage": pct(strokes and sum(c for _, c in words) - skipped, sum(c for _, c in words)),
    }


HEADERS = ["layout", "effort", "SFB", "home row", "R pinky", "L pinky",
           "left hand", "alternation"]


def table(lang: str, markdown: bool) -> str:
    words = corpus(lang)
    rows = []
    for name, layout in LAYOUTS.items():
        rows.append((name, score(layout, words)))
    rows.sort(key=lambda item: item[1]["effort"])
    best = rows[0][1]["effort"]

    lines = []
    if markdown:
        lines.append("| " + " | ".join(HEADERS) + " |")
        lines.append("|" + "---|" * len(HEADERS))
    for name, r in rows:
        delta = "" if r["effort"] == best else f" (+{100 * (r['effort'] / best - 1):.0f}%)"
        cells = [f"{name}", f"{r['effort']:.3f}{delta}", f"{r['sfb']:.2f}%",
                 f"{r['home']:.0f}%", f"{r['pinky_r']:.1f}%", f"{r['pinky_l']:.1f}%",
                 f"{r['left']:.0f}%", f"{r['alt']:.0f}%"]
        lines.append("| " + " | ".join(cells) + " |" if markdown
                     else "  ".join(cell.ljust(18 if i == 0 else 12)
                                    for i, cell in enumerate(cells)))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=["vi", "en", "both"], default="both")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    langs = ["vi", "en"] if args.lang == "both" else [args.lang]
    for lang in langs:
        title = {"vi": "Vietnamese (Telex keystrokes)", "en": "English"}[lang]
        print(f"\n### {title} — OpenSubtitles 50k, real counts\n")
        print(table(lang, args.markdown))
    print()


if __name__ == "__main__":
    main()

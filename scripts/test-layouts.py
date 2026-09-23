#!/usr/bin/env python3
"""Check every file in dist/ against layout.json, independently of the builder.

    ./scripts/test-layouts.py

The builder walks the table once and writes four formats; this walks the four
formats back and asks what each one types. A typo that reaches only one output
file — the classic way a layout ends up correct on one operating system and
subtly wrong on another — has to survive both directions to get through.

What this does NOT prove is that macOS accepts the bundle: only the system can
answer that, by serving the layout back. `scripts/verify-macos-layout.swift`
asks it, once the layout is installed and the machine has been logged out and
back in (macOS does not pick up a newly added layout bundle before that).
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYOUT = json.loads((ROOT / "layout.json").read_text(encoding="utf-8"))
DIST = ROOT / "dist"
ROWS = ("top", "home", "bottom")
SHIFTED = {";": ":", ",": "<", ".": ">", "/": "?", "'": '"'}

MAC_CODES = {
    "top": [12, 13, 14, 15, 17, 16, 32, 34, 31, 35],
    "home": [0, 1, 2, 3, 5, 4, 38, 40, 37, 41],
    "bottom": [6, 7, 8, 9, 11, 45, 46, 43, 47, 44],
}
WIN_SCAN = {
    "top": ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
    "home": ["1e", "1f", "20", "21", "22", "23", "24", "25", "26", "27"],
    "bottom": ["2c", "2d", "2e", "2f", "30", "31", "32", "33", "34", "35"],
}
XKB_POS = {row: [f"{prefix}{i:02d}" for i in range(1, 11)]
           for row, prefix in zip(ROWS, ("AD", "AC", "AB"))}
XKB_NAMES = {";": "semicolon", ",": "comma", ".": "period", "/": "slash",
             ":": "colon", "<": "less", ">": "greater", "?": "question"}
QWERTY = {"top": "qwertyuiop", "home": "asdfghjkl;", "bottom": "zxcvbnm,./"}

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def expected():
    for row in ROWS:
        for index, char in enumerate(LAYOUT["rows"][row]):
            yield row, index, char, SHIFTED.get(char, char.upper())


def unescape(value: str) -> str:
    """&#x0027; and &amp; both mean one character; compare characters."""
    return html.unescape(re.sub(r"&#x([0-9A-Fa-f]{1,6});",
                                lambda m: chr(int(m.group(1), 16)), value))


def macos_maps() -> list[dict[int, str]]:
    text = (DIST / "macos" / f"{LAYOUT['name']}.keylayout").read_text(encoding="utf-8")
    body = text.split('<keyMapSet id="ansi">')[1].split("</keyMapSet>")[0]
    maps = []
    for _, block in re.findall(r'<keyMap index="(\d+)"[^>]*>(.*?)</keyMap>', body, re.S):
        entry = {}
        for code, attrs in re.findall(r'<key code="(\d+)"\s+(\w+="[^"]*")\s*/>', block):
            output = re.search(r'output="([^"]*)"', attrs)
            action = re.search(r'action="ch_([^"]*)"', attrs)
            if output:
                entry[int(code)] = unescape(output.group(1))
            elif action:
                entry[int(code)] = unescape(action.group(1))
        maps.append(entry)
    return maps


def test_macos() -> None:
    maps = macos_maps()
    check(len(maps) == 8, f"macOS: expected 8 key maps, found {len(maps)}")
    plain, shift, caps = maps[0], maps[1], maps[2]
    for row, index, char, upper in expected():
        code = MAC_CODES[row][index]
        check(plain.get(code) == char,
              f"macOS plain: key {code} types {plain.get(code)!r}, expected {char!r}")
        check(shift.get(code) == upper,
              f"macOS shift: key {code} types {shift.get(code)!r}, expected {upper!r}")
        want_caps = upper if char.isalpha() else char
        check(caps.get(code) == want_caps,
              f"macOS caps: key {code} types {caps.get(code)!r}, expected {want_caps!r}")
    # Every letter of the alphabet has to be reachable, or the layout is unusable
    # in a way no single-key test would notice.
    typed = {plain[code] for code in plain}
    missing = sorted(set("abcdefghijklmnopqrstuvwxyz") - typed)
    check(not missing, f"macOS: no key types {missing}")


def test_windows() -> None:
    text = (DIST / "windows" / "colemak-viet.klc").read_bytes().decode("utf-16-le")
    rows = {}
    for line in text.splitlines():
        cells = line.split("\t")
        if len(cells) >= 5 and re.fullmatch(r"[0-9a-f]{2}", cells[0]):
            rows[cells[0]] = (cells[3], cells[4])
    for row, index, char, upper in expected():
        scan = WIN_SCAN[row][index]
        check(rows.get(scan) == (char, upper),
              f"Windows: scan {scan} types {rows.get(scan)}, expected {(char, upper)}")


def test_linux() -> None:
    text = (DIST / "linux" / "colemak_viet").read_text(encoding="utf-8")
    keys = dict(re.findall(r"key <(\w+)> \{ \[ ([^\]]+) \] \};", text))
    for row, index, char, upper in expected():
        pos = XKB_POS[row][index]
        want = f"{XKB_NAMES.get(char, char)}, {XKB_NAMES.get(upper, upper)}"
        check(keys.get(pos) == want,
              f"Linux: {pos} is [{keys.get(pos)}], expected [{want}]")


def test_karabiner() -> None:
    rule = json.loads((DIST / "karabiner" / "colemak-viet.json").read_text(encoding="utf-8"))
    pairs = {m["from"]["key_code"]: m["to"][0]["key_code"]
             for m in rule["rules"][0]["manipulators"]}
    names = {";": "semicolon", ",": "comma", ".": "period", "/": "slash"}
    for row, index, char, _ in expected():
        source = QWERTY[row][index]
        if source == char:
            check(names.get(source, source) not in pairs,
                  f"Karabiner: remaps {source} to itself")
            continue
        check(pairs.get(names.get(source, source)) == names.get(char, char),
              f"Karabiner: {source} → {pairs.get(names.get(source, source))}, "
              f"expected {char}")


def test_shortcut_constraint() -> None:
    """The Cmd-shortcut letters stay reachable by the left hand alone.

    This is a design constraint, not a nicety: it is why several otherwise
    better-scoring arrangements were rejected. A future edit to layout.json that
    quietly breaks it should fail here rather than in someone's muscle memory.
    """
    left = set(LAYOUT["rows"]["top"][:5] + LAYOUT["rows"]["home"][:5]
               + LAYOUT["rows"]["bottom"][:5])
    for letter in LAYOUT["shortcut_letters_left"]:
        check(letter in left, f"shortcut letter {letter!r} is not on the left half")


def main() -> None:
    for test in (test_macos, test_windows, test_linux, test_karabiner,
                 test_shortcut_constraint):
        test()
    if failures:
        print("\n".join(failures))
        print(f"\n{len(failures)} failure(s)")
        sys.exit(1)
    rows = " / ".join(LAYOUT["rows"][row] for row in ROWS)
    print(f"all four outputs type: {rows}")


if __name__ == "__main__":
    main()

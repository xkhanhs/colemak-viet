#!/usr/bin/env python3
"""Generate every Colemak-Viet keyboard file in dist/ from layout.json.

One table in, four platforms out. The point of generating instead of
hand-writing: a macOS .keylayout alone carries eight modifier maps plus a
dead-key action table. Edit the letters in one map by hand, forget the other
seven, and six months later the layout types the wrong character under Option
and nobody knows why. Here every map is built from the same three rows.

    ./scripts/build-layouts.py             # → dist/
    ./scripts/build-layouts.py --install   # → dist/, and into ~/Library/…
    ./scripts/build-layouts.py --check     # rebuild in a temp dir and diff

Nothing here needs Colemak or Colemak-DH to be installed: the files are built
from scratch, not permuted out of someone else's bundle.
"""

import argparse
import filecmp
import plistlib
import shutil
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape
import json

ROOT = Path(__file__).resolve().parent.parent
LAYOUT = json.loads((ROOT / "layout.json").read_text(encoding="utf-8"))

NAME = LAYOUT["name"]
VERSION = LAYOUT["version"]
BUNDLE_ID = "com.colemakviet.keyboardlayout"

# macOS input-source ids are built from the <keyboard name=>, spaces stripped —
# NOT from the TISInputSourceID below, which is only a hint and was measured
# being ignored. Derive it the same way or print an id nothing resolves.
SOURCE_ID = f"{BUNDLE_ID}.keylayout.{NAME.replace(' ', '')}"

# Layout ids are a global namespace with no registry; a collision makes macOS
# serve the wrong layout. Picked from the private range, clear of the stock
# layouts and of Colemak DH ANSI (-7379).
LAYOUT_ID = "-25901"

# Physical key order, left to right, matching layout.json's rows.
QWERTY = {
    "top": "qwertyuiop",
    "home": "asdfghjkl;",
    "bottom": "zxcvbnm,./",
}

# macOS virtual keycodes, in the same physical order.
MAC_CODES = {
    "top": [12, 13, 14, 15, 17, 16, 32, 34, 31, 35],
    "home": [0, 1, 2, 3, 5, 4, 38, 40, 37, 41],
    "bottom": [6, 7, 8, 9, 11, 45, 46, 43, 47, 44],
}

# Windows scan codes, same physical order.
WIN_SCAN = {
    "top": ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
    "home": ["1e", "1f", "20", "21", "22", "23", "24", "25", "26", "27"],
    "bottom": ["2c", "2d", "2e", "2f", "30", "31", "32", "33", "34", "35"],
}

# XKB position names, same physical order.
XKB_POS = {
    "top": [f"AD{i:02d}" for i in range(1, 11)],
    "home": [f"AC{i:02d}" for i in range(1, 11)],
    "bottom": [f"AB{i:02d}" for i in range(1, 11)],
}

# Keys the layout does not move: they keep their ANSI positions and characters.
UNMOVED = {
    50: ("`", "~"), 18: ("1", "!"), 19: ("2", "@"), 20: ("3", "#"),
    21: ("4", "$"), 23: ("5", "%"), 22: ("6", "^"), 26: ("7", "&"),
    28: ("8", "*"), 25: ("9", "("), 29: ("0", ")"), 27: ("-", "_"),
    24: ("=", "+"), 33: ("[", "{"), 30: ("]", "}"), 42: ("\\", "|"),
    39: ("'", '"'),
    # The key left of Z on an ISO board, and § on an ANSI one.
    10: ("§", "±"),
}

SHIFTED = {";": ":", ",": "<", ".": ">", "/": "?", "'": '"'}

# Option layer, keyed by the LETTER rather than by the key, so it travels with
# the letter the way macOS users expect: Option+the key that types c gives ç.
OPTION = {
    "a": ("å", "Å"), "b": ("∫", "ı"), "c": ("ç", "Ç"), "d": ("∂", "Î"),
    "e": ("DEAD:acute", "DEAD:acute"), "f": ("ƒ", "Ï"), "g": ("©", "˝"),
    "h": ("˙", "Ó"), "i": ("DEAD:circ", "DEAD:circ"), "j": ("∆", "Ô"),
    "k": ("˚", ""), "l": ("¬", "Ò"), "m": ("µ", "Â"),
    "n": ("DEAD:tilde", "DEAD:tilde"), "o": ("ø", "Ø"), "p": ("π", "∏"),
    "q": ("œ", "Œ"), "r": ("®", "‰"), "s": ("ß", "Í"), "t": ("†", "ˇ"),
    "u": ("DEAD:uml", "DEAD:uml"), "v": ("√", "◊"), "w": ("∑", "„"),
    "x": ("≈", "˛"), "y": ("¥", "Á"), "z": ("Ω", "¸"),
    "`": ("DEAD:grave", "`"), "1": ("¡", "⁄"), "2": ("™", "€"), "3": ("£", "‹"),
    "4": ("¢", "›"), "5": ("∞", "ﬁ"), "6": ("§", "ﬂ"), "7": ("¶", "‡"),
    "8": ("•", "°"), "9": ("ª", "·"), "0": ("º", "‚"), "-": ("–", "—"),
    "=": ("≠", "±"), "[": ("“", "”"), "]": ("‘", "’"), "\\": ("«", "»"),
    ";": ("…", "Ú"), "'": ("æ", "Æ"), ",": ("≤", "¯"), ".": ("≥", "˘"),
    "/": ("÷", "¿"),
}

# Dead-key completions. Vietnamese itself is typed through a Telex input method
# (the IME reads characters, not key positions, so it needs nothing from here) —
# these exist so the layout is no worse than the stock US one for every other
# Latin language.
DEAD_STATES = {
    "grave": ("`", {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
                    "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù"}),
    "acute": ("´", {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý",
                    "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú", "Y": "Ý"}),
    "circ": ("ˆ", {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û",
                   "A": "Â", "E": "Ê", "I": "Î", "O": "Ô", "U": "Û"}),
    "tilde": ("˜", {"a": "ã", "n": "ñ", "o": "õ",
                    "A": "Ã", "N": "Ñ", "O": "Õ"}),
    "uml": ("¨", {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü", "y": "ÿ",
                  "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü", "Y": "Ÿ"}),
}

CONTROL = {"[": "\u001b", "\\": "\u001c", "]": "\u001d", "/": "\u001f"}


def letters():
    """(row, index, qwerty char, this layout's char) for every moved key."""
    for row in ("top", "home", "bottom"):
        for i, ch in enumerate(LAYOUT["rows"][row]):
            yield row, i, QWERTY[row][i], ch


def base_map():
    """macOS keycode → (unshifted, shifted) for the whole ANSI block."""
    out = dict(UNMOVED)
    for row, i, _, ch in letters():
        out[MAC_CODES[row][i]] = (ch, SHIFTED.get(ch, ch.upper()))
    return out


# ---------------------------------------------------------------- macOS

def _attr(value: str) -> str:
    """Quote an attribute value, control characters as numeric references.

    The stock Apple layouts declare XML 1.1 and write Return, Escape and the
    Control-letter codes as &#x000D; and friends. Written raw they are not legal
    XML at all, and macOS silently refuses to load the layout.
    """
    out = []
    for ch in value:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append(f"&#x{ord(ch):04X};")
        elif ch == "&":
            out.append("&amp;")
        elif ch == "<":
            out.append("&lt;")
        elif ch == '"':
            out.append("&quot;")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def _key(code: int, value: str, is_action: bool = False) -> str:
    attr = "action" if is_action else "output"
    return f'            <key code="{code}" {attr}={_attr(value)}/>'


def _composable(ch: str) -> bool:
    return any(ch in table for _, table in DEAD_STATES.values())


def _char_key(code: int, ch: str) -> str:
    """A character key — an action when a dead key can reach it, else output."""
    if _composable(ch):
        return _key(code, f"ch_{ch}", is_action=True)
    return _key(code, ch)


def _option_entry(code: int, value: str) -> str:
    if value.startswith("DEAD:"):
        return _key(code, f"dead_{value.split(':')[1]}", is_action=True)
    if value == "":
        return _key(code, "")  # Apple logo, as on the stock layout
    return _key(code, value)


def keylayout_xml() -> str:
    base = base_map()
    maps: list[list[str]] = [[] for _ in range(8)]

    for code, (plain, shift) in sorted(base.items()):
        maps[0].append(_char_key(code, plain))
        maps[1].append(_char_key(code, shift))
        maps[2].append(_char_key(code, shift if plain.isalpha() else plain))
        opt, sopt = OPTION.get(plain, (plain, shift))
        maps[3].append(_option_entry(code, opt))
        maps[4].append(_option_entry(code, sopt))
        maps[5].append(_option_entry(code, opt))
        maps[6].append(_key(code, plain))
        if plain.isalpha():
            maps[7].append(_key(code, chr(ord(plain.lower()) - 96)))
        elif plain in CONTROL:
            maps[7].append(_key(code, CONTROL[plain]))
        else:
            maps[7].append(_key(code, plain))

    # Keys every map shares: space completes a dead key, the rest are literal.
    fixed = {36: "\r", 48: "\t", 51: "\u0008", 53: "\u001b", 52: "\u0003"}
    for index, rows in enumerate(maps):
        rows.append(_key(49, "ch_space", is_action=True))
        for code, ch in fixed.items():
            rows.append(_key(code, ch))

    body = []
    for index, rows in enumerate(maps):
        body.append(f'        <keyMap index="{index}">')
        body.extend(sorted(rows, key=lambda line: int(line.split('"')[1])))
        body.append("        </keyMap>")

    actions = []
    composable = sorted({ch for _, table in DEAD_STATES.values() for ch in table})
    for ch in composable:
        whens = [f'            <when state="none" output={_attr(ch)}/>']
        for state, (_, table) in DEAD_STATES.items():
            if ch in table:
                whens.append(
                    f'            <when state="{state}" output={_attr(table[ch])}/>'
                )
        actions.append(f'        <action id="ch_{ch}">')
        actions.extend(whens)
        actions.append("        </action>")
    for state, (spacing, _) in DEAD_STATES.items():
        actions.append(f'        <action id="dead_{state}">')
        actions.append(f'            <when state="none" next="{state}"/>')
        actions.append("        </action>")
    actions.append('        <action id="ch_space">')
    actions.append('            <when state="none" output=" "/>')
    for state, (spacing, _) in DEAD_STATES.items():
        actions.append(
            f'            <when state="{state}" output={_attr(spacing)}/>'
        )
    actions.append("        </action>")

    terminators = [
        f'        <when state="{state}" output={_attr(spacing)}/>'
        for state, (spacing, _) in DEAD_STATES.items()
    ]

    return "\n".join([
        '<?xml version="1.1" encoding="UTF-8"?>',
        '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
        f'<keyboard group="126" id="{LAYOUT_ID}" name="{escape(NAME)}" maxout="2">',
        "    <layouts>",
        # One map set for every keyboard type. Apple's own layouts send the JIS
        # types to a second set that overrides ¥ and the two kana keys; this
        # layout moves no key those sets disagree about, so one set serves all.
        '        <layout first="0" last="255" mapSet="ansi" modifiers="modifiers"/>',
        "    </layouts>",
        '    <modifierMap id="modifiers" defaultIndex="0">',
        '        <keyMapSelect mapIndex="0">',
        '            <modifier keys="command?"/>',
        '            <modifier keys="anyShift? caps? command"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="1">',
        '            <modifier keys="anyShift caps?"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="2">',
        '            <modifier keys="caps"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="3">',
        '            <modifier keys="anyOption"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="4">',
        '            <modifier keys="anyShift caps? anyOption command?"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="5">',
        '            <modifier keys="caps anyOption"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="6">',
        '            <modifier keys="caps? anyOption command"/>',
        "        </keyMapSelect>",
        '        <keyMapSelect mapIndex="7">',
        '            <modifier keys="anyShift caps? option? command? control"/>',
        '            <modifier keys="shift? caps? anyOption command? control"/>',
        '            <modifier keys="caps? anyOption? command? control"/>',
        "        </keyMapSelect>",
        "    </modifierMap>",
        '    <keyMapSet id="ansi">',
        *body,
        "    </keyMapSet>",
        "    <actions>",
        *actions,
        "    </actions>",
        "    <terminators>",
        *terminators,
        "    </terminators>",
        "</keyboard>",
        "",
    ])


def write_macos(out: Path) -> None:
    layout = keylayout_xml()
    bundle = out / f"{NAME}.bundle"
    if bundle.exists():
        shutil.rmtree(bundle)
    resources = bundle / "Contents" / "Resources"
    resources.mkdir(parents=True)
    (resources / f"{NAME}.keylayout").write_text(layout, encoding="utf-8")
    info = {
        "CFBundleIdentifier": BUNDLE_ID,
        "CFBundleName": NAME,
        "CFBundleVersion": VERSION,
        "CFBundlePackageType": "BNDL",
        f"KLInfo_{NAME}": {
            "TISInputSourceID": SOURCE_ID,
            "TISIntendedLanguage": "en",
            "TICapsLockLanguageSwitchCapable": False,
        },
    }
    with (bundle / "Contents" / "Info.plist").open("wb") as handle:
        plistlib.dump(info, handle)
    (out / f"{NAME}.keylayout").write_text(layout, encoding="utf-8")


# ---------------------------------------------------------------- Windows

WIN_VK = {";": "OEM_1", "'": "OEM_7", ",": "OEM_COMMA", ".": "OEM_PERIOD",
          "/": "OEM_2"}


def write_windows(out: Path) -> None:
    rows = []
    for row, i, _, ch in letters():
        scan = WIN_SCAN[row][i]
        shift = SHIFTED.get(ch, ch.upper())
        if ch.isalpha():
            vk, cap = ch.upper(), "1"
        else:
            vk, cap = WIN_VK[ch], "0"
        rows.append(f"{scan}\t{vk}\t{cap}\t{ch}\t{shift}\t// {ch} {shift}")

    text = "\r\n".join([
        f'KBD\tclmkvi\t"{NAME}"',
        "",
        'COPYRIGHT\t"(c) Colemak-Viet contributors"',
        'COMPANY\t"colemak-viet"',
        'LOCALENAME\t"en-US"',
        'LOCALEID\t"00000409"',
        "VERSION\t1.0",
        "",
        "SHIFTSTATE",
        "",
        "0\t//Column 4",
        "1\t//Column 5 : Shft",
        "",
        "LAYOUT\t\t;an extra '@' at the end is a dead key",
        "",
        "//SC\tVK_\t\tCap\t0\t1",
        "//--\t----\t\t----\t----\t----",
        *rows,
        "",
        "DESCRIPTIONS",
        "",
        f"0409\t{NAME}",
        "",
        "LANGUAGENAMES",
        "",
        "0409\tEnglish (United States)",
        "",
        "ENDKBD",
        "",
    ])
    (out / "colemak-viet.klc").write_bytes(text.encode("utf-16-le"))


# ---------------------------------------------------------------- Linux

XKB_NAMES = {";": "semicolon", ",": "comma", ".": "period", "/": "slash",
             ":": "colon", "<": "less", ">": "greater", "?": "question"}


def _xkb(ch: str) -> str:
    return XKB_NAMES.get(ch, ch)


def write_linux(out: Path) -> None:
    keys = []
    for row, i, _, ch in letters():
        shift = SHIFTED.get(ch, ch.upper())
        pos = XKB_POS[row][i]
        keys.append(
            f"    key <{pos}> {{ [ {_xkb(ch)}, {_xkb(shift)} ] }};"
        )
    text = "\n".join([
        "// Colemak-Viet — Colemak with the DH mod, retuned for Vietnamese Telex.",
        "//",
        "// Install: copy this file to /usr/share/X11/xkb/symbols/colemak_viet",
        "// then:    setxkbmap colemak_viet",
        "// (see README for the systemd/Wayland notes)",
        "",
        "default partial alphanumeric_keys",
        'xkb_symbols "basic" {',
        '    include "us(basic)"',
        f'    name[Group1] = "English (Colemak-Viet)";',
        "",
        *keys,
        "",
        '    include "level3(ralt_switch)"',
        "};",
        "",
    ])
    (out / "colemak_viet").write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- Karabiner

KARABINER_NAMES = {";": "semicolon", ",": "comma", ".": "period", "/": "slash"}


def write_karabiner(out: Path) -> None:
    manipulators = []
    for row, i, qwerty, ch in letters():
        if qwerty == ch:
            continue
        manipulators.append({
            "type": "basic",
            "from": {"key_code": KARABINER_NAMES.get(qwerty, qwerty),
                     "modifiers": {"optional": ["any"]}},
            "to": [{"key_code": KARABINER_NAMES.get(ch, ch)}],
        })
    rule = {
        "title": f"{NAME} keyboard layout",
        "rules": [{
            "description": f"{NAME} — Colemak-DH retuned for Vietnamese Telex",
            "manipulators": manipulators,
        }],
    }
    (out / "colemak-viet.json").write_text(
        json.dumps(rule, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------- driver

def build(dist: Path) -> None:
    for sub, writer in (("macos", write_macos), ("windows", write_windows),
                        ("linux", write_linux), ("karabiner", write_karabiner)):
        target = dist / sub
        target.mkdir(parents=True, exist_ok=True)
        writer(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--install", action="store_true",
                        help="also install the macOS bundle into "
                             "~/Library/Keyboard Layouts (no logout needed)")
    parser.add_argument("--check", action="store_true",
                        help="build into a temp dir and fail if dist/ differs")
    args = parser.parse_args()

    if not args.check:
        build(args.out)
        print(f"wrote {args.out}")
        if args.install:
            target = Path.home() / "Library" / "Keyboard Layouts"
            target.mkdir(parents=True, exist_ok=True)
            bundle = target / f"{NAME}.bundle"
            if bundle.exists():
                shutil.rmtree(bundle)
            shutil.copytree(args.out / "macos" / f"{NAME}.bundle", bundle)
            print(f"installed {bundle}")
            print("add it in System Settings → Keyboard → Input Sources")
        print(f"macOS input source id: {SOURCE_ID}")
        return

    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "dist"
        build(fresh)
        diff = filecmp.dircmp(fresh, args.out)
        stale = []

        def walk(cmp_result: filecmp.dircmp, prefix: str = "") -> None:
            stale.extend(prefix + n for n in cmp_result.diff_files)
            stale.extend(prefix + n for n in cmp_result.left_only)
            stale.extend(prefix + n for n in cmp_result.right_only)
            for name, sub in cmp_result.subdirs.items():
                walk(sub, f"{prefix}{name}/")

        walk(diff)
        if stale:
            raise SystemExit("dist/ is stale, rerun the build: " + ", ".join(stale))
        print("dist/ matches layout.json")


if __name__ == "__main__":
    main()

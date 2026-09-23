// Ask macOS what the installed Colemak-Viet layout actually types.
//
//     ./scripts/build-layouts.py --out ~/Library/Keyboard\ Layouts
//     swift scripts/verify-macos-layout.swift
//
// A .keylayout that parses is not a .keylayout that works: macOS will register
// a file and then serve something else from cache, and Carbon calls here return
// noErr whether or not they did anything. So this reads the layout data back
// out of Text Input Sources and runs UCKeyTranslate on it — the same call the
// system makes for a keystroke — and compares every key against layout.json.

import Carbon
import Foundation

let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent()
    .deletingLastPathComponent()
let sourceID = "com.colemakviet.keyboardlayout.keylayout.Colemak-Viet"

// Physical key order, matching scripts/build-layouts.py.
let codes: [String: [Int]] = [
    "top": [12, 13, 14, 15, 17, 16, 32, 34, 31, 35],
    "home": [0, 1, 2, 3, 5, 4, 38, 40, 37, 41],
    "bottom": [6, 7, 8, 9, 11, 45, 46, 43, 47, 44],
]

struct Layout: Decodable {
    struct Rows: Decodable { let top: String, home: String, bottom: String }
    let rows: Rows
}

let layout = try JSONDecoder().decode(
    Layout.self, from: Data(contentsOf: root.appendingPathComponent("layout.json")))
let expected: [String: String] = [
    "top": layout.rows.top, "home": layout.rows.home, "bottom": layout.rows.bottom,
]

let filter = [kTISPropertyInputSourceID as String: sourceID] as CFDictionary
guard let list = TISCreateInputSourceList(filter, true)?.takeRetainedValue() as? [TISInputSource],
      let source = list.first else {
    print("not installed: \(sourceID)")
    print("run ./scripts/build-layouts.py --out ~/Library/Keyboard\\ Layouts first")
    exit(1)
}

guard let raw = TISGetInputSourceProperty(source, kTISPropertyUnicodeKeyLayoutData) else {
    print("no uchr data — macOS did not parse the layout")
    exit(1)
}
let data = Unmanaged<CFData>.fromOpaque(raw).takeUnretainedValue() as Data

func type(_ keyCode: Int, shift: Bool = false) -> String {
    var deadState: UInt32 = 0
    var length = 0
    var chars = [UniChar](repeating: 0, count: 8)
    let modifiers = UInt32(shift ? (shiftKey >> 8) : 0)
    let status = data.withUnsafeBytes { buffer -> OSStatus in
        let uchr = buffer.baseAddress!.assumingMemoryBound(to: UCKeyboardLayout.self)
        return UCKeyTranslate(uchr, UInt16(keyCode), UInt16(kUCKeyActionDown), modifiers,
                              UInt32(LMGetKbdType()), 0, &deadState, chars.count,
                              &length, &chars)
    }
    guard status == noErr else { return "<err \(status)>" }
    return String(utf16CodeUnits: chars, count: length)
}

var failures = 0
for row in ["top", "home", "bottom"] {
    let want = Array(expected[row]!)
    var got = ""
    for (index, code) in codes[row]!.enumerated() {
        let char = type(code)
        got += char
        if char != String(want[index]) {
            print("row \(row) position \(index + 1): expected \(want[index]), got \(char)")
            failures += 1
        }
        let upper = type(code, shift: true)
        let wantUpper = [",": "<", ".": ">", "/": "?", ";": ":"][String(want[index])]
            ?? String(want[index]).uppercased()
        if upper != wantUpper {
            print("row \(row) position \(index + 1) shifted: expected \(wantUpper), got \(upper)")
            failures += 1
        }
    }
    print("\(row.padding(toLength: 7, withPad: " ", startingAt: 0)) \(got)")
}

// The shortcut constraint the layout is built around: Cmd+C/V/S/T/R/A/Z must
// stay reachable by the left hand alone.
let leftCodes = Set(codes["top"]!.prefix(5) + codes["home"]!.prefix(5) + codes["bottom"]!.prefix(5))
for letter in ["c", "v", "s", "t", "r", "a", "z", "x"] {
    let onLeft = leftCodes.contains { type($0) == letter }
    if !onLeft {
        print("shortcut letter \(letter) is not on the left half")
        failures += 1
    }
}

print(failures == 0 ? "\nOK — the system types this layout" : "\n\(failures) mismatch(es)")
exit(failures == 0 ? 0 : 1)

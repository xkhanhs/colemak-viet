# Contributing

The layout itself lives in one file, [`layout.json`](layout.json). Everything in
`dist/` is generated from it by `scripts/build-layouts.py`, so:

**Never edit a file in `dist/` by hand.** Change `layout.json` or the builder,
rerun the build, and commit both. `./scripts/build-layouts.py --check` fails if
`dist/` and `layout.json` have drifted apart.

```bash
./scripts/build-layouts.py     # rebuild
./scripts/test-layouts.py      # read all four outputs back and compare
```

## The most useful thing you can send

The Windows and Linux files have never been run by anyone. If you install one
and a key is wrong — or the file will not compile or load at all — please open
an issue saying what you did and what happened. That is worth more than a
carefully argued change to the letter positions.

## Changing where letters go

Bring a measurement. `./scripts/score-layouts.py` scores any arrangement you add
to its `LAYOUTS` table, on Vietnamese and on English. Two things to know before
reading its output as a verdict:

- Differences under about 2% are inside this model's noise — re-scored against a
  different corpus and effort grid, margins moved that much while rankings held.
- Some constraints are deliberate and not visible in the score: the Cmd-shortcut
  letters stay on the left half, and the Telex mark keys `s f r x j` keep their
  standard places. [docs/comparison.md](docs/comparison.md) says why, including
  what it cost to keep them.

#!/usr/bin/env python3
"""The GPS Swears It Was a Shortcut — entry program.

Writes one original GPS excuse to entry.txt.

The bounty gate (kit RULES.txt): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. This program writes a fixed
string, so every run produces byte-identical output. No network, no
randomness, no clock reads, standard library only.
"""

import os
import sys

ENTRY = "That cul-de-sac was a shortcut on the 2019 map \u2014 I can't help it if they built a house, a fence, and a very angry dog on it since."

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    if not MIN_CHARS <= len(ENTRY) <= MAX_CHARS:
        print(
            "entry is %d characters, outside the 1-200 gate" % len(ENTRY),
            file=sys.stderr,
        )
        return 1
    if not ENTRY.strip():
        print("entry is only white space", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        # An excuse is one spoken line: a stray newline would break the
        # gate's "one text" reading and the judge's side-by-side display.
        print("entry must be a single line", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip():
        # Leading or trailing white space would waste the judge's reading
        # and could push the entry over the gate on a recount.
        print("entry has leading or trailing white space", file=sys.stderr)
        return 1
    if any(ord(c) < 32 for c in ENTRY):
        print("entry holds a control character", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back what was written and verify it is exactly the entry:
    # a silent truncation or encoding slip must fail loudly, not ship.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        print("entry.txt does not match the entry after writing", file=sys.stderr)
        return 1
    if not MIN_CHARS <= len(written) <= MAX_CHARS:
        print(
            "entry.txt is %d characters, outside the 1-200 gate" % len(written),
            file=sys.stderr,
        )
        return 1
    import hashlib

    print(
        "wrote entry.txt: %d characters, sha256 %s"
        % (len(written), hashlib.sha256(written.encode("utf-8")).hexdigest())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

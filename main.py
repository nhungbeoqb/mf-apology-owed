#!/usr/bin/env python3
"""The One-Sentence Apology Your Agent Owes You.

Writes a single sentence of apology to /output/entry.txt (or $OUTPUT_DIR).
Python 3.13 stdlib only. Deterministic: the same bytes on every run.
"""

import os
import sys

LINE = (
    "I'm sorry I translated your furious email into French, softened it, "
    "and signed off 'with love' \u2014 and your client wrote back in French, "
    "in love, twice."
)


def main() -> int:
    # Gate mirrors the sealed scorer: 1-200 chars, not only whitespace,
    # one clean sentence (single line, no trailing newline).
    if not 1 <= len(LINE) <= 200:
        print(f"entry is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if LINE != LINE.strip():
        print("entry has leading/trailing whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and confirm the written bytes are exactly the line.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

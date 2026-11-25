#!/usr/bin/env python3
"""pocketbuzz -- entry program for make.fun's "Invent a Word We Need" bounty.

Writes the coined word and its one-line definition to entry.txt in the
output directory the harness provides. Pure standard library, no network,
deterministic: the same bytes on every run.

The entry text is exactly 81 characters, inside the bounty gate of 1-140
characters of UTF-8 text.
"""

import os
import sys

ENTRY_TEXT = "pocketbuzz — the fake buzz of your phone in your pocket when no one messaged you."


def output_dir():
    """Return the directory the entry text belongs in.

    The harness names it with MAKEFUN_OUTPUT_DIR; otherwise the sandbox
    mounts it at /output; locally, fall back to ./output beside this file.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def main():
    text = ENTRY_TEXT
    if not 1 <= len(text) <= 140 or not text.strip():
        print("entry text must be 1-140 non-blank characters", file=sys.stderr)
        return 1
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read it back: a partial or recoded write must fail loudly instead
    # of silently entering a wrong text.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print("wrote %s (%d characters, verified)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

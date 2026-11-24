#!/usr/bin/env python3
"""news-23 b21 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != PNG_SIG:
        print("entry.png: bad PNG signature", file=sys.stderr)
        return 1
    # Parse IHDR chunk: length (4) + type (4) + data (13) + CRC (4).
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        print("entry.png: bad IHDR", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        print("entry.png: expected 1024x1024, got %dx%d" % (w, h), file=sys.stderr)
        return 1
    # Trailer must be a well-formed 12-byte IEND chunk.
    if data[-12:-8] != struct.pack(">I", 0) or data[-8:-4] != b"IEND":
        print("entry.png: bad IEND trailer", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    # Guard: never write into the repo itself (the grader runs from a
    # read-only copy, so writing next to main.py must fail loudly instead).
    repo = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == repo or os.path.abspath(out_dir).startswith(repo + os.sep):
        print("refusing to write into the repo dir", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    # Re-read and confirm the output is byte-identical to the source.
    with open(dst, "rb") as f:
        if f.read() != data:
            print("output differs from source", file=sys.stderr)
            return 1
    print("wrote %s (%d bytes, 1024x1024)" % (dst, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

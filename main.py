#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with /bot read-only and a writable output
directory in MAKEFUN_OUTPUT_DIR, so the program must never write next to
itself: the only output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    width, height = png_size(dst)
    if (width, height) != (1024, 1024):
        print(f"bad size: {width}x{height}", file=sys.stderr)
        return 1
    if not os.path.exists(SRC):
        print(f"missing source image: {SRC}", file=sys.stderr)
        return 1
    if sha256(SRC) != sha256(dst):
        print("sha256 mismatch", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} ({width}x{height}, {os.path.getsize(dst)} bytes, "
          f"sha256 {sha256(dst)[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

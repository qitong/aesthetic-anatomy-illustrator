#!/usr/bin/env python3
"""
Local de-identification for clinical face photographs.

Adds an opaque rounded eye-occlusion bar BEFORE any image is sent to a cloud
image model. Purely local: no network access, no deletion, no writes outside
the declared output path, and the original file is never modified.

Usage:
  python deidentify_portrait.py photo.jpg --out photo_deidentified.png
  python deidentify_portrait.py front.jpg oblique.jpg profile.jpg --out-dir masked/
  python deidentify_portrait.py photo.jpg --wide
  python deidentify_portrait.py photo.jpg --bar 100 260 400 380

Bar coordinates are expressed in a 500x650 reference frame (standardized
frontal clinical portrait) and scaled proportionally to the actual image size.
Override with --ref-width / --ref-height for a different framing.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REF_W, REF_H = 500, 650
DEFAULT_BAR = (118, 296, 382, 340)  # narrow: eye fissures + upper nasal bridge
WIDE_BAR = (100, 262, 400, 378)     # stricter: brows down to infraorbital skin


def scale_box(box, w, h, ref_w, ref_h):
    sx, sy = w / ref_w, h / ref_h
    return tuple(round(v * (sx if i % 2 == 0 else sy)) for i, v in enumerate(box))


def deidentify(src, dst, box, color, radius, ref_w, ref_h, force=False):
    if not src.is_file():
        raise FileNotFoundError(f"input not found: {src}")
    if dst.resolve() == src.resolve():
        raise ValueError(f"refusing to overwrite the original: {src}")
    if dst.exists() and not force:
        raise FileExistsError(f"output exists (use --force): {dst}")

    im = Image.open(src).convert("RGB")
    w, h = im.size
    scaled = scale_box(box, w, h, ref_w, ref_h)
    r = max(0, round(radius * min(w / ref_w, h / ref_h)))
    ImageDraw.Draw(im).rounded_rectangle(scaled, radius=r, fill=tuple(color))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst)
    return (w, h), scaled


def main():
    p = argparse.ArgumentParser(
        description="Add a local eye-occlusion bar to clinical face photos before any upload."
    )
    p.add_argument("inputs", nargs="+", type=Path, help="one or more source photos")
    p.add_argument("--out", type=Path, help="output file (only with a single input)")
    p.add_argument("--out-dir", type=Path, help="output directory for batch mode")
    p.add_argument("--suffix", default="_deidentified", help="batch filename suffix")
    p.add_argument("--wide", action="store_true",
                   help="wider bar covering brows to infraorbital skin")
    p.add_argument("--bar", nargs=4, type=int, metavar=("X1", "Y1", "X2", "Y2"),
                   help="custom bar in the 500x650 reference frame")
    p.add_argument("--ref-width", type=int, default=REF_W)
    p.add_argument("--ref-height", type=int, default=REF_H)
    p.add_argument("--color", nargs=3, type=int, default=[15, 15, 15],
                   metavar=("R", "G", "B"))
    p.add_argument("--radius", type=int, default=8)
    p.add_argument("--force", action="store_true",
                   help="allow overwriting an existing output")
    args = p.parse_args()

    if args.out and len(args.inputs) != 1:
        p.error("--out requires exactly one input; use --out-dir for batch mode")
    if args.bar and args.wide:
        p.error("--bar and --wide are mutually exclusive")

    box = tuple(args.bar) if args.bar else (WIDE_BAR if args.wide else DEFAULT_BAR)
    if not (0 <= box[0] < box[2] <= args.ref_width and 0 <= box[1] < box[3] <= args.ref_height):
        p.error(f"invalid bar {box} for reference frame {args.ref_width}x{args.ref_height}")
    if any(c < 0 or c > 255 for c in args.color):
        p.error("--color values must be 0-255")

    ok = 0
    for src in args.inputs:
        if args.out:
            dst = args.out
        elif args.out_dir:
            dst = args.out_dir / f"{src.stem}{args.suffix}.png"
        else:
            dst = src.with_name(f"{src.stem}{args.suffix}.png")
        try:
            size, scaled = deidentify(src, dst, box, args.color, args.radius,
                                      args.ref_width, args.ref_height, args.force)
            print(f"[OK] {src.name} {size[0]}x{size[1]} -> {dst}  bar={scaled}")
            ok += 1
        except Exception as e:
            print(f"[FAIL] {src}: {e}", file=sys.stderr)
    print(f"Done: {ok}/{len(args.inputs)} de-identified. Originals untouched.")
    return 0 if ok == len(args.inputs) else 1


if __name__ == "__main__":
    sys.exit(main())

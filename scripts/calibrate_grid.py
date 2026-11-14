#!/usr/bin/env python3
"""
Coordinate Calibration Grid Generator for Precision SVG Leader-Line Annotation.

Why this exists:
When placing SVG anchor dots and leader lines onto a newly generated or cropped
anatomical portrait, guessing pixel coordinates by eye leads to 30-80px drift
(e.g., an arrow meant for the Nasolabial Fat Compartment lands on the upper lip).

This script overlays a dual-scale coordinate ruler grid (major lines every 100px,
minor lines every 50px, or mapped to a target SVG viewBox like 1280x720) onto
an image and saves a temporary inspection copy (`*_grid.png`).
The agent inspects the grid image once, reads the exact (x, y) coordinates of
every anatomical target, and writes 100% pinpoint SVG coordinates into the
HTML template.

Usage:
  # Overlay native pixel grid on a generated portrait
  python scripts/calibrate_grid.py generated_base.png --out generated_base_grid.png

  # Map coordinates directly to a target SVG viewBox (e.g. 1280x720 or 550x715)
  python scripts/calibrate_grid.py portrait_crop.png --viewbox 550 715 --out portrait_grid.png
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def draw_calibration_grid(src: Path, dst: Path, viewbox: tuple[int, int] | None,
                          step: int = 50, major: int = 100):
    if not src.is_file():
        raise FileNotFoundError(f"input image not found: {src}")

    im = Image.open(src).convert("RGBA")
    w, h = im.size
    vw, vh = viewbox if viewbox else (w, h)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Vertical grid lines (X coordinates)
    for vx in range(0, vw + 1, step):
        px = round(vx * w / vw)
        is_major = (vx % major == 0)
        color = (0, 240, 255, 175) if is_major else (255, 255, 255, 85)
        width = 2 if is_major else 1
        draw.line([(px, 0), (px, h)], fill=color, width=width)
        if is_major and vx > 0:
            # Top & middle X labels
            for ly in (6, h // 2):
                draw.rectangle([(px + 2, ly), (px + 34, ly + 15)], fill=(0, 0, 0, 190))
                draw.text((px + 4, ly + 2), f"x{vx}", fill=(0, 245, 255, 255))

    # Horizontal grid lines (Y coordinates)
    for vy in range(0, vh + 1, step):
        py = round(vy * h / vh)
        is_major = (vy % major == 0)
        color = (255, 210, 0, 175) if is_major else (255, 255, 255, 85)
        width = 2 if is_major else 1
        draw.line([(0, py), (w, py)], fill=color, width=width)
        if is_major and vy > 0:
            # Left & middle Y labels
            for lx in (6, w // 2):
                draw.rectangle([(lx, py + 2), (lx + 34, py + 17)], fill=(0, 0, 0, 190))
                draw.text((lx + 3, py + 3), f"y{vy}", fill=(255, 220, 40, 255))

    # Center crosshair
    cx, cy = w // 2, h // 2
    draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], outline=(255, 60, 60, 230), width=2)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst)
    return (w, h), (vw, vh)


def main():
    ap = argparse.ArgumentParser(
        description="Overlay a pixel/viewBox coordinate calibration grid onto an anatomical base image."
    )
    ap.add_argument("input", type=Path, help="source anatomical base image")
    ap.add_argument("--out", type=Path, help="output grid image path (default: <stem>_grid.png)")
    ap.add_argument("--viewbox", nargs=2, type=int, metavar=("VW", "VH"),
                    help="target SVG viewBox dimensions if different from image pixel size")
    ap.add_argument("--step", type=int, default=50, help="minor grid step (default: 50)")
    ap.add_argument("--major", type=int, default=100, help="major labeled grid step (default: 100)")
    args = ap.parse_args()

    dst = args.out if args.out else args.input.with_name(f"{args.input.stem}_grid.png")
    vb = tuple(args.viewbox) if args.viewbox else None
    img_sz, vb_sz = draw_calibration_grid(args.input, dst, vb, args.step, args.major)
    print(f"[OK] Calibration grid saved to {dst} (image={img_sz[0]}x{img_sz[1]}, coord_space={vb_sz[0]}x{vb_sz[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Standard Anatomical Spatial Guide & Atlas Generator for Medical Aesthetics.

Why this exists:
Generic text-to-image models reliably render large surface muscles and bones,
but frequently misplace or distort fine/deep structures such as superficial fat
compartments (nasolabial, medial cheek, middle cheek, jowl), deep fat pads
(SOOF, DMCF, Ristow's space), retaining ligaments (ORL, zygomatic, mandibular),
and vascular danger zones.

This script provides two modes:
1. --mode atlas   : Generates a clean, standardized anatomical reference diagram
                    (with exact polygon geometry and boundaries in a 500x650 frame)
                    that can be inspected or passed as a visual reference image to
                    multimodal image generators.
2. --mode overlay : Overlays semi-transparent anatomical compartment geometry
                    onto an existing (already de-identified!) portrait photo to
                    serve as a spatial control guide for image-to-image generation.

Purely local PIL execution. No network calls.

Usage:
  # List all built-in presets and individual structure keys
  python scripts/build_anatomy_guide.py --list

  # Generate a standalone reference atlas card for superficial fat compartments
  python scripts/build_anatomy_guide.py --preset superficial_fat --out atlas_superficial_fat.png

  # Overlay midface fat + ligament spatial guides onto a de-identified portrait
  python scripts/build_anatomy_guide.py --base front_deidentified.png --preset midface_fat_ligaments --out guide_overlay.png --alpha 0.38

  # Select specific custom structures (comma-separated) on right/left/both sides
  python scripts/build_anatomy_guide.py --preset custom --structures nasolabial_fat,medial_cheek_fat,orl_ligament,zygomatic_ligament --side right --out custom_guide.png
"""
import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REF_W, REF_H = 500, 650

# Canonical right-hemiface polygons/polylines in a 500x650 frontal portrait frame
# (Midline x = 250; subject's left / viewer's right is x > 250; mirrored automatically for viewer's left x < 250)
# Landmark anchors in 500x650:
#   Glabella: (250, 265) | Medial canthus: (282, 315) | Lateral canthus: (355, 312)
#   Inferior orbital rim arc: (280, 338) -> (320, 348) -> (360, 335)
#   Nasal ala base: (278, 398) | Mouth corner: (292, 468) | Chin tip: (250, 548)
#   Zygomatic arch: (365, 348) -> (412, 355) | Mandibular angle: (392, 488)

STRUCTURES = {
    # --- Superficial Fat Compartments (Pale Golden Yellow) ---
    "nasolabial_fat": {
        "name_zh": "鼻唇沟浅层脂肪室",
        "name_en": "Nasolabial Superficial Fat",
        "kind": "polygon",
        "color": (246, 208, 92),
        "outline": (255, 245, 200),
        "points": [(282, 342), (308, 348), (324, 412), (308, 456), (288, 442), (279, 392)],
        "desc": "Oblique teardrop strip hugging lateral nasal ala above nasolabial crease",
    },
    "medial_cheek_fat": {
        "name_zh": "内侧颊浅层脂肪室",
        "name_en": "Medial Cheek Superficial Fat",
        "kind": "polygon",
        "color": (242, 196, 78),
        "outline": (255, 245, 200),
        "points": [(311, 350), (354, 344), (358, 398), (327, 424), (325, 408)],
        "desc": "Inverted-triangle wedge at central malar apex lateral to nasolabial fat",
    },
    "middle_cheek_fat": {
        "name_zh": "中间颊浅层脂肪室",
        "name_en": "Middle Cheek Superficial Fat",
        "kind": "polygon",
        "color": (235, 184, 68),
        "outline": (255, 245, 200),
        "points": [(357, 348), (388, 356), (384, 448), (344, 462), (329, 426), (360, 400)],
        "desc": "Broad vertical compartment over mid-lateral cheek",
    },
    "lateral_temporal_cheek_fat": {
        "name_zh": "外侧颞颊浅层脂肪室",
        "name_en": "Lateral Temporal-Cheek Fat",
        "kind": "polygon",
        "color": (228, 175, 62),
        "outline": (255, 245, 200),
        "points": [(386, 265), (412, 275), (410, 478), (384, 488), (386, 358)],
        "desc": "Long vertical strip anterior to ear from temple to mandibular angle",
    },
    "jowl_fat": {
        "name_zh": "口角下/下颌缘浅层脂肪室(羊腮)",
        "name_en": "Superior & Inferior Jowl Fat",
        "kind": "polygon",
        "color": (240, 190, 75),
        "outline": (255, 245, 200),
        "points": [(308, 462), (342, 464), (352, 526), (314, 536), (298, 505)],
        "desc": "Drooping ovoid fat compartment lateral to marionette line crossing jawline",
    },
    "forehead_fat": {
        "name_zh": "额部浅层脂肪室",
        "name_en": "Forehead Superficial Fat",
        "kind": "polygon",
        "color": (244, 204, 88),
        "outline": (255, 245, 200),
        "points": [(252, 168), (348, 176), (356, 255), (252, 258)],
        "desc": "Flat vertical forehead adipose compartments separated by septa",
    },

    # --- Deep Fat Compartments (Amber Gold / Deeper Orange-Gold) ---
    "soof_medial_lateral": {
        "name_zh": "眼轮匝肌下深层脂肪垫(内/外侧SOOF)",
        "name_en": "Medial & Lateral SOOF (Deep)",
        "kind": "polygon",
        "color": (218, 142, 38),
        "outline": (255, 226, 160),
        "points": [(284, 340), (324, 349), (366, 338), (368, 362), (324, 368), (284, 356)],
        "desc": "Two-lobed crescentic deep fat pad on bone immediately below ORL",
    },
    "dmcf_deep": {
        "name_zh": "深层内侧颊脂垫(DMCF)",
        "name_en": "Deep Medial Cheek Fat (DMCF)",
        "kind": "polygon",
        "color": (208, 128, 32),
        "outline": (255, 220, 150),
        "points": [(288, 362), (326, 370), (322, 418), (290, 412)],
        "desc": "Triangular deep fat cushion on anterior maxilla beneath levator muscles",
    },
    "ristow_pyriform": {
        "name_zh": "梨状孔深层空间(Ristow空间)",
        "name_en": "Deep Pyriform Space (Ristow)",
        "kind": "polygon",
        "color": (196, 110, 28),
        "outline": (255, 215, 140),
        "points": [(272, 382), (288, 384), (290, 412), (272, 408)],
        "desc": "Compact crescentic deep space on bone around lateral pyriform aperture",
    },
    "buccal_fat": {
        "name_zh": "颊脂垫(Bichat深部脂垫)",
        "name_en": "Buccal Fat Pad (Deep)",
        "kind": "polygon",
        "color": (212, 136, 42),
        "outline": (255, 224, 155),
        "points": [(346, 408), (376, 410), (378, 456), (344, 458)],
        "desc": "Rounded encapsulated deep fat pad anterior to masseter border",
    },

    # --- Retaining Ligaments (Pearlescent White Thick Tether Lines) ---
    "orl_ligament": {
        "name_zh": "眼轮匝肌支持韧带(ORL/泪沟韧带)",
        "name_en": "Orbicularis Retaining Ligament (ORL)",
        "kind": "polyline",
        "color": (250, 250, 255),
        "width": 5,
        "points": [(278, 334), (305, 344), (335, 345), (364, 333)],
        "desc": "Curved white fibrous tether along inferior orbital rim (tear trough boundary)",
    },
    "zygomatic_ligament": {
        "name_zh": "颧皮韧带/颧弓韧带",
        "name_en": "Zygomatic Cutaneous Ligament",
        "kind": "polyline",
        "color": (245, 248, 255),
        "width": 5,
        "points": [(318, 372), (355, 362), (396, 354)],
        "desc": "Oblique white fibrous shelf ~1cm below orbital rim (midcheek Indian groove)",
    },
    "maxillary_ligament": {
        "name_zh": "上颌支持韧带",
        "name_en": "Maxillary Retaining Ligament",
        "kind": "polyline",
        "color": (245, 248, 255),
        "width": 4,
        "points": [(278, 396), (294, 435)],
        "desc": "Deep fibrous tether along upper nasolabial crease beside nasal ala",
    },
    "masseteric_ligaments": {
        "name_zh": "咬肌皮韧带列",
        "name_en": "Masseteric Cutaneous Ligaments",
        "kind": "polyline",
        "color": (242, 246, 255),
        "width": 4,
        "points": [(372, 385), (370, 428), (366, 476)],
        "desc": "Vertical row of fibrous tethers along anterior border of masseter",
    },
    "mandibular_ligament": {
        "name_zh": "下颌骨支持韧带",
        "name_en": "Mandibular Retaining Ligament",
        "kind": "polyline",
        "color": (250, 250, 255),
        "width": 6,
        "points": [(288, 514), (308, 522)],
        "desc": "Strong osteocutaneous tether on anterior mandible medial to jowl fat",
    },

    # --- Vascular Danger Zones (Crimson Red Cylindrical Vessels) ---
    "facial_angular_artery": {
        "name_zh": "面动脉-内眦动脉主干",
        "name_en": "Facial-to-Angular Artery",
        "kind": "polyline",
        "color": (225, 38, 52),
        "width": 4,
        "points": [(352, 522), (334, 492), (312, 466), (298, 432), (284, 394), (278, 352), (276, 318)],
        "desc": "Tortuous crimson artery from mandibular notch past mouth corner up nasolabial fold",
    },
    "supratrochlear_supraorbital_artery": {
        "name_zh": "滑车上/眶上动脉",
        "name_en": "Supratrochlear & Supraorbital a.",
        "kind": "polyline",
        "color": (225, 38, 52),
        "width": 3,
        "points": [(276, 282), (272, 225), (268, 175)],
        "desc": "Vertical forehead arteries emerging from medial supraorbital rim",
    },
    "superficial_temporal_artery": {
        "name_zh": "颞浅动脉额支",
        "name_en": "Superficial Temporal Artery",
        "kind": "polyline",
        "color": (225, 38, 52),
        "width": 3,
        "points": [(408, 355), (402, 295), (382, 238), (352, 192)],
        "desc": "Oblique artery ascending in front of ear across temple toward forehead",
    },
}

PRESETS = {
    "superficial_fat": {
        "title": "浅层脂肪室标准几何图谱 (Superficial Fat Compartments)",
        "keys": [
            "forehead_fat",
            "nasolabial_fat",
            "medial_cheek_fat",
            "middle_cheek_fat",
            "lateral_temporal_cheek_fat",
            "jowl_fat",
        ],
    },
    "deep_fat": {
        "title": "深层脂肪室标准几何图谱 (Deep Fat Compartments)",
        "keys": [
            "soof_medial_lateral",
            "dmcf_deep",
            "ristow_pyriform",
            "buccal_fat",
        ],
    },
    "retaining_ligaments": {
        "title": "面部五大支持韧带图谱 (Retaining Ligaments)",
        "keys": [
            "orl_ligament",
            "zygomatic_ligament",
            "maxillary_ligament",
            "masseteric_ligaments",
            "mandibular_ligament",
        ],
    },
    "midface_fat_ligaments": {
        "title": "中下面部脂肪室与支持韧带卡压关系 (Fat + Ligaments)",
        "keys": [
            "nasolabial_fat",
            "medial_cheek_fat",
            "middle_cheek_fat",
            "jowl_fat",
            "orl_ligament",
            "zygomatic_ligament",
            "mandibular_ligament",
        ],
    },
    "danger_vessels": {
        "title": "面部高危动脉血管走行图谱 (Vascular Danger Zones)",
        "keys": [
            "facial_angular_artery",
            "supratrochlear_supraorbital_artery",
            "superficial_temporal_artery",
        ],
    },
}


def scale_pt(pt, w, h, mirror=False):
    x, y = pt
    if mirror:
        x = REF_W - x
    return (round(x * w / REF_W), round(y * h / REF_H))


def draw_reference_face_silhouette(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Draw a clean anatomical reference silhouette in standalone atlas mode."""
    def sp(x, y):
        return (round(x * w / REF_W), round(y * h / REF_H))

    # Face contour oval
    face_pts = [
        sp(250, 125), sp(335, 140), sp(398, 205), sp(414, 305),
        sp(404, 415), sp(386, 488), sp(325, 538), sp(250, 555),
        sp(175, 538), sp(114, 488), sp(96, 415), sp(86, 305),
        sp(102, 205), sp(165, 140),
    ]
    draw.polygon(face_pts, fill=(44, 38, 35, 255), outline=(120, 108, 98, 255))

    # Midline dashed guide
    for y in range(125, 560, 12):
        draw.line([sp(250, y), sp(250, min(y + 6, 555))], fill=(90, 82, 76, 180), width=1)

    # Brows, orbital rims, nose, lips landmarks
    for side in (-1, 1):
        def m(x, y):
            rx = 250 + side * (x - 250)
            return sp(rx, y)

        # Brow
        draw.line([m(268, 272), m(315, 260), m(368, 274)], fill=(140, 126, 115, 220), width=3)
        # Eye fissure
        draw.polygon([m(282, 315), m(318, 304), m(355, 312), m(318, 322)],
                     outline=(155, 140, 128, 220), fill=(28, 24, 22, 255))
        # Inferior orbital rim dotted arc
        draw.line([m(278, 334), m(318, 346), m(364, 333)], fill=(110, 100, 92, 180), width=1)
        # Nasal ala
        draw.line([m(250, 310), m(250, 388), m(278, 398), m(250, 404)],
                  fill=(145, 130, 120, 220), width=2)

    # Mouth
    draw.polygon([sp(208, 468), sp(250, 458), sp(292, 468), sp(250, 482)],
                 outline=(155, 132, 125, 220), fill=(68, 48, 46, 255))


def render_guide(base_path: Path | None, keys: list[str], side: str,
                 alpha: float, out_path: Path):
    if base_path:
        base = Image.open(base_path).convert("RGBA")
    else:
        base = Image.new("RGBA", (1000, 1300), (24, 22, 20, 255))
        sil = ImageDraw.Draw(base)
        draw_reference_face_silhouette(sil, base.width, base.height)

    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    mirrors = []
    if side in ("right", "both"):
        mirrors.append(False)  # viewer's right (x > 250)
    if side in ("left", "both"):
        mirrors.append(True)   # viewer's left (x < 250)

    fill_a = max(30, min(235, round(255 * alpha)))
    line_a = max(140, min(255, round(255 * min(1.0, alpha + 0.35))))
    scale_factor = min(w / REF_W, h / REF_H)

    for key in keys:
        spec = STRUCTURES[key]
        for mir in mirrors:
            pts = [scale_pt(p, w, h, mirror=mir) for p in spec["points"]]
            if spec["kind"] == "polygon":
                rgba = spec["color"] + (fill_a,)
                out_rgba = spec["outline"] + (line_a,)
                draw.polygon(pts, fill=rgba, outline=out_rgba)
                # Draw subtle septal border line
                draw.line(pts + [pts[0]], fill=out_rgba, width=max(2, round(2 * scale_factor)))
            elif spec["kind"] == "polyline":
                lw = max(2, round(spec.get("width", 4) * scale_factor))
                # High-contrast dark under-stroke + bright main stroke
                draw.line(pts, fill=(20, 18, 16, line_a), width=lw + 2)
                draw.line(pts, fill=spec["color"] + (line_a,), width=lw)

    composed = Image.alpha_composite(base, overlay)

    # In standalone atlas mode, draw a crisp legend box at the bottom
    if not base_path:
        leg = ImageDraw.Draw(composed)
        y0 = h - 36 * len(keys) - 30
        leg.rectangle([(24, y0 - 12), (w - 24, h - 16)], fill=(18, 16, 15, 225), outline=(90, 82, 74, 255))
        for idx, key in enumerate(keys):
            spec = STRUCTURES[key]
            yy = y0 + idx * 32
            leg.rectangle([(40, yy), (64, yy + 20)], fill=spec["color"] + (255,), outline=(255, 255, 255, 200))
            label = f"{idx + 1}. {spec['name_zh']} ({spec['name_en']}) — {spec['desc']}"
            leg.text((78, yy + 2), label, fill=(235, 228, 220, 255))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    composed.convert("RGB").save(out_path)
    return composed.size


def main():
    ap = argparse.ArgumentParser(
        description="Build anatomical spatial reference cards or image-to-image guide overlays."
    )
    ap.add_argument("--list", action="store_true", help="list all presets and structure keys")
    ap.add_argument("--base", type=Path, help="optional de-identified portrait image to overlay onto")
    ap.add_argument("--preset", default="midface_fat_ligaments",
                    choices=list(PRESETS.keys()) + ["custom"],
                    help="anatomical preset group")
    ap.add_argument("--structures", help="comma-separated structure keys when --preset custom")
    ap.add_argument("--side", default="both", choices=["left", "right", "both"],
                    help="which side of the image to draw (default: both)")
    ap.add_argument("--alpha", type=float, default=0.45,
                    help="overlay opacity 0.1-0.9 (default: 0.45)")
    ap.add_argument("--out", type=Path, default=Path("anatomy_guide.png"),
                    help="output PNG path")
    args = ap.parse_args()

    if args.list:
        print("=== Built-in Presets ===")
        for k, v in PRESETS.items():
            print(f"  {k:24s} : {v['title']} -> {', '.join(v['keys'])}")
        print("\n=== Individual Structure Keys ===")
        for k, v in STRUCTURES.items():
            print(f"  {k:34s} : {v['name_zh']} ({v['name_en']})")
        return 0

    if args.preset == "custom":
        if not args.structures:
            ap.error("--preset custom requires --structures key1,key2,...")
        keys = [s.strip() for s in args.structures.split(",") if s.strip()]
        unknown = [k for k in keys if k not in STRUCTURES]
        if unknown:
            ap.error(f"unknown structure keys: {unknown}. Run with --list to see valid keys.")
    else:
        keys = PRESETS[args.preset]["keys"]

    size = render_guide(args.base, keys, args.side, args.alpha, args.out)
    mode_str = f"overlay on {args.base.name}" if args.base else "standalone reference atlas"
    print(f"[OK] Generated {mode_str} ({size[0]}x{size[1]}) with {len(keys)} structures -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

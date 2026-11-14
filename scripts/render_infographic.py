#!/usr/bin/env python3
"""
将 templates/ 下的医美解剖 HTML/SVG 标注模板一键渲染为 4K 超高清 PNG 图片。
支持两种渲染引擎（自动优先使用本机无头 Chrome，零依赖极速出图；若无则自动回退至 Playwright）：
1. macOS / Linux 本机 Google Chrome Headless（免安装任何浏览器驱动）
2. Python Playwright Chromium

用法:
  python scripts/render_infographic.py templates/type_b_layered_cutaway.html output.png
  python scripts/render_infographic.py templates/type_a_biomechanics_overlay.html output.png --width 1280 --height 720 --scale 3
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return str(c)
    return None


def render_with_chrome(chrome_bin: str, html_path: Path, output_png: Path,
                       width: int, height: int, scale: int) -> bool:
    abs_uri = html_path.resolve().as_uri()
    out_abs = output_png.resolve()
    out_abs.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--force-device-scale-factor={scale}",
        f"--window-size={width},{height}",
        "--virtual-time-budget=4000",
        f"--screenshot={out_abs}",
        abs_uri,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0 and out_abs.is_file()


def render_with_playwright(html_path: Path, output_png: Path,
                           width: int, height: int, scale: int) -> None:
    from playwright.sync_api import sync_playwright

    abs_uri = html_path.resolve().as_uri()
    output_png.resolve().parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page.goto(abs_uri, wait_until="networkidle")
        canvas = page.locator(".canvas")
        if canvas.count() > 0:
            canvas.first.screenshot(path=str(output_png))
        else:
            page.screenshot(path=str(output_png))
        browser.close()


def main():
    ap = argparse.ArgumentParser(description="Render HTML/SVG medical anatomy template to 4K PNG.")
    ap.add_argument("html_path", type=Path, help="input HTML file")
    ap.add_argument("output_png", type=Path, help="output PNG file")
    ap.add_argument("--width", type=int, default=1280, help="viewport width (default: 1280)")
    ap.add_argument("--height", type=int, default=720, help="viewport height (default: 720)")
    ap.add_argument("--scale", type=int, default=3, help="device scale factor (default: 3 for 4K)")
    ap.add_argument("--engine", choices=["auto", "chrome", "playwright"], default="auto")
    args = ap.parse_args()

    if not args.html_path.is_file():
        print(f"[Error] HTML file not found: {args.html_path}", file=sys.stderr)
        return 1

    chrome_bin = find_chrome()
    if args.engine in ("auto", "chrome") and chrome_bin:
        ok = render_with_chrome(chrome_bin, args.html_path, args.output_png,
                               args.width, args.height, args.scale)
        if ok:
            print(f"[Success] High-res ({args.width*args.scale}x{args.height*args.scale}) PNG rendered via Chrome Headless -> {args.output_png}")
            return 0
        if args.engine == "chrome":
            print("[Error] Chrome headless rendering failed.", file=sys.stderr)
            return 1

    render_with_playwright(args.html_path, args.output_png, args.width, args.height, args.scale)
    print(f"[Success] High-res ({args.width*args.scale}x{args.height*args.scale}) PNG rendered via Playwright -> {args.output_png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

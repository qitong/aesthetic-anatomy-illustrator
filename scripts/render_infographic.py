#!/usr/bin/env python3
"""
将 templates/ 下的医美解剖 HTML/SVG 标注模板一键渲染为 4K 超高清 PNG 图片。
依赖安装: pip install playwright && playwright install chromium
用法: python scripts/render_infographic.py templates/type_a_biomechanics_overlay.html output.png
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def render_html_to_png(html_path: str, output_png: str, scale: int = 3):
    abs_html = Path(html_path).resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=scale  # 3x 缩放直接输出 3840x2160 (4K) 印刷级清晰度
        )
        page.goto(abs_html, wait_until="networkidle")
        canvas = page.locator(".canvas")
        canvas.screenshot(path=output_png)
        browser.close()
    print(f"[Success] High-res 4K medical aesthetic illustration saved to: {output_png}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_infographic.py <input_template.html> <output.png>")
        sys.exit(1)
    render_html_to_png(sys.argv[1], sys.argv[2])

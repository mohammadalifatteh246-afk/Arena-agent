#!/usr/bin/env python3
"""
24 FPS Frame Generator & Compressor for 'APIs & Backends Explained'.
Renders 24-fps sequence frames and high-res scene master graphics,
then passes them through LosslessImageOptimizer to slash file size without visual quality loss.
"""

import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT.parent))

from ytvideos.src.image_optimizer import LosslessImageOptimizer


SCENES = [
    {
        "id": 1,
        "title": "THE INVISIBLE MESSENGER",
        "subtitle": "Client Request & The 40ms Journey",
        "tag": "API (Application Programming Interface)",
        "theme": "dark",
        "color_primary": (99, 102, 241),      # Indigo/Cyan
        "color_accent": (236, 72, 153),       # Pink
        "bg_color": (11, 15, 25),             # Dark Blue/Grey
    },
    {
        "id": 2,
        "title": "DINING ROOM VS KITCHEN",
        "subtitle": "Frontend Interface vs Backend Database",
        "tag": "Architecture Anatomy",
        "theme": "split",
        "color_primary": (16, 185, 129),      # Emerald
        "color_accent": (245, 158, 11),       # Amber
        "bg_color": (15, 23, 42),
    },
    {
        "id": 3,
        "title": "WHICH PROTOCOL WHERE?",
        "subtitle": "REST (GET/POST) vs WebSockets",
        "tag": "Real-World Delivery Example",
        "theme": "vector",
        "color_primary": (6, 182, 212),       # Cyan
        "color_accent": (168, 85, 247),       # Purple
        "bg_color": (10, 10, 20),
    },
    {
        "id": 4,
        "title": "THE INTELLIGENT ENGINE",
        "subtitle": "Global Cloud Server Constellation",
        "tag": "Security & Scaling",
        "theme": "climax",
        "color_primary": (239, 68, 68),       # Red/Orange
        "color_accent": (249, 115, 22),       # Orange
        "bg_color": (5, 7, 15),
    }
]


def render_stylized_scene_png(scene: dict, output_path: Path, width: int = 1920, height: int = 1080):
    img = Image.new("RGBA", (width, height), scene["bg_color"])
    draw = ImageDraw.Draw(img)

    # 1. Subtle High-Tech Vector Grid Lines
    for x in range(160, width, 240):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 20), width=1)
    for y in range(100, height, 180):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 20), width=1)

    # 2. Concentric Center Orbital Visual Rings
    cx, cy = width // 2, height // 2
    for r in [280, 200, 120]:
        draw.ellipse(
            [(cx - r, cy - r), (cx + r, cy + r)],
            outline=scene["color_primary"] + (80,),
            width=2
        )

    # Central Core Node
    core_r = 50
    draw.ellipse(
        [(cx - core_r, cy - core_r), (cx + core_r, cy + core_r)],
        fill=scene["color_accent"] + (200,),
        outline=(255, 255, 255, 240),
        width=3
    )

    # 3. Typography & Badges
    # Draw scene tag badge
    badge_text = f" ACT {scene['id']} // {scene['tag']} "
    draw.rectangle([(width // 2 - 250, 280), (width // 2 + 250, 320)], fill=(0, 0, 0, 180), outline=scene["color_primary"], width=2)
    draw.text((width // 2, 300), badge_text, anchor="mm", fill=(255, 255, 255, 240))

    # Main Title
    draw.text((width // 2, 400), scene["title"], anchor="mm", fill=(255, 255, 255, 255))
    # Subtitle
    draw.text((width // 2, 680), scene["subtitle"], anchor="mm", fill=scene["color_primary"] + (240,))

    # 4. 24 FPS Calibration Tag
    draw.text((100, height - 60), "24.00 FPS CALIBRATION // BEYONDSUMI VECTOR ENGINE", fill=(255, 255, 255, 120))
    draw.text((width - 100, height - 60), f"SCENE 0{scene['id']} / 04", anchor="ra", fill=(255, 255, 255, 160))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")
    return output_path


def render_scene_svg_frame(scene: dict, output_path: Path, frame_idx: int, total_frames: int):
    width, height = 1920, 1080
    progress = frame_idx / max(1, total_frames)
    bar_width = int(progress * (width - 200))
    hex_prim = "#{:02x}{:02x}{:02x}".format(*scene["color_primary"])
    hex_acc = "#{:02x}{:02x}{:02x}".format(*scene["color_accent"])

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090D1A"/>
      <stop offset="100%" stop-color="#141E33"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#bg)"/>
  <!-- Vector Grid -->
  <g stroke="{hex_prim}" stroke-opacity="0.15" stroke-width="1">
    <line x1="200" y1="0" x2="200" y2="{height}"/>
    <line x1="{width//2}" y1="0" x2="{width//2}" y2="{height}"/>
    <line x1="{width-200}" y1="0" x2="{width-200}" y2="{height}"/>
  </g>
  <!-- Orbit Ring -->
  <circle cx="{width//2}" cy="{height//2}" r="220" fill="none" stroke="{hex_prim}" stroke-width="2" stroke-dasharray="10 8" opacity="0.4"/>
  <circle cx="{width//2}" cy="{height//2}" r="60" fill="{hex_acc}" opacity="0.8"/>
  <text x="{width//2}" y="{height//2 - 90}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="48" font-weight="800" fill="#FFFFFF">
    {scene["title"]}
  </text>
  <text x="{width//2}" y="{height//2 + 130}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="24" font-weight="600" fill="{hex_prim}">
    {scene["subtitle"].upper()}
  </text>
  <!-- Progress Bar (24 FPS) -->
  <rect x="100" y="{height - 60}" width="{bar_width}" height="6" rx="3" fill="{hex_acc}"/>
  <text x="{width - 100}" y="{height - 50}" text-anchor="end" font-family="monospace" font-size="14" fill="#FFFFFF" opacity="0.6">
    24 FPS FRAME {frame_idx:04d} / {total_frames:04d}
  </text>
</svg>"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
    return output_path


def generate_and_optimize():
    images_dir = WORKSPACE_ROOT / "assets" / "images"
    svg_dir = WORKSPACE_ROOT / "assets" / "svg_frames"
    images_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)

    print("\n[+] Step 1: Rendering high-resolution scene master images & 24 FPS frames...")
    generated_pngs = []
    generated_svgs = []

    for i, sc in enumerate(SCENES, 1):
        png_path = images_dir / f"api_backend_scene_{i:02d}.png"
        render_stylized_scene_png(sc, png_path)
        generated_pngs.append(png_path)
        print(f"  - Rendered PNG: {png_path.name}")

        # Render 24 fps sequential vector frames
        svg_path = svg_dir / f"api_backend_24fps_scene_{i:02d}.svg"
        render_scene_svg_frame(sc, svg_path, frame_idx=i * 24, total_frames=len(SCENES) * 24)
        generated_svgs.append(svg_path)
        print(f"  - Rendered SVG (24fps cadence): {svg_path.name}")

    print("\n[+] Step 2: Applying Lossless Image & Vector Optimization (Zero Quality Drop)...")
    optimizer = LosslessImageOptimizer()
    
    # 1. Optimize PNGs with max DEFLATE
    png_stats = [optimizer.optimize_png_lossless(p) for p in generated_pngs]
    # 2. Also convert to Lossless WebP to show maximum size reduction option
    webp_stats = [optimizer.convert_to_lossless_webp(p) for p in generated_pngs]
    # 3. Minify SVGs
    svg_stats = [optimizer.optimize_svg_lossless(s) for s in generated_svgs]

    total_saved = sum(s["bytes_saved"] for s in png_stats + webp_stats + svg_stats)
    print(f"\n[+] Optimization Results:")
    print(f"  - Total Files Processed: {len(png_stats) + len(webp_stats) + len(svg_stats)}")
    print(f"  - Total Bandwidth / Storage Saved: {total_saved:,} Bytes")
    for s in png_stats:
        print(f"    * {s['file']}: {s['original_bytes']:,} B -> {s['optimized_bytes']:,} B ({s['percent_saved']}% reduction)")
    for s in webp_stats:
        print(f"    * {s['output_file']}: {s['original_bytes']:,} B -> {s['optimized_bytes']:,} B ({s['percent_saved']}% reduction, Lossless WebP)")


if __name__ == "__main__":
    generate_and_optimize()

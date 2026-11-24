"""
Visual Engine for BeyondSumi YouTube Automation.
Provides:
1. Production visual prompts for LMArena Agent Mode image generation (Sumi Original, Sumi Light, Sumi Dark).
2. Code-driven SVG Vector Frame Renderer (Zero external tool requirement).
"""

from pathlib import Path
from typing import Dict, Any, List


class BeyondSumiVisualEngine:
    STYLE_MODIFIERS = {
        "sumi_original": (
            "Japanese anime aesthetic, vibrant digital painting, colorful atmospheric lighting, "
            "Makoto Shinkai and Studio Ghibli cinematic composition, highly detailed expressive linework"
        ),
        "sumi_light": (
            "Soft pencil sketch rendering, gentle watercolor wash, storybook illustration, "
            "warm minimal color palette, innocent emotional atmosphere, ideal for children's storytelling"
        ),
        "sumi_dark": (
            "Traditional Japanese Sumi-e brush-style ink wash rendering, heavy ink splatters, "
            "stark chiaroscuro contrast, haunting monochrome with subtle crimson accents, ominous documentary mood"
        ),
        "svg_code": (
            "Pure vector geometric illustration, sharp SVG paths, neon cybernetic accents, "
            "mathematical grid aesthetics, modular token architecture"
        )
    }

    def format_arena_image_prompt(self, scene_description: str, style: str = "sumi_original", camera_angle: str = "cinematic wide angle") -> str:
        """Constructs an optimized visual prompt for LMArena Image Generation."""
        modifier = self.STYLE_MODIFIERS.get(style, self.STYLE_MODIFIERS["sumi_original"])
        return f"{scene_description}, {camera_angle}, {modifier}, 8k resolution, cinematic lighting, masterpiece --ar 16:9"

    def render_svg_frame(self, title: str, subtitle: str, frame_index: int, total_frames: int, theme: str = "dark") -> str:
        """
        Renders a code-driven SVG frame without any external image generation tools.
        Enables 100% free vector video frames.
        """
        bg_color = "#0B0F19" if theme == "dark" else "#F7FAFC"
        text_color = "#E2E8F0" if theme == "dark" else "#1A202C"
        accent_color = "#6366F1" if theme == "dark" else "#4F46E5"
        secondary_accent = "#EC4899"

        progress_width = int((frame_index / max(1, total_frames)) * 1800)

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="100%" height="100%">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}" />
      <stop offset="100%" stop-color="#1E1B4B" />
    </linearGradient>
    <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_color}" />
      <stop offset="100%" stop-color="{secondary_accent}" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1920" height="1080" fill="url(#bg-grad)" />

  <!-- Animated Vector Grids / Nodes -->
  <g stroke="{accent_color}" stroke-opacity="0.15" stroke-width="1">
    <line x1="160" y1="0" x2="160" y2="1080" />
    <line x1="960" y1="0" x2="960" y2="1080" />
    <line x1="1760" y1="0" x2="1760" y2="1080" />
    <line x1="0" y1="200" x2="1920" y2="200" />
    <line x1="0" y1="880" x2="1920" y2="880" />
  </g>

  <!-- Center Decorative Vector Arc -->
  <circle cx="960" cy="540" r="280" fill="none" stroke="{accent_color}" stroke-width="2" stroke-dasharray="12 8" opacity="0.4" />
  <circle cx="960" cy="540" r="160" fill="none" stroke="{secondary_accent}" stroke-width="3" filter="url(#glow)" opacity="0.7" />

  <!-- Typography -->
  <text x="960" y="490" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="54" font-weight="bold" fill="{text_color}" letter-spacing="2">
    {title}
  </text>
  <text x="960" y="580" text-anchor="middle" font-family="'Segoe UI', Roboto, Helvetica, sans-serif" font-size="28" fill="{accent_color}" opacity="0.9" letter-spacing="4">
    {subtitle.upper()}
  </text>

  <!-- Frame progress bar -->
  <rect x="60" y="1020" width="{progress_width}" height="6" rx="3" fill="url(#bar-grad)" />
  <text x="1860" y="1030" text-anchor="end" font-family="monospace" font-size="16" fill="{text_color}" opacity="0.6">
    FRAME {frame_index:04d} / {total_frames:04d}
  </text>
</svg>"""
        return svg_content

    def export_svg_frame(self, output_path: Path, title: str, subtitle: str, frame_index: int, total_frames: int):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        svg = self.render_svg_frame(title, subtitle, frame_index, total_frames)
        output_path.write_text(svg, encoding="utf-8")
        return output_path

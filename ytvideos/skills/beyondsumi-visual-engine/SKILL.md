---
name: beyondsumi-visual-engine
description: Use when generating, engineering prompts for, or rendering visual assets in the 4 BeyondSumi art styles (Sumi Original, Sumi Light, Sumi Dark, SVG Code Mode) for automated video workflows.
---

# BeyondSumi Visual Engine: Art Styles, Prompts & SVG Vector Frames

## Overview
The BeyondSumi visual paradigm replaces expensive, slow 3D video generation tools (Runway, Pika, Sora) with **artistic, frame-based illustrations and code-driven SVG vector rendering**. This keeps per-video generation costs at or near **\$0.00**, completely bypasses generic AI video artifacts, and produces distinct, copyright-clean, monetizable YouTube content.

---

## The 4 Core Art Styles

| Style | Aesthetic & Technique | Frame Rate | Ideal Niches & Use Cases |
| :--- | :--- | :--- | :--- |
| **1. Sumi Original** | Vibrant Japanese digital anime, rich lighting, Makoto Shinkai / Ghibli atmospheric color palette. | 16–24 fps | Anime recaps, high-concept tech journeys, inspirational narratives, lore breakdowns. |
| **2. Sumi Light** | Soft pencil sketch, delicate charcoal hatching, gentle watercolor wash, storybook minimalism. | 8–16 fps | Children's stories, heartfelt moral tales, philosophical essays, bedtime calm. |
| **3. Sumi Dark** | Traditional Japanese Sumi-e brush ink wash, stark chiaroscuro, heavy ink splatters, crimson accents. | 12–16 fps | Horror, true crime, historical mysteries, dystopian science, dark documentaries. |
| **4. SVG Code Mode** | 100% programmatic vector graphics generated via Python code. Zero image tools or external APIs required. | 16–24 fps | Tech explainers, mathematical breakdowns, zero-budget channels, fallback modes. |

---

## Prompt Construction Formulas

When sending generation requests to LMArena Agent Mode:

### Formula for Sumi Original (Anime):
```
[Subject/Action], [Specific Environment], vibrant Japanese digital anime aesthetic, 
Makoto Shinkai atmospheric lighting, luminous particle embers, cinematic wide angle, 
clean expressive linework, highly detailed, 8k resolution, cinematic color grading --ar 16:9
```

### Formula for Sumi Light (Pencil Sketch):
```
[Subject/Action], soft pencil sketch rendering, fine charcoal hatching on textured handmade paper, 
minimalist pastel watercolor accents, warm natural daylight, nostalgic storybook illustration, 
expressive emotional composition, timeless art style --ar 16:9
```

### Formula for Sumi Dark (Ink Wash / Mystery):
```
[Subject/Action], traditional Japanese Sumi-e ink wash painting, dynamic black ink brush strokes, 
expressive ink splatter texture, stark dramatic chiaroscuro contrast, haunting monochrome with subtle blood-crimson highlights, 
cinematic atmospheric fog, ominous documentary aesthetic --ar 16:9
```

---

## Character & Scene Consistency Rules

1. **The Seed Invariant:** When invoking image generation across multiple scenes featuring the same character, lock physical descriptors:
   - Specific clothing tags: *"wearing a worn indigo haori with silver stitch on the collar"*.
   - Distinctive facial markers: *"sharp amber eyes, slight scar across bridge of nose"*.
2. **Palette Cohesion:** Maintain identical background lighting tokens across consecutive scenes (e.g., *"dawn golden hour over misty pines"*).

---

## Code-Driven SVG Vector Frame Generation (Zero-Cost Mode)

When image generation APIs are unavailable or zero token spend is required, the Visual Engine directly synthesizes SVG code vector frames:

```python
def generate_vector_frame(title: str, subtitle: str, progress: float, theme: str = "dark") -> str:
    """
    Renders pure SVG vector frame without calling any external image model.
    """
    bg = "#0A0D14" if theme == "dark" else "#FFFFFF"
    accent = "#6366F1"
    width = int(progress * 1800)
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
      <rect width="100%" height="100%" fill="{bg}"/>
      <circle cx="960" cy="540" r="220" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="8 6" opacity="0.5"/>
      <text x="960" y="520" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="52" font-weight="bold" fill="#E2E8F0">
        {title}
      </text>
      <text x="960" y="580" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="26" fill="{accent}">
        {subtitle.upper()}
      </text>
      <rect x="60" y="1030" width="{width}" height="4" fill="{accent}"/>
    </svg>"""
```

---

## Quality Gate Checklist

- [ ] Every prompt specifies aspect ratio (`--ar 16:9` for landscape or `--ar 9:16` for Shorts).
- [ ] No generic AI buzzwords ("photorealistic, trending on artstation") that trigger plastic AI looks.
- [ ] Art style remains consistent within a single chapter or transitions deliberately as a pattern interrupt.
- [ ] SVG fallback frames render with valid XML and viewBox coordinates.

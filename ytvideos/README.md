# 📺 ytvideos — YouTube Automation Workspace

> **Dedicated YouTube Video Automation Engine** inside `Arena-agent`.  
> Combines the **BeyondSumi Video Framework** (Frame-by-frame rendering, procedural sound, and strong emotional storytelling) with **LMArena Agent Mode** for **100% Free Image & Audio Generation**.

---

## 🏗️ Architecture

```
                                  ┌──────────────────────────────┐
                                  │      Google Antigravity      │
                                  │   (Orchestrator & Director)  │
                                  └──────────────┬───────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────┐
                                  │      ytvideos Workspace      │
                                  │    (D:/Arena-agent/ytvideos) │
                                  └──────┬───────────────┬───────┘
                                         │               │
                 Free Images & Narration │               │ Procedural Audio & SVGs
                                         ▼               ▼
                       ┌────────────────────────┐  ┌────────────────────────┐
                       │   LMArena Agent Mode   │  │ BeyondSumi Core Engine │
                       │ (.agent/CURRENT_TASK)  │  │ - Procedural Sound     │
                       │ - Free AI Image Gen    │  │ - 4 Visual Art Styles  │
                       │ - Free AI Audio / TTS  │  │ - 16-24 FPS Vector/SVG │
                       └────────────────────────┘  └────────────────────────┘
```

---

## 📁 Directory Structure

```text
ytvideos/
├── pipeline_config.json      # Video resolution, frame rates, and generation provider rules
├── generate_video.py         # Main entrypoint to generate a full video production package
├── references/
│   └── 24FPS_BATCH_FORMULA.md # Official mathematical specification for 24 FPS image batching
├── src/
│   ├── __init__.py
│   ├── arena_bridge.py       # Interfaces with LMArena Agent Mode via GitHub Shared Bus
│   ├── batch_calculator.py   # Dynamic 24 FPS frame & micro-batch calculator (4 batches/sec)
│   ├── story_engine.py       # High-retention scriptwriting engine (Story > Graphics)
│   ├── visual_engine.py      # BeyondSumi art prompt generator & SVG vector frame renderer
│   ├── audio_engine.py       # Algorithmic Python audio synthesizer (Zero-cost, royalty-free)
│   └── assembler.py          # Asset packager and YouTube metadata compiler
├── assets/
│   ├── audio/                # Procedural ambient drones, attention whooshes, zaps
│   ├── images/               # LMArena-generated scene illustrations
│   └── svg_frames/           # Standalone SVG code-driven vector frames
├── scripts/                  # Production markdown scripts & scene breakdowns
├── renders/                  # Final production packages and video manifests
└── thumbnails/               # YouTube thumbnails
```

---

## 🎨 BeyondSumi 4 Art Styles Supported

1. **Sumi Original:** Japanese anime digital painting style, vibrant atmospheric lighting.
2. **Sumi Light:** Gentle pencil sketch rendering, storybook illustration (ideal for kids/bedtime stories).
3. **Sumi Dark:** Traditional Japanese Sumi-e brush ink wash rendering (ideal for horror, crime, mystery, dark documentaries).
4. **SVG Code Mode:** Pure code-driven vector graphics that need zero external image generation tools.

---

## 🚀 How to Run

### Local Generation (Procedural Audio + SVG Frames + LMArena Task Dispatch):
```bash
python D:/Arena-agent/ytvideos/generate_video.py
```

### Full Cloud Dispatch (Pushes work order to GitHub for Arena Cloud Agent):
```bash
python D:/Arena-agent/ytvideos/generate_video.py --push
```

---

## 📐 24 FPS Frame & Micro-Batching Standard

To respect Arena's $\le 10$ image batch ceiling while maintaining cinematic 24 FPS smoothness:
- **Total Frames:** $T_{\text{frames}} = 24 \times S$
- **Total Micro-Batches:** $N_{\text{batches}} = 4 \times S$ (at 6 images per batch)
- **Batch Duration:** 250 ms per batch ($0.25\text{s}$)
- **Frame Duration:** 41.67 ms per frame ($\approx 0.04167\text{s}$)

See detailed specification in [`references/24FPS_BATCH_FORMULA.md`](references/24FPS_BATCH_FORMULA.md).

```bash
# Calculate frames, micro-batches, and storage for any duration (e.g. 90 seconds):
python ytvideos/src/batch_calculator.py --seconds 90
```

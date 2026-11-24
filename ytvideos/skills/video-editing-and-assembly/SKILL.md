---
name: video-editing-and-assembly
description: Use when assembling, editing, stitching frames and audio, generating dynamic captions, or packaging completed video files for YouTube publication.
---

# Video Editing, Frame Assembly & YouTube Packaging

## Overview
The assembly stage takes all upstream assets—script text, visual frames (illustrations or SVGs), voiceover narration, and procedural soundscapes—and compiles them into a finalized, high-retention video ready for YouTube publication.

This skill covers:
1. **Frame-by-Frame Sequencing (16-24 FPS)**.
2. **Audio/Visual Beat Matching & Music Ducking**.
3. **High-Retention Dynamic Subtitles (Active Word Highlighting)**.
4. **YouTube Packaging (Metadata, Tags, Thumbnails)**.

---

## 1. Frame-by-Frame Assembly Pipeline

```
  Visual Frames (PNG / SVG) ───┐
                               ├────► [Video Assembler Engine] ───► Final MP4
  Voiceover + Procedural WAV ──┘      - 16-24 FPS Sequencing         - 1080p / 4K
                                      - Audio Ducking (-6dB)        - -14 LUFS Mastered
                                      - Kinetic Subtitles           - Packaged Manifest
```

### Frame Rate Calibration
- **Shorts / Fast-Paced Anime (Sumi Original):** 24 FPS (Smooth action motion).
- **Documentary / Drama (Sumi Dark):** 16 FPS (Cinematic, deliberate weight).
- **Storybook / Sketch (Sumi Light):** 8–12 FPS (Hand-drawn stop-motion aesthetic, minimal token spend).

---

## 2. Dynamic Captioning & Subtitle Styling

Modern YouTube retention benchmarks indicate that over **70% of mobile users watch with partial or muted sound**. Dynamic captions are mandatory for retention.

### Styling Invariants:
- **Font:** Bold, clean sans-serif (e.g., *Montserrat ExtraBold*, *Poppins*, or *Impact*).
- **Placement:** Lower third (`y = 80%`), centered horizontally.
- **Word Chunking:** Never display more than **3 to 5 words simultaneously**. Long blocks of text cause reading cognitive load and drop retention.
- **Kinetic Highlighting:** The active spoken word lights up with bright accent color (`#FACC15` Yellow or `#22D3EE` Cyan), while inactive words remain white (`#FFFFFF`) with a subtle black stroke/shadow.

---

## 3. Python Frame & Audio Assembly Recipe

When assembling using standard Python video compilation or FFmpeg wrappers:

```python
import subprocess
from pathlib import Path

def compile_frames_to_video(
    frame_pattern: str,
    audio_path: str,
    output_mp4: str,
    fps: int = 16,
    resolution: str = "1920x1080"
):
    """
    Assembles image/SVG sequence and audio into high-efficiency YouTube-ready MP4 (H.264 / AAC).
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", frame_pattern,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-s", resolution,
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    subprocess.run(cmd, check=True)
```

---

## 4. YouTube Publishing Package Manifest

Every completed video assembly generates an upload manifest:

```json
{
  "video_file": "ytvideos/renders/the_day_a_single_token_awoke.mp4",
  "thumbnail_file": "ytvideos/thumbnails/the_day_a_single_token_awoke_thumb.png",
  "youtube_metadata": {
    "title": "What REALLY Happens Inside an AI Model in 60 Seconds ⚡",
    "description": "An emotional journey inside a transformer neural network...\n\n#AI #BeyondSumi #MachineLearning",
    "tags": ["Transformers", "Artificial Intelligence", "Deep Learning", "BeyondSumi"],
    "category": "Science & Technology",
    "privacy_status": "public",
    "made_for_kids": false
  },
  "compliance_verification": {
    "audio_lufs": -14.1,
    "true_peak_dbtp": -1.1,
    "copyright_audio_risk": "0% (Procedural Synth)",
    "visual_uniqueness_score": "High (Original BeyondSumi Art)"
  }
}
```

---

## Assembly Quality Gate Checklist

- [ ] Video duration strictly matches voiceover duration (no dangling black frames).
- [ ] Music bed ducks by at least -6dB whenever voiceover is active.
- [ ] Subtitles are large, legible, and chunked into 3-5 words maximum.
- [ ] Export is formatted in H.264 (yuv420p) with AAC audio at -14 LUFS.

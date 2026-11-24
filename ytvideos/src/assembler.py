"""
Video Production Assembler & Packager for ytvideos.
Compiles scene assets, procedural audio tracks, SVG fallback frames, and YouTube metadata.
"""

import json
from pathlib import Path
from typing import Dict, Any

from ytvideos.src.audio_engine import ProceduralAudioEngine
from ytvideos.src.visual_engine import BeyondSumiVisualEngine


class VideoProductionAssembler:
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.audio_engine = ProceduralAudioEngine()
        self.visual_engine = BeyondSumiVisualEngine()

        self.assets_dir = self.workspace_root / "assets"
        self.audio_dir = self.assets_dir / "audio"
        self.images_dir = self.assets_dir / "images"
        self.svg_dir = self.assets_dir / "svg_frames"
        self.renders_dir = self.workspace_root / "renders"
        self.scripts_dir = self.workspace_root / "scripts"

    def assemble_production_package(self, script_data: Dict[str, Any]) -> Path:
        """
        Builds all procedural audio assets, generates SVG frames for each scene,
        and saves a production package manifest.
        """
        title = script_data["title"]
        slug = title.lower().replace(" ", "_")[:30]
        package_dir = self.renders_dir / slug
        package_dir.mkdir(parents=True, exist_ok=True)

        # 1. Synthesize Procedural Audio Tracks
        drone_data = self.audio_engine.generate_ambient_drone(duration_sec=15.0)
        drone_file = self.audio_engine.save_wav(drone_data, self.audio_dir / f"{slug}_ambient_drone.wav")

        whoosh_data = self.audio_engine.generate_attention_whoosh(duration_sec=2.0)
        whoosh_file = self.audio_engine.save_wav(whoosh_data, self.audio_dir / f"{slug}_attention_whoosh.wav")

        click_data = self.audio_engine.generate_flash_click(duration_sec=0.5)
        click_file = self.audio_engine.save_wav(click_data, self.audio_dir / f"{slug}_flash_click.wav")

        # 2. Render SVG Vector Frames for Each Scene
        total_scenes = len(script_data["scenes"])
        svg_frames = []
        for i, scene in enumerate(script_data["scenes"], 1):
            svg_file = self.svg_dir / f"{slug}_scene_{i:02d}.svg"
            self.visual_engine.export_svg_frame(
                output_path=svg_file,
                title=f"SCENE {i}: {scene['name']}",
                subtitle=scene['style'].replace('_', ' '),
                frame_index=i,
                total_frames=total_scenes
            )
            svg_frames.append(str(svg_file))

        # 3. Create YouTube Publishing Manifest
        manifest = {
            "title": script_data["title"],
            "youtube_metadata": {
                "title": script_data["youtube_title"],
                "description": script_data["description"],
                "tags": script_data["tags"],
                "category_id": "28"  # Science & Technology
            },
            "audio_assets": {
                "ambient_drone": str(drone_file),
                "attention_whoosh": str(whoosh_file),
                "flash_click": str(click_file)
            },
            "svg_frames": svg_frames,
            "scenes": script_data["scenes"]
        }

        manifest_path = package_dir / "production_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        # Save formatted script in scripts dir
        script_md = self.scripts_dir / f"{slug}_production_script.md"
        lines = [
            f"# 🎬 Production Script: {script_data['title']}",
            f"**Target Format:** YouTube Short / Long Form",
            f"**YouTube Title:** `{script_data['youtube_title']}`\n",
            "## Description",
            script_data["description"],
            "\n## Scene Breakdown",
        ]
        for s in script_data["scenes"]:
            lines.append(f"### Scene {s['scene_id']}: {s['name']} ({s['timecode']})")
            lines.append(f"- **Visual Style:** `{s['style']}`")
            lines.append(f"- **Visual Prompt:** `{s['visual_prompt']}`")
            lines.append(f"- **Voiceover Narration:** {s['narration']}")
            lines.append(f"- **Sound FX:** `{s['sound_effect']}`\n")

        script_md.write_text("\n".join(lines), encoding="utf-8")

        return manifest_path

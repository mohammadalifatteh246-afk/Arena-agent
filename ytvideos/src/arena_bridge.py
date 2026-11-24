"""
LMArena Agent Mode Bridge for ytvideos.
Interfaces with LMArena's Agent Mode execution sandbox via the GitHub Shared Bus (.agent/CURRENT_TASK.md).
Dispatches image generation prompts and audio generation orders to Arena's free cloud runtime.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class LMArenaBridge:
    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            # ytvideos/src/arena_bridge.py -> repo_root is D:/Arena-agent
            self.repo_root = Path(__file__).resolve().parent.parent.parent
        else:
            self.repo_root = Path(repo_root)

        self.agent_dir = self.repo_root / ".agent"
        self.current_task_path = self.agent_dir / "CURRENT_TASK.md"

    def format_generation_work_order(
        self,
        video_title: str,
        scenes: List[Dict[str, Any]],
        generation_type: str = "FULL_MULTIMEDIA"  # "IMAGES", "AUDIO", or "FULL_MULTIMEDIA"
    ) -> str:
        """
        Formats a structured work order for LMArena Cloud Agent to generate free images and audio.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slug = video_title.lower().replace(" ", "-").replace(":", "")[:30]
        target_branch = f"arena/ytvideo-{slug}"

        instructions = []
        instructions.append(f"# Task Work Order: Generate Video Assets for '{video_title}'")
        instructions.append(f"- **Dispatched By:** Google Antigravity (ytvideos engine)")
        instructions.append(f"- **Date:** {timestamp}")
        instructions.append(f"- **Target Branch:** `{target_branch}`")
        instructions.append(f"- **Status:** READY_FOR_ARENA")
        instructions.append(f"- **Asset Generation Scope:** {generation_type}\n")

        instructions.append("## Objective")
        instructions.append("Generate high-quality video visual assets and audio narration for this YouTube production using Arena's free generation toolkits.\n")

        instructions.append("## Production Scenes & Prompts")
        for i, scene in enumerate(scenes, 1):
            instructions.append(f"### Scene {i}: {scene.get('name', f'Scene {i}')}")
            instructions.append(f"- **Duration:** {scene.get('duration_sec', 5)}s")
            instructions.append(f"- **Visual Art Style:** `{scene.get('style', 'sumi_original')}`")
            instructions.append(f"- **Visual Prompt:** `{scene.get('visual_prompt', '')}`")
            instructions.append(f"- **Narration Script:** \"{scene.get('narration', '')}\"")
            instructions.append(f"- **Target Image Path:** `ytvideos/assets/images/scene_{i:02d}.png`")
            instructions.append(f"- **Target Audio Path:** `ytvideos/assets/audio/voice_{i:02d}.wav`\n")

        instructions.append("## Instructions for Arena Cloud Agent")
        instructions.append("1. Read the scene visual prompts and generate corresponding images into `ytvideos/assets/images/`.")
        instructions.append("2. Generate voiceover audio files for each narration block into `ytvideos/assets/audio/`.")
        instructions.append("3. Commit all generated assets to `{target_branch}`.")
        instructions.append("4. Open a Pull Request to `master` with summary of generated media.")

        return "\n".join(instructions)

    def dispatch_generation_task(self, video_title: str, scenes: List[Dict[str, Any]], push_remote: bool = False) -> Dict[str, Any]:
        """
        Writes the work order to .agent/CURRENT_TASK.md and optionally commits and pushes to Git remote.
        """
        work_order = self.format_generation_work_order(video_title, scenes)
        self.current_task_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_task_path.write_text(work_order, encoding="utf-8")

        result = {
            "status": "dispatched_locally",
            "task_file": str(self.current_task_path),
            "video_title": video_title,
            "scene_count": len(scenes)
        }

        if push_remote:
            try:
                subprocess.run(["git", "-C", str(self.repo_root), "add", str(self.current_task_path)], check=True)
                subprocess.run(["git", "-C", str(self.repo_root), "commit", "-m", f"dispatch(ytvideos): assets for {video_title}"], check=True)
                subprocess.run(["git", "-C", str(self.repo_root), "push", "origin", "master"], check=True)
                result["status"] = "dispatched_and_pushed"
            except Exception as e:
                result["git_error"] = str(e)

        return result

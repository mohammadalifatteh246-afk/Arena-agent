#!/usr/bin/env python3
"""
ytvideos - Main Execution Entrypoint.
Orchestrates YouTube Video Production with BeyondSumi Framework & LMArena Agent Mode.
"""

import sys
import argparse
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = WORKSPACE_ROOT.parent

# Ensure packages can be imported
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ytvideos.src.story_engine import StoryScriptEngine
from ytvideos.src.arena_bridge import LMArenaBridge
from ytvideos.src.assembler import VideoProductionAssembler


def run_pipeline(dispatch_arena: bool = True, push_git: bool = False):
    print("=" * 70)
    print("  🎬 YOUTUBE AUTOMATION ENGINE: BEYONDSUMI + LMARENA AGENT MODE")
    print("  📍 Workspace: D:/Arena-agent/ytvideos")
    print("=" * 70)

    # 1. Script & Story Creation
    print("\n[1/4] Generating high-retention production script...")
    story_engine = StoryScriptEngine()
    script_data = story_engine.create_transformer_token_story()
    print(f"  ✅ Script generated: '{script_data['title']}' ({len(script_data['scenes'])} scenes)")

    # 2. Dispatch to LMArena Agent Mode (for Free Images & Audio)
    if dispatch_arena:
        print("\n[2/4] Formatting work order for LMArena Agent Mode...")
        bridge = LMArenaBridge(repo_root=REPO_ROOT)
        dispatch_res = bridge.dispatch_generation_task(
            video_title=script_data["title"],
            scenes=script_data["scenes"],
            push_remote=push_git
        )
        print(f"  ✅ Dispatched to LMArena Agent Bus: {dispatch_res['task_file']}")
        print("  💡 LMArena Cloud Agent can generate images and voiceover without paid API spend.")
    else:
        print("\n[2/4] Skipped LMArena dispatch (offline / local-only mode).")

    # 3. Assemble Local Assets (Procedural Audio + Vector Frames)
    print("\n[3/4] Synthesizing procedural audio & rendering vector frames...")
    assembler = VideoProductionAssembler(workspace_root=WORKSPACE_ROOT)
    manifest_path = assembler.assemble_production_package(script_data)
    print(f"  ✅ Production Manifest written to: {manifest_path}")

    # 4. Summary
    print("\n[4/4] Production package ready!")
    print("=" * 70)
    print(f"  🎉 Output files:")
    print(f"     - Script: ytvideos/scripts/")
    print(f"     - Audio:  ytvideos/assets/audio/")
    print(f"     - Frames: ytvideos/assets/svg_frames/")
    print(f"     - Renders: ytvideos/renders/")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Generate YouTube Video with ytvideos engine")
    parser.add_argument("--no-arena", action="store_true", help="Skip dispatch to LMArena Agent bus")
    parser.add_argument("--push", action="store_true", help="Push dispatched task to GitHub remote for Arena Cloud Agent")
    args = parser.parse_args()

    run_pipeline(dispatch_arena=not args.no_arena, push_git=args.push)


if __name__ == "__main__":
    main()

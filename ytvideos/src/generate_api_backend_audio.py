#!/usr/bin/env python3
"""
Procedural Audio Synthesizer & Sound Designer for 'APIs & Backends Explained'.
Synthesizes 100% royalty-free sound effects & background beds matching the 4 scenes.
"""

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT.parent))

from ytvideos.src.audio_engine import ProceduralAudioEngine


def generate_audio_beds():
    audio_dir = WORKSPACE_ROOT / "assets" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    engine = ProceduralAudioEngine()

    print("\n[+] Synthesizing Procedural Audio Tracks for 'APIs & Backends'...")

    # Scene 1: 40ms Request / Hook Whoosh
    whoosh_pcm = engine.generate_attention_whoosh(duration_sec=2.0, start_freq=120.0, end_freq=1100.0)
    whoosh_path = audio_dir / "api_backend_hook_whoosh.wav"
    engine.save_wav(whoosh_pcm, whoosh_path)
    print(f"  - Generated: {whoosh_path.name}")

    # Scene 2: Backend Kitchen & Server Hum (Sub-bass drone)
    drone_pcm = engine.generate_ambient_drone(duration_sec=16.0, base_freq=65.41)
    drone_path = audio_dir / "api_backend_kitchen_drone.wav"
    engine.save_wav(drone_pcm, drone_path)
    print(f"  - Generated: {drone_path.name}")

    # Scene 3: REST vs WebSocket Kinetic Pulse (High tech click / zaps)
    click_pcm = engine.generate_flash_click(duration_sec=0.4)
    click_path = audio_dir / "api_backend_protocols_click.wav"
    engine.save_wav(click_pcm, click_path)
    print(f"  - Generated: {click_path.name}")

    # Scene 4: Climax & Global Cloud Constellation
    outro_pcm = engine.generate_ambient_drone(duration_sec=14.0, base_freq=73.42)
    outro_path = audio_dir / "api_backend_engine_drone.wav"
    engine.save_wav(outro_pcm, outro_path)
    print(f"  - Generated: {outro_path.name}")

    print("\n[+] All procedural audio tracks synthesized successfully (0% copyright risk).")


if __name__ == "__main__":
    generate_audio_beds()

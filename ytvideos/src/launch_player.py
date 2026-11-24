#!/usr/bin/env python3
"""
Launches the interactive 24 FPS Video Player in your default browser.
"""

import webbrowser
from pathlib import Path

PLAYER_FILE = Path(r"C:\Users\Admin\.gemini\antigravity\brain\f9d3bb7a-340b-4e4c-b876-b878a65ec057\video_player.html")


def main():
    if PLAYER_FILE.exists():
        print(f"Opening video player in browser: {PLAYER_FILE}")
        webbrowser.open(PLAYER_FILE.as_uri())
    else:
        print(f"Player file not found at: {PLAYER_FILE}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Launches the interactive 24 FPS Video Player in your default browser.
"""

import webbrowser
from pathlib import Path

PLAYER_FILE = Path(r"C:\Users\Admin\.gemini\antigravity\brain\6ec269d5-459c-434b-a3a2-2dd1ba17bc3e\video_player.html")


def main():
    if PLAYER_FILE.exists():
        print(f"Opening video player in browser: {PLAYER_FILE}")
        webbrowser.open(PLAYER_FILE.as_uri())
    else:
        print(f"Player file not found at: {PLAYER_FILE}")


if __name__ == "__main__":
    main()

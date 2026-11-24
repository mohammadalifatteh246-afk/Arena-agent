#!/usr/bin/env python3
"""
Direct Live CDP Trigger for Arena Agent Mode (arena.ai/agent).
Directly connects to the live authenticated Chrome browser on port 9222,
navigates to Arena Agent Mode, injects the Human Character production prompt,
and clicks the submit trigger automatically.
"""

import asyncio
import json
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.cdp_client import ArenaCDPClient


HUMAN_CHARACTER_PROMPT = """
[AGENT TASK: CREATE HIGH-RETENTION ANIME CHARACTER YOUTUBE VIDEO]

Topic: "APIs & Backends: How, Where, What, Which to use (Practical Guide)"
Creative Direction: Human Character Protagonist + Dynamic Anime Creative Edits

Protagonist Specification:
- Name: "Leo" (21-year-old expressive junior developer, messy dark brown hair, oversized dark blue hoodie, silver headphones around his neck, energetic and relatable anime expressions like Death Note / Steins;Gate / Shinkai).

Scene Visual & Creative Editing Breakdown:
1. Scene 1 (The Panic Hook):
   Close-up on Leo's stressed face illuminated by a laptop screen flashing bright red "500 INTERNAL SERVER ERROR". Papers flying, coffee mug shaking. 
   Style: Vivid Japanese anime, dramatic lighting, intense anime expression, 8k cinematic --ar 16:9

2. Scene 2 (The Cyber Dive & The Messenger):
   Leo gets pulled through his monitor into a luminous cybernetic Tokyo-style digital highway. A charismatic courier in a sleek white trench coat (The API) catches him mid-air: "Relax kid. You're screaming at an empty room. I'm your API. You talk to me, I talk to the backend."
   Style: Studio Ghibli meets Cyberpunk, glowing particle trails, cinematic wide angle --ar 16:9

3. Scene 3 (The Backend Kitchen & Database Vaults):
   The API courier leads Leo through a towering fortress: massive glowing steel vaults labeled 'DATABASE', high-speed hyperloop trains labeled 'REST GET/POST', and live lightning conduits labeled 'WEBSOCKETS'. Dynamic camera whip pan, vibrant colors, expressive character acting.
   Style: Makoto Shinkai aesthetic, intricate architectural detail, breathtaking lighting --ar 16:9

4. Scene 4 (The Mastery & Climax):
   Leo is back in his real-world room, grinning with confidence. He types one clean line of code, hits Enter, and the screen glows bright green: '200 OK — Synced in 14ms'. He sips coffee and smirks at the camera.
   Style: Warm cinematic anime, golden hour room lighting, clean triumphant character composition --ar 16:9

Please generate the visual illustrations for these 4 anime scenes and synthesize the corresponding voiceover audio files.
"""


async def trigger_live_arena(mode_url: str = "https://arena.ai/agent", prompt_text: str = HUMAN_CHARACTER_PROMPT):
    client = ArenaCDPClient()
    
    print("=" * 70)
    print("  🚀 LIVE ARENA CDP TRIGGER")
    print("  🎯 Target: arena.ai/agent (Direct Browser Injection)")
    print("=" * 70)

    # 1. Check Chrome Port 9222
    if not await client.is_chrome_running():
        print("\n❌ Chrome is NOT running on port 9222.")
        print("💡 Solution: Run `D:\\Arena-agent\\scripts\\launch_chrome.bat` first,")
        print("   log in to arena.ai, and then run this script again.")
        return False

    print("\n[+] Step 1: Connecting to Chrome remote debugging session on port 9222...")
    tabs = await client.get_tabs()
    target_tab = None

    for t in tabs:
        url = t.get("url", "")
        if "arena.ai" in url:
            target_tab = t
            break

    if not target_tab:
        print(f"[+] Opening new tab pointing to {mode_url}...")
        target_tab = await client.open_arena_tab(mode_url)
        await asyncio.sleep(4.0)
    else:
        print(f"[+] Found existing Arena tab: {target_tab.get('title', '')}")

    ws_url = target_tab.get("webSocketDebuggerUrl")
    if not ws_url:
        print("❌ Could not obtain WebSocket debugger URL for Arena tab.")
        return False

    # 2. Inject Prompt into Editor
    print("\n[+] Step 2: Injecting Human Character Video Prompt into Arena Agent UI...")
    escaped_prompt = json.dumps(prompt_text)
    inject_js = f"""
    (() => {{
        const pm = document.querySelector('.ProseMirror, [contenteditable="true"]');
        if (pm) {{
            pm.focus();
            pm.innerHTML = `<p>{escaped_prompt[1:-1]}</p>`;
            pm.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return {{ success: true, target: 'ProseMirror' }};
        }}
        const textarea = document.querySelector('textarea');
        if (textarea) {{
            textarea.value = {escaped_prompt};
            textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return {{ success: true, target: 'textarea' }};
        }}
        return {{ success: false, error: 'Input editor not found' }};
    }})()
    """
    res = await client.evaluate_js(ws_url, inject_js)
    print(f"  - Editor injection result: {res}")

    # 3. Trigger Submission (Enter / Submit button)
    print("\n[+] Step 3: Triggering Task Submission in Arena...")
    await asyncio.sleep(0.5)
    
    # Click submit button if visible
    click_submit_js = """
    (() => {
        const btn = document.querySelector('button[type="submit"], button[aria-label*="send" i], button:has(svg)');
        if (btn && !btn.disabled) {
            btn.click();
            return { clicked: true };
        }
        return { clicked: false };
    })()
    """
    click_res = await client.evaluate_js(ws_url, click_submit_js)

    # Also dispatch Enter key
    await client.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
        "type": "rawKeyDown",
        "windowsVirtualKeyCode": 13,
        "key": "Enter",
        "code": "Enter"
    })
    await client.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
        "type": "keyUp",
        "windowsVirtualKeyCode": 13,
        "key": "Enter",
        "code": "Enter"
    })

    print("  ✅ Prompt submitted directly into Arena Agent interface!")
    print("=" * 70)
    print("  🎉 Arena Agent is now processing your Human Character Video in the cloud!")
    print("=" * 70)
    return True


def main():
    parser = argparse.ArgumentParser(description="Trigger Arena Agent Mode Live via CDP")
    parser.add_argument("--url", default="https://arena.ai/agent", help="Arena mode URL")
    args = parser.parse_args()

    asyncio.run(trigger_live_arena(mode_url=args.url))


if __name__ == "__main__":
    main()

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def tiptap_submit():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    prompt = "What is the difference between synchronous and asynchronous programming in 3 bullet points?"
    escaped = json.dumps(prompt)

    # 1. Focus ProseMirror and set innerHTML
    js_focus = f"""
    (() => {{
        const pm = document.querySelector('.ProseMirror');
        if (!pm) return {{ error: 'No ProseMirror' }};
        pm.focus();
        pm.innerHTML = `<p>{prompt}</p>`;
        pm.dispatchEvent(new Event('input', {{ bubbles: true }}));
        return {{ success: true }};
    }})()
    """
    res = await client.evaluate_js(ws_url, js_focus)
    print("Set text:", res)
    await asyncio.sleep(0.5)

    # 2. Dispatch Enter key via CDP
    await client.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
        "type": "rawKeyDown",
        "windowsVirtualKeyCode": 13,
        "unmodifiedText": "\r",
        "text": "\r",
        "key": "Enter",
        "code": "Enter"
    })
    await client.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
        "type": "keyUp",
        "windowsVirtualKeyCode": 13,
        "key": "Enter",
        "code": "Enter"
    })
    print("Dispatched Enter key!")


if __name__ == "__main__":
    asyncio.run(tiptap_submit())

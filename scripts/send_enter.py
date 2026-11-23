import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def send_enter():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    # Focus textarea
    await client.evaluate_js(ws_url, "document.querySelector('textarea').focus();")
    await asyncio.sleep(0.3)

    # Send Enter key down & up
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
    asyncio.run(send_enter())

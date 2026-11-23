import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def inspect_form_state():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    js = """
    (() => {
        const form = document.querySelector('form');
        const buttons = Array.from(document.querySelectorAll('form button, div[role="presentation"] button'));
        return buttons.map(b => ({
            tag: b.tagName,
            type: b.type,
            ariaLabel: b.getAttribute('aria-label'),
            text: b.innerText,
            disabled: b.disabled,
            svg: !!b.querySelector('svg'),
            rect: b.getBoundingClientRect()
        }));
    })()
    """
    res = await client.evaluate_js(ws_url, js)
    print("Buttons detail:")
    for b in res:
        print(b)


if __name__ == "__main__":
    asyncio.run(inspect_form_state())

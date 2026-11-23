import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def dump_form_bottom():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    js = """
    (() => {
        const form = document.querySelector('form');
        if (form) {
            return {
                html: form.outerHTML.slice(1000)
            };
        }
        return { error: 'no form' };
    })()
    """
    res = await client.evaluate_js(ws_url, js)
    print(res.get("html", res))


if __name__ == "__main__":
    asyncio.run(dump_form_bottom())

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def get_response():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    js = """
    (() => {
        // Collect all assistant messages / prose
        const elements = Array.from(document.querySelectorAll('.prose, [data-role="assistant"], .markdown'));
        if (elements.length > 0) {
            return elements.map(el => (el.innerText || '').trim()).filter(Boolean);
        }
        return [];
    })()
    """
    res = await client.evaluate_js(ws_url, js)
    print(f"Total prose blocks: {len(res)}")
    for i, block in enumerate(res):
        print(f"\n--- BLOCK {i+1} ---")
        print(block)


if __name__ == "__main__":
    asyncio.run(get_response())

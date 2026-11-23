import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def inspect_models():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    if not tab:
        print("No arena tab")
        return
    ws_url = tab.get("webSocketDebuggerUrl")

    # Click model button
    click_js = """
    (() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Model');
        if (btn) {
            btn.click();
            return { clicked: true };
        }
        return { clicked: false };
    })()
    """
    res1 = await client.evaluate_js(ws_url, click_js)
    print("Click Model button:", res1)
    await asyncio.sleep(1.0)

    # Check search input in dropdown or list items
    list_js = """
    (() => {
        const searchInput = document.querySelector('input[placeholder*="search" i], input[placeholder*="model" i], input[type="search"]');
        const items = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], [data-radix-collection-item], button'))
            .map(el => (el.innerText || '').trim())
            .filter(t => t.length > 0 && t.length < 80);
        return {
            hasSearch: !!searchInput,
            searchPlaceholder: searchInput ? searchInput.placeholder : null,
            items: items.slice(0, 50)
        };
    })()
    """
    res2 = await client.evaluate_js(ws_url, list_js)
    print("Dropdown info:")
    print("hasSearch:", res2.get("hasSearch"))
    print("searchPlaceholder:", res2.get("searchPlaceholder"))
    print("Items found:", len(res2.get("items", [])))
    for it in res2.get("items", [])[:30]:
        print("  -", it)


if __name__ == "__main__":
    asyncio.run(inspect_models())

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def check():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")
    js = """
    (() => {
        const text = (document.querySelector('textarea') || {}).value || '';
        const msgs = Array.from(document.querySelectorAll('[data-role="assistant"], .prose, .markdown, [class*="response"]')).map(m => (m.innerText || '').slice(0, 200));
        return { textarea: text, msgsCount: msgs.length, msgs: msgs };
    })()
    """
    res = await client.evaluate_js(ws_url, js)
    print("Page state:")
    print("Textarea:", res.get("textarea"))
    print("Messages count:", res.get("msgsCount"))
    for m in res.get("msgs", []):
        print("MSG:", m)


if __name__ == "__main__":
    asyncio.run(check())

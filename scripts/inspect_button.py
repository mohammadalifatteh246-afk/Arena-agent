import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def inspect_send_button():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")
    js = """
    (() => {
        const form = document.querySelector('form');
        const formButtons = form ? Array.from(form.querySelectorAll('button')).map(b => ({
            tag: b.tagName,
            type: b.type,
            ariaLabel: b.getAttribute('aria-label'),
            text: b.innerText,
            disabled: b.disabled,
            className: b.className
        })) : [];
        const allButtons = Array.from(document.querySelectorAll('button')).filter(b => {
            const l = (b.getAttribute('aria-label') || '').toLowerCase();
            const t = (b.innerText || '').toLowerCase();
            return l.includes('send') || t.includes('send') || b.querySelector('svg');
        }).map(b => ({
            type: b.type,
            ariaLabel: b.getAttribute('aria-label'),
            text: b.innerText,
            disabled: b.disabled
        }));
        return { hasForm: !!form, formButtons, allButtons: allButtons.slice(0, 10) };
    })()
    """
    res = await client.evaluate_js(ws_url, js)
    print("Button inspection:")
    print("hasForm:", res.get("hasForm"))
    print("formButtons:", res.get("formButtons"))
    print("allButtons:", res.get("allButtons"))


if __name__ == "__main__":
    asyncio.run(inspect_send_button())

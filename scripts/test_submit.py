import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def trigger_submit():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    # Check form submit
    submit_js = """
    (() => {
        const form = document.querySelector('form');
        if (form) {
            try {
                form.requestSubmit();
                return { submitted: true, method: 'requestSubmit' };
            } catch(e) {
                return { submitted: false, error: e.message };
            }
        }
        return { submitted: false, error: 'No form' };
    })()
    """
    res = await client.evaluate_js(ws_url, submit_js)
    print("Submit result:", res)


if __name__ == "__main__":
    asyncio.run(trigger_submit())

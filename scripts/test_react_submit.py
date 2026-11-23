import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.cdp_client import ArenaCDPClient


async def react_input_and_submit():
    client = ArenaCDPClient()
    tab = await client.find_arena_tab()
    ws_url = tab.get("webSocketDebuggerUrl")

    prompt = "What is the difference between synchronous and asynchronous programming in 3 bullet points?"
    escaped = json.dumps(prompt)

    js = f"""
    (() => {{
        const textarea = document.querySelector('textarea');
        if (!textarea) return {{ error: 'No textarea' }};

        // React controlled input setter
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
        setter.call(textarea, {escaped});
        textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
        textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));

        // Now find the submit button or form
        const form = document.querySelector('form');
        if (form) {{
            form.requestSubmit();
            return {{ success: true, method: 'react_requestSubmit' }};
        }}
        return {{ success: false, error: 'No form' }};
    }})()
    """
    res = await client.evaluate_js(ws_url, js)
    print("React submit result:", res)


if __name__ == "__main__":
    asyncio.run(react_input_and_submit())

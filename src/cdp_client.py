import json
import asyncio
import httpx
import websockets
from typing import Optional, Dict, Any, List

CDP_HTTP_BASE = "http://127.0.0.1:9222"


class ArenaCDPClient:
    """
    Lightweight, dependency-minimal Chrome DevTools Protocol client
    connecting Antigravity to a live authenticated Chrome browser.
    """

    def __init__(self, base_url: str = CDP_HTTP_BASE):
        self.base_url = base_url

    async def is_chrome_running(self) -> bool:
        """Checks if Chrome is listening on the remote debugging port."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/json/version")
                return res.status_code == 200
        except Exception:
            return False

    async def get_tabs(self) -> List[Dict[str, Any]]:
        """Retrieves all open inspectable tabs in Chrome."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/json")
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        return []

    async def find_arena_tab(self) -> Optional[Dict[str, Any]]:
        """Finds an existing arena.ai tab or returns None."""
        tabs = await self.get_tabs()
        for tab in tabs:
            url = tab.get("url", "")
            if "arena.ai" in url or "lmarena.ai" in url:
                return tab
        return None

    async def open_arena_tab(self, url: str = "https://arena.ai/chat") -> Optional[Dict[str, Any]]:
        """Opens a new tab with arena.ai if none is open."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.put(f"{self.base_url}/json/new?{url}")
                if res.status_code == 200:
                    return res.json()
        except Exception:
            pass
        return None

    async def execute_cdp_command(self, ws_url: str, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Sends a single CDP JSON-RPC command over WebSocket."""
        async with websockets.connect(ws_url) as ws:
            cmd_id = 1
            payload = {
                "id": cmd_id,
                "method": method,
                "params": params or {}
            }
            await ws.send(json.dumps(payload))
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == cmd_id:
                    return data

    async def evaluate_js(self, ws_url: str, expression: str) -> Any:
        """Evaluates JavaScript expression in the tab and returns value."""
        res = await self.execute_cdp_command(
            ws_url,
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True
            }
        )
        result = res.get("result", {}).get("result", {})
        return result.get("value")

    async def select_model(self, ws_url: str, model_query: str) -> Dict[str, Any]:
        """Selects a model from the Arena model selector dropdown."""
        escaped_query = json.dumps(model_query.lower())
        select_js = f"""
        (() => {{
            const query = {escaped_query};
            // 1. Find and click model selector button if dropdown not open
            let searchInput = document.querySelector('input[placeholder*="search" i], input[placeholder*="model" i]');
            if (!searchInput) {{
                const buttons = Array.from(document.querySelectorAll('button'));
                const modelBtn = buttons.find(b => {{
                    const t = (b.innerText || '').trim();
                    return t === 'Model' || t.includes('Router') || t.includes('gemini') || t.includes('claude') || t.includes('gpt');
                }});
                if (modelBtn) {{
                    modelBtn.click();
                }}
            }}
            return {{ opened: true }};
        }})()
        """
        await self.evaluate_js(ws_url, select_js)
        await asyncio.sleep(0.8)

        # 2. In dropdown, find matching item and click
        click_item_js = f"""
        (() => {{
            const query = {escaped_query};
            const allElements = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], [data-radix-collection-item], button, div, span'));
            
            const matches = allElements.filter(el => {{
                const t = (el.innerText || '').toLowerCase().trim();
                return t.includes(query) || (query.includes('argon') && t.includes('argon'));
            }});

            if (matches.length > 0) {{
                const target = matches[matches.length - 1];
                target.click();
                return {{ success: true, selected: target.innerText }};
            }}

            return {{ success: false, error: 'Model not found in dropdown' }};
        }})()
        """
        res = await self.evaluate_js(ws_url, click_item_js)
        await asyncio.sleep(0.8)
        return res if isinstance(res, dict) else {"success": False}

    async def send_direct_prompt(self, prompt: str, model: Optional[str] = None, timeout_seconds: int = 120) -> str:
        """
        Sends a prompt to the Arena Chat tab, triggers submission,
        and polls for the completed response.
        """
        if not await self.is_chrome_running():
            return (
                "ERROR: Chrome is not running with remote debugging port 9222.\n"
                "Please run `D:\\Arena-agent\\scripts\\launch_chrome.bat` to launch Chrome, "
                "or start Chrome with: `chrome.exe --remote-debugging-port=9222 https://arena.ai/chat`"
            )

        tab = await self.find_arena_tab()
        if not tab:
            tab = await self.open_arena_tab("https://arena.ai/chat")
            if not tab:
                return "ERROR: Could not open or find arena.ai tab in Chrome."
            await asyncio.sleep(4.0)

        ws_url = tab.get("webSocketDebuggerUrl")
        if not ws_url:
            return "ERROR: No webSocketDebuggerUrl available for the Arena tab."

        # Select model if requested
        if model:
            await self.select_model(ws_url, model)
            await asyncio.sleep(0.5)

        # Count existing assistant messages before sending
        count_pre_js = """
        (() => {
            const msgs = document.querySelectorAll('.prose, [data-role="assistant"], .markdown');
            return msgs.length;
        })()
        """
        pre_count = await self.evaluate_js(ws_url, count_pre_js) or 0

        # Inject prompt into ProseMirror / TipTap editor or textarea
        escaped_prompt = json.dumps(prompt)
        inject_js = f"""
        (() => {{
            const pm = document.querySelector('.ProseMirror');
            if (pm) {{
                pm.focus();
                pm.innerHTML = `<p>{escaped_prompt[1:-1]}</p>`;
                pm.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return {{ success: true, editor: 'prosemirror' }};
            }}
            const textarea = document.querySelector('textarea');
            if (textarea) {{
                textarea.value = {escaped_prompt};
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return {{ success: true, editor: 'textarea' }};
            }}
            return {{ success: false, error: 'No editor found' }};
        }})()
        """
        inject_res = await self.evaluate_js(ws_url, inject_js)
        if isinstance(inject_res, dict) and not inject_res.get("success", False):
            return f"ERROR: Failed to inject prompt: {inject_res.get('error')}"

        await asyncio.sleep(0.5)

        # Dispatch Enter key to submit
        await self.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
            "type": "rawKeyDown",
            "windowsVirtualKeyCode": 13,
            "unmodifiedText": "\r",
            "text": "\r",
            "key": "Enter",
            "code": "Enter"
        })
        await self.execute_cdp_command(ws_url, "Input.dispatchKeyEvent", {
            "type": "keyUp",
            "windowsVirtualKeyCode": 13,
            "key": "Enter",
            "code": "Enter"
        })

        # Wait for new response
        poll_interval = 2.0
        elapsed = 0.0
        await asyncio.sleep(3.0)

        extract_js = """
        (() => {
            const elements = Array.from(document.querySelectorAll('.prose, [data-role="assistant"], .markdown'));
            if (elements.length > 0) {
                return elements[elements.length - 1].innerText.trim();
            }
            return '';
        })()
        """

        last_text = ""
        stable_count = 0

        while elapsed < timeout_seconds:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            current_text = await self.evaluate_js(ws_url, extract_js)
            if isinstance(current_text, str) and current_text:
                if current_text == last_text and len(current_text) > 30:
                    stable_count += 1
                    if stable_count >= 2:
                        return current_text
                else:
                    stable_count = 0
                    last_text = current_text

        return last_text or "TIMEOUT: Response took longer than timeout limit."

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

    async def open_arena_tab(self, url: str = "https://arena.ai/direct") -> Optional[Dict[str, Any]]:
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

    async def send_direct_prompt(self, prompt: str, timeout_seconds: int = 120) -> str:
        """
        Sends a prompt to the Arena Direct Chat tab, triggers submission,
        and polls for the completed response.
        """
        if not await self.is_chrome_running():
            return (
                "ERROR: Chrome is not running with remote debugging port 9222.\n"
                "Please run `D:\\Arena-agent\\scripts\\launch_chrome.bat` to launch Chrome, "
                "or start Chrome with: `chrome.exe --remote-debugging-port=9222 https://arena.ai/direct`"
            )

        tab = await self.find_arena_tab()
        if not tab:
            tab = await self.open_arena_tab("https://arena.ai/direct")
            if not tab:
                return "ERROR: Could not open or find arena.ai tab in Chrome."
            await asyncio.sleep(4.0)

        ws_url = tab.get("webSocketDebuggerUrl")
        if not ws_url:
            return "ERROR: No webSocketDebuggerUrl available for the Arena tab."

        # Escape prompt for safe JS string literal
        escaped_prompt = json.dumps(prompt)

        # 1. Fill prompt into input box
        inject_js = f"""
        (() => {{
            const textarea = document.querySelector('textarea') || document.querySelector('input[type="text"]');
            if (!textarea) return {{ success: false, error: 'Textarea not found' }};
            
            textarea.value = {escaped_prompt};
            textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));

            // Find send button
            const buttons = Array.from(document.querySelectorAll('button'));
            const sendBtn = buttons.find(b => b.getAttribute('aria-label') === 'Send' || b.innerText.includes('Send') || b.querySelector('svg'));
            if (sendBtn && !sendBtn.disabled) {{
                sendBtn.click();
                return {{ success: true }};
            }}

            // Fallback: trigger Enter keydown
            textarea.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
            return {{ success: true, method: 'enter_key' }};
        }})()
        """

        inject_res = await self.evaluate_js(ws_url, inject_js)
        if isinstance(inject_res, dict) and not inject_res.get("success", False):
            return f"ERROR: Failed to inject prompt into Arena chat: {inject_res.get('error')}"

        # 2. Wait for completion and extract response text
        poll_interval = 2.0
        elapsed = 0.0

        # Wait initial 2s for generation to start
        await asyncio.sleep(2.0)

        extract_js = """
        (() => {
            // Find assistant / model response messages
            const messages = document.querySelectorAll('[data-role="assistant"], .prose, .markdown, [class*="response"]');
            if (messages.length > 0) {
                const last = messages[messages.length - 1];
                return { text: last.innerText || last.textContent, count: messages.length };
            }
            return { text: '', count: 0 };
        })()
        """

        last_text = ""
        stable_count = 0

        while elapsed < timeout_seconds:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            data = await self.evaluate_js(ws_url, extract_js)
            if isinstance(data, dict):
                current_text = data.get("text", "").strip()
                if current_text:
                    if current_text == last_text and len(current_text) > 20:
                        stable_count += 1
                        if stable_count >= 2:  # Text remained identical for 4 seconds -> done
                            return current_text
                    else:
                        stable_count = 0
                        last_text = current_text

        if last_text:
            return last_text
        return "TIMEOUT: Response took longer than timeout limit or could not be parsed."

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import asyncio
import subprocess
import json
from mcp.server.mcpserver import MCPServer
from src.cdp_client import ArenaCDPClient
cdp_client = ArenaCDPClient()

server = MCPServer("arena-relay")


@server.tool()
async def arena_status() -> str:
    """
    Checks the status of the local Chrome DevTools Protocol (CDP) bridge on port 9222
    and verifies if an arena.ai tab is open.
    """
    is_running = await cdp_client.is_chrome_running()
    if not is_running:
        return (
            "🔴 Chrome is NOT running on port 9222.\n"
            "Action required: Run `D:\\Arena-agent\\scripts\\launch_chrome.bat` or launch Chrome with:\n"
            "chrome.exe --remote-debugging-port=9222 https://arena.ai/direct"
        )

    tab = await cdp_client.find_arena_tab()
    if tab:
        return f"🟢 Chrome CDP is active! Found Arena tab: {tab.get('title')} ({tab.get('url')})"
    else:
        return "🟡 Chrome CDP is active, but no arena.ai tab is currently open. It will be opened automatically upon query."


@server.tool()
async def arena_direct_chat(prompt: str, model: str = "") -> str:
    """
    Submits a prompt to LMArena (arena.ai/chat) via the live Chrome tab
    and retrieves the model's response.
    Optional model parameter: e.g. "gemini-4-argon-high", "claude-sonnet", "gpt-6".
    """
    return await cdp_client.send_direct_prompt(prompt, model=model if model else None)


@server.tool()
def arena_dispatch_task(title: str, objective: str, branch: str = "feature") -> str:
    """
    Dispatches a structured work order to the Arena-agent repository on GitHub.
    The Arena Cloud Agent connected via OAuth will read this task, execute it in its cloud sandbox,
    and open a Pull Request.
    """
    dispatch_script = REPO_ROOT / "scripts" / "dispatch_to_arena.py"
    try:
        res = subprocess.run(
            ["python", str(dispatch_script), "--title", title, "--objective", objective, "--branch", branch],
            capture_output=True,
            text=True,
            check=True
        )
        return f"✅ Task successfully dispatched to GitHub:\n{res.stdout}"
    except Exception as e:
        return f"❌ Failed to dispatch task: {str(e)}"


@server.tool()
def arena_check_prs() -> str:
    """
    Checks GitHub for open Pull Requests created by Arena Cloud Agent.
    """
    try:
        res = subprocess.run(
            ["gh", "pr", "list", "--repo", "mohammadalifatteh246-afk/Arena-agent", "--json", "number,title,headRefName,url"],
            capture_output=True,
            text=True,
            check=True
        )
        prs = json.loads(res.stdout)
        if not prs:
            return "No open Pull Requests found on mohammadalifatteh246-afk/Arena-agent."
        summary = [f"Found {len(prs)} open Pull Request(s):"]
        for p in prs:
            summary.append(f"- PR #{p['number']}: {p['title']} ({p['url']})")
        return "\n".join(summary)
    except Exception as e:
        return f"Error checking GitHub PRs: {str(e)}"


def main():
    server.run(transport="stdio")


if __name__ == "__main__":
    main()

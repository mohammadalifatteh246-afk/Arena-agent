# ⚡ Arena-Agent

> **Zero-Cost, Unlimited Bi-Directional Bridge between Google Antigravity & LMArena (Arena.ai)**  
> Supports both **Direct Chat Mode** (`arena.ai/direct`) via Chrome CDP Relay MCP and **Agent Mode** (`arena.ai/agent`) via GitHub Shared Bus.

---

## 🌟 Architecture Overview

```
                                      ┌────────────────────────────────────────────────┐
                                      │              Google Antigravity                │
                                      │ (Any Workspace & Any Interactive Conversation) │
                                      └───────┬──────────────────────────────┬─────────┘
                                              │                              │
                        Direct Chat Tool Call │                              │ Task Dispatch & PR Sync
                                              ▼                              ▼
                    ┌───────────────────────────────────┐    ┌─────────────────────────────────┐
                    │ Chrome CDP Relay FastMCP Server   │    │ GitHub Shared Bus (.agent/TASK) │
                    │ (Lightweight, <5MB, Local stdio)  │    │ (Official OAuth Connector)      │
                    └─────────────────┬─────────────────┘    └────────────────┬────────────────┘
                                      │ CDP port 9222                         │ Git Remote Push / PRs
                                      ▼                                       ▼
                    ┌───────────────────────────────────┐    ┌─────────────────────────────────┐
                    │ Live Authenticated Chrome Session │    │ Arena.ai Agent Cloud Sandbox    │
                    │ (arena.ai/direct)                 │    │ (arena.ai/agent)                │
                    └───────────────────────────────────┘    └─────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Zero Paid Spend Invariant:** Completely free, forever. Uses official free surfaces and zero-cost local stdio processes.
2. **Direct Chat Mode (Chrome CDP Relay):**
   - No cookie hunting or scraping. Connects to your live authenticated Chrome tab via Chrome DevTools Protocol (`port 9222`).
   - Completely bypasses Cloudflare Turnstile bot blocks by operating in a genuine browser profile.
   - Callable globally from **any Antigravity workspace and conversation** via MCP.
3. **Agent Mode (GitHub Shared Bus):**
   - Connects to `arena.ai/agent` through Arena's official GitHub OAuth Connector.
   - Antigravity dispatches work orders to `.agent/CURRENT_TASK.md` on a staging branch.
   - Arena's cloud agent reads instructions, executes in its remote bash sandbox, and opens a Pull Request.
   - Antigravity pulls the PR, runs local verification test suites, and merges.

---

## 📦 Directory Structure

```text
Arena-agent/
├── .agent/                         # Shared Bus protocols for Arena Agent Mode
│   ├── AGENT_INSTRUCTIONS.md       # Persona & execution directives for Arena Agent
│   ├── CURRENT_TASK.md             # Active work order dispatched by Antigravity
│   └── TASK_TEMPLATE.md            # Work order template
├── scripts/
│   ├── launch_chrome.bat           # Helper to start Chrome with port 9222
│   ├── dispatch_to_arena.py        # Antigravity CLI to dispatch tasks to Arena
│   └── sync_arena_pr.py            # Antigravity CLI to pull and test Arena PRs
├── src/
│   ├── __init__.py
│   ├── cdp_client.py               # Pure-WebSocket CDP connector for Chrome
│   └── server.py                   # Global MCP Server (MCPServer stdio)
├── tests/
│   ├── __init__.py
│   └── test_cdp_relay.py           # Unit tests
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Launch Chrome with Remote Debugging
Run the launcher script:
```cmd
scripts\launch_chrome.bat
```
Log in to [arena.ai](https://arena.ai) once. Keep the tab open.

### 2. Antigravity Global Integration
The server is registered in your Antigravity global MCP configuration. Tools available:
- `arena_status`: Verifies connection to the live Chrome tab.
- `arena_direct_chat`: Sends prompts to Arena Direct Chat and returns frontier model responses.
- `arena_agent_dispatch`: Pushes a task to GitHub for Arena Agent Mode.

### 3. Connect GitHub in Arena.ai
In [arena.ai/agent](https://arena.ai/agent):
1. Click **Settings** -> **Connectors**.
2. Connect your GitHub account and select `mohammadalifatteh246-afk/Arena-agent`.

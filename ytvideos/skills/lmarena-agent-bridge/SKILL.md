---
name: lmarena-agent-bridge
description: Use when dispatching tasks, prompts, image generation orders, or audio requests to LMArena (Arena.ai) via Chrome CDP relay or the GitHub Shared Bus Agent Mode.
---

# LMArena Agent Bridge: Zero-Cost Dual-Mode Integration

## Overview
LMArena (`arena.ai`) provides access to frontier AI models, image generators, and execution sandboxes at **zero API cost**. This skill defines how Google Antigravity coordinates with LMArena through two distinct pathways:

1. **Direct Chat Mode (`arena.ai/direct`)**: Interactive prompting and reasoning via local Chrome DevTools Protocol (`port 9222`) and FastMCP relay (`arena-relay`).
2. **Agent Mode (`arena.ai/agent`)**: Asynchronous cloud task dispatch via the GitHub Shared Bus (`.agent/CURRENT_TASK.md`).

---

## Architecture Diagram

```
                               ┌─────────────────────────────────┐
                               │       Google Antigravity        │
                               └───────┬─────────────────┬───────┘
                                       │                 │
                 Interactive Reasoning │                 │ Asynchronous Task Order
                 (CDP Relay Port 9222) │                 │ (.agent/CURRENT_TASK.md)
                                       ▼                 ▼
                        ┌────────────────────┐    ┌─────────────────────┐
                        │ arena_direct_chat  │    │ GitHub Shared Bus   │
                        │ (FastMCP stdio)    │    │ (OAuth Connector)   │
                        └─────────┬──────────┘    └──────────┬──────────┘
                                  │                          │
                                  ▼                          ▼
                        ┌────────────────────┐    ┌─────────────────────┐
                        │ arena.ai/direct    │    │ arena.ai/agent      │
                        │ Live Browser Tab   │    │ Remote Bash Sandbox │
                        └────────────────────┘    └─────────────────────┘
```

---

## 1. Operating Direct Chat Mode (FastMCP Relay)

When requiring fast conversational reasoning, prompt expansion, or creative brainstorming from frontier models without token costs:

1. Verify Chrome CDP status using `arena_status`:
   - If offline, launch using `D:\Arena-agent\scripts\launch_chrome.bat` or run:
     ```cmd
     chrome.exe --remote-debugging-port=9222 https://arena.ai/direct
     ```
2. Send prompt via `arena_direct_chat` tool:
   - Tool handles Cloudflare verification automatically within the user's authentic browser session.

---

## 2. Operating Agent Mode (GitHub Shared Bus for Images & Audio)

When requesting heavy asset generation (scene illustrations, TTS voiceover packages, or code refactoring):

### Step A: Format Work Order
Write structured task directives to `.agent/CURRENT_TASK.md`:

```markdown
# Task Work Order: Generate Scene Visuals & Audio
- **Dispatched By:** Google Antigravity
- **Target Branch:** arena/ytvideo-transformer-scene
- **Status:** READY_FOR_ARENA

## Objective
Generate 4 scene illustrations in Sumi-e dark style and audio narration WAVs.

## Scene 1
- Visual Prompt: `Traditional Japanese Sumi-e ink wash, glowing mathematical coordinate vector, cinematic`
- Narration: "In 8 milliseconds, the token must find its attention weights."
- Target Output: `ytvideos/assets/images/scene_01.png`
```

### Step B: Push to Remote
```bash
git -C D:/Arena-agent add .agent/CURRENT_TASK.md
git -C D:/Arena-agent commit -m "dispatch(arena): generate video assets"
git -C D:/Arena-agent push origin master
```

### Step C: LMArena Execution & Pull Request Sync
1. The Arena Cloud Agent picks up the assignment from GitHub.
2. It executes inside its remote bash sandbox, generates assets, commits to the target branch, and opens a Pull Request.
3. Antigravity syncs the PR locally:
   ```bash
   python D:/Arena-agent/scripts/sync_arena_pr.py --pr <PR_NUMBER>
   ```

---

## 3. Strict Zero-Cost & Failover Guardrails

- **Zero-Cost Invariant:** Never route to paid commercial endpoints if LMArena or local OmniRoute can fulfill the task.
- **Auto-Failover:** If LMArena Chrome tab is closed or rate-limited:
  1. Attempt local OmniRoute port `20128` (using `hermes-pro` or approved free models).
  2. If both external generators are unavailable for video frames, immediately fall back to `ytvideos` code-driven SVG vector frame engine.

---

## Anti-Patterns

| Anti-Pattern | Solution |
|---|---|
| Scraping arena.ai using raw curl/httpx without CDP | Will be blocked by Cloudflare. Always use genuine Chrome CDP relay on port 9222. |
| Overwriting `.agent/CURRENT_TASK.md` while a task is still in progress | Check PR status or branch before pushing a new dispatch order. |
| Hardcoding absolute cloud paths | Always use relative paths from repo root (e.g., `ytvideos/assets/images/`). |

# Task Work Order: Multi-Agent Production for 'How The Internet ACTUALLY Works: APIs & Backends'

- **Dispatched By:** Google Antigravity (`ytvideos` engine)
- **Target:** Arena Cloud Multi-Agent Framework (`arena.ai/agent`)
- **Execution Mode:** Dual-Session Parallel Work Orders
- **Status:** READY_FOR_ARENA

---

## 👥 Dual-Session Architecture

This production is split into two specialized agent work orders:

1. **Session 1 (Images & 24 FPS Frames):**
   - Detailed specifications: [ytvideos/dispatches/TASK_IMAGES.md](file:///D:/Arena-agent/ytvideos/dispatches/TASK_IMAGES.md)
   - Branch: `arena/ytvideo-api-backend-images`
   - Tasks: Generate 4 high-res scene illustrations, render 24 FPS vector frames, and apply lossless image compression.

2. **Session 2 (Audio & Humanized Narration):**
   - Detailed specifications: [ytvideos/dispatches/TASK_AUDIO.md](file:///D:/Arena-agent/ytvideos/dispatches/TASK_AUDIO.md)
   - Branch: `arena/ytvideo-api-backend-audio`
   - Tasks: Synthesize humanized SSML voiceover, generate procedural soundscapes, and master to YouTube -14 LUFS standard.

---

## Instructions for Arena Cloud Agents
1. Agents picking up Session 1: Check `ytvideos/dispatches/TASK_IMAGES.md`, generate scene assets, compress, and PR to `master`.
2. Agents picking up Session 2: Check `ytvideos/dispatches/TASK_AUDIO.md`, generate audio assets, master, and PR to `master`.

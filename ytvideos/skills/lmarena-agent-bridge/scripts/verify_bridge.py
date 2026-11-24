#!/usr/bin/env python3
"""
LMArena Agent Bridge Verification & Healthcheck Utility.
Validates the presence of the Chrome CDP relay port (9222) and the Git Shared Bus (.agent/CURRENT_TASK.md).
"""

import os
import sys
import json
import socket
from pathlib import Path


def check_port(host: str = "127.0.0.1", port: int = 9222, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def verify_arena_setup(repo_path: str = "D:/Arena-agent") -> dict:
    repo = Path(repo_path)
    cdp_active = check_port("127.0.0.1", 9222)
    bus_file = repo / ".agent" / "CURRENT_TASK.md"
    git_dir = repo / ".git"

    status = {
        "repo_exists": repo.exists(),
        "git_initialized": git_dir.exists(),
        "shared_bus_ready": bus_file.exists(),
        "chrome_cdp_port_9222": cdp_active,
        "direct_chat_mode": "ONLINE" if cdp_active else "OFFLINE (Launch launch_chrome.bat)",
        "agent_cloud_bus_mode": "ONLINE" if bus_file.exists() else "OFFLINE",
        "zero_cost_invariant": "ACTIVE (100% Free Tiers)"
    }
    return status


def main():
    res = verify_arena_setup()
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()

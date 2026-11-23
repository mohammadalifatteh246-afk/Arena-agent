import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.cdp_client import ArenaCDPClient
from src.server import server, arena_dispatch_task, arena_check_prs


@pytest.mark.asyncio
async def test_chrome_not_running_graceful_handling():
    client = ArenaCDPClient(base_url="http://127.0.0.1:9999")  # Non-existent port
    is_running = await client.is_chrome_running()
    assert is_running is False

    response = await client.send_direct_prompt("Hello")
    assert "ERROR: Chrome is not running" in response


@pytest.mark.asyncio
async def test_find_arena_tab_mock():
    client = ArenaCDPClient()
    mock_tabs = [
        {"id": "1", "title": "Google", "url": "https://www.google.com"},
        {"id": "2", "title": "Chatbot Arena", "url": "https://arena.ai/direct", "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/2"}
    ]
    with patch.object(client, "get_tabs", new=AsyncMock(return_value=mock_tabs)):
        tab = await client.find_arena_tab()
        assert tab is not None
        assert tab["title"] == "Chatbot Arena"
        assert "arena.ai" in tab["url"]


@pytest.mark.asyncio
async def test_server_tools_registered():
    from src.server import arena_status, arena_direct_chat, arena_dispatch_task, arena_check_prs
    assert callable(arena_status)
    assert callable(arena_direct_chat)
    assert callable(arena_dispatch_task)
    assert callable(arena_check_prs)
    
    tools = await server.list_tools()
    tool_names = [t.name for t in tools]
    assert "arena_status" in tool_names
    assert "arena_direct_chat" in tool_names
    assert "arena_dispatch_task" in tool_names
    assert "arena_check_prs" in tool_names

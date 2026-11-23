"""Unit tests for the Antigravity -> Arena dispatch protocol.

These tests verify that:
- ``scripts/dispatch_to_arena.py`` renders well-formed work orders and
  namespaces branches correctly.
- The work order actually received in ``.agent/CURRENT_TASK.md`` conforms to
  the same protocol.
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import scripts.dispatch_to_arena as dispatch


def parse_metadata(text: str) -> dict:
    """Extracts the ``- **Key:** value`` metadata block from a work order."""
    return dict(re.findall(r"^- \*\*(?P<key>[^*]+):\*\* (?P<value>.+)$", text, flags=re.MULTILINE))


def test_normalize_branch_name_adds_arena_prefix():
    assert dispatch.normalize_branch_name("test-dispatch") == "arena/test-dispatch"


def test_normalize_branch_name_keeps_existing_prefix():
    assert dispatch.normalize_branch_name("arena/test-dispatch") == "arena/test-dispatch"


def test_render_work_order_includes_required_fields():
    text = dispatch.render_work_order(
        "Test Task from Antigravity",
        "Verify that the repository receives dispatches cleanly",
        "test-dispatch",
        timestamp="2026-11-23 12:07:04",
    )

    assert text.startswith("# Task Work Order: Test Task from Antigravity")

    metadata = parse_metadata(text)
    assert metadata["Dispatched By"] == "Google Antigravity"
    assert metadata["Date"] == "2026-11-23 12:07:04"
    assert metadata["Target Branch"] == "`arena/test-dispatch`"
    assert metadata["Status"] == "READY_FOR_ARENA"

    assert "## Objective\nVerify that the repository receives dispatches cleanly" in text
    assert "Add or update unit tests under `tests/`." in text
    assert "open a Pull Request to `master`." in text


def test_render_work_order_defaults_timestamp_to_now():
    before = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = dispatch.render_work_order("Title", "Objective", "some-branch")
    after = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    timestamp = parse_metadata(text)["Date"]
    assert before <= timestamp <= after


def test_dispatch_task_writes_work_order_and_pushes(monkeypatch, tmp_path):
    target = tmp_path / "CURRENT_TASK.md"
    monkeypatch.setattr(dispatch, "CURRENT_TASK_PATH", target)

    calls = []

    def fake_run(args, **kwargs):
        calls.append(list(args))
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(dispatch.subprocess, "run", fake_run)

    dispatch.dispatch_task(
        "Test Task from Antigravity",
        "Verify that the repository receives dispatches cleanly",
        "test-dispatch",
    )

    text = target.read_text(encoding="utf-8")
    assert "# Task Work Order: Test Task from Antigravity" in text
    assert "## Objective\nVerify that the repository receives dispatches cleanly" in text
    assert "`arena/test-dispatch`" in text

    repo_root = str(dispatch.REPO_ROOT)
    assert ["git", "-C", repo_root, "add", str(target)] in calls
    assert ["git", "-C", repo_root, "commit", "-m", "dispatch(arena): Test Task from Antigravity"] in calls
    assert ["git", "-C", repo_root, "push", "origin", "master"] in calls


def test_dispatched_current_task_is_well_formed():
    """The repository must receive a dispatch that conforms to the protocol."""
    text = (REPO_ROOT / ".agent" / "CURRENT_TASK.md").read_text(encoding="utf-8")

    assert text.startswith("# Task Work Order: ")

    metadata = parse_metadata(text)
    assert metadata["Dispatched By"] == "Google Antigravity"
    assert datetime.strptime(metadata["Date"], "%Y-%m-%d %H:%M:%S")
    assert metadata["Target Branch"].strip("`").startswith("arena/")
    assert metadata["Status"] == "READY_FOR_ARENA"

    assert "## Objective" in text
    assert "## Instructions for Arena Cloud Agent" in text

    objective = text.split("## Objective", 1)[1].split("##", 1)[0].strip()
    assert objective

    instructions = text.split("## Instructions for Arena Cloud Agent", 1)[1]
    assert "tests/" in instructions
    assert "master" in instructions

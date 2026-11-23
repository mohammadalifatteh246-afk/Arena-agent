import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
CURRENT_TASK_PATH = REPO_ROOT / ".agent" / "CURRENT_TASK.md"

WORK_ORDER_TEMPLATE = """# Task Work Order: {title}

- **Dispatched By:** Google Antigravity
- **Date:** {timestamp}
- **Target Branch:** `{branch}`
- **Status:** READY_FOR_ARENA

## Objective
{objective}

## Instructions for Arena Cloud Agent
1. Implement all changes requested above.
2. Add or update unit tests under `tests/`.
3. Verify tests pass inside your cloud bash sandbox.
4. Commit your work to `{branch}` and open a Pull Request to `master`.
"""


def normalize_branch_name(branch_name: str) -> str:
    """Namespaces a branch under ``arena/`` unless it already is."""
    return branch_name if branch_name.startswith("arena/") else f"arena/{branch_name}"


def render_work_order(
    title: str,
    objective: str,
    branch_name: str,
    timestamp: Optional[str] = None,
) -> str:
    """Renders the Markdown work order that is written to ``.agent/CURRENT_TASK.md``."""
    clean_branch = normalize_branch_name(branch_name)
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return WORK_ORDER_TEMPLATE.format(
        title=title,
        timestamp=timestamp,
        branch=clean_branch,
        objective=objective,
    )


def dispatch_task(title: str, objective: str, branch_name: str):
    """
    Updates .agent/CURRENT_TASK.md, commits to the branch, and pushes to GitHub.
    """
    content = render_work_order(title, objective, branch_name)
    CURRENT_TASK_PATH.write_text(content, encoding="utf-8")
    print(f"Updated {CURRENT_TASK_PATH}")

    # Git operations
    subprocess.run(["git", "-C", str(REPO_ROOT), "add", str(CURRENT_TASK_PATH)], check=True)
    subprocess.run(
        ["git", "-C", str(REPO_ROOT), "commit", "-m", f"dispatch(arena): {title}"],
        check=True,
    )
    subprocess.run(["git", "-C", str(REPO_ROOT), "push", "origin", "master"], check=True)
    print(f"Dispatched task to origin/master successfully.")
    print(f"Arena Cloud Agent can now pick up this task from https://github.com/mohammadalifatteh246-afk/Arena-agent")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dispatch a task to Arena Agent via GitHub")
    parser.add_argument("--title", required=True, help="Title of the task")
    parser.add_argument("--objective", required=True, help="Objective / instructions for Arena")
    parser.add_argument("--branch", default="feature", help="Target branch name")
    args = parser.parse_args()

    dispatch_task(args.title, args.objective, args.branch)

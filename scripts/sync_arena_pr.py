import subprocess
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_and_sync_prs():
    """
    Checks for open Pull Requests from Arena Agent, fetches them, and runs tests.
    """
    print("Checking for Pull Requests opened by Arena Cloud Agent...")
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", "mohammadalifatteh246-afk/Arena-agent", "--json", "number,title,headRefName,author,url"],
        capture_output=True,
        text=True,
        check=True
    )
    
    prs = json.loads(result.stdout)
    if not prs:
        print("No open Pull Requests found. Arena Cloud Agent is either working or idle.")
        return

    print(f"Found {len(prs)} open Pull Request(s):")
    for pr in prs:
        print(f"  #{pr['number']}: {pr['title']} (Branch: {pr['headRefName']}, URL: {pr['url']})")

    # Checkout and test latest PR if requested
    latest_pr = prs[0]
    pr_branch = latest_pr['headRefName']
    print(f"\nFetching and verifying PR #{latest_pr['number']} ({pr_branch})...")
    subprocess.run(["git", "-C", str(REPO_ROOT), "fetch", "origin", pr_branch], check=True)
    subprocess.run(["git", "-C", str(REPO_ROOT), "checkout", pr_branch], check=True)

    print("\nRunning local verification test suite...")
    test_result = subprocess.run([sys.executable, "-m", "pytest", str(REPO_ROOT / "tests"), "-v"])
    if test_result.returncode == 0:
        print("\n✅ Verification PASSED! You can now merge the PR via:")
        print(f"   gh pr merge {latest_pr['number']} --squash --delete-branch")
    else:
        print("\n❌ Verification FAILED. Feedback can be posted to the PR.")


if __name__ == "__main__":
    check_and_sync_prs()

# 🤖 ARENA CLOUD AGENT INSTRUCTIONS

Welcome to the **Arena-Agent** repository. You are operating inside the Arena.ai cloud execution sandbox via the GitHub OAuth Connector.

## 🎯 Your Operating Mission
1. **Find Current Assignment:**
   Check `.agent/CURRENT_TASK.md`. It contains the active work order dispatched by Google Antigravity.
2. **Execute In Sandbox:**
   Use your cloud bash environment, file editor, and external tools to complete all tasks specified in `.agent/CURRENT_TASK.md`.
3. **Write Unit Tests:**
   Ensure any new functionality has corresponding test files under `tests/`. Verify tests pass cleanly in your sandbox.
4. **Deliver via Pull Request:**
   - Commit all changes to a feature branch (e.g., `arena/<task-name>`).
   - Open a GitHub Pull Request targeting the `master` branch.
   - In the PR description, summarize:
     - Changes made
     - Test execution logs
     - Verification proof

"""
Auto Git Sync & Commit Daemon
Automatically detects file changes in the repository, commits them with structured timestamps,
and pushes to the GitHub remote repository (https://github.com/adithiyagit/Automated-Job-Outreach.git).
"""
import subprocess
import time
import sys
import argparse
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent

def run_git_cmd(args, cwd=REPO_DIR):
    """Executes a git command and returns (success, output)."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        return res.returncode == 0, res.stdout.strip() or res.stderr.strip()
    except Exception as e:
        return False, str(e)

def has_uncommitted_changes():
    """Checks if working directory has modified, deleted, or untracked files."""
    success, output = run_git_cmd(["status", "--porcelain"])
    return success and bool(output.strip()), output

def get_current_branch():
    """Returns the name of the current active git branch."""
    success, output = run_git_cmd(["branch", "--show-current"])
    return output.strip() if success and output else "main"

def auto_commit_and_push(custom_message=None):
    """Stages all changes, creates a timestamped commit, and pushes to remote."""
    has_changes, status_output = has_uncommitted_changes()
    if not has_changes:
        print("ℹ️ Working directory clean. No changes to commit.")
        return True, "No changes"

    # Stage all changes
    print("📦 Staging changes...")
    ok, err = run_git_cmd(["add", "-A"])
    if not ok:
        print(f"❌ Failed to git add: {err}")
        return False, err

    # Create commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = custom_message or f"Auto-sync: project updates [{timestamp}]"
    print(f"💾 Committing: {commit_msg}")
    ok, err = run_git_cmd(["commit", "-m", commit_msg])
    if not ok:
        print(f"❌ Commit failed: {err}")
        return False, err

    # Push to remote
    branch = get_current_branch()
    print(f"🚀 Pushing to origin/{branch}...")
    ok, err = run_git_cmd(["push", "origin", branch])
    if not ok:
        # Check if upstream needs to be set
        if "no upstream branch" in err.lower() or "set-upstream" in err.lower():
            ok, err = run_git_cmd(["push", "-u", "origin", branch])

    if ok:
        print("✅ Successfully pushed all changes to GitHub!")
        return True, "Pushed successfully"
    else:
        print(f"⚠️ Push notice: {err}")
        return False, err

def run_watch_loop(interval_seconds=60):
    """Continuously monitors repo and auto-commits on detection of changes."""
    print(f"👁️ Auto Git Sync Watcher running (monitoring every {interval_seconds}s)...")
    print(f"📂 Repository: {REPO_DIR}")
    branch = get_current_branch()
    print(f"🌿 Active Branch: {branch}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            has_changes, _ = has_uncommitted_changes()
            if has_changes:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Detected project file changes!")
                auto_commit_and_push()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n🛑 Auto Git Sync Watcher stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Git Commit & Push Utility")
    parser.add_argument("--watch", action="store_true", help="Run in continuous watch loop")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds for watch mode")
    parser.add_argument("-m", "--message", type=str, default=None, help="Custom commit message")

    args = parser.parse_args()

    if args.watch:
        run_watch_loop(interval_seconds=args.interval)
    else:
        auto_commit_and_push(custom_message=args.message)

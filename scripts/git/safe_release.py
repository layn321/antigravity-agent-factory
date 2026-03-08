#!/usr/bin/env python3
"""
Safe Release Automation (SRA)

Automates the release process:
1. Validates the state via safe_commit.py.
2. Extracts current version from CHANGELOG.md.
3. Bumps version (patch, minor, major).
4. Updates CHANGELOG.md.
5. Commits and Tags the release.
6. Pushes to remote.

Usage:
    python scripts/git/safe_release.py --bump minor
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
SAFE_COMMIT_PATH = ROOT / "scripts" / "git" / "safe_commit.py"


def get_current_version() -> Tuple[str, int]:
    """Extract the latest version and its line number from CHANGELOG.md."""
    if not CHANGELOG_PATH.exists():
        raise FileNotFoundError(f"CHANGELOG.md not found at {CHANGELOG_PATH}")

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    # Matches ## [1.2.3]
    match = re.search(r"## \[(\d+\.\d+\.\d+)\]", content)
    if not match:
        raise ValueError("Could not find a version in CHANGELOG.md")

    return match.group(1), content.find(match.group(0))


def bump_version(current: str, bump_type: str) -> str:
    """Bump semantic version."""
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return f"{major}.{minor}.{patch}"


def update_changelog(new_version: str):
    """Insert the new version header into CHANGELOG.md."""
    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    new_header = f"## [{new_version}] - {today}\n"

    # We find the position after "All notable changes to this project will be documented in this file.\n\n"
    # Or just after the introduction.
    # Actually, a better way is to find the first existing version and insert before it.
    match = re.search(r"## \[\d+\.\d+\.\d+\]", content)
    if not match:
        raise ValueError("Could not find insertion point in CHANGELOG.md")

    insertion_point = match.start()
    updated_content = (
        content[:insertion_point]
        + new_header
        + "\n### Added\n- \n\n### Changed\n- \n\n### Fixed\n- \n\n"
        + content[insertion_point:]
    )
    CHANGELOG_PATH.write_text(updated_content, encoding="utf-8")
    print(f"[OK] Updated CHANGELOG.md to version {new_version}")


def run_command(cmd: list, description: str) -> bool:
    """Run a shell command."""
    print(f"[RUN] {description}...")
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Safe Release Automation")
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        default="patch",
        help="Type of version bump",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions without executing"
    )

    args = parser.parse_args()

    try:
        current_version, _ = get_current_version()
        new_version = bump_version(current_version, args.bump)
        print(f"RELEASE: {current_version} -> {new_version}")

        if args.dry_run:
            print("--- DRY RUN ---")
            print(f"Would update CHANGELOG.md to {new_version}")
            print(f"Would run safe_commit.py 'Release {new_version}'")
            print(f"Would run git tag v{new_version}")
            print("Would run git push and git push --tags")
            return 0

        # 1. Update Changelog
        update_changelog(new_version)

        # 2. Safe Commit (this runs verification)
        commit_msg = f"Release {new_version}"
        if not run_command(
            [sys.executable, str(SAFE_COMMIT_PATH), commit_msg],
            "Running Safe Commit (Verification)",
        ):
            print("❌ Safe commit failed. Aborting release.")
            return 1

        # 3. Tag
        tag_name = f"v{new_version}"
        if not run_command(
            ["git", "tag", "-a", tag_name, "-m", commit_msg], f"Creating tag {tag_name}"
        ):
            return 1

        # 4. Push
        if not run_command(["git", "push"], "Pushing commit"):
            return 1
        if not run_command(
            ["git", "push", "origin", tag_name], f"Pushing tag {tag_name}"
        ):
            return 1

        print(f"\n[DONE] Successfully released version {new_version}!")
        return 0

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

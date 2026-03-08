import os
import sys


def trigger_architecture():
    """
    Entry point for SDLC Phase 3: Architecture.
    Orchestrates the formalization of technical design and system architecture.
    """
    print("[START] Initializing Architecture Phase")

    # Step 1: Verify Input Artifacts
    if not os.path.exists("knowledge/prd.md") or not os.path.exists("knowledge/nfr.md"):
        print("[ERROR] Phase 2 Gate Artifacts (prd.md, nfr.md) missing.")
        return False

    print("[INFO] Requirements artifacts found. Initializing /ai-system-design.")

    # Step 2: Context Loading
    print("[PLAN] Loading requirements context into Architecture Agent...")

    # Step 3: Check Gate Readiness
    print("[GATE] Checking Phase 3 Gate prerequisites...")
    if not os.path.exists("knowledge/templates/ai-design.md"):
        print("[ERROR] Phase 3 Gate Template missing.")
        return False

    print("[SUCCESS] Architecture environment ready. Proceeding with design.")
    return True


if __name__ == "__main__":
    if trigger_architecture():
        sys.exit(0)
    else:
        sys.exit(1)

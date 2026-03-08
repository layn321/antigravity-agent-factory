import os
import sys


def trigger_requirements():
    """
    Entry point for SDLC Phase 2: Requirements.
    Orchestrates the formalization of constraints and functional requirements.
    """
    print("[START] Initializing Requirements Phase")

    # Step 1: Verify Input Artifact
    if not os.path.exists("knowledge/prototype-brief.md"):
        print("[ERROR] Phase 1 Gate Artifact (prototype-brief.md) missing.")
        return False

    print("[INFO] Prototype Brief found. Initializing /write-prd and /elicit-nfr.")

    # Step 2: Adversarial Review (Placeholder for logic)
    print("[PLAN] Queuing Adversarial Requirements Review: 3 Personas + Judge.")

    # Step 3: Check Gate Readiness
    print("[GATE] Checking Phase 2 Gate prerequisites...")
    if not os.path.exists("knowledge/templates/prd.md") or not os.path.exists(
        "knowledge/templates/nfr.md"
    ):
        print("[ERROR] Phase 2 Gate Templates missing.")
        return False

    print("[SUCCESS] Requirements environment ready. Proceeding with analysis.")
    return True


if __name__ == "__main__":
    if trigger_requirements():
        sys.exit(0)
    else:
        sys.exit(1)

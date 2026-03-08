import os
import sys


def trigger_ideation(problem_statement):
    """
    Entry point for SDLC Phase 1: Ideation.
    Orchestrates the transition from a raw requirement to a formalized Prototype Brief.
    """
    print(f"[START] Initializing Ideation Phase for: {problem_statement}")

    # Step 1: Memory Grounding (Proactive)
    print("[MEMORY] Querying Memory MCP for prior art and 'System_Consciousness'...")
    try:
        import subprocess

        # Use sys.executable to ensure we stay in the same conda env without recursion issues
        subprocess.run(
            [sys.executable, "scripts/ai/memory/ground_ideation.py"], check=True
        )
        if os.path.exists("tmp/ideation_context.json"):
            with open("tmp/ideation_context.json", "r") as f:
                context = f.read()
                print(f"[INFO] Loaded Context: {context[:100]}...")
    except Exception as e:
        print(f"[WARN] Memory grounding failed ({e}), proceeding with default context.")

    # Step 2: Inform the user about the workflows
    print("[PLAN] Workflows queued: /brainstorm, /cluster, /brief-prototype")

    # Step 3: Check Gate Readiness
    print("[GATE] Checking Phase 1 Gate prerequisites...")
    if not os.path.exists("knowledge/templates/prototype-brief.md"):
        print("[ERROR] Phase 1 Gate Template missing.")
        return False

    print("[SUCCESS] Ideation environment ready. Proceeding with /brainstorm.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trigger_ideation.py '<problem_statement>'")
        sys.exit(1)

    problem = sys.argv[1]
    if trigger_ideation(problem):
        sys.exit(0)
    else:
        sys.exit(1)

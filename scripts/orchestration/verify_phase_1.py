import os
import sys
import re


def check_phase_1_gate(artifact_path):
    """
    Checks if the Phase 1 Gate (Ideation) is satisfied.
    Required Artifact: knowledge/prototype-brief.md
    """
    if not os.path.exists(artifact_path):
        print(f"FAILED: Artifact {artifact_path} not found.")
        return False

    with open(artifact_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Required Sections in prototype-brief.md
    required_sections = [
        "# Prototype Brief",
        "## Problem Statement",
        "## Opportunity Clusters",
        "## Proposed Solution",
    ]

    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    if missing:
        print(
            f"FAILED: {artifact_path} missing required sections: {', '.join(missing)}"
        )
        return False

    # Check for placeholder text (generic check)
    if "[Describe" in content or "<Insert" in content:
        print("FAILED: Artifact contains unresolved placeholders.")
        return False

    print("SUCCESS: Phase 1 Gate satisfied.")
    return True


if __name__ == "__main__":
    brief_path = "knowledge/prototype-brief.md"
    if len(sys.argv) > 1:
        brief_path = sys.argv[1]

    if check_phase_1_gate(brief_path):
        sys.exit(0)
    else:
        sys.exit(1)

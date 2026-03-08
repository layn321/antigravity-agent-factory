import os
import sys


def check_phase_2_gate(prd_path, nfr_path):
    """
    Checks if the Phase 2 Gate (Requirements) is satisfied.
    Required Artifacts: knowledge/prd.md, knowledge/nfr.md
    """
    for path in [prd_path, nfr_path]:
        if not os.path.exists(path):
            print(f"FAILED: Artifact {path} not found.")
            return False

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Basic Check for PRD
        if "prd.md" in path.lower():
            required_sections = [
                "# Product Requirements Document",
                "## Goal",
                "## User Stories",
                "## Functional Requirements",
            ]
        else:
            # Basic Check for NFR
            required_sections = [
                "# Non-Functional Requirements",
                "## Performance",
                "## Security",
                "## Scalability",
            ]

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            print(f"FAILED: {path} missing required sections: {', '.join(missing)}")
            return False

    print("SUCCESS: Phase 2 Gate satisfied.")
    return True


if __name__ == "__main__":
    prd = "knowledge/prd.md"
    nfr = "knowledge/nfr.md"
    if check_phase_2_gate(prd, nfr):
        sys.exit(0)
    else:
        sys.exit(1)
